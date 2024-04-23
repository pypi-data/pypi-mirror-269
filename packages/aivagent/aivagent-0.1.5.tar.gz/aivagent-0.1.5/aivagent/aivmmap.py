'''
    Aiv平台进程共享内存管理模块 (2023.10)
    Aiv系统使用多进程运行模式,包含Aivc.exe主进程、wc进程(websocket + webrtc 进程<使用multiprocessing创建>)、
    还有bot模块(全部是独立进程,window下是用nuitka编译成的独立的exe执行文件,用subprocess.Popen启动)。
    因此,进程之间需要共享数据,在Aiv系统中,使用mmap实现进程数据共享
    在此aivmmap.py类中,实现了各进程需要使用的共享内存管理类,而且实现共享内存锁。
    每个模块（进程）之间,通过mmap互相协作。使用Aiv平台成一个“来料加工”的AI平台
    每个进程之间,可以共享两种数据：控制信息、加工的数据
'''
# from typing import Any
from loguru import logger
import mmap,os,asyncio,time
from enum import Enum
from .aivtool import _write_mmap,_read_mmap

taskMMAPLen = 1024*1024*10 # 每个任务 10M ,如果有10个任务,则是 10*10M
taskMMAPName = 'aivtask'
taskMMAPStart = 10  #读任务共享内存的起始位置,默认是10, 即前面留10个字节给以后扩展用(前面2字节用来存TaskState状态了) 2023.10
newTaskMMAPName = 'aivnewtask' #新任务的共享内存类。只给  AivWcMmap与AivMainMmap类用

confMMAPLen = 1024*1024 # 1M
confMMAPName = 'aivconf'

botMMAPLen = 1024*1024*10 # 10M
botMMAPName = 'aivbot'


# 这是服务端使用的状态码：在各共享内存中共享
class TaskState(Enum):
    taskNone = 0        # 无任务在流水线中
    # taskNew = 50         # 新任务状态
    # taskCheck = 80       # 检查状态
    taskReady = 100      # 有任务,还在准备阶段(主程序先要把运行任务需要的文件下载)
    # taskOk = 200         # 服务器执行完成（成功)
    taskBot = 300       # 各bot 抢任务阶段 (wc模块把任务 taskBot 状态, bot模块判断如是taskBot就可以接单 2023.11)
    taskRun = 400        # bot锁定任务,并开始运行阶段
    taskFinished = 500   #bot任务完成,交回流水线中(但任务还没结束,因为接下来还要把生成的文件发回js端。如果任务完成,会设为 TaskEnd状态)
    taskProExit  = 600    # 用户取消
    # taskBusy = 700       # 服务器繁忙
    taskEnd  = 1000      # 任务已经终止 (也许未成功,也许成功,如果出现此标志,websocket马上返回)
    # taskProExit = 2000   # 有关进程退出 2023.11


# 这是前端与服务端交流的任务返回码.前端根据返回的任务码判断任务执行到什么阶段,是否成功等?  2023.11
class TaskResultCode(Enum):
    '''
        返回客户端的标识
        * 类似web请求返回码
        * 在task的'result'字段中记录
    '''
    taskNew = 50   # 接收新任务
    taskReady = 100  # 1xx：信息类，表示客户发送的请求服务端正在处理。
    taskOk = 200    # 2xx：成功类，服务器成功接收请求。
    taskBot = 300   # 3xx：已经进入bot模块处理阶段
    taskId = 400  # 4xx: 客户端验证错误类，对于发的请求服务器无法处理(主要是没登录或权限不够)
    taskSvr = 500   # 5xx: 服务端错误
    taskUser = 600  # 6xx: 客户中止

    def getMsg(self):
        '''
            要调用此getMsg()函数,例如下：
            TaskResultCode.taskOk.getMsg()   TaskResultCode.taskSvr.getMsg()
            因为每个枚举成员（枚举值）都是一个实例
        '''
        if self.value==100:
            return '任务处理准备中'
        elif self.value==200:
            return '任务成功!'
        elif self.value==300:
            return '任务正在由bot模块处理'
        elif self.value==400:
            return '任务的发起用户权限不足'
        elif self.value==500:
            return '任务引起服务器错误'
        elif self.value==600:
            return '任务的发起用户中止操作'
        else:
            return '未知状态'


