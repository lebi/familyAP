#coding=utf-8
#!/usr/bin/python
from file import dbmanager
from server import settings

class EventDao():

	fm=dbmanager.FileManager()
	table=settings.JOBPATH+'/db/event.db'
	# table='../db/event.db'
	columns=['id','username','date','datetime','content']

	def __init__(self):
		self.data=[]

	def addEvent(self,event):
		eventCol=[]
		maxid=0
		for id in self.fm.select(self.table,['id']):
			if maxid < int(id[0]):
				maxid=int(id[0])
		maxid+=1
		eventCol.append(maxid)
		for colName in self.columns[1:]:
			eventCol.append(event[colName])
		self.fm.insert(self.table,self.columns,eventCol)

	def deleteEvent(self,id):
		self.fm.delete(self.table,['id='+str(id)])

	def selectEvent(self,conditions=[],columns=columns):
		eventlist=self.fm.select(self.table,columns,conditions)
		returnlist=[]
		for event in eventlist:
			eventmap={}
			for i in range(len(event)):
				eventmap[columns[i]]=event[i]
			returnlist.append(eventmap)
		return returnlist

	def updateEvent(self,eventMap,conditions=[]):
		updateCol=self.columns
		valueCol=[]
		for col in self.columns:
			if eventMap.has_key(col):
				valueCol.append(eventMap[col])
			else:
				updateCol.remove(col)
		self.fm.update(self.table,updateCol,valueCol,conditions)

	def createtable(self):
		self.fm.create(self.table,self.columns)

	def droptable(self):
		self.fm.drop(self.table)
