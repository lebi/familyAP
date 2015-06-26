#coding=utf-8
#!/usr/bin/python
from file import dbmanager

class NATDao:
	fm=dbmanager.FileManager()
	table='../db/nat.db'
	columns=['username','ip','speed']
	def __init__(self):
		self.data=[]

	def createNAT(self):
		self.fm.create(self.table,self.columns)

	def addNAT(self,user,ip,speed='null'):
		value=[user,ip,speed]
		self.fm.insert(self.table,self.columns,value)

	def deleteNAT(self,user):
		condition=['username='+user]
		self.fm.delete(self.table,condition)

	def dropNAT(self):
		self.fm.drop(self.table)

# if __name__ == '__main__':
	# natdao=NATDao()
	# natdao.createNAT()
	# natdao.addNAT('lebi','100.100.100.1')
	# natdao.dropNAT()
	# natdao.deleteNAT('lebi')