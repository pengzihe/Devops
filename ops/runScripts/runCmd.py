import global_setting,os
os.environ["DJANGO_SETTINGS_MODULE"]= "ops.settings"
import pxssh,time,threading,pexpect
from ops01.models import *




class execute:
	def __connectHost(self,command,hostname,ip,username,password):
		try:
			
        		s = pxssh.pxssh()
       			s.login(ip,username,password)
        		s.sendline(command)
        		s.prompt()
        		print "\n-------------------------------%s----------------------------------\n%s\n%s" % (hostname,s.before,time.ctime())
			a = s.before
			print '--------------'
			print a
			ops_log = OpsLogTemp(user = username, 
				ip = ip,
				event_type = 'cmd',
				cmd = command, 
				event_log = s.before,
				result='success',
				track_mark = 1)
			ops_log.save()
			s.logout()
			
		except pxssh.ExceptionPxssh,e:
       			print "pxssh failed on login."
       			print str(e)


	def run(self,cmd,username,password):
		#print time.ctime()
		host = IP.objects.annotate()   #get hostname and ip address
		for h in host:
			t = threading.Thread(target=self.__connectHost,args=(cmd,h.display_name,h.ip,username,password))
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
	r.run('date',username,password)
	
	#r.scp('menu.py',"select * from host where hostname='test_pay'")
