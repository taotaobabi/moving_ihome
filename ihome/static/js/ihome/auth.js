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
		// $(".popup_con").show();
		$.get("/api/profile/auth",function(data){
			// console.log(data)
			if("4101" === data.errno){
				window.location.href="/";
			}else{
				if("1" === data.errno){
					$("#real-name").val(data.data["name"]);
					$("#real-name").attr("disabled",true);
					$("#id-card").val(data.data["idcard"]);
					$("#id-card").attr("disabled",true);
					$("input[type='submit']").hide();
			}else{
				$("#real-name").attr("disabled",false);
				$("#id-card").attr("disabled",false);
				}
			}
		
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
					showSuccessMsg();
				}else{
					$(".error-msg").text(data.errmsg);
					$(".error-msg").show();
				}

				// console.log(data);
			}
		});
	})
	
	// $("#id-card").attr("disabled",false)
})

