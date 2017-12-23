import paramiko
import ConfigParser
import time

class Paramiko_cient:
    def __init__(self,device_name,config_file):
        self.device_name = device_name
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    def connect(self):

        try:
            self.client.connect(hostname=self.config.get(self.device_name,'host'),
                                port = self.config.getint(self.device_name,'port'),
                                username=self.config.get(self.device_name,'username'),
                                password=self.config.get(self.device_name,'password'),
                                timeout=self.config.getfloat(self.device_name,'timeout'))
            print 'Device %s connected' %self.config.get(self.device_name,'host')
        except Exception,e:
            print e
            try:
                self.client.close()
                print '%s could not connected'%self.config.get(self.device_name,'host')
                return e
            except:
                pass

    def run(self,cmd_str,timeout=None):
        timeout = timeout
        #while i< 5 and (not self.client.get_transport()):
        #    self.connect()
        #    print "Trying to reconnect,please wait"
        #    time.sleep(2)
        stdin,stdout,stderr = self.client.exec_command(cmd_str,timeout)
        res = stdout.read()
        err = stderr.read()
        result = res if res else err
        return result

    def run_cmd(self,cmd_str):
        print cmd_str
        result = self.run(cmd_str)
        print result
        return result


    def close(self):
        self.client.close()


