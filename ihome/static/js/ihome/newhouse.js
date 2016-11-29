function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get("/api/house/area", function(data){
        if("0" == data.errno){
            $("#area-id").html(template("areas-list-temp",{areas:data.areas}));
        }
    });
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    // $("#form-house-image").hide();
    // $("#form-house-info").hide();
    $("#form-house-info").submit(function(e){
        e.preventDefault();
        var data = {};
        $(this).serializeArray().map(function(x){data[x.name]=x.value});
        console.log(data);
        
        var list = [];
        var facility = $("input:checkbox:checked[name='facility']").serializeArray();
        for(var i=0;i<facility.length;i++){
                list.push(facility[i].value);
        }
        data.facility = list;
        // console.log(data.facility[0]);
        var jsonData = JSON.stringify(data);

        $.ajax({
            url:"/api/house/new",
            type:"POST",
            data: jsonData, 
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function (data){

            }
    })
        
       

})
})    