class AivBaseMmap:
    def __init__(self,isMain, newTaskMMAPName= None) -> None:
        if newTaskMMAPName is None:
            newTaskMMAPName = taskMMAPName

        # logger.warning('AivBaseMmap新建的名是：{}'.format(newTaskMMAPName))
        self.isMain = isMain  
        # self.state = TaskState.taskNone
        self.task = None
        try:
            if isMain:
                self.confMMAP = mmap.mmap(0, confMMAPLen, access=mmap.ACCESS_WRITE, tagname=confMMAPName)
            else:
                # 子进程 (isMain = False),以只读模式建立的内存共享
                self.confMMAP = mmap.mmap(0, confMMAPLen, access=mmap.ACCESS_COPY, tagname=confMMAPName)
        except Exception as e:
            logger.warning('AivBaseMmap: 建立进程通讯错误( isMain= {} ) ! error = {}'.format(isMain,e))

        # 每个任务占一格,任务池里就像格子一样
        self.taskMMAP = mmap.mmap(0, taskMMAPLen, access=mmap.ACCESS_WRITE, tagname = newTaskMMAPName)

        #记录了系统的信息,AivSys是附属类。这里AivBaseMmap 的 AivSys 可以从系统读取(isMain==True时候)
        # 也可以从共享内存读取(isMain==False时候)
        self.sysInfo = None # 记录系统的信息 2023.12    
        self.updateSysInfo()



    def readTask(self,mmap = None):
        tempMmap = mmap
        if mmap is None:
            tempMmap = self.taskMMAP
        return _read_mmap(tempMmap,taskMMAPStart,0,True)    
    
    def writeTask(self,taskData,mmap = None):
        tempMmap = mmap
        if mmap is None:
            tempMmap = self.taskMMAP #默认读写 taskMMAP
        return _write_mmap(tempMmap,taskData,taskMMAPStart)    
    
    # 清空指定索引的任务块内存----2023.11
    def clearTask(self,mmap= None):
        tempMmap = mmap
        if mmap is None:
            tempMmap = self.taskMMAP #默认读写 taskMMAP
        tempMmap.seek(0)
        for i in range(taskMMAPLen):
            tempMmap.write(b'\x00')
        tempMmap.flush()


    # 更新共享内存中的系统信息---2023.10---
    def updateSysInfo(self):
        self.sysInfo = _read_mmap(self.confMMAP,0,0,True)  
        return self.sysInfo      

    def getFilePath(self,file):
        '''
            根据前端给的文件 file 信息,生成文件在服务端相对应的绝对路径
        '''
        if file['md5'] is None:
            logger.warning('文件的 MD5 值为空！')
            return ''
        
        md5 = file['md5']
        extName = os.path.splitext(file['name'])[1] #获取文件扩展名
        return os.path.join(self.sysInfo['sys.tempDir'], md5 + extName)


    def checkState(self,value):
       return next((item for item in TaskState if item.value == value), TaskState.taskNone)
    

    def setTaskResultCode(self,state:TaskResultCode,msg = None):
        '''
            设置任务的返回值 2023.10
            * 每个任务数据,都带有一个  result 参数,里面有 'code' 和 'msg' 'data' 数据字段
            * code和msg的内容固定, data 数据字段可以写扩展内容
            * 无论任务是否成功执行,这个 result 都会返回,result里的数据可以说明什么原因出错,或执行到哪一步返回的
        '''
        if self.task is None:
            return
        self.task['result']['code'] = state.value # 设置返回值的状态
        if msg is None:
            self.task['result']['msg'] = state.getMsg()
        else:
            self.task['result']['msg'] = msg


    # 设置共享内存中的任务标志
    def setTaskState(self,state:TaskState):
         # 写入标志位
        tag = state.value
        byte = tag.to_bytes(2, 'big') #写入双字节, 2表示双字节 , 1字节最大只能写 256位
        self.taskMMAP.seek(0)
        self.taskMMAP.write(byte)
        self.taskMMAP.flush()

    #读出任务共享内存中的标志
    def getTaskState(self,mmap=None):
        self.taskMMAP.seek(0)
        chr = self.taskMMAP.read(2) #读入双字节
        value = int.from_bytes(chr, 'big') #读出第一个字节
        return self.checkState(value)

    def killMe(self,proName,isBot=False):
        if isBot:
            logger.info('Bot app: {} (pid={}) 进程退出.'.format(proName,os.getpid())) 
        else:
            logger.debug('{} (pid={}) 进程退出.'.format(proName,os.getpid()))
        os._exit(0)
        # sys.exit(0)   

    def createCheckPidThread(self,pids,proName):
        ''' 2023.11
            用线程检测 主进程 pid 是否退出
            (不是 asyncio协程,用threading检测),如果主进程退出,线程的主进程也跟着退出 
            pids 参数是一个包含多个 pid 的数组(可以监控多个进程)
            proName 是当前的进程名字
        '''
        import psutil
        # print('当前 {} 模块进程 pid = {} , 守护进程 ppid = {}'.format(name,os.getpid(),pid))

        def check(pid):   
            # 获取当前子进程的 主进程ppid是否还运行
            if pid is None:
                return
            
            is_run = True
            try:
                pp = psutil.Process(pid)
            except Exception as e:
                is_run = False
                # logger.warning('守护进程 ppid= {} 已退出！错误是：\n{}'.format(wcPid,e))
                
            if not is_run or not pp.is_running():
                logger.debug('进程 {} 退出.'.format(proName))
                os._exit(0) #在调试模式下,python主进程不退出,本进程可能退出也不成功
                # sys.exit(0)   
        
        def threadCheck():
            while True:
                for pid in pids:
                    check(pid) 
                time.sleep(1)

        from threading import Thread
        Thread(target= threadCheck, daemon= True).start()  # daemon= True即设为守护进程.守护进程只要主进程退出,它就会立即退出。(主进程也不会等待子进程执行完才退出) 2024.2

