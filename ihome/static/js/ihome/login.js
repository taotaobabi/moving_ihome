function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        var ret_data = {
            mobile:mobile,
            password:passwd
        }
        $.ajax({
            url:"/api/login",
            type:"post",
            contentType:"application/json",
            dataType:"json",
            data:JSON.stringify(ret_data),
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf")
            },
            success:function(data){
                if("0" != data.errno){
                    $("#password-err span").html(data.errmsg);
                    $("#password-err").show();
                }
                else{
                    window.location.href="/"
                }
            }
        })
    });
})