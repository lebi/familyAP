#coding=utf-8
import json
import re
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import onlinedao
from dao import userdao

class AuthMiddleware(object):
	onlinedao=onlinedao.onlinedao()

	def __init__(self):
		self.data=[]

	def process_request(self,request):
		ip=request.META.get('REMOTE_ADDR')
		if re.match(r'^/admin/*',request.path) or re.match(r'^/guest/*',request.path):
			if request.session.has_key(ip) and \
				len(self.onlinedao.selectuser(['username='+request.session[ip],'ip='+ip]))>0 :
				if re.match(r'^/admin/*',request.path):
					dao=userdao.userdao()
					rank=dao.selectuser(['username='+request.session[ip]])[0][3]
					if int(rank)==2 or int(rank)==-1:
						return HttpResponseRedirect('/guest')
				pass
			else:
				if re.match(r'^/admin/$',request.path) or re.match(r'^/guest/$',request.path) or re.match(r'^/.*/file/$',request.path):
					print "redirect"
					return HttpResponseRedirect('/')
				else:
					print "forbidden"
					return HttpResponseForbidden('not login');
		else:
			pass