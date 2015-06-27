# Create your views here.
#coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.servers.basehttp import FileWrapper
from django.views.decorators.csrf import csrf_exempt
from django import template
from server import settings
from django import forms
ISOTIMEFORMAT='%Y-%m-%d %H:%M:%S'
import json
import os
import urllib
import datetime,time
import sys
import traceback
from model import usermod
from model import onlinemod
from model import logmod
from model import confmod
from model import eventmod
from model import filemod
from model import favoritemod
from dwebsocket.decorators import accept_websocket
from dwebsocket.decorators import require_websocket

clients = []
wsipList=[]

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()

def index(request):
	return render_to_response('admin/admin.html')

def guest(request):
	return render_to_response('guest/guest.html')

def rtcView(request):
    return render_to_response('rtc/webrtc1.html')

def fileView(request):
    return render_to_response('file/file.html')

def guestFileView(request):
    return render_to_response('file/guestfile.html')

def login(request):
	mod=logmod.LogMod()
	check=mod.checkLogin(request)
	topage='login.html'
	if check==1:
		print check
		topage='admin/admin.html'
		return HttpResponseRedirect('/admin')
	elif check!=0:
		topage='guest/guest,html'
		return HttpResponseRedirect('/guest')
	# return render_to_response('index.html',{},context_instance=RequestContext(request))
	# fp=open("{0}/login.html".format(settings.PATH))
	result={'status':1}
	return render_to_response(topage,result)

def ajax(request):
	name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
	return HttpResponse(json.dumps(name_dict), content_type='application/json')

def userList(request):
	mod=usermod.UserMod()
	userlist={'data':mod.getUserList(),'status':1}
	return HttpResponse(json.dumps(userlist),content_type='application/json')

def onlineList(request):
	mod=onlinemod.OnlineMod()
	userlist={'data':mod.getOnlineList(request),'status':1}
	return HttpResponse(json.dumps(userlist),content_type='application/json')

def updateRank(request):
	mod=usermod.UserMod()
	mod.updateRank(request)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def auth(request):
	mod=logmod.LogMod()
	result=mod.login(request)
	topage='login.html'
	if result.has_key('rank'):
		if int(result['rank'])==1:
			topage='admin/admin.html'
			return HttpResponseRedirect('/admin')
		else:
			topage='guest/guest.html'
			return HttpResponseRedirect('/guest')
	result={'status':-1}
	return render_to_response(topage,result)