# 进程通讯状态类 (Enum)
class AivQueueState(Enum):
    ''' 2024.1
        AivQueue类的状态码
    '''
    msgNone = 0         # 无消息在Queue中
    msgParent = 10      # 父进程写状态 (子进程可以读)
    msgChild = 20       # 子进程写状态 (父进程可以读)


class AivQueue(AivBaseMmap):
    ''' 2024.1
        父子进程通讯
        用MMAP实现类似于Queue的进程通讯类
    '''

    def __init__(self,isParentPro, newTaskMMAPName=None) -> None:
        super().__init__(False, newTaskMMAPName)
        self.isParentPro = isParentPro  #标识是父进程还是子进程

    def put(self,msg):
        ''' 2024.1
            写数据进入共享进程队列
            如果写成功则返回True, 如果状态不能写,则返回 False
            msg 参数: dict 数据类型
        '''
        # 先判断是否能写
        ret = False
        queueState = self.getQueueState()
        if self.isParentPro:
            if queueState == AivQueueState.msgNone or queueState == AivQueueState.msgParent:
                _write_mmap(self.taskMMAP,msg,taskMMAPStart) # 从aivmmap.taskMMAPStart 的位置开始写数据
                self.setQueueState(AivQueueState.msgParent) #把数据写进去后,把标识改为 msgParent
                ret = True
        else:
            if queueState == AivQueueState.msgNone or queueState == AivQueueState.msgChild:
                _write_mmap(self.taskMMAP,msg,taskMMAPStart) # 从aivmmap.taskMMAPStart 的位置开始写数据
                self.setQueueState(AivQueueState.msgChild) #把数据写进去后,把标识改为 msgChild
                ret = True

        return ret

    def get(self):
        ''' 2024.1
            从进程队列中读出数据 
            读成功返回数据类型为 dict 类型,不成功返回 None
        '''
        # 先判断是否能读
        ret = None
        queueState = self.getQueueState()
        if self.isParentPro:
            if queueState == AivQueueState.msgChild: #只能读子进程写的 2024.1
                ret = _read_mmap(self.taskMMAP,taskMMAPStart,leng=0, return_dict=True) # 从aivmmap.taskMMAPStart 的位置开始读数据
                self.setQueueState(AivQueueState.msgNone) #把数据写进去后,把标识改为 msgNone
        else:
            if queueState == AivQueueState.msgParent: #只能读父进程写的 2024.1
                ret = _read_mmap(self.taskMMAP,taskMMAPStart,leng=0, return_dict=True) # 从aivmmap.taskMMAPStart 的位置开始读数据
                self.setQueueState(AivQueueState.msgNone) #把数据写进去后,把标识改为 msgNone
        return ret

    # 设置共享内存中的任务标志
    def setQueueState(self,state:AivQueueState):
         # 写入标志位
        tag = state.value
        byte = tag.to_bytes(2, 'big') #写入双字节, 2表示双字节 , 1字节最大只能写 256位
        self.taskMMAP.seek(0)
        self.taskMMAP.write(byte)
        self.taskMMAP.flush()

    #读出任务共享内存中的标志
    def getQueueState(self):
        self.taskMMAP.seek(0)
        chr = self.taskMMAP.read(2) #读入双字节
        value = int.from_bytes(chr, 'big') #读出第双字节,转换成int类型 2024.1
        return self.checkQueueState(value)
    
    def checkQueueState(self,value): # 通过整型值读出AivQueueState的值 2024.1
       return next((item for item in AivQueueState if item.value == value), AivQueueState.msgNone)
        

