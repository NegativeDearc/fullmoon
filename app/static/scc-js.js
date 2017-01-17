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