#coding=utf-8
#!/usr/bin/python
from file import filemanage

class ApdDao():
	path='/etc/hostapd.conf'
	fc=filemanage.FileControl()
	def __init__(self):
		self.data=[]

	def deleteRules(self,rules):
		for rule in rules:
			self.fc.delete(self.path,rule)
		
	def addRules(self,target,rule):
		for i in len(target):
			self.fc.add(self.path,target[i]+'='+rule[i])

	def changeRules(self,target,rule):
		self.fc.update(self.path,target,rule)

	def getRules(self,targets):
		map={}
		for tag in targets:
			map[tag]=self.fc.select(self.path,tag)
		return map