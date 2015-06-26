$(function () {
	ajaxAllUser();
})

function settingClear(dom){
	$(dom).parent().find('input').val('');
}

function ajaxAllUser() {
	$.getJSON('user',function(userList) {
		if(userList.status>0){
			var html="";
			for(var i in userList.data){
				html+="<option>"+userList.data[i].username+"</option>";
			}
			$('#dg .morph-content select[name=username]').append(html);
			ajaxSettingDetail();
		}
	})
}

function settingAddUser(dom) {
	var form = $(dom).parent().parent();
	var username = $(form).find("input[name=username]").val();
	var password=$(form).find("input[name=password]").val();
	var confirm=$(form).find("input[name=confirm]").val();
	if(username==""||password==""||confirm==""||password!=confirm){
		alert("illegal");
		return;
	}
	$.post("user/adduser",{username:username,password:password},function (result) {
		if(result.status>0){
			$("#account .active").removeClass('open');
			$("#account .active").removeClass('active');
		}
	})
}

function settingModifyUser(dom) {
	var form = $(dom).parent().parent();
	var username = $(form).find("select[name=username]").val();
	var password=$(form).find("input[name=password]").val();
	console.log(username);
	var confirm=$(form).find("input[name=confirm]").val();
	if(username==""||password==""||confirm==""||password!=confirm){
		alert("illegal");
		return;
	}
	$.post("user/updateuser",{username:username,password:password},function (result) {
		if(result.status>0){
			$("#account .active").removeClass('open');
			$("#account .active").removeClass('active');
		}
	})
}

function ajaxSettingDetail(){
	var username=$('.morph-button-modal-3 select[name=username]').val();
	var url='user/settingdetail';
	$('.morph-button-modal-3 input').val('');
	$.getJSON(url,{username:username},function(detail){
		if(detail.status>0){
			var user=detail.data;
			var limit=user.limit;
			$('.morph-button-modal-3 input[name=wendstoptime]').val(user.wendstoptime);
			$('.morph-button-modal-3 input[name=wendstarttime]').val(user.wendstarttime);
			$('.morph-button-modal-3 input[name=wdaystoptime]').val(user.wdaystoptime);
			$('.morph-button-modal-3 input[name=wdaystarttime]').val(user.wdaystarttime);
			$('.morph-button-modal-3 input[name=wendstoptime]').val(user.wendstoptime);
			if(user.sfileauth!="")
				$('.morph-button-modal-3 select[name=sfileauth]').val(user.sfileauth);
			if(user.limit!="")
				$('.morph-button-modal-3 textarea').val(user.limit);
			else
				$('.morph-button-modal-3 textarea').val("以分号分隔");
		}
	});
}

function settingUserDetail(dom) {	
	var username=$('.morph-button-modal-3 select[name=username]').val();		
	var wendstoptime=$('.morph-button-modal-3 input[name=wendstoptime]').val();
	var wendstarttime=$('.morph-button-modal-3 input[name=wendstarttime]').val();
	var wdaystoptime=$('.morph-button-modal-3 input[name=wdaystoptime]').val();
	var wdaystarttime=$('.morph-button-modal-3 input[name=wdaystarttime]').val();
	var wendstoptime=$('.morph-button-modal-3 input[name=wendstoptime]').val();
	var sfileauth=$('.morph-button-modal-3 select[name=sfileauth]').val();
	var limit=$('.morph-button-modal-3 textarea').val();
	if(limit=="以分号分隔")
		limit="";
	var url='user/settinguser';
	$.post(url,{username:username,wendstoptime:wendstoptime,wendstarttime:wendstarttime,wdaystarttime:wdaystarttime
		,wdaystoptime:wdaystoptime,sfileauth:sfileauth,limit:limit},function(result){
			if(result.status>0){
				$("#account .active").removeClass('open');
				$("#account .active").removeClass('active');
			}
		})
	// body...
}

function checkTimeFormat(dom){
	var value=$(dom).val();
	console.log(value);
	var re=/^[0-3][0-9]?:[0-6][0-9]$/;
	if(!re.exec(value))
		$(dom).val('');
}