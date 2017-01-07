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

var BasicAuthorizationCode = function(username, password){
    //http://magic-conch.cool/article/2016/01/26/basic-auth-in-jquery-ajax
    var safeStr = unescape(encodeURIComponent(username + ':' + password));
    var btoaCode = btoa(safeStr);
    return 'Basic ' + btoaCode;
};
