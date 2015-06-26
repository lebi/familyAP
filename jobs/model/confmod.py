#coding=utf-8
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import confdao

class ConfMod():
	apddao=confdao.ApdDao()
	def __init__(self):
		self.data=[]

	def selectApd(self,request):
		type=request.GET.get('type')
		targets=[]
		if int(type)==1:
			targets=['ssid','channel','interface']
		elif int(type)==2:
			targets=['wpa']
		return self.apddao.getRules(targets)

	def updateApd(self,request):
		ssid=request.GET.get('ssid')
		channel=request.GET.get('channel')
		interface=request.GET.get('interface')
		target=['ssid','channel','interface']
		value=[ssid,channel,interface]
		self.apddao.changeRules(target,value)

