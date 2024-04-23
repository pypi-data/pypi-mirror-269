'''
### AIV平台Bot自动化程序管理模块
* 此模块的 run()函数,在用户的Bot模块中被调用,必须是最先运行的代码 (不一定是顺序排前面,
    相反,run应该写__main__里(在api开头的函数声明后面);
* 本模块是 AivAgent 端的核心。负责初始化用户开发的Bot自动化程序模块,并管理bot的api函数列表、参数等
* Aiv的Bot模块接口为api开头命名函数,以此开头的函数将自动注册为bot的api函数,在客户端可以直接被调用;
    如果api函数比较多,也可以分模块写,然后使用import导入;
* run()启动前,最好把Bot所在的路径添加到Path中,然后import入loguru(AIV Bot必备模块),否则容易报 
    import错误,找不到依赖包,然后初始化日志工具等,最后再调用run()函数;
* 根据AIV平台注册的Bot 接口,匹配api开头的函数,并把参数拼接和格式化,最后成功调用Bot的api函数;
* 每个Bot api 函数,都有三个阶段被AIV AGI调用,分别是 cmd='init'(Bot被初始化调用)、cmd='param'
    (初始化后获取参数)、cmd='run'(前端用户调用)三个阶段;
* 用户的Bot程序,由AIV AGI服务程序直接调用,而AIV AGI与AIV客户端(app/web)相连接,
* 关于调试: 找到安装目录下: aivc/bin/debug.bat,直接运行即可(运行前要把AIV AGI服务程序关闭);
* AIV AGI 服务程序管理地址: http://127.0.0.1:28067/
* 常用的工具函数,统一放在 aivtool.py 模块中(比如生成文件md5码的函数)
    (2023.12)
'''
import sys,os,time
import argparse,random

aivBot = None
aivBotMmap = None

