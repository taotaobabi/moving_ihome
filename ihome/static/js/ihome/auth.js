function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}
$(document).ready(function(){
		$(".popup_con").show();
		$.get("/api/profile/auth",function(){

		})
	$("#form-auth").submit(function(e){
		e.preventDefault();
		var idcard = $("#id-card").val();
		var realname = $("#real-name").val();
		ret_data = {
			idcard:idcard,
			realname:realname
		}
		$.ajax({
			url:"/api/profile/auth",
			type:"post",
			dataType:"json",
			contentType:"application/json",
			data:JSON.stringify(ret_data),
			headers:{
				"X-XSRFTOKEN":getCookie("_xsrf")
			},
			success:function(data){
				if("0"=== data.errno){

				}
			}
		});
	})
	
	// $("#id-card").attr("disabled",false)
})

