import time
import os

default_loc='~/Documents/tmp'
class Logger:
    def __init__(self,loc=default_loc):
        if(loc[-1]!='/'):
            loc=loc+'/'

        # check if directory exists
        if not os.path.isdir(loc):
            result=create_dic(loc)
            if result<0:
                raise LoggerException("Failed to create dic "+loc)

        self.filename=loc+'log_'+time.asctime()+'.txt'
    
        self.level_dic=level_dic={0:"log",1:"warning",2:"warning handling",
                    3:"error",4:"error-handling",5:"log system warning"}

        
        self.f=open(self.filename,'w')
    
    def print(self,msg,level=0):
        if(not level in self.level_dic):
            msg="Trying to log message \""+msg+"\" with invalid level "+str(level)
            level=len(self.level_dic)-1
        if msg[-1]=='\n':
            msg=msg[0:-1]
        template="<<{0}>>[{1}] - {2}\n"
        self.f.write(template.format(time.asctime(),self.level_dic[level],msg))
        self.f.flush()

    def level_dic_lookup(self,level):
        if(not level in self.level_dic):
            return "Not Found"
        else:
            return self.level_dic[level]

    def __del__(self):
        self.f.close()

def create_dic(path):
    try:
        os.makedirs(path)
        return 0
    except Exception as e:
        print("A Exception is Thrown "+e)
        return -1

class LoggerException(Exception):
    def __init__(self, message):
        self.message=message

def SoftWrapper(var):
    if not var is None:
        return var
    else:
        return _SoftBlow()

class _SoftBlow:

    def __getattr__(self,name):
        return lambda *args:None