## 1、初始化Aiv Bot 的第一个函数=======================================================================
def run(botId=None,callFun=None,logLevel = 'INFO') -> None:
    '''
        ### 注册AIV平台的Bot
        - param
            - botId:   Aiv平台分配的bot唯一的token
            - callfun:  程序初始化后,回调的函数
            - logLevel: 可选 'DEBUG','INFO','SUCCESS','WARNING','ERROR','CRITICAL' 
        - desc
        * 此函数,必须是在用户Bot中执行的第一行代码(__main__中,但应该在bot api函数<以api开头>声明之后)
        * 当前模块下,所有以 api 开头的函数,都自动注册为aiv系统的bot接口函数
            其它不用作为bot api函数输出的函数,可以用"_"开头,或用其它命名开头
        * 在bot api函数内,可以调用 regParser() 注册bot api函数调用的参数,包含默认值、数据类型、可选值等等
        ### 本函数必须在模块的 "__main__" 后面调用,并且不能包裹在函数里面调用！
    '''
    try:
        import inspect
        # inspect.stack() 返回函数的调用栈
        frame = inspect.stack()
        if frame[1][3] != '<module>':
            raise Exception('run() 函数必须在用户的bot模块"__main__"下调用,且不能包裹在函数中调用')
        
        obj = inspect.getmembers(frame[1][0]) #  
        #数据是[(,) , (,) , (,) , (,)] 这样的
        globalvar = None 
        for tup in obj:
            if tup[0]=='f_globals': #字段'f_globals'记录的值 ,等同于函数 globals() 返回的值, 但globals()必须在自己的模块下运行,灵活性不足
                globalvar = tup[1]
                break

        from aiv.aivapp import _aivAppInit #初始化全局路径、环境变量、logger
        _aivAppInit(globalvar['__file__'],False,loglevel=logLevel)
        
        import asyncio
        from loguru import logger
        import cv2 #对于用到opencv-python包,在用nuitka编译,如果在main.exe代码中不显式import cv2
        # 会导至以下错误：
        # ImportError: DLL load failed while importing cv2: 找不到指定的模块。

        os.environ['PYTHONUNBUFFERED'] = '1' #禁用标准输出的缓冲区 2023.10
        #当使用Python调用FFmpeg时，如果输出信息太多，可能会导致标准输出（stdout）
        # 缓冲区溢出并引发错误。这通常是因为输出信息超过了缓冲区的容量。
        # 标准输出的默认缓冲区大小通常是8192字节,通过设置环境变量PYTHONUNBUFFERED为1来禁用缓冲区

        # 设置日志保存的文件路径,每一个子进程都要设置一次(loguru) 2024.2
        botPath = os.path.dirname(os.path.abspath(globalvar['__file__'])) #Bot程序路径
        from .aivtool import setLogFile  
        #设置日志保存的文件路径和级别,默认把WARNING级别的日志保存在执行程序目录的botError.log文件中(但不影响控制台输出的日志) 2024.2 
        logFile = os.path.join(botPath,'botError.log') #在bot模块根目录下生成一个日志文件 2024.3
        setLogFile(logFile, logLevel= 'INFO')  #默认只显示 INFO信息(只影响写入本地文件的日志等级,不影响控制台输入日志的等级)
        

        global aivBot
        aivBot = AivBot()
        aivBot.botInfo.path = botPath
        # aivBot.botInfo.botName = botName
        aivBot.botInfo.botId = botId

        aivBot.regBotApi(globalvar)

        from aiv.aivmmap import AivBotMmap
        global aivBotMmap
        # print('AivBot收到的 taskMMAPName333 ==> {}'.format(aivBot.taskMMAPName))
        aivBotMmap = AivBotMmap(aivBot.botInfo.botName,aivBot.botInfo.botId,aivBot.botInfo.taskMMAPName)
        # aivBotMmap.aivBot = aivBot
        aivBotMmap.onStartTask = aivBot.onStartTask

        if callFun is not None:
            callFun()  #调用用户设置的回调函数----------

        aivBot.initParam() # 加载 Bot Api的参数,在这里,可以选择性加载 2023.11

        ''' 2023.11
            用线程检测进程 wcPid 是否退出
            用线程检测 wcPid 进程是否退出(不是用 asyncio协程,是用threading检测),如果wcPid进程退出,线程也跟着退出 
            原因是 asyncio的所有子协程都是在进程的主线程运行, 当Aiv平台的bot模块运行任务时,基本是上独占模式(死循环)
            这样如果用户中止任务,虽然bot模块也收到 TaskState.taskProExit 信号,但 aivBotMmap.run() 阻塞在运行任务上
            没办法响应  TaskState.taskProExit 信号, 但线程是可以的.因此,在 aivBotMmap.run()检测任务是否中止信号上,
            另外用线程 threading 建立一个独立于主线程的子线程,用于检测wcPid是否退出(这里是检测aivwc.py 的进程)。这样,
            当协程失灵时,threading的线程仍然可用,可以保证用户下达的中止指令可以执行。
        '''
        aivBotMmap.createCheckPidThread([aivBot.botInfo.ppid,aivBot.botInfo.wcpid],aivBot.botInfo.botName)

        logger.debug('Bot模块[ {} ]启动成功.'.format(aivBot.botInfo.botName))
        # 协程函数
        async def main():
            # aivBotMmap的功能主要是检测是否有新任务(抢单),二是检测任务的状态,如果任务被前端取消,则马上退出进程
            # 另外,也要不断检测任务是否超时,超时就自动中止进程 2023.11
            asyncio.create_task(aivBotMmap.run())  
            while True:
                await asyncio.sleep(0.2) #只要主程序不退出,上面的两个协程就一直运行

        asyncio.run(main())
    except Exception as e:
        from loguru import logger
        logger.warning('运行Bot.run() 出错! Error= {}'.format(e))

class AivBotInfo:
    def __init__(self) -> None:
        self.pid = os.getpid() # 当前进程的PID
        self.ppid = None #父进程的pid,根据父进程pid,如果它退出,自己也退出
        self.wcpid = None # 同级子进程 wc的进程pid,如果在命令行参数中传入此值,则可以监控此值,同步退出进程 2023.11
        self.botId = ''
        self.botName = ''
        self.path = '' #主执行文件路径(含文件名)
        self.taskMMAPName = '' #当前任务启用的共享内存名称

    def getBotInfo(self):
        '''
            返回当前模块的信息
        '''
        return {
            'botName': self.botName,
            'botId' : self.botId,
            'path': self.path,
            'pid': self.pid,
            'ppid': self.ppid,
            'wcpid': self.wcpid,
            'taskMMAPName': self.taskMMAPName
        }

