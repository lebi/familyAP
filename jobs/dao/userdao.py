#coding=utf-8
#!/usr/bin/python
from file import dbmanager
from server import settings
import sys
sys.path.append(settings.JOBPATH)

class userdao():

	fm=dbmanager.FileManager()
	table=settings.JOBPATH+'/db/user.db'
	columns=['id','username','password','rank']

	admintable=settings.JOBPATH+'/db/admin.db'
	admincolumns=['username','sfileauth','wdaystarttime','wdaystoptime','wendstarttime','wendstoptime','limit']

	def __init__(self):
		self.data=[]

	def adduser(self,user):
		self.fm.insert(self.table, self.columns, user)

	def deleteuser(self,user):
		self.fm.delete(self.table, ['username='+user])

	def selectuser(self,conditions=[]):
		return self.fm.select(self.table, self.columns, conditions)

	def updateuser(self,columns,value,conditions=[]):
		self.fm.update(self.table, columns, value, conditions);

	def createtable(self):
		self.fm.create(self.table, self.columns)

	def droptable(self):
		self.fm.drop(self.table)

	def manageuser(self,columns,value,conditions=[]):
		self.fm.update(self.admintable,columns,value,conditions)

	def addusertoadmin(self,columns,value):
		self.fm.insert(self.admintable,columns,value)

	def selectadminuser(self,conditions):
		return self.fm.select(self.admintable,self.admincolumns,conditions)

# if __name__ == '__main__':
# 	dao=userdao()
# 	dao.createtable()