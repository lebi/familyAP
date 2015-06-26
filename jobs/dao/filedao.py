#coding=utf-8
#!/usr/bin/python
from file import dbmanager
from server import settings
import sys
sys.path.append(settings.JOBPATH)

class filedao():

	fm=dbmanager.FileManager()
	table=settings.JOBPATH+'/db/file.db'
	columns=['id','username','filepath','filename','priority','timestamp']

	def __init__(self):
		self.data=[]

	def selectfile(self,conditions=[]):
		return self.fm.select(self.table, self.columns, conditions)

	def insertfile(self,value):
		self.fm.insert(self.table,self.columns,value,flag=0)

	def deletefile(self,conditions=[]):
		self.fm.delete(self.table,conditions,flag=0)
