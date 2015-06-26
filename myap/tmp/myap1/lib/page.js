var maxpage;
var low;
var high;
var nowpage;
var dealfunc;
var newPage=function (max,sendfunc,per) {
	// body...
	maxpage=max;
	if(per==null)
		per=5;
	if(max<per)
		per=max;
	var html='<li class="disabled"><a href="javascript:void(0);" onclick="toPage(this)">上一页</a></li>'+
			'<li class="active"><a href="javascript:void(0);" onclick="toPage(this)">1</a></li>';
	for(var i=2;i<=per;i++){
        html+='<li><a href="javascript:void(0);" onclick="toPage(this)">'+i+'</a></li>';
	}
	html+='<li><a href="javascript:void(0);" onclick="toPage(this)">下一页</a></li>';
	nowpage=1;
	low=1;
	high=per;
	dealfunc=sendfunc;
	return html;
	// $(this).append(html);
}

var toPage=function (dom){
	if($($(dom).parent()).attr("class")=="disabled"){
		console.log("disabled");
		return;
	}
	var toP=$(dom).html();
	var act=$(dom).parent().parent().find(".active");
	$(dom).parent().parent().children().each(function () {
			// body...
		$(this).removeClass("disabled");
		$(this).removeClass("active");
	});
	if(toP=="上一页"){
		if(low==nowpage){
			low--;
			high--;
			nowpage--;
			resetpage(dom);
			$($(dom).parent().parent().children().get(1)).addClass("active");
		}else{
			console.log("tttttt");
			$(act.prev()).addClass("active");
			act.removeClass("active");
			nowpage--;
		}
	}else if(toP=="下一页"){
		if(high==nowpage){
			low++;
			high++;
			nowpage++;
			resetpage(dom);
			$($(dom).parent().parent().children().get(high-low+1)).addClass("active");
		}else{
			$(act.next()).addClass("active");
			act.removeClass("active");
			nowpage++;
		}
	}else{

		$($(dom).parent()).addClass("active");
		nowpage=toP;
	}
	if (nowpage==1) $($(dom).parent().parent().find("li:first")).addClass("disabled");
	if (nowpage==maxpage) $($(dom).parent().parent().find("li:last")).addClass("disabled");
	dealfunc();
	// console.log(toP);
}

var resetpage=function (dom) {
	// body...
	for(var i=low;i<=high;i++){
		$($(dom).parent().parent().children().get(i-low+1)).children().html(i);
	}
}