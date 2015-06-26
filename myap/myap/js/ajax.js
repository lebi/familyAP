$(document).ready(function($) {
	$.ajaxSetup({　　　　
		error: function (data) {
			// console.log(data.responseText);
			if(data.responseText=='not login'){
				window.location.href="/";
			}
		},
// 　　　　//请求失败遇到异常触发
// 　　　　error: function (xhr, status, e) { show.append('error invoke! status:' + status+'<br/>'); },
// 　　　　//完成请求后触发。即在success或error触发后触发
// 　　　　complete: function (xhr, status) { show.append('complete invoke! status:' + status+'<br/>'); },
// 　　　　//发送请求前触发
// 　　　　beforeSend: function (xhr) {
// 　　　　//可以设置自定义标头
// 　　　　xhr.setRequestHeader('Content-Type', 'application/xml;charset=utf-8');
// 　　　　show.append('beforeSend invoke!' +'<br/>');
// 　　　　},
　　});	
});