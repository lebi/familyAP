#coding=utf-8
#!/usr/bin/python
from file import dbmanager
from server import settings

class EventDao():

	fm=dbmanager.FileManager()
	table=settings.JOBPATH+'/db/event.db'
	# table='../db/event.db'
	columns=['id','username','date','datetime','title','content']

	def __init__(self):
		self.data=[]

	def addEvent(self,event):
		eventCol=[]
		maxid=0
		print self.fm.select(self.table,['id'])
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

	def updateEvent(self,columns,value,conditions=[]):
		self.fm.update(self.table,columns,value,conditions)

	def createtable(self):
		self.fm.create(self.table,self.columns)

	def droptable(self):
		self.fm.drop(self.table)

# if __name__ == '__main__':
	# dao=EventDao()
	# event={'username':'lebi','date':'2015-5-23','datetime':'07:00','title':'empty','content':'getup'}
	# dao.createtable()
	# dao.addEvent(event)
	# dao.deleteEvent(2)
	# print dao.selectEvent()