# bot的内存共享管理类
class AivBotMmap(AivBaseMmap):
    '''
        AivBotMmap 由AivBot模块启动并使用
        完成Bot模块与AIV平台父子进程之间的通讯
    '''
    def __init__(self,botName,botId,newTaskMMAPName) -> None:
        super().__init__(False,newTaskMMAPName)
        self.botId = botId
        self.botName = botName
        self.onStartTask = None #有任务触发的事件
    
    async def run(self):
        '''
            AivBotMmap类的 协程函数入口
            目的就是不断检测是否有新任务可以执行（抢单）
        '''
        while True:
            
            #这是 AivBotMmap,因此 self.checkTask() 中只有 TaskState.taskBot 状态才开始工作 2024.4
            await self.checkTask() 

            state = self.getTaskState()
            # logger.warning('AivBotMmap: run() 检测任务情况. state == {}'.format(state))
            if state == TaskState.taskProExit:
                self.endTask(TaskState.taskProExit)

            await asyncio.sleep(1)   


    # 从共享内存中读取 任务内容
    async def checkTask(self): # run()中的协程函数
        '''
            抢任务单
            * 通过不断检测任务的共享内存状态,如果有合适自己的任务,即抢过来执行。
            * 匹配的条件一是 botId 相等, 二是自己处于空闲状态
        '''    

        taskState = self.getTaskState()

        # logger.debug('读到的任务状态是：{}'.format(taskState))

        if taskState != TaskState.taskBot: #如果第一项是taskBot任务标记,则读出里面的内容，然后再分析任务内容是否是自己要执行的
            return
        
        # 读出任务内容,如果是自己的任务,则开始处理,并锁定共享任务内存
        currTask =  _read_mmap(self.taskMMAP,taskMMAPStart,0,True)  # taskMMAPStart 决定是从哪个字节开始读,默认是 10
        if self.task is None:
            self.task = currTask

        # logger.debug('读到的任务内容是：{}'.format(currTask))
        # 查询当前的任务指定的BotId 是否是自己的Id, 如果是就可以执行的任务（抢单）
        # if currTask['botId'] != self.botId:
        #     errMsg = '''任务指定的bot模块与被调用的bot模块的不符! 任务指定: botId = {} ,
        #                 被调用的botId = {} [{}]. 
        #                 出错原因可能是bot模块初始化时使用了错误的 botId 码.
        #              '''.format(currTask['botId'],self.botId,self.botName)
            
        #     logger.error(errMsg)
        #     self.setTaskResultCode(TaskResultCode.taskSvr,errMsg)
        #     self.endTask()
        #     currTask = None
        #     return
        
        # logger.warning('开始设置任务的标识： bot== {}'.format(self.aivBot.botId))
        self.setTaskState(TaskState.taskRun) #把共享任务的标志设置为运行状态
        # 重新读一次看是否成功,如果发现不成功(或被抢了单,则返回)
        await asyncio.sleep(0.01) # 暂停10毫秒,如果不能锁定,则返回
        taskState = self.getTaskState()
        if taskState != TaskState.taskRun:
            currTask = None
            logger.warning('锁定任务 _id = {} 不成功!'.format(currTask['_id']))
            return
        
        # logger.debug('bot: readTaskInfo 模块: 抢单成功！任务内容是: {}'.format(currTask))
        
        # 触发任务开始任务事件
        if self.onStartTask is not None:
            # logger.debug('bot: 准备触发 运行任务Api ,任务内容是：{}'.format(currTask))
            self.setTaskResultCode(TaskResultCode.taskBot) # 设置为进入bot模块处理状态
            self.onStartTask(self.task)

            

    def endTask(self,state = TaskState.taskFinished):
        '''
            这个函数是bot模块调用 2023.10
            * 在bot模块的api函数执行完成后,则调用此函数.
            * 此函数把任务完成标志写入共享内存中, 由aivc.exe端查询触发其它操作
        '''
        # logger.warning('bot: 模块endTask {} 本次任务执行完成！任务内容是: {}'.format(self.botName,self.task))
        try:
            # 把任务内容更新回共享内存中: 主要是输出文件是后面增加的内容
            _write_mmap(self.taskMMAP,self.task,taskMMAPStart) # taskMMAPStart 是从哪个字节开始读,默认是 10
            self.task = None
            self.setTaskState(state) # 把任务的共享内存的状态设为 已完成状态, 由后续的 wc.py 从共享内存计出模块处理
        except Exception as e:
            logger.warning('aivmmap: 任务完成后,数据处理阶段出错: Error= {}'.format(e))
        
        # 无论endTask()遇到什么错误,都要把当前进程关闭 2024.3
        self.killMe(self.botName,True)

        

