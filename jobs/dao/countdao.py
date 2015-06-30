#coding=utf-8
#!/usr/bin/python
from file import dbmanager
from server import settings
import sys
sys.path.append(settings.JOBPATH)

class CountDao():
	fm=dbmanager.FileManager()
	table=settings.JOBPATH+'/db/count.db'
	columns=['username','count']

	def __init__(self):
		self.data=[]

	def add(self,countMap):
		if len(self.fm.select(self.table,self.columns,['username='+countMap['username']]))>0:
			return
		countVal=[]
		for col in self.columns:
			if countMap.has_key(col):
				countVal.append(countMap[col])
			else:
				countVal.append('null')
		self.fm.insert(self.table,self.columns,countVal)

	def delete(self,conditons):
		self.fm.delete(self.table,conditons)

	def select(self,username):
		countList=self.fm.select(self.table,self.columns,['username='+username])[0]
		countMap={}
		for i in range(len(self.columns)):
			countMap[self.columns[i]]=countList[i]
		return countMap

	def setCount(self,count,username):
		print count
		self.fm.update(self.table,['count'],[count],['username='+username])