function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
		$("#form-name").submit(function(e){
				e.preventDefault();
				var name = $("#user-name").val();
				ret_data = {
					name:name
				}
				console.log(name);
				$.ajax({
						url:"/api/profile/name",
						type:"post",
						dataType:"json",
						contentType:"application/json",
						data:JSON.stringify(ret_data),
						headers:{
							"X-XSRFTOKEN":getCookie("_xsrf")
						},
						success:function(data){
							if("0" === data.errno){
								$(".popup").show();
							}
							else{
								$(".error-msg").show();
							}
						}
				})

		});
		$("#form-avatar").submit(function(e){
        e.preventDefault();
        $('.image_uploading').fadeIn('fast');
        var options = {
            url:"/api/profile/avatar",
            type:"POST",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function(data){
                if ("0" == data.errno) {
                    $('.image_uploading').fadeOut('fast');
                    $("#user-avatar").attr("src", data.url);
                }
            }
        };
        $(this).ajaxSubmit(options);
    });

})

