var usermanager=new UserManager();
var cm=new ConfManager();
$(function(){
	$('#menuToggle, .menu-close').on('click', function(){
		$('#menuToggle').toggleClass('active');
		if(document.body.clientWidth>600)
			$('#theMenu').toggleClass('menu-open');
		else{
			$(".menu-wrap").toggleClass("open");
		}
	});

	$('.menu-wrap a').on('click', function(){
		$('#menuToggle').toggleClass('active');
		$('.menu-wrap .active').removeClass('active');
		$(this).toggleClass('active');
		if(document.body.clientWidth<=600)
			$(".menu-wrap").toggleClass("open");
		else
			$('#theMenu').toggleClass('menu-open');
	});
});

function ConfManager() {

	var ssid;
	var channel;
	var interface;

	this.basicres=function(){
		$("#basicset input[name=ssid]").val(ssid);
		$("#basicset input[name=channel]").val(channel);
		$("#basicset input[name=interface]").val(interface);
	}

	this.basiclist=function() {
		var url="/admin/basiclist"
		$.getJSON(url,({type:1}),function (data) {
			$("#basicset input[name=ssid]").val(data.ssid);
			$("#basicset input[name=channel]").val(data.channel);
			$("#basicset input[name=interface]").val(data.interface);
			ssid=data.ssid;
			channel=data.channel;
			interface=data.interface;
			// console.log(ssid);
		})
	}

	this.basicsub=function (dom) {
		var ssid=$("#basicset input[name=ssid]").val();
		var channel=$("#basicset input[name=channel]").val();
		var interface=$("#basicset input[name=interface]").val();
		var data=({ssid:ssid,channel:channel,interface:interface});
		var url="/admin/basicset/";

		$.post(url,data,function(data){

		});
	}

	this.securesub=function (dom) {
		var wpa=$("#secureset select[name=wpa]").val();
		var password=$("#secureset input[name=password]").val();
		var confirm=$("#secureset input[name=confirm]").val();
		var data=({wpa:wpa,password:password,confirm:confirm})
		var url="/admin/secureset/";

		$.post(url,data,function(data){
			
		});
	}
}


$(document).ready(function(){
	usermanager.getUserList();
	usermanager.getOnlineList();
	cm.basiclist();
});

function UserManager() {
	this.getUserList=function(status){
		var url='/admin/user';
		$.getJSON(url,function (data) {
			// body...
			// console.log(data);
			for(var i in data.data){
				console.log(user);
				if(data.data[i].rank==2){
					var html=String.format('<tr><td class="text-center"><span>{0}</span><strong>'
					+'<a href="javascript:void(0)" onclick="usermanager.changeRank(this,-1)">加入黑名单</a></strong></td></tr>',data.data[i].username);
					$("#userlist").append(html);
				}else if(data.data[i].rank==-1){
					var html=String.format('<tr><td class="text-center"><span>{0}</span><strong>'
						+'<a href="javascript:void(0)" onclick="usermanager.changeRank(this,2)">还原用户</a></strong></td></tr>',data.data[i].username);
					$("#banlist").append(html);
				}
			}
                            
		})
	};

	this.getOnlineList=function() {
		var url='/admin/online';
		$.getJSON(url,function (data) {
			var list=data.data
			for(var i in list){
				var speed='不限';
				if(list[i].speed!='null'){
					speed=list[i].speed;
				}
				var html=String.format('<tr><td class="text-left">{0}</td><td class="text-left ip">{1}</td>'
                    +'<td class="text-left">{2}</td>'
                    +'<td class="text-left"><span>{3}</span>'
                    +'<a href="javascript:void(0)" onclick="usermanager.setspeed(this)">'
                    +'<span class="glyphicon glyphicon-edit"></span></a></td>'
                    +'<td class="text-left"><a href="javascript:void(0)" onclick="usermanager.kickUser(this)">删除</a></td></tr>'
                    ,list[i].username,list[i].ip,list[i].mac,speed);
				$("#online").append(html)
			}
		})
	}

	this.changeRank=function(dom,type) {
		var username=$($(dom).parent().parent().parent().find('span')).html();
		console.log(username);
		var url='/admin/user/updaterank';
		$.getJSON(url,({username:username,rank:type}),function (data){
			console.log(data);
			if(data.status>0){
				// console.log($(dom).parentsUntil('tr'));
				var id=$(dom).parents('table').attr('id');
				$(dom).parents('tr').remove();
				console.log(id);
				if(id=='banlist'){
					var html=String.format('<tr><td class="text-center"><span>{0}</span><strong>'
					+'<a href="javascript:void(0)" onclick="usermanager.changeRank(this,-1)">加入黑名单</a></strong></td></tr>',username);
					$("#userlist").append(html);
				}else if(id=='userlist'){
					var html=String.format('<tr><td class="text-center"><span>{0}</span><strong>'
					+'<a href="javascript:void(0)" onclick="usermanager.changeRank(this,-1)">还原用户</a></strong></td></tr>',username);
					$("#banlist").append(html);
				}
			}
		});
	}

	this.kickUser=function(dom){
		var username=$($(dom).parents('tr').find('td').get(0)).html();
		var ip=$($(dom).parents('tr').find('td').get(1)).html();
		var index=username.indexOf('(');
		if(index>0)
			username=username.substr(0,index);
		var url='/admin/user/kick';
		$.getJSON(url,({username:username,ip:ip}),function(data){
			console.log(data);
			if(data.status>0){
				$(dom).parents('tr').remove();
			}
		});
	}

	var prespeed;

	this.setspeed=function(dom){
		var speeddom=$(dom).parents('td').find('span').get(0);
		var speed=$(speeddom).html();
		var input=String.format("<input value='{0}' style='width:40px'>",speed);
		$($(speeddom).parent()).prepend(input);
		$(speeddom).remove();
		$(dom).children().attr("class","glyphicon glyphicon-ok");
		$(dom).attr("onclick","usermanager.submitspeed(this)");
		prespeed=speed;
	}

	this.submitspeed=function(dom){
		var inputdom=$(dom).parents('td').find('input').get(0);
		var speed=$(inputdom).val();

		var username=$($(dom).parents('tr').find('td').get(0)).html();
		var ip=$($(dom).parents('tr').find('td').get(1)).html();
		var index=username.indexOf('(');
		if(index>0)
			username=username.substr(0,index);
		var url="/admin/user/speed";

		$.getJSON(url,({username:username,ip:ip,speed:speed}),function(data){
			if(data.status>0){
				if(speed=='')
					speed='不限';
				else if(isNaN(speed))
					speed=prespeed;
				var span=String.format("<span>{0}</span>",speed);
				$($(inputdom).parent()).prepend(span);
				$(inputdom).remove();
				$(dom).children().attr("class","glyphicon glyphicon-edit");
				$(dom).attr("onclick","usermanager.setspeed(this)");
			}
		});
	}
}	

