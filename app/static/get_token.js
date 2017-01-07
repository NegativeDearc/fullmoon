/**
 * Created by Dearc on 2017/1/7.
 */
var verify_token=function () {
    var token = get_token();
    $.ajax({
        url:'/verify_token',
        method:"post",
        data:{"token": token},
        success:function () {
            console.log("success")
        }
    })
};

var get_token = function () {
    var result;
    $.ajax({
       url:"/get_token",
       method:"get",
       async:false,
       success:function (data) {
           result =  data['token']
       }
    });
    return result
};
