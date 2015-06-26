#coding=utf-8
#!/usr/bin/python
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import onlinedao
from shell import speed

class OnlineMod():
	onlinedao=onlinedao.onlinedao()
	speedlimit=speed.SpeedLimit()
	def __init__(self):
		self.data=[]

	def getOnlineList(self,request):
		list=self.onlinedao.selectuser()
		ip=request.META['REMOTE_ADDR']
		jsonlist=[]
		for u in list:
			user={}
			if u[2]==ip:
				u[0]+='(当前)'
			user['username']=u[0]
			user['mac']=u[1]
			user['ip']=u[2]
			user['speed']=u[3]
			jsonlist.append(user)
		return jsonlist


	def getOnlineByIp(self,ip):
		list=self.onlinedao.selectuser(['ip='+ip])
		user={}
		for u in list:
			user['username']=u[0]
			user['mac']=u[1]
			user['ip']=u[2]
			user['speed']=u[3]
		return user

	def updateSpeed(self,request):
		username=request.GET.get('username');
		ip=request.GET.get('ip')
		speed=request.GET.get('speed')
		condition=['username='+username,'ip='+ip]
		prespeed=self.onlinedao.selectuser(condition)[0][3]
		# if not speed.isdigit():
		# 	return
		# elif speed=='':

		# 	self.speedlimit.addLimit(ip,speed)
		# 	self.onlinedao.updateuser(['speed'],[speed],['username='+username,'ip='+ip])
		if speed=='':
			speed='null'
			self.speedlimit.deleteLimit(ip,prespeed)
		elif speed.isdigit():
			if prespeed!='null':
				self.speedlimit.updateLimit(ip,prespeed,speed)
			else:
				self.speedlimit.addLimit(ip,speed)
		else:
			return
		self.onlinedao.updateuser(['speed'],[speed],condition)