def addUser(request):
	mod=usermod.UserMod()
	username=str(request.POST.get('username'))
	userpwd=str(request.POST.get('password'))
	value=['3',username,userpwd,'2']
	mod.addUser(value)
	mod.addUsertoadmin(username)
	path = settings.FILEPATH+"/private/"+username 
	if not os.path.exists(path):
		os.makedirs(path)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def modifyUser(request):
	mod=usermod.UserMod()
	username=str(request.POST.get('username'))
	conditions=['username='+username]
	newpwd=str(request.POST.get('password'))
	value=[username,newpwd]
	mod.updateUser(value,conditions)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def settingUser(request):
	mod=usermod.UserMod()
	sfileauth=str(request.POST.get('sfileauth'))
	wdaystarttime=str(request.POST.get('wdaystarttime'))
	wdaystoptime=str(request.POST.get('wdaystoptime'))
	wendstarttime=str(request.POST.get('wendstarttime'))
	wendstoptime=str(request.POST.get('wendstoptime'))
	limit=str(request.POST.get('limit'))
	username=str(request.POST.get('username'))
	conditions=['username='+username]
	value=[sfileauth,wdaystarttime,wdaystoptime,wendstarttime,wendstoptime,limit]
	mod.manageUser(value,conditions)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def settingDetail(request):
	mod=usermod.UserMod()
	username=str(request.GET.get('username'))
	detail=mod.selectSettingDetail(username)
	result={'data':detail,'status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def kickUser(request):
	mod=logmod.LogMod()
	mod.logout(request)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')
	
def updateSpeed(request):
	mod=onlinemod.OnlineMod()
	mod.updateSpeed(request)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def basicList(request):
	mod=confmod.ConfMod()
	result=mod.selectApd(request)
	return HttpResponse(json.dumps(result),content_type='application/json')

def basicSet(request):
	mod=confmod.ConfMod()
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def secureSet(request):
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')
#=======================================================event======================================
def eventDate(request):
	mod=eventmod.EventMod()
	datelist=mod.getActiveDate(request)
	result={'data':datelist,'status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def eventList(request):
	mod=eventmod.EventMod()
	eventlist=mod.getEventList(request)
	result={'data':eventlist,'status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def eventAdd(request):
	mod=eventmod.EventMod()
	mod.addEvent(request)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def eventUpdate(request):
	mod=eventmod.EventMod()
	mod.updateEvent(request)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def eventDelete(request):
	mod=eventmod.EventMod()
	mod.deleteEvent(request)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

@accept_websocket
def videoWs(request):
	if request.is_websocket:
		try:
			clients.append(request.websocket)
			wsipList.append(request.META['REMOTE_ADDR'])
			for message in request.websocket:
				wsmessage=json.loads(message)
				print wsmessage
				wsmessage['ip']=request.META['REMOTE_ADDR']
				if wsmessage['target']=='0.0.0.0':
					mod=onlinemod.OnlineMod()
					user=mod.getOnlineByIp(request.META['REMOTE_ADDR'])
					username=user['username']
					wsmessage['username']=username
					mac=user['mac']
					wsmessage['mac']=mac
					for client in clients:
						if client!=request.websocket:
							print json.dumps(wsmessage)
							client.send(json.dumps(wsmessage))
							# client.send(wsmessage)
				else:
					i=wsipList.index(wsmessage['target'])
					clients[i].send(json.dumps(wsmessage))
		finally:
			# wsmessage['source']=request.META['REMOTE_ADDR']
			wsmessage={'action':'remove'}
			wsmessage['ip']=request.META['REMOTE_ADDR']
			i=clients.index(request.websocket)
			wsipList.remove(wsipList[i])
			clients.remove(request.websocket)
			for client in clients:
				client.send(json.dumps(wsmessage))

def wsOnline(request):
	mod=onlinemod.OnlineMod()
	userList=[]
	for ip in wsipList:
		userList.append(mod.getOnlineByIp(ip))
	result={'data':userList,'status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

#=========================================FILE=====================================
def privatefileList(request):
	mod=filemod.FileMod()
	ip=request.META['REMOTE_ADDR']
	username=request.session[ip]
	result=mod.getFileList(['username='+username])
	result={"data":result,"status":1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def sharefileList(request):
	mod=filemod.FileMod()
	result=mod.getFileList(['priority=share'])
	result={"data":result,"status":1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def AllfileList(request):
	mod=filemod.FileMod()
	result={"data":mod.getFileList(),"status":1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def downloadFile(request):
	priority=str(request.GET.get('priority'))
	if priority=="private":
		username=request.GET.get('username')
		path = settings.FILEPATH+"/private/"+username+"/"
	else:
		path = settings.FILEPATH+"/share/"
	filename=str(request.GET.get('filename'))
	filename=urllib.unquote(filename)
	tmpname=filename
	filename = path+filename
	wrapper = FileWrapper(file(filename))  
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=%s' %tmpname
	response['Content-Length'] = os.path.getsize(filename)
	return response  
 

def handle_uploaded_file(request):
	f=request.FILES['file']
	filename=""
	try:
		ip=request.META['REMOTE_ADDR']
		username=request.session[ip]
		priority=str(request.POST.get('priority'))
		print priority
		if priority=="private":
			path = settings.FILEPATH+"/private/"+username+"/"
		else:
			path = settings.FILEPATH+"/share/"
		if not os.path.exists(path):
			os.makedirs(path)
		print f.name
		filename=f.name.encode('utf-8')
		filename = path + filename
		destination = open(filename, 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
			destination.close()
		mod=filemod.FileMod()
		value=['5' , username , 'null' , f.name.encode('utf-8') , priority ,time.strftime( ISOTIMEFORMAT, time.localtime(time.time()) )]
		mod.insertFile(value)

	except Exception, e:
		traceback.print_exc(file=sys.stdout)
	return filename

def uploadFile(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		handle_uploaded_file(request)
		# result={"data":"success","status":1}
		# return HttpResponseRedirect('..')
		return HttpResponse("<script>alert('success!');window.location.href='..'</script>")
  	else:
		form = UploadFileForm()
		result={"data":"fail","status":-1}
		return HttpResponse(json.dumps(result),content_type='application/json')

def rmFile(request):
	username=str(request.GET.get('username'))
	# ip=request.META['REMOTE_ADDR']
	priority=str(request.GET.get('priority'))
	if priority=='private':
		filepath=settings.FILEPATH+"/private/"+username+"/"
	elif priority=='share':
		filepath=settings.FILEPATH+"/share/"
	filename=str(request.GET.get('filename'))
	filename=urllib.unquote(filename)
	conditions=['filename='+filename,'username='+username]
	mod=filemod.FileMod()
	mod.deleteFile(conditions)
	filename=filepath + filename
	if os.path.exists(filename):
		os.remove(filename)
		result={"data":"success","status":1}
		return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		result={"data":"fail","status":-1}
		return HttpResponse(json.dumps(result),content_type='application/json')

#====================================FAVORITE====================================
def favoriteList(request):
	mod=favoritemod.FavoriteMod()
	fList=mod.getFavoriteList(request)
	result={'data':fList,'status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')

def favoriteAdd(request):
	mod=favoritemod.FavoriteMod()
	mod.addFavorite(request)
	result={'data':'success','status':1}
	return HttpResponse(json.dumps(result),content_type='application/json')
