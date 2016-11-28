function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get("/api/house/area", function(data){
        if(0 == data.errno){
            $("#area-id").html(template("areas-list-temp",{areas:data.areas}));
            // console.log(data);
        }
    })
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    // $("#form-house-image").hide();
    // $("#form-house-info").show();
    $("#form-house-info").submit(function(e){
        e.preventDefault();
        var data = {};
        $(this).serializeArray().map(function(x){data[x.name]=x.value});
        console.log(data);
    })
        
       

})