class AivBot:
    def __init__(self) -> None:
        self.task = None #用于临时记录任务信息, 在 addFileToTaskOutParam()调用
        self.botInfo = AivBotInfo()
        self.api = [] # 记录当前bot模块所有的Api信息

        if len(sys.argv)>1:
            self.botInfo.ppid = int(sys.argv[1]) #如果命令行第一个参数传应用的主进程pid过来
        if len(sys.argv)>2:
            self.botInfo.taskMMAPName = sys.argv[2] #这个是前端传过来的 taskId (32位长度的字符串,全球唯一)
        if len(sys.argv)>3:
            self.botInfo.wcpid = int(sys.argv[3])  # 同级子进程 wc的进程pid,如果在命令行参数中传入此值,则可以根据此值,同步退出进程
        if len(sys.argv)>4:
            self.botInfo.botName = sys.argv[4] #第4个参数传 botName 2023.12

        # print('AivBot收到的 taskMMAPName ==> {}'.format(self.taskMMAPName))


    def initParam(self):
        from loguru import logger

        if self.api is not None:
            # logger.debug('self.api 不为空!')

            for aivApi in self.api:
                # logger.debug('循环所有Api {}'.format(aivApi['name']))
                if aivApi['paramIn'] is None:
                    try:
                        callParam = {'bot':self, 'sysInfo':aivBotMmap.sysInfo} #把任务信息和系统信息打包,一起给bot的api传参
                        aivApi['fun']('init', callParam) #执行api的初始化函数, 传递 cmd = 'param' 指令进去
                    except Exception as e:
                        logger.warning('函数: {}获取参数阶段出错, Error= {}'.format(aivApi['name'],e))
        
        
            # 检查所有的Api函数的参数是否都设置了---
            haveParam = True
            for aivApi in self.api:
                if aivApi['paramIn'] is None:
                    haveParam = False
                    break

            if haveParam:
                logger.debug('Bot模块 {} 载入完成!'.format(self.botInfo.botName))
                # break


    def onStartTask(self,task):
        ''' 2023.09
            ### 生成调用函数的参数
            * 前端返回服务器,服务器调用 Bot 的参数,是一个dict列表,本函数用 parser.parse_args 把dict转换成 Namespace 命名空间
            * 此函数把多余的数据删除,只留下类似格式dict: {'参数名1': '参数值1','参数名2': '参数值2', ... } 
        '''
        from loguru import logger
        from .aivtool import getFileInfo
        # logger.debug('aivBot 收到的启动任务参数是: task ==> {}'.format(task))

        # =====================================================================
        # ======= 调api的参数准备 ============================================== 1
        try:
            # 检测是否有输入参数 'paramIn'
            if task['paramIn'] is None:
                raise Exception("任务的 ParamIn 为空！")
            
            self.task = task

            # 检查是否有调用的bot api 函数名
            apiName = task['apiInfo'].get('name',None)
            if apiName is None:
                logger.error('客户端没有指定要调用的bot api函数名! ')

            if len(self.api)==0:
                logger.error('检测到Bot: {} 无注册任何api函数.'.format(self.botInfo.botName))


            apiName = apiName.strip()
            # 根据任务给定的api函数名,找出 bot 对应的真实函数 (通过 botName)
            apiFun = None
            parser = None
            for api in self.api:
                if api['name'].strip().lower() == apiName.lower():

                    apiFun = api['fun']
                    parser = api['parser']
                    break

            if apiFun is None:
                raise Exception('本地Bot模块无api函数:[ {} ]! 请检测Bot模块的api函数名称.'.format(apiName))


            args = None
            if parser is not None:
                logger.debug('当前 bot api 函数 {} 运行时不依赖 parser 对象, 直接传 dict 参数!'.format(apiName))

                params = {}

                # 先把paramIn 参数转换------------------------------
                for param in task['paramIn']:
                    if param['type'].lower() == 'file':
                        file = param['data'][0] #暂时取第一项内容
                        filename = aivBotMmap.getFilePath(file)
                        params['--'+param['name']] = filename

                    elif param['type'] == 'bool':
                        if param['value'] is None:
                            param['value'] = False    

                        params['--'+param['name']] = param['value']
                    elif param['type'] == 'string':
                        params['--'+param['name']] = param['value']
                    elif param['type'] == 'int':
                        params['--'+param['name']] = param['value']
                    elif param['type'] == 'float':
                        params['--'+param['name']] = param['value']

                # 转换 paramOut 参数 ---------------------------------------
                paramOut = task['paramOut']
                
                files = []
                for param in paramOut: # 把输出参数与变成 args的一个参数(cmd 命令行下也是用 --xxxx xxxx 传给 bot 模块) 2023.12
                    if param['type'].lower() == 'file':  
                        #根据当前时间生成一个文件名
                        file = str(int(time.time()))+'.mp4' 
                        fileName =os.path.join(aivBotMmap.sysInfo['sys.outDir'],file)
                        fileInfo = getFileInfo(fileName) #用函数getFileInfo 生成文件的信息
                        files.append(fileInfo)
                        if param['data'] is None:
                            param['data'] = files
                        params['--'+param['name']] = fileName

                
                # ----------------------------------------------------------

                tup = tuple(params.items())
                fun_tup = self.dictToList(tup)

                # logger.warning('生成的 fun_tup 参数列表是 self.api：{}'.format(self.api)) 
                
                
                #把参数赋值给  parser 对象 2023.11
                args = parser.parse_args(fun_tup) 
                
                # logger.warning('生成的 args 参数是：{}'.format(args))
            
            else: 
                # 在 api 函数调用 regParser()时,写成 regParser(None) 即是不依赖 argparse.ArgumentParser() 模式, 开发者自己手动读出task任务参数,再调有api函数 2023.12
                # 此 api 函数调用不依赖 argparse.ArgumentParser(), 则直接传递 task 参数给 api 函数 (函数中可以判断一下数据类型是否是 dict) 2023.12
                # 转换 paramOut 参数 ---------------------------------------
                paramOut = task['paramOut']
                
                files = []
                for param in paramOut: # 把输出参数与变成 args的一个参数(cmd 命令行下也是用 --xxxx xxxx 传给 bot 模块) 2023.12
                    if param['type'].lower() == 'file':  
                        #根据当前时间生成一个文件名
                        file = str(int(time.time()) + random.randint(1,100))+'.png' 
                        fileName =os.path.join(aivBotMmap.sysInfo['sys.outDir'],file)
                        fileInfo = getFileInfo(fileName) #用函数getFileInfo 生成文件的信息
                        # files.append(fileInfo)
                        if param['data'] is None:
                            param['data'] = []
                        param['data'].append(fileInfo)
                    

                args = task


            # ========================================================================================
            # ============正式调用bot api 函数 =========================================================== 2 
            from aiv.aivmmap import TaskResultCode
        
            # 运行bot api函数('run'阶段)----------------------------------------------
            callParam = {'bot':self, 'sysInfo':aivBotMmap.sysInfo, 'taskInfo': args} #把任务信息和系统信息打包,一起给bot的api传参
            retTask = apiFun('run',callParam) #调用用户Bot的api函数 2024.4
            # logger.warning('bot: args参数的类型是: {}, 内容是：{}'.format(type(args)))
            # logger.warning('Bot api {} 运行返回结果是: {}'.format(apiName,retTask))
            # -----------------------------------------------------------------------

            # 根据生成的文件,生成文件信息---------------------------------
            paramOut = task['paramOut']
            for param in paramOut:
                if (param['type'].lower() == 'file') and (param['data'] is not None):  
                    for i in range(len(param['data'])):
                        file = param['data'][i]
                        # 根据文件名生成文件信息（如果文件没有生成在磁盘,则部分信息为空<如文件大小、md5码等>)
                        param['data'][i] = getFileInfo(file['path']) #用函数getFileInfo 生成文件的信息 更新原来的文件信息
                        # print('文件信息是:',fileInfo)
            # ---------------------------------------------------------
            
            if retTask is None or  retTask['result']['code'] != 200:
                # 设置成功标志
                aivBotMmap.setTaskResultCode(TaskResultCode.taskOk,'Bot:{} 的api {}运行完成.'.format(self.botInfo.botName, apiName)) # 设置为OK状态

        except Exception as e:
            errMsg = 'Bot模块[ {} ]的api函数:{} 执行出现错误: {}'.format(self.botInfo.botName,api['name'],e)
            logger.warning(errMsg)
            aivBotMmap.setTaskResultCode(TaskResultCode.taskSvr,errMsg) # 设置为服务器出错状态,并把出错信息回传js端 2023.12
        finally:
            aivBotMmap.endTask() # api函数内修改了task对象,也会同步返回
            # logger.warning('apiFun finally 运行完成222!') 

    
    def addFileToTaskOutParam(self,filePath):
        from loguru import logger
        if self.task is None:
            logger.warning('没有任务信息')
        else:
            logger.debug('接收新的回传文件: {}'.format(filePath))


            from .aivtool import getFileInfo

            
            isEmptyFile = True
            if len(self.task['paramOut']) > 0:                
                for param in self.task['paramOut']:
                    # 'paramOut'里面必须有且仅有一条 'type'=='FILE'的记录 2024.4
                    if param['type'] == 'FILE' and param['data'] is not None:
                        isFind = False

                        # 如果已经存在 param['type'] == 'FILE' 的记录,则查询当前文件是否保存在里面
                        for file in param['data']:
                            if file['path'].lower() == filePath.lower():
                                isFind = True
                                break

                        if not isFind:
                            logger.debug('接收新的回传文件222: {}'.format(filePath))
                            # 如果判断没有保存,则新增一个文件记录到 'data'数组
                            param['data'].append(getFileInfo(filePath))

                        isEmptyFile = False

            if isEmptyFile: #没有 'type' == 'FILE' 的记录,直接添加一条
                self.task['paramOut'].append({'type': 'FILE', 'data': [getFileInfo(filePath)]})


    def addStringToTaskOutParam(self, text):
        isEmptyText = True
        if len(self.task['paramOut'])>0:
            for param in self.task['paramOut']:
                # 'paramOut'里面必须有且仅有一条 'type'=='STRING'的记录 2024.4
                if param['type'] == 'STRING' and param['data'] is not None:
                    param['data'].append(text)
                    isEmptyText = False
                    break
 
        if isEmptyText:            
            self.task['paramOut'].append({'type':'STRING', 'data': [text]})


    def dictToList(self,tup:tuple):  
        '''     
            ## tuple 转 list
            要把 dict = tuple(dict.items()) 先转成元组，再调用此函数
            {
                '--face' : 'docs/imgs/007.mp4',
                '--audio' :  'docs/imgs/004.wav',
                '--outfile' :  'docs/out/003.mp4',
                '--face_det_batch_size' : '1',
                '--wav2lip_batch_size' : '1' ,
                '--face_enhancement' : True

            }
            ## 像上面这样的Dict ，转成:
            [
            '--face', 'docs/imgs/007.mp4', '--audio', 'docs/imgs/004.wav', '--outfile', 
            'docs/out/003.mp4', '--face_det_batch_size', '1', '--wav2lip_batch_size', 
            '1', '--face_enhancement'
            ]
            ## 目的是从dict拿参数,调用命令行工具 (传参给命令行工具) 2023.8 
        ''' 
        myls = []
        for t in tup:
            if (isinstance(t,tuple)) and (len(t)>1):
                myls = myls + self.dictToList(t) #递归调用
            else:
                if not isinstance(t,bool) : #把参数值是 True 或 False 的值剔除 (命令行中,Bool参数不用显式赋值True或False)

                    if isinstance(t,int): # 把参数是 int 的转成字符串
                        myls.append(str(t))
                    else:
                        # 把参数是 'True'  的剔除
                        if (t.strip().lower()=='true') :
                            pass
                        elif (t.strip().lower()=='false'):
                            if len(myls)>0:
                                myls.pop() # 'False'时，把整个参数项删除
                        else:
                            myls.append(t)
        return myls

    def regBotApi(self,glob:dict): #利用 globals() 读取指定模块的所有函数名
        '''
        ### 注册 bot 模块
        * 参数 glob 包含有模块的函数及函数地址！
        * 将自动注册以 api 开头的函数为Api函数!
        * Api 函数,必须要有一个参数: paramdict=None ,其它参数可以自行添加,外部调用时,paramdict将包含有调用Api的参数
        * Api 函数内,调用一个参数转换函数_aivparam(),可以把 parser.add_argument()添加的参数自动导出
        * 函数必须以 api 开头才能导出
        * 如果要导入其它模块的函数,可以在集中一个模块中，使用 from xxx.xxx import xxx 这样的方式导入
        * 导入的函数也可以改名 : from xxx.xxx import fun01 as api_fun01
        '''
        from loguru import logger
        from .aivtool import checkReservedName
        lst = list(glob)
        import types
        # logger.debug('bot 模块所有参数如下 (包含模块内所有函数、方法名称和内存地址): \n{}'.format(glob))

        #循环模块的所有函数,把aiv 开头的函数自动导入----------------------------------
        for fun_name in lst:
            fun = glob[fun_name]   
            if (type(fun) == types.FunctionType) or (type(fun) == types.MethodType): #判断是方法（而不是属性)
                if fun_name != 'run' and not fun_name.startswith('_'): #排除检测 run()函数和 "_"开头的函数 2024.3 ,其它函数都可以导出                              
                    
                    if not checkReservedName(fun_name,'注册Bot的Api函数'):
                        # apidict 只记录静态的信息
                        apidict = {'api':self.botInfo.botName, 'name':fun_name,'fun':fun,'paramIn':None,'parser':None}
                        self.api.append(apidict)

                        # callParam = {'bot':self, 'sysInfo':aivBotMmap.sysInfo} #把任务信息和系统信息打包,一起给bot的api传参  
                        # fun('init', callParam) #初始化Api函数
                 

        logger.info('\nbot模块:[ {} ] api函数初始化完成.'.format(self.botInfo.botName))

        if len(self.api)==0:
            logger.warning('Bot: {} 还没有注册任何 api 函数.'.format(self.botInfo.botName))
        else:
            logger.debug('\nrun() 成功启动bot模块:{} \n它的api函数列表是: \n{}'.format(self.botInfo.botName,self.api))


    def getOutPath(self,childPath):
        ''' 
            在AIV系统默认的输出目录中创建一个子文件夹
            可以在此目录基础上新建一个子目录给每个Bot专用 ,在设置'sys.outDir'目录里的生成文件会定时被清理, 
            可以避免系统运行久了垃圾过多的问题. (每隔10分钟系统清理一次超过24小时未使用的临时文件,比如图片、社频等)
            客户端一般都是生成图片或程序即会自动下载,AGI端无需长期保存. 2024.3
        '''
        outPath = aivBotMmap.sysInfo['sys.outDir'] 
        outPath = os.path.normpath(os.path.join(outPath,childPath)) #需要用normpath()规范化路径,不然
        if not os.path.exists(outPath):
            os.mkdir(outPath)
        return outPath


