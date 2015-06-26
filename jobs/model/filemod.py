#coding=utf-8
#!/usr/bin/python
# import os
# sys.path.append(os.path.abspath('..'))
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import filedao

class FileMod(object):
	filedao=filedao.filedao()

	def __init__(self):
		self.data=[]

	def getFileList(self,conditions=[]):
		files=self.filedao.selectfile(conditions)
		print files
		filejsonlist=[]
		for f in files:
			filepath={}
			filepath['id']=f[0]
			filepath['username']=f[1]
			filepath['filepath']=f[2]	
			filepath['filename']=f[3]
			filepath['priority']=f[4]
			filepath['timestamp']=f[5]
			filejsonlist.append(filepath)
		return filejsonlist
	def insertFile(self,value):
		self.filedao.insertfile(value)

	def deleteFile(self,conditions=[]):
		self.filedao.deletefile(conditions)