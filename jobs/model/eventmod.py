#coding=utf-8
#!/usr/bin/python
from server import settings
import sys
sys.path.append(settings.JOBPATH)
from dao import eventdao

class EventMod(object):
	dao=eventdao.EventDao()

	def __init__(self):
		self.data=[]

	def getActiveDate(self,request):
		ip=request.META.get('REMOTE_ADDR')
		username=request.session[ip]
		datelist=self.dao.selectEvent(['username='+username],['date'])
		print datelist
		return datelist

	def getEventList(self,request):
		ip=request.META.get('REMOTE_ADDR')
		username=request.session[ip]
		date=request.GET.get('date')
		eventlist=self.dao.selectEvent(['username='+username,'date='+date])
		print eventlist
		return eventlist

	def addEvent(self,request):
		ip=request.META.get('REMOTE_ADDR')
		username=request.session[ip]
		date=str(request.POST.get('date'))
		time=str(request.POST.get('time'))
		content=str(request.POST.get('content'))
		event={'username':username,'date':date,'datetime':time,'content':content}
		print event
		self.dao.addEvent(event)

	def updateEvent(self,request):
		ip=request.META.get('REMOTE_ADDR')
		username=request.session[ip]
		date=str(request.POST.get('date'))
		time=str(request.POST.get('time'))
		eventid=str(request.POST.get('eventId'))
		content=str(request.POST.get('content'))
		event={'id':eventid,'username':username,'date':date,'datetime':time,'content':content}
		print event
		self.dao.updateEvent(event,['id='+eventid])

	def deleteEvent(self,request):
		eventid=request.GET.get('eventId')
		self.dao.deleteEvent(eventid)