#coding=utf-8
#!/usr/bin/python
# import os
# sys.path.append(os.path.abspath('..'))
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import userdao

class UserMod(object):
	userdao=userdao.userdao()

	def __init__(self):
		self.data=[]

	def getUserList(self):
		users=self.userdao.selectuser()
		userjsonlist=[]
		for u in users:
			user={}
			user['username']=u[1]
			user['rank']=u[3]
			userjsonlist.append(user)
		return userjsonlist

	def updateRank(self,request):
		username=request.GET.get('username')
		rank=request.GET.get('rank')
		if int(rank) < 0:
			self.userdao.updateuser(['rank'],[-1],['username='+username])
		else :
			self.userdao.updateuser(['rank'],[2],['username='+username])

	def addUser(self,value):
		userList=self.userdao.selectuser(['username='+value[1]])
		if len(userList) == 0:
			self.userdao.adduser(value)

	def updateUser(self,value,conditions):
		columns=['username','password']
		self.userdao.updateuser(columns,value,conditions)

	def manageUser(self,value,conditions):
		username=conditions[0].split('=')[1]
		self.addUsertoadmin(username)
		for i in range(len(value)):
			if value[i]=="":
				value[i]='null'
		columns=['sfileauth','wdaystarttime','wdaystoptime','wendstarttime','wendstoptime','limit']
		self.userdao.manageuser(columns,value,conditions)

	def addUsertoadmin(self,username):
		settingList=self.userdao.selectadminuser(['username='+username])
		if len(settingList)==0:
		# columns=['username','sfileauth','wdaystarttime','wdaystoptime','wendstarttime','wendstoptime','limit']
			columns=['username']
			self.userdao.addusertoadmin(columns,[username])

	def selectSettingDetail(self,username):
		detail=self.userdao.selectadminuser(['username='+username])[0]
		print detail
		columns=['username','sfileauth','wdaystarttime','wdaystoptime','wendstarttime','wendstoptime','limit']
		detailmap={}
		for i in range(len(columns)):
			if detail[i]=='null':
				detail[i]=''
			detailmap[columns[i]]=detail[i]
		return detailmap

# if __name__ == '__main__':
# 	mod=UserMod()
# 	print mod.getUserList()
