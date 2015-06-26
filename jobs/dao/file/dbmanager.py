#coding=utf-8
#!/usr/bin/python
import linecache
import shutil
import datetime,time 
import os
#from server import settings
#import sys
#sys.path.append(settings.JOBPATH)

class FileManager:
	def __init__(self):
		self.data = []

	def readALine(self,fileName,row):
		linecache.clearcache()
		columnName=linecache.getline(fileName,row);
		columnName=columnName[:len(columnName)-1]
		return columnName.split('\t')

	def checkCondition(self,rowResult,columnName,conditions):  
		conditionCol=[]
		conditionVal=[]
		for condition in conditions:
			con=condition.split('=')                        
			conditionCol.append(con[0])
			conditionVal.append(con[1])
		if len(rowResult)==1:
			return False
		for i in range(len(conditionCol)):
			conIndex=columnName.index(conditionCol[i])
			if conIndex < 0 or rowResult[conIndex] != conditionVal[i]:
				return False
		return True

	def getColIndex(self,columnName,columns):  #get the columns index of the table
		resultIndex=[0 for i in range(len(columns))]
		for i in range(len(columns)):
			resultIndex[i]=columnName.index(columns[i])
		return resultIndex

	def timeFormat(self,stamp,type):  
		timeStruct=time.localtime(stamp)
		date=str(timeStruct.tm_year)+'-'+str(timeStruct.tm_mon)+'-'+str(timeStruct.tm_mday)
		if type==1:					#type 1 means yy-MM-dd
			pass
		elif type==2:
			date+=' '+str(timeStruct.tm_hour)+':'+str(timeStruct.tm_min)+':'+str(timeStruct.tm_sec)
		return date

	def toLog(self,action,table,before,after=[]):
		if action=='insert':
			after=before
			before=[]
		logStr='log at {0}: {1} to {2} change data {3} to {4}\n'.format(self.timeFormat(time.time(),2),action,table,before,after)
		# fileName=settings.JOBPATH+'/log/log-'+self.timeFormat(time.time(),1)
		# file=open(fileName,'a+')
		# file.seek(1,2)
		# file.write(logStr)
		# file.close()

	def select(self,table,columns,conditions=[]):
		result=[]
		file=open(table,'r')
		count=len(file.readlines())

		columnName=self.readALine(table,1)
		resultIndex=self.getColIndex(columnName,columns)

		for i in range(2,count+1):
			rowResult=self.readALine(table,i)
			if self.checkCondition(rowResult,columnName,conditions):
				row=[0 for n in range(len(columns))]
				for j in range(len(resultIndex)):
					row[j]=rowResult[resultIndex[j]]
				result.append(row)
		file.close()
		return result

	def insert(self,table,columns,value,flag=0):
		file = open(table,'a+')
		columnName = self.readALine(table,1)
		insertVal = ['null' for i in range(len(columnName))]
		colIndex = self.getColIndex(columnName,columns)
		for i in range(len(colIndex)):
			insertVal[colIndex[i]] = value[i]
		writeStr=insertVal[0]
		for i in range(1,len(insertVal)):
			writeStr=str(writeStr)+str('\t')
			writeStr+=str(insertVal[i])
		writeStr+='\n'
		file.seek(1,2)
		file.write(writeStr)
		if flag==0:
			self.toLog('insert',table,insertVal)
		file.close()

	def update(self,table,columns,value,conditions=[]):
		# file = open(table,'a+')
		columnName = self.readALine(table,1)
		store=self.select(table,columnName,conditions)
		self.delete(table,conditions,1)
		colIndex=self.getColIndex(columnName,columns)
		after=[]
		for row in store:
			for i in range(len(colIndex)):
				row[colIndex[i]]=value[i]
				after.append(row)
			self.insert(table,columnName,row,1)
		self.toLog('update',table,store,after)


	def delete(self,table,conditions=[],flag=0):
		file=open(table,'r')
		new=open(table+'.new','w')
		new.write(file.readline())
		columnName = self.readALine(table,1)
		deleteRow=[]
		for line in file.readlines():
			column=line[:len(line)-1].split('\t')
			if not self.checkCondition(column,columnName,conditions):
				new.write(line)
			else:
				deleteRow.append(column)
		new.close()
		file.close()
		shutil.move(table+'.new',table)
		if flag==0:
			self.toLog('delete',table,deleteRow)

	def create(self,table,columnName):
		file=open(table,'a+')
		if len(file.readlines())>0:
			file.close()
			return	
		writeStr=columnName[0]
		for i in range(1,len(columnName)):
			writeStr+='\t'
			writeStr+=columnName[i]
		file.write(writeStr+'\n')
		file.close()
		self.toLog('create',table,columnName)

	def drop(self,table):
		file=open(table,'r')
		store=[]
		for i in range(1,len(file.readlines())+1):
			store.append(self.readALine(table,i))
		self.toLog('drop',table,store)
		os.system('rm '+table)
# if __name__ == '__main__':
# 	fm=FileManager()
# 	fm.update('user_table',['username'],['lebi'],['id=1'])
