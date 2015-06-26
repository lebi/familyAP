function favoriteAdd(dom){
	$("#f-modal input").val('');
	$("#f-modal").modal('toggle');
	favoriteDom=dom;
}
var favoriteDom;
$(function () {
	$.getJSON('favorite/list',function(favoriteList) {
		favoriteList=favoriteList.data;
		var temp=_.template($("#favorite-template").html())
		if(favoriteList.length>8){
			favoriteList=favoriteList.slice(0,8);
		}
		$("#pages").append(temp({favoriteList:favoriteList}));
	})
})

function jumpTo(dom) {
	window.open('http://'+$(dom).html(),'_blank');
}

function favoriteSub (){
	var address=$("#f-modal input").val();
	if(address=='')
		return;
	$.post('favorite/add',{address:address},function(result) {
		if(result.status>0){
			$(favoriteDom).attr('onclick','jumpTo(this)');
			$(favoriteDom).html(address);
			$("#f-modal").modal('toggle');
		}
	})
}