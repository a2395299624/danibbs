function ShowMsg(btn, args) {
    $(function () {
            let name_input = $("input[name=" + args.name + "]");
            let image_input = $("input[name=" + args.image + "]");
            let url_input = $("input[name=" + args.url + "]");
            let priority_input = $("input[name=" + args.priority + "]");

            let submit = $(btn);
            let error_message = $('.error_message');
            let modal_title = $('.modal-title');

            submit.click(function () {
                if (dnshake.shake(name_input) && dnshake.shake(image_input) && dnshake.shake(url_input) && dnshake.shake(priority_input)) {
                    let url;
                    submit.attr('disabled', 'disabled');
                    if (submit.attr('data-type') === 'save') {
                        url = '/cms/ubanner/'
                    } else {
                        url = '/cms/abanner/'
                    }
                    ajax.post({
                        url: url,
                        data: {
                            name: name_input.val(),
                            image: image_input.val(),
                            url: url_input.val(),
                            priority: priority_input.val(),
                            id: submit.attr('data-id')
                        },
                        success: function (data) {
                            if (data.code === 200) {
                                $('#banner-modal').modal('hide');
                                let timeout = setTimeout(function () {
                                    window.location.reload();
                                    clearTimeout(timeout)
                                }, 200)
                            }
                            if (data.code === 400) {
                                $('#banner-modal').modal('hide');
                                m_alert.alertError(data.message)
                            }
                        },
                        error: function () {
                            m_alert.alertNetworkError(1500)
                        }
                    })
                } else {
                    error_message.fadeIn();
                }
            });

            $('.edit-banner-btn').click(function () {
                $('#banner-modal').modal('show');
                let tr = $(this).parent().parent();
                let name = tr.attr('data-name');
                let image = tr.attr('data-image');
                let url = tr.attr('data-url');
                let priority = tr.attr('data-priority');

                name_input.val(name);
                image_input.val(image);
                url_input.val(url);
                priority_input.val(priority);

                submit.attr('data-type', 'save');
                submit.attr('data-id', tr.attr('data-id'));
                submit.text('保存');
                modal_title.text('修改');
            });

            $('.close').click(function () {
                error_message.fadeOut()
            });
            modal_close();
            add_btn();
            delete_btn({
                btn: ".delete-banner-btn",
                mes: "确定要删除这个轮播图吗",
                url: "/cms/dbanner/"
            });

            dnqiniu.setUp({
                'domain': 'http://q9xc69071.bkt.clouddn.com/',
                'browse_button': 'upload-btn',
                'uptoken_url': '/common/uptoken/',
                'success': function (up, file, info) {
                    image_input.val(file.name);
                }
            })
        }
    )
}

ShowMsg.prototype.args = {
    name: "",
    image: "",
    url: "",
    priority: "",

};

new ShowMsg("#submit", {
    name: "name",
    image: "image",
    url: "url",
    priority: "priority",
},);

