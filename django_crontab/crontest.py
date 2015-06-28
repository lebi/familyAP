#coding=utf-8
#!/usr/bin/python
from server import settings
import sys
sys.path.append(settings.JOBPATH)
import os

def testSchedule():
	conf='/etc/myap.conf'
	file = open(conf)
	line=file.readline()
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