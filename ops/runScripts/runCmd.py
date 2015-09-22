import global_setting,os
os.environ["DJANGO_SETTINGS_MODULE"]= "ops.settings"
import pxssh,time,threading,pexpect
from ops01.models import *




class execute:
	def __connectHost(self,command,hostname,ip,username,password,trackMark):
		try:
			
        		s = pxssh.pxssh()
       			s.login(ip,username,password)
        		s.sendline(command)
        		s.prompt()
        		print "\n-------------------------------%s----------------------------------\n%s\n%s" % (hostname,s.before,time.ctime())
			ops_log = OpsLogTemp(user = username, 
				ip = ip,
				event_type = 'cmd',
				cmd = command, 
				event_log = s.before,
				result='success',
				track_mark = trackMark)
			ops_log.save()
			s.logout()
			
		except pxssh.ExceptionPxssh,e:
			ops_log = OpsLogTemp(user = username, 
				ip = ip,
				event_type = 'cmd',
				cmd = command, 
				event_log = s.before,
				result='failed',
				track_mark = trackMark)
			ops_log.save()
       			print "pxssh failed on login."
       			print str(e)


	def run(self,cmd,hostInfo,username,password,trackMark):
		#print time.ctime()
		#host = IP.objects.annotate()   #get hostname and ip address
		for hostname,ip in hostInfo.items():  #hostInfo is dic
			t = threading.Thread(target=self.__connectHost,args=(cmd,hostname,ip,username,password,trackMark))
			t.start()
		print "current has %d threads" % (threading.activeCount() - 1)

"""	def __connectScp(self,hostname,ip,username,password,filename,pathname):
		child = pexpect.spawn('/usr/bin/scp',[filename,username+'@'+ip+':'+pathname])
		try:
        		child.expect('(?i)password:')
        		child.sendline(password)
        		child.expect(pexpect.EOF)
        		print "\n-------------------------------%s----------------------------------\n%s\n%s" % (hostname,child.before,time.ctime())
		except EOF:
        		print "EOF error."
		except TIMEOUT:
        		print "Timeout error"
	
	def scp(self,filename,sql,pathname='/root'):
		print time.ctime()
		HInfo = host_info.hostInfo()
		host = HInfo.hostInfo(sql)
		for i in host:
			t = threading.Thread(target=self.__connectScp,args=(i[0],i[1],i[2],i[3],filename,pathname,))
			t.start()
		print "current has %d threads" % (threading.activeCount() - 1)

"""
if __name__ == "__main__":
	r = execute()
	username = "root"
	password = "www.eegoo"
	hostInfo= {'test_www':'172.16.20.51','test_member':'172.16.20.53'}
	trackMark = 1
	r.run('ifconfig',hostInfo,username,password,trackMark)
	
	#r.scp('menu.py',"select * from host where hostname='test_pay'")
