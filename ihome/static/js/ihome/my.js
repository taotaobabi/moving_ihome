function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
	$.get("/api/profile",function(data){
		if("0" === data.errno){
			$("#user-name").text(data.data.name);
			$("#user-mobile").text(data.data.mobile);
		}
		else{
			window.location.href = "/";
		}
	})
})