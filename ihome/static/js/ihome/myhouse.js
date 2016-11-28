$(document).ready(function(){
    $.get("/api/house/my", function(data){
        if("4101" === data.errno){
            window.location.href = "/"
        }else if("0" === data.errno){
            $(".auth-warn").hide();
            // $("#houses-list").hide();
            $("#houses-list").html(template("houses-list-temp",{houses:data.houses}));
            console.log(data.houses);
        }else if("1" === data.errno){
            $(".auth-warn").show();
            $("#houses-list").hide();
        }
    })
    // $(".auth-warn").show();
})