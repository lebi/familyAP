#coding=utf-8
#!/usr/bin/python
# import os
# sys.path.append(os.path.abspath('..'))
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import favoritedao


class FavoriteMod(object):
	dao=favoritedao.FavoriteDao()

	def __init__(self):
		self.data=[]

	def getFavoriteList(self,request):
		ip=request.META['REMOTE_ADDR']
		username=request.session[ip]
		return self.dao.selectFavorite(username)

	def addFavorite(self,request):
		ip=request.META['REMOTE_ADDR']
		username=request.session[ip]
		address=request.POST.get('address')
		self.dao.addFavorite({'username':username,'address':address})