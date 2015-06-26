function login () {
	// body...
	var username=$("input[name=username]").val();
	var password=$("input[name=password]").val();
	data=({username:username,password:password});
	$.getJSON("auth",data,function (data) {
		// body...
		console.log(data);
	})
}