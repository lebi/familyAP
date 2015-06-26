#!/usr/bin/python
import os
class SpeedLimit():
	def __init__(self):
		self.data=[]

	def addLimit(self,ip,speed):
		target1='echo 123456|sudo -S iptables -A FORWARD -m limit --limit '+speed+'/s -j ACCEPT -s '+ ip
		target2='echo 123456|sudo -S iptables -A FORWARD -j DROP -s' + ip
		os.system(target1)
		os.system(target2)

	def deleteLimit(self,ip,speed):
		target1='echo 123456|sudo -S iptables -D FORWARD -m limit --limit '+speed+'/s -j ACCEPT -s '+ ip
		target2='echo 123456|sudo -S iptables -D FORWARD -j DROP -s' + ip
		os.system(target1)
		os.system(target2)

	def updateLimit(self,ip,pre,speed):
		target1='echo 123456|sudo -S iptables -D FORWARD -m limit --limit '+pre+'/s -j ACCEPT -s '+ ip
		target11='echo 123456|sudo -S iptables -D FORWARD -j DROP -s' + ip
		target2='echo 123456|sudo -S iptables -A FORWARD -m limit --limit '+speed+'/s -j ACCEPT -s '+ ip
		target21='echo 123456|sudo -S iptables -A FORWARD -j DROP -s' + ip
		os.system(target1)
		os.system(target11)
		os.system(target2)
		os.system(target21)
# if __name__ == '__main__':
# 	sl=SpeedLimit()
# 	sl.deleteLimit('192.168.1.135')