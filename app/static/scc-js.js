/**
 * Created by datin_000 on 2017/1/16.
 */
//ajax for recent articles/comments/achieve/categories
var insert_submit_form = function (e) {
    var _this = $(e);

    if (_this.attr("status")) {
        //destroy the inline-leave-a-message form
        $("[name='inline-form']").remove();
        _this.attr("class", "btn btn-sm btn-info");
        _this.removeAttr("status");
        _this.html("回复");
    } else {
        //get the id of the comment message
        var reply_id = _this.siblings("[name='reply']").html();
        var reply_to_id = _this.siblings("[name='reply_to']").html();

        //clone DOM
        var fm_html = $("#leave-a-message").clone(true);
        var fm_form = fm_html.find(".form");
        fm_form.attr("name", "inline-form");
        //insert reply_id to form, make reply_id as the new comment's reply_to_id
        fm_form.append('<input type="hidden" name="reply_to_id" value="' + reply_id + '" >');

        var _this_parent = _this.parents().parents(":first");
        _this_parent.append(fm_form[0]);
        //when it's all done, turn btn-info to btn-warning and change the button html
        _this.attr("class", "btn btn-sm btn-warning");
        _this.attr("status", "clicked");
        _this.html("取消");
    }
};

share_weibo = function () {
    var _shareUrl = 'http://v.t.sina.com.cn/share/share.php?&appkey=788764452';     //真实的appkey ，必选参数
    var _url = '';
    var _title = "我发现了一篇美文" + "《" +$("#title").html() + "》" + "--来自优美的独立博客full moon，快来发表你的评论吧！";
    var _source = false;
    var _sourceUrl = false;
    var _pic = false;
    var _width =  window.screen.width / 2 - 250;
    var _height = window.screen.height / 2 - 300;
    _shareUrl += '&url='+ encodeURIComponent(_url||document.location);     //参数url设置分享的内容链接|默认当前页location，可选参数
    _shareUrl += '&title=' + encodeURIComponent(_title||document.title);    //参数title设置分享的标题|默认当前页标题，可选参数
    _shareUrl += '&source=' + encodeURIComponent(_source||'');
    _shareUrl += '&sourceUrl=' + encodeURIComponent(_sourceUrl||'');
    _shareUrl += '&content=' + 'utf-8';   //参数content设置页面编码gb2312|utf-8，可选参数
    _shareUrl += '&pic=' + encodeURIComponent(_pic||'');  //参数pic设置图片链接|默认为空，可选参数
    window.open(_shareUrl,'_blank','toolbar=no,menubar=no,scrollbars=no,resizable=1,location=no,status=0,' + 'width=' + _width + ',height=' + _height + ',top=' + (screen.height-_height)/2 + ',left=' + (screen.width-_width)/2);
};

share_qzone = function () {
    var _shareUrl = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?';
    var _url = '';
    var _title = false;
    var _showcount = 1;
    var _desc = "我发现了一篇美文" + "《" +$("#title").html() + "》" + "--来自优美的独立博客full moon，快来发表你的评论吧！";
    var _pic = false;
    var _summary = false;
    var _site = false;
    var _width =  window.screen.width / 2 - 250;
    var _height = window.screen.height / 2 + 50;

    _shareUrl += 'url=' + encodeURIComponent(_url||document.location);   //参数url设置分享的内容链接|默认当前页location
    _shareUrl += '&showcount=' + _showcount||0;      //参数showcount是否显示分享总数,显示：'1'，不显示：'0'，默认不显示
    _shareUrl += '&desc=' + encodeURIComponent(_desc||'分享的描述');    //参数desc设置分享的描述，可选参数
    _shareUrl += '&summary=' + encodeURIComponent(_summary||'分享摘要');    //参数summary设置分享摘要，可选参数
    _shareUrl += '&title=' + encodeURIComponent(_title||document.title);    //参数title设置分享标题，可选参数
    _shareUrl += '&site=' + encodeURIComponent(_site||'');   //参数site设置分享来源，可选参数
    _shareUrl += '&pics=' + encodeURIComponent(_pic||'');   //参数pics设置分享图片的路径，多张图片以＂|＂隔开，可选参数
    window.open(_shareUrl,'_blank','width='+_width+',height='+_height+',top='+(screen.height-_height)/2+',left='+(screen.width-_width)/2+',toolbar=no,menubar=no,scrollbars=no,resizable=1,location=no,status=0');
};

share_weixin = function () {
    var _this = $(".fa.fa-wechat");
    var _offset = _this.offset();
    var qr_div = $('<div id="qrcode" style="margin-left: -64px;margin-top: -206px;center;z-index: 9;position:absolute;padding: 10px;border: 1px solid #dadada;background: #ffffff;">扫描分享到朋友圈</div>');
    var _url = document.location;
    var qrcode = new QRCode(qr_div[0], {
        text: _url,
        width: 128,
        height: 128,
        colorDark : "#000000",
        colorLight : "#ffffff",
        correctLevel : QRCode.CorrectLevel.M
    });
    console.log(_offset);
    // qr_div.css(_offset);
    _this.parent("div").append(qr_div);
};