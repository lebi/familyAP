from django.conf.urls import patterns, include, url

from server import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from dwebsocket.decorators import accept_websocket

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/$', 'jobs.views.index', name='home'),
    url(r'^guest/$','jobs.views.guest',name='guest'),
    url(r'^$','jobs.views.login',name='login'),

    url(r'^/$','jobs.views.login',name='login'),

    url(r'^admin/file/$','jobs.views.fileView',name='fileView'),

    url(r'^guest/file/$','jobs.views.guestFileView',name='fileView'),

    url(r'^error/$','jobs.views.errorView',name='ajax'),

    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root':'{0}/css'.format(settings.PATH)}),

    url(r'^lib/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root':'{0}/lib'.format(settings.PATH)}),

    url(r'^img/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root':'{0}/img'.format(settings.PATH)}),

    url(r'^style/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root':'{0}/style'.format(settings.PATH)}),

    url(r'^js/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root':'{0}/js'.format(settings.PATH)}),

    url(r'^font/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root':'{0}/font'.format(settings.PATH)}),

    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':'{0}/fonts'.format(settings.PATH)}),

    url(r'^auth/$','jobs.views.auth',name='auth'), #two param :username,password

    url(r'^admin/user/$','jobs.views.userList',name='userlist'),    

    url(r'^admin/user/adduser$','jobs.views.addUser',name='adduser'),

    url(r'^admin/user/updateuser$','jobs.views.modifyUser',name='updateuser'),

    url(r'^admin/user/settinguser$','jobs.views.settingUser',name='settinguser'),

    url(r'^admin/user/settingdetail$','jobs.views.settingDetail',name='settingdetail'),

    url(r'^admin/user/kick$','jobs.views.kickUser',name='kickuser'),

    url(r'^admin/user/logout$','jobs.views.logout',name='kickuser'),

    url(r'^guest/user/logout$','jobs.views.logout',name='kickuser'),

    url(r'^admin/user/speed$','jobs.views.updateSpeed',name='kickuser'),

    url(r'^admin/user/updaterank/$','jobs.views.updateRank',name='updaterank'),  #two params :username,rank

    url(r'^admin/online/$','jobs.views.onlineList',name='onlinelist'),

    url(r'^admin/basiclist/$','jobs.views.basicList',name='basiclist'),

    url(r'^admin/basicset/$','jobs.views.basicSet',name='basicset'),

    url(r'^admin/secureset/$','jobs.views.secureSet',name='secureset'),

    #----------------------------------------------guest---------------------------------------------------
    url(r'^guest/resttime/$','jobs.views.countRest'),

    url(r'^guest/eventdate/$','jobs.views.eventDate',name='eventdate'),

    url(r'^guest/eventlist/$','jobs.views.eventList',name='eventlist'),

    url(r'^guest/eventupdate$','jobs.views.eventUpdate',name='eventlist'),

    url(r'^guest/eventadd$','jobs.views.eventAdd',name='eventlist'),

    url(r'^guest/eventdelete$','jobs.views.eventDelete',name='eventlist'),
    #----------------------------------------------video---------------------------------------------------

    url(r'^admin/videows$','jobs.views.videoWs'),

    url(r'^guest/videows$','jobs.views.videoWs'),

    url(r'^guest/videolist$','jobs.views.wsOnline'),

    url(r'^admin/videolist$','jobs.views.wsOnline'),

    url(r'^guest/rtcview/$','jobs.views.rtcView',name='rtcView'),
    #----------------------------------------------file---------------------------------------------------
    url(r'^guest/file/private$','jobs.views.privatefileList',name='pfilelist'),

    url(r'^guest/file/share$','jobs.views.sharefileList',name='sfilelist'),

    url(r'^guest/file/download/$','jobs.views.downloadFile',name='downloadfile'),

    url(r'^guest/file/upload/$','jobs.views.uploadFile',name='uploadfile'),

    url(r'^guest/file/remove/$','jobs.views.rmFile',name='rmfile'),

    url(r'^admin/file/private$','jobs.views.privatefileList',name='pfilelist'),

    url(r'^admin/file/share$','jobs.views.sharefileList',name='sfilelist'),

    url(r'^admin/file/all$','jobs.views.AllfileList',name='allfilelist'),

    url(r'^admin/file/download/$','jobs.views.downloadFile',name='downloadfile'),

    url(r'^admin/file/upload/$','jobs.views.uploadFile',name='uploadfile'),

    url(r'^admin/file/remove/$','jobs.views.rmFile',name='rmfile'),

    #--------------------------------------------favorite-----------------------------------
    url(r'^guest/favorite/list$','jobs.views.favoriteList'),

    url(r'^guest/favorite/add$','jobs.views.favoriteAdd'),
    )
