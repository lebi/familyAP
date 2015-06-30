#coding=utf-8
#!/usr/bin/python
from server import settings
import sys
sys.path.append(settings.JOBPATH)
import os

def checkOnline():
	conf='/etc/myap.conf'
	file = open(conf)
	line=file.readline()
	print settings.JOBPATH
	while line:
		line=file.readline()
		if line.find('root') >= 0:
			break
	if line:
		path=line.split('=')[1]
		if path.find('\n')>=0:
			path=path[:len(path)-1]
			path='{0}/shell/check.sh'.format(path)
			os.system(path)

def resetCount():
	pass


# class CountDao():
# 	table=''
# 	columns=['username','count',]

# 	def __init__(self):
# 		self.data=[]
# 		conf='/etc/myap.conf'
# 		file = open(conf)
# 		line=file.readline()
# 		while line:
# 			line=file.readline()
# 			if line.find('root') >= 0:
# 				break
# 		if line:
# 			path=line.split('=')[1]
# 			if path.find('\n')>=0:
# 				path=path[:len(path)-1]
# 				self.table='{0}/jobs/db/count.db'.format(path)
# 				print 'dao table:'+self.table