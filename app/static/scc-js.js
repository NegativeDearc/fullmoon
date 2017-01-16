/**
 * Created by datin_000 on 2017/1/16.
 */
//ajax for recent articles/comments/achieve/categories
var insert_submit_form = function (e) {
    var _this = $(e);
    var _this_parent = _this.parents().parents(":first")[0];
    //must ensure add form only once when clicked many times
    _this_parent.append('111');
};