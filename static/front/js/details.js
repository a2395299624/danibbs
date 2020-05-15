function alert_error(value, info) {
    if (value === '') {
        let pop_error = $('.pop-error');
        let er_text = $('.er-text');
        er_text.children().text(info);
        pop_error.css('display', 'block');
        let timeout = setTimeout(function () {
            er_text.children().text('');
            pop_error.css('display', 'none');
            clearTimeout(timeout)
        }, 1500);
        return false
    }
    return true
}


$(function () {
    let ue = UE.getEditor('container', {
        serverUrl: '/ueditor/upload/',
        initialFrameHeight: 100,
        initialFrameWidth: 952,
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传\
                'emotion' //表情k
            ]]
    });
    $('#comment-btn').click(function () {
        let content = ue.getContent();
        let longin = $('.avatar').html();
        let post_id = $('.post-content').attr('post-id');
        if (!longin) {
            window.location.href = '/login/'
        } else {
            if (alert_error(content, '您输入的内容不合法，请修改后重新提交。')) {
                ajax.post({
                    url: '/comment/',
                    data: {
                        content: content,
                        post_id: post_id
                    },
                    success: function (data) {
                        window.location.href = ''
                    },
                    error: function () {

                    }
                })
            }
        }


    })

});