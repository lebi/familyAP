#coding=utf-8
#!/usr/bin/python
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import userdao
from dao import onlinedao
from shell import nat

class LogMod(object):
	userdao=userdao.userdao()
	onlinedao=onlinedao.onlinedao()

	def __init__(self):
		self.data=[]

	def login(self,request):
		username=request.GET.get('username')
		password=request.GET.get('password')
		user=self.userdao.selectuser(['username='+username,'password='+password])
		userjson={}
		if len(user)==1:
			ip = request.META['REMOTE_ADDR']
			request.session[ip]=username  #session set key:ip address  value:username
			agent=request.META['HTTP_USER_AGENT']
			agents=agent.split(' ')
			if len(self.onlinedao.selectuser(['username='+username,'ip='+ip]))==0:
				self.onlinedao.adduser(['username','mac','ip'],[username,agents[3],ip])
				NAT=nat.NAT()
				NAT.allowUser(ip)
			userjson={'username':username,'rank':user[0][3]}
		return userjson

	def checkLogin(self,request):
		ip = request.META['REMOTE_ADDR']
		if request.session.has_key(ip):
			username=request.session[ip]
			if len(self.onlinedao.selectuser(['username='+username,'ip='+ip]))>0:
				return int(self.userdao.selectuser(['username='+username])[0][3])
		return 0

	def logout(self,request):
		username=request.GET.get('username')
		ip=request.GET.get('ip')
		condition=['username='+username,'ip='+ip]
		try:
			NAT=nat.NAT()
			NAT.banUser(ip)
		finally:
			self.onlinedao.deleteuser(condition)	
			if request.session.has_key(ip):
				del request.session[ip]
