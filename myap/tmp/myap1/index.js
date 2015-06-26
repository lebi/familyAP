$(function(){
	$('#menuToggle, .menu-close').on('click', function(){
		$('#menuToggle').toggleClass('active');
		if(document.body.clientWidth>600)
			$('#theMenu').toggleClass('menu-open');
		else{
			$(".menu-wrap").toggleClass("open");
		}
	});
});