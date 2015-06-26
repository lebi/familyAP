#coding=utf-8
#!/usr/bin/python
from file import dbmanager
from server import settings
import sys
sys.path.append(settings.JOBPATH)

class onlinedao():

	fm=dbmanager.FileManager()
	table=settings.JOBPATH+'/db/online.db'
	# table='../db/online.db'
	columns=['username','mac','ip','speed']

	def __init__(self):
		self.data=[]

	def adduser(self,columns,user):
		self.fm.insert(self.table, columns, user)

	def deleteuser(self,conditions):
		self.fm.delete(self.table, conditions)

	def selectuser(self,conditions=[]):
		return self.fm.select(self.table, self.columns, conditions)

	def updateuser(self,columns,value,conditions):
		self.fm.update(self.table, columns, value, conditions)

	def createtable(self):
		self.fm.create(self.table, self.columns)

	def droptable(self):
		self.fm.drop(self.table)

# if __name__ == '__main__':
# 	dao=userdao()
# 	dao.createtable()