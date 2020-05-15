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
        toolbars: [
            [
                'fontfamily', //字体
                'fontsize', //字号
                'horizontal', //分隔线
                'inserttable', //插入表格
                'justifyleft', //居左对齐
                'justifyright', //居右对齐
                'justifycenter', //居中对齐
                'justifyjustify', //两端对齐
            ],
            [
                'bold', //加粗
                'italic', //斜体
                'underline', //下划线
                'forecolor', //字体颜色
                'backcolor', //背景色
                'link', //超链接
                'unlink', //取消链接
                'scrawl', //涂鸦
                'removeformat', //清除格式
                'background', //背景
                'emotion', //表情
                'simpleupload', //单图上传
                'insertvideo', //视频
                'attachment', //附件
            ],
        ],
    },);
    let submit = $('#submit');
    let title = $('input[name=title]');
    let plate_id = $('select[name=plate_id]');
    submit.click(function (event) {
        let text = ue.getContent();
        event.preventDefault();
        if (alert_error(title.val(), '抱歉，您尚未输入标题或内容') && alert_error(text, '抱歉，您尚未输入标题或内容')
            && alert_error(plate_id.val(), '请选择一个板块')) {
            ajax.post({
                url: '/post/',
                data: {
                    title: title.val(),
                    plate_id: plate_id.val(),
                    text: text,
                },
                success: function (data) {
                    window.location.href = data.data.url_go
                },
                error: function () {
                    m_alert.alertErrorTitle('网络错误',)
                }
            })
        }
    });
});