#coding=utf-8
#!/usr/bin/python
import os
import linecache

class FileControl():
	def __init__(self):
		self.data=[]

	def delete(self,path,target):
		file=open(path,'r')
		new=open(path+'new','w')
		filelines=linecache.getlines(path)
		for line in filelines:
			if line.split('=')[0] != target:
				new.write(line)
		new.close()
		file.close()
		shell="echo 123456|sudo -S mv {0} {1}".format(path+'new',path)
		os.system(shell)

	def add(self,path,line):
		shell="echo 123456|sudo -S echo {0} >> {1}".format(line,path)
		os.system(shell)

	def update(self,path,target,surrenal):
		file=open(path,'r')
		new=open(path+'new','w')
		filelines=linecache.getlines(path)
		for line in filelines:
			if line.split('=')[0] != target:
				new.write(line)
		new.write('{0}={1}\n'.format(target,surrenal))
		new.close()
		file.close()
		shell="echo 123456|sudo -S mv {0} {1}".format(path+'new',path)
		os.system(shell)

	def select(self,path,target):
		linecache.updatecache(path)
		file=open(path,'r')
		filelines=linecache.getlines(path)
		# result={}
		for line in filelines:
			arr=line.split('=')
			if arr[0]==target:
				val=arr[1]
				val=val[:len(val)-1]
				print val
				return val

# if __name__ == '__main__':
# 	fc=FileControl()
	# fc.select('test','ba')
	# fc.add('test','haha=c')
	# fc.delete('test','ba')
	# fc.update('test','ba',1)
