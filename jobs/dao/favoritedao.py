#coding=utf-8
#!/usr/bin/python
from file import dbmanager
from server import settings
import sys
sys.path.append(settings.JOBPATH)

class FavoriteDao():

	fm=dbmanager.FileManager()
	table=settings.JOBPATH+'/db/favorite.db'
	columns=['username','address']

	def __init__(self):
		self.data=[]

	def selectFavorite(self,username):
		faList=self.fm.select(self.table,self.columns,['username='+username])
		retList=[]
		for favorite in faList:
			faMap={}
			for i in range(len(favorite)):
				faMap[self.columns[i]]=favorite[i]
			retList.append(faMap)
		return retList

	def addFavorite(self,favorite):
		value=[]
		for col in self.columns:
			if favorite.has_key(col):
				value.append(favorite[col])
			else:
				value.append('null')
		self.fm.insert(self.table,self.columns,value)