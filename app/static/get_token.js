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

/**
 * @return {string}
 */
var BasicAuthorizationCode = function(username, password){
    //http://magic-conch.cool/article/2016/01/26/basic-auth-in-jquery-ajax
    var safeStr = unescape(encodeURIComponent(username + ':' + password));
    var btoaCode = btoa(safeStr);
    return 'Basic ' + btoaCode;
};

var utf8_to_b64 = function(str) {
    return window.btoa(unescape(encodeURIComponent(str)));
};

var b64_to_utf8 = function(str) {
    return decodeURIComponent(escape(window.atob(str)));
};

var modal_delete = function () {
    //ajax to delete the article
    var uuid = $(this).parents().siblings('td:first').html();
    console.log(uuid);
    $("#check_to_delete").find(".modal-body p").attr("id",uuid);
    $("#check_to_delete").modal("show");
};

var select_click = function(){
    var uuid = $(this).parents().siblings("td.uuid").html();
    var self = $(this);
    console.log(uuid);
    if (self.children("option").length > 1){return false}//prevent add options unlimited
    $.ajax({
         beforeSend:function (request) {
             //WWW-Authenticate:Basic realm="Authentication Required"
             //自己构造HTTP头Authorization: Basic 用BASE64加密"用户:密码"
             //HTTP使用BASIC认证的原理及实现方法
             //http://blog.itpub.net/23071790/viewspace-709367/
             request.setRequestHeader("Authorization", BasicAuthorizationCode(get_token(),"unused"));
         },
         url:$SCRIPT_ROOT + '/api/article/uuid/' + uuid,
         type:"POST",
         data:{"uuid":uuid,"_method":"POST","demands":"1"},
         success:function (data) {
             console.log(data);
             for (var i=0;i<data['list'].length;i++) {
                 var d = data['list'][i];
                 self.append('<option value="' + d + '">' + d + '</option>');
            }
        }
    });
};

var select_select = function(){
    var value = $(this).val();
    var uuid = $(this).parents().siblings("td.uuid").html();
    $.ajax({
        beforeSend:function (request) {
             request.setRequestHeader("Authorization", BasicAuthorizationCode(get_token(),"unused"));
        },
        url:$SCRIPT_ROOT + '/api/article/uuid/' + uuid,
        type:"PUT",
        data:{
            "edit_date":new Date().toISOString(),
            "uuid":uuid,
            "_method":"PUT",
            "status":value
        },
        success:function (res) {
            console.log(res);
        }
});
};