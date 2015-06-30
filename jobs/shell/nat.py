#!/usr/bin/python
from server import settings
import os
import sys
sys.path.append(settings.JOBPATH)

class NAT:
	def __init__(self):
		self.data = []

	def allowUser(self,ip):
		target='echo 123456 | sudo -S iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE -s '+ip+' 2>>errorlog'
		os.system(target)

	def banUser(self,ip):
		target='echo 123456 | sudo -S iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE -s '+ip+' 2>>errorlog'
		os.system(target)

	def webBan(self,ip,web):
		target='echo 123456 | sudo -S iptables -t nat -A PREROUTING -p tcp --dport 80 -d '+web+ \
		' -j DNAT -s '+ip+' --to 192.168.10.1:80 2>>errorlog'
		os.system(target)

	def webAllow(self,ip,web):
		target='echo 123456 | sudo -S iptables -t nat -D PREROUTING -p tcp --dport 80 -d '+web+ \
		' -j DNAT -s '+ip+' --to 192.168.10.1:80 2>>errorlog'
		os.system(target)
#if __name__ == '__main__':
	# nat=NAT()
	# iptables.allowUser('192.168.10.2')
	# nat.banUser('192.168.10.2')
	# natdao=natdao.NATDao()
	# natdao.createNAT()
