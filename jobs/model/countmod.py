#coding=utf-8
#!/usr/bin/python
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import countdao
import usermod
from shell import nat
import datetime

class CountMod(object):
	dao=countdao.CountDao()
	nat=nat.NAT()

	def __init__(self):
		self.data=[]

	def addCount(self,username):
		countMap={'username':username}
		self.dao.add(countMap)
		self.resetCount(username)

	def getUserCount(self,username):
		count=self.dao.select(username)
		return count

	def countdown(self,username):
		countMap=self.dao.select(username)
		if len(countMap)==0:
			self.addCount(username)
		count=countMap['count']
		if count.isdigit() and int(count) > 0:
			count-=1
			self.dao.setCount(count,username)

	def resetCount(self,username):
		mod=usermod.UserMod()
		detail=mod.selectSettingDetail(username)
		d=datetime.datetime.now()
		if d.weekday()==6 or d.weekday()==7:
			count='null'
			if detail['wendstarttime'].isdigit():
				count=int(detail['wendstarttime'])*2
				if detail['wendstoptime'].isdigit() and int(detail['wendstoptime']) != 0:
					count+=1
		else:
			count='null'
			if detail['wdaystarttime'].isdigit():
				count=int(detail['wdaystarttime'])*2
				if detail['wdaystoptime'].isdigit() and int(detail['wdaystoptime']) != 0:
					count+=1
		if len(self.dao.select(username))==0:
			self.dao.add(countMap={'username':username})
		self.dao.setCount(count,username)