jQuery.fn.shake = function (intShakes, intDistance, intDuration) {
    this.each(function () {
        let jqNode = $(this);
        jqNode.css({position: 'relative'});
        for (let x = 1; x <= intShakes; x++) {
            jqNode.animate({left: (intDistance * -1)}, (((intDuration / intShakes) / 4)))
                .animate({left: intDistance}, ((intDuration / intShakes) / 2))
                .animate({left: 0}, (((intDuration / intShakes) / 4)));
        }
    });
    return this;
};

function error_shake(input) {
    input.shake(2, 10, 500);
    input.css('border-color', '#FF0033');
    let timeout = setTimeout(function () {
        input.css('border-color', '');
        clearTimeout(timeout)
    }, 500);
}

function input_isnull(input) {
    if (input.val() === '') {
        error_shake(input);
        return false
    }
    return true
}

let dnshake = {
    "shake": function (input) {
        return input_isnull(input)
    },
};

function delete_btn(args) {
    $(args.btn).click(function () {
        let tr = $(this).parent().parent();
        let id = tr.attr('data-id');
        m_alert.alertConfirm(
            {
                msg: args.mes,
                confirmCallback: function () {
                    ajax.post({
                        url: args.url,
                        data: {
                            id: id
                        },
                        success: function (data) {
                            if (data.code === 200) {
                                let timout1 = setTimeout(function () {
                                    m_alert.alertSuccessToast('删除成功', 1400);
                                    clearTimeout(timout1)
                                }, 200);
                                let timout = setTimeout(function () {
                                    window.location.reload();
                                    clearTimeout(timout)
                                }, 1600)
                            }
                            if (data.code === 400) {
                                m_alert.alertError(data.message)
                            }
                        },
                        error: function () {
                            m_alert.alertError('网络错误')
                        }
                    })
                }
            },
        )
    });
}

function add_btn() {
    $('.add-banner').children("button").eq(0).click(function () {
        let submit = $("#submit");
        submit.attr('data-type', 'add');
        submit.text('添加');
        $('.modal-title').text('新增')
    });
}

function modal_close() {
    $('#banner-modal').on('hidden.bs.modal', function () {
        let submit = $("#submit");
        let error_message = $(".error_message");
        $('.modal-body :input').each(function () {
            $(this).val('');
        });
        submit.removeAttr('data-id');
        submit.removeAttr('data-type');
        error_message.css('display', '')
    });
}