## 2、注册Api的调用参数 (必须由bot模块在api函数内调用 )============================================================================
def regParser(parser :argparse.ArgumentParser,modify=None, #此函数不带使用 2024.4
                    dev=None):
    '''
        ### 注册命令行参数
        * 参数
            parser          argparse.ArgumentParser 类实例
            modify          修改默认值的字段列表
                            文件类的修改如下：
                                ['checkpoint_path','type','file_open|model|all'],
                                ['audio','type','file_open|audio'],
            dev             开发人员才能配置（显示）的字段
 

        * 为当前函数注册调用的参数及格式，包含：关键字、默认值、数据类型、可选值...等等
        * 对大多数命令行工具,都是用ArgumentParser解析参数。如果参数是从dict输入,而不是从命令行中得来
        * Api函数默认有两个参数 (cmd,args=None) ,AivAgent 调用 Api函数时,有三种情况：
             cmd='init' 时, 只在bot初始化时调用一次
             cmd='param' 时,在用户读param时,调用一次 (如果param不为空,就不会带调用)
             cmd='run' 时,用户运行api函数调用,可以无数次

        #### 注意:此函数需要先用ArgumentParser实例的函数 parser.add_argument() 添加参数到Api函数内,才能自动转换成 ,2023.8

        从命令行参数转换成Aiv参数样例格式如下: ----------------------------------
        [
            {'option_strings': ['--checkpoint_path'], 'dest': 'checkpoint_path', 'default': None, 'type': 'file_open|model|all', 'choices': None, 'required': False, 'help': 'Name of saved checkpoint to load weights from', 'value': None}, 
            {'option_strings': ['--audio'], 'dest': 'audio', 'default': None, 'type': 'file_open|audio', 'choices': None, 'required': True, 'help': 'Filepath of video/audio file to use as raw audio source', 'value': None}, 
            {'option_strings': ['--face'], 'dest': 'face', 'default': None, 'type': 'file_open|video|image|all', 'choices': None, 'required': True, 'help': 'Filepath of video/image that contains faces to use', 'value': None}, 
            {'option_strings': ['--outfile'], 'dest': 'outfile', 'default': 'results/result_voice.mp4', 'type': 'file_save|video', 'choices': None, 'required': True, 'help': 'Video path to save result. See default for an e.g.', 'value': None}, 
            {'option_strings': ['--static'], 'dest': 'static', 'default': False, 'type': 'bool', 'choices': None, 'required': False, 'help': 'If True, then use only first video frame for inference', 'value': None}, 
            {'option_strings': ['--fps'], 'dest': 'fps', 'default': 25.0, 'type': 'float', 'choices': None, 'required': False, 'help': 'Can be specified only if input is a static image (default: 25)', 'value': None}, 
            {'option_strings': ['--pads'], 'dest': 'pads', 'default': [0, 10, 0, 0], 'type': 'int', 'choices': None, 'required': False, 'help': 'Padding (top, bottom, left, right). Please adjust to include chin at least', 'value': None}, 
            {'option_strings': ['--face_det_batch_size'], 'dest': 'face_det_batch_size', 'default': 1, 'type': 'int', 'choices': None, 'required': False, 'help': 'Batch size for face detection', 'value': None}, 
            {'option_strings': ['--wav2lip_batch_size'], 'dest': 'wav2lip_batch_size', 'default': 1, 'type': 'int', 'choices': None, 'required': False, 'help': 'Batch size for Wav2Lip model(s)', 'value': None}, 
            {'option_strings': ['--resize_factor'], 'dest': 'resize_factor', 'default': 1, 'type': 'int', 'choices': None, 'required': False, 'help': 'Reduce the resolution by this factor. Sometimes, best results are obtained at 480p or 720p', 'value': None}, 
            {'option_strings': ['--crop'], 'dest': 'crop', 'default': [0, -1, 0, -1], 'type': 'int', 'choices': None, 'required': False, 'help': 'Crop video to a smaller region (top, bottom, left, right). Applied after resize_factor and rotate arg. Useful if multiple face present. -1 implies the value will be auto-inferred based on height, width', 'value': None}, 
            {'option_strings': ['--box'], 'dest': 'box', 'default': [-1, -1, -1, -1], 'type': 'int', 'choices': None, 'required': False, 'help': 'Specify a constant bounding box for the face. Use only as a last resort if the face is not detected.Also, might work only if the face is not moving around much. Syntax: (top, bottom, left, right).', 'value': None}, 
            {'option_strings': ['--rotate'], 'dest': 'rotate', 'default': False, 'type': 'bool', 'choices': None, 'required': False, 'help': 'Sometimes videos taken from a phone can be flipped 90deg. If true, will flip video right by 90deg.Use if you get a flipped result, despite feeding a normal looking video', 'value': None}, 
            {'option_strings': ['--nosmooth'], 'dest': 'nosmooth', 'default': False, 'type': 'bool', 'choices': None, 'required': False, 'help': 'Prevent smoothing face detections over a short temporal window', 'value': None}, 
            {'option_strings': ['--cpu'], 'dest': 'cpu', 'default': False, 'type': 'bool', 'choices': None, 'required': False, 'help': 'cpu mode.', 'value': None}, 
            {'option_strings': ['--face_detector'], 'dest': 'face_detector', 'default': 'sfd', 'type': 'str', 'choices': None, 'required': False, 'help': 'face detector to be used, can choose s3fd or blazeface', 'value': None}, 
            {'option_strings': ['--face_enhancement'], 'dest': 'face_enhancement', 'default': False, 'type': 'bool', 'choices': None, 'required': False, 'help': 'use face enhance for face', 'value': None}, 
            {'option_strings': ['--path_to_enhance'], 'dest': 'path_to_enhance', 'default': None, 'type': 'file_open|model|all', 'choices': None, 'required': False, 'help': 'face_enhancement path_to_enhance to be used, 设置本地路径', 'value': None}
        ]
    '''

    if parser is None: #bot初始化时,也可以传空的 parser进来 (这意味着调用此 api 函数不依赖 parser) 2023.12
        return
    
    from loguru import logger
    
    def _change_type(param_list,fileparam=None,devfield=None):
        '''
        #### 对argparse 自动生成的参数进行调整
        id001 -> str
        id002 -> int
        float -> float
        bool -> bool
        null -> 根据 default 判断,如果有 false 或 true 就判断为 bool
        * 这是对parser 复制出来的内容修改,所以不会影响原来的parser 对象

        * 类似以下的格式
        *       params = {   
        *           '--face' : 'docs/imgs/007.mp4',
        *           '--audio' :  'docs/imgs/004.wav',
        *           '--outfile' :  'docs/out/003.mp4',
        *           '--face_det_batch_size' : 1,
        *           '--wav2lip_batch_size' : 1 ,
        *           '--face_enhancement' : 'True',
        *       }
        * 转换成 tuple:
            tuple('--face','docs/imgs/007.mp4','--audio', 'docs/imgs/004.wav','--outfile', 'docs/out/003.mp4',....)
        '''
        for param in param_list:
            if 'type' in param: # 根据常规的type字段内容,修改成易于读写的格式: str,int,float,bool (把一些类的信息去除)
                typeclass = param['type']  # type 自动生成的值是： 'type': <class 'str'>
                if  typeclass==str: 
                    #pass
                    param['type'] = 'str'
                elif typeclass == int:
                    param['type'] = 'int'
                elif typeclass==bool:
                    param['type'] = 'bool'
                elif typeclass==float:
                    param['type'] = 'float'
                elif typeclass==None:
                    if 'default' in param: #如果字段有默认值,通过默认值,也可以判断字段的类型 (特别是bool类型)
                        default_value = param['default']
                        #print('bool类型：\n',type(boolvalue))
                        if type(default_value)==bool:
                            param['type'] = 'bool'

            #根据 dest 的字段名,修改指定'type'字段类型
            if fileparam is not None and 'dest' in param:
                for file in fileparam:
                    if (param['dest']==file[0]) and (file[1]=='type'): #只修改 'type'字段的值
                        param['type'] = file[2]

            #增加一个字段,以便web端用户返回值
            # param['value'] = None 
        return param_list
    
    #修改已添加的参数属性-------------
    def _param_change(parser :argparse.ArgumentParser,modlist):
        '''
        ### 修改参数的字段值
        * 功能 在参数添加后,又修改部位属性。
        * 用途 不用修改原来的代码,又能改变已经添加的参数的属性。
        * 场景 原来的代码是其他人/公司开发,是一个整体;或者更新很快,如果直接修改,迭代成本高。因此此函数修改原代码参数属性。
        * 参数 parser :argparse.ArgumentParser 对象 ,
        * modlist 参数类似下面：
            ['face_det_batch_size','default',1]
            数组[0] 需要修改的参数名; 数组[1] 参数的字段是argparse.ArgumentParser中的
            'default','action','help' 等; 数组[2] 将要修改的结果值
        '''
        for action_group in parser._action_groups:
            if len(action_group._group_actions)>0:
                for action_ in action_group._group_actions:  
                    dic = action_.__dict__
                    #这个函数,是直接修改parser里面的值,是直接影响到外面传进来的参数表
                    #因此,只能修改 default,required等值,不能修改'type'的值
                    if dic['dest']==modlist[0] and (modlist[1] not in ['type']):
                        #logger.debug('----参数: {} \n'.format(action_.__dict__))
                        if modlist[1] in dic: #直接修改外面传进来的 parser
                            dic[modlist[1]] = modlist[2]
                        break  
    
    if aivBot is None or aivBot.api is None:
        return
    
    #查找调用本函数的上层函数名 (即是Api函数)
    import inspect
    frame = inspect.stack() #返回函数的调用栈

    # 如果上一级调用是函数,则是函数名,如果是__main__中调用,值则是"module" 
    fun_name = frame[1][3] #从调用栈中获取上一级调用的函数名
    if not fun_name.startswith('api'):
        logger.error('_aiv_reg_parser() 必须在以 bot 开头的函数中调用!' )
        return
    
    #根据函数名,找出对应的运行时信息,更新它
    for api_run in aivBot.api:

        # 循环所有的 api 函数,对比找出是哪一个api函数调用 regParser()函数 (通过调用栈inspect.stack() 可以获取) 2023.11
        if api_run['name']==fun_name:

            if api_run['parser'] is None:
                api_run['parser'] = parser  # 给api函数对应的 parser 变量赋值 (AIV系统设计, parser也可以为空,这样调用api函数就不依赖argparse.ArgumentParser() ) 2023.12
                  
            # if api_run['i18n'] is None:
            #     api_run['i18n'] = i18n 

            if api_run['paramIn'] is None:
                #根据要修改的字段,先修改好
                if modify is not None:
                    for modlist in modify:
                        #这个函数,是直接修改parser里面的值,是直接影响到外面传进来的参数表
                        #因此,只能修改 default,required等值
                        _param_change(parser,modlist)

                #根据 parser 对象的值,生成run_time的param信息--------------------------
                import copy
                param_list = []
                for action_group in parser._action_groups:
                    #print('长度：  ',len(action_group))
                    if len(action_group._group_actions)>0:
                        for action_ in action_group._group_actions:  
                            #logger.debug('----参数: {} \n'.format(action_))
                            # action_数据格式类似下面：----------------------------------------------------------
                            #_StoreTrueAction(option_strings=['--rotate'], dest='rotate', nargs=0, const=True, 
                            # default=False, type=None, choices=None, required=False, 
                            # help='Sometimes videos taken from a phone can be flipped 90deg.', metavar=None)
                            dic = copy.deepcopy(action_.__dict__) #深度复制一份,不然会修改到原始的数据, 导致许多意想不到的错误 2023.09
                            dellist = ['container','metavar','nargs','const'] #删除一些用不上的的字段
                            for li in dellist:
                                if li in dic:
                                    del dic[li] #删除无用的参数

                            #dic = action_.__dict__
                            # dic['label'] = dic['dest'] #增加一个字段,用于翻译国际化
                            # dic['devhelp'] = None #增加一个字段 'devhelp' ，表示开发者帮助
                            # dic['dev'] = False #增加一个字段 'dev' ，表示开发者控制的字段,前端读出时,只有注册为开发者的用户,才能修改此字段的值
                            
                            param_list.append(dic)
                
                # logger.aiv('函数{}() 原始的参数paramlist列表是:\n{}'.format(fun_name,param_list))  
                #默认第一组元素是：  ['-h', '--help'] ，所以要删除它
                if len(param_list)>0:
                    del param_list[0]

                #如果不对自动生成的参数加工，则有些数据可能不适合 Web 端使用-----------------------------
                param_list = _change_type(param_list,modify,dev) #对自动生成的param参数,进行一些基本的调整,包括指定输入输出文件
                #-----------------------------------------------------------------------------------
                logger.debug('函数{}() 加工后的参数paramlist列表是:\n{}'.format(fun_name,param_list) )
                api_run['paramIn'] = param_list

            
            break







    







