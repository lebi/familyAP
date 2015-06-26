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

class AuthMiddleware(object):
	onlinedao=onlinedao.onlinedao()

	def __init__(self):
		self.data=[]

	def process_request(self,request):
		ip=request.META.get('REMOTE_ADDR')
		# print request.session
		if re.match(r'^/admin/*',request.path) or re.match(r'^/guest/*',request.path):
			print request.session.has_key(ip)
			if request.session.has_key(ip) and \
				len(self.onlinedao.selectuser(['username='+request.session[ip],'ip='+ip]))>0 :
				print "permission"
				pass
			else:
				if re.match(r'^/admin/$',request.path) or re.match(r'^/guest/$',request.path):
					print "redirect"
					return HttpResponseRedirect('/')
				else:
					# return HttpResponse(json.dumps(result),content_type='application/json')
					print "forbidden"
					return HttpResponseForbidden('not login');
		else:
			pass