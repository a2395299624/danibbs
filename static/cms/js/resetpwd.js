function create_box(error, place) {
    place = $(place).parent().parent();
    let div = $('<div></div>');
    let strong = $('<strong></strong>');
    let img = $('<i></i>');
    div.append(img);
    div.append(strong);
    strong.text(error);
    div.addClass('alert alert-danger error');
    div.attr('role', 'alert');
    img.addClass('fa fa-exclamation-triangle fa-2x');
    img.attr('aria-hidden', 'true');
    if (place.find('.error').length < 1) {
        place.append(div)
    }
    $(".show_span").text(error);
    div.hide();
    div.fadeIn(700);
    let timeId = setTimeout(function () {
        div.remove();
        clearTimeout(timeId);
    }, 3700);


}

function clear_value(values) {
    for (let i = 0; i <= values.length; i++) {
        $(values[i]).val('')
    }
}

function extend(a, b) {
    for (let key in a) {
        if (b.hasOwnProperty(key)) {
            a[key] = b[key];
        }
    }
    return a;
}

function ShowMsg(btn, args) {
    let input_len_new = "input[name=" + args.input_len_new + "]";
    let input_unlike_sure = "input[name=" + args.input_unlike_sure + "]";
    let input_equal_old = "input[name=" + args.input_equal_old + "]";
    args = extend(this.args, args);
    $(function () {
            $(btn).click(function (event) {
                    let oldpwd = $(input_equal_old).val();
                    let newpwd = $(input_len_new).val();
                    let surepwd = $(input_unlike_sure).val();
                    let notnull = oldpwd !== '' && newpwd !== '' && surepwd !== '';
                    let check = true;
                    // 验证输入框是否为空
                    if (notnull) {
                        event.preventDefault();
                        // 验证新密码与旧密码是否一致
                        if (oldpwd === newpwd) {
                            create_box(args.error_equal, input_equal_old);
                            clear_value([input_equal_old, input_len_new, input_unlike_sure]);
                            check = false
                        }
                        // 验证密码长度是否正确
                        if (args.error_len !== '' && newpwd.length <= 5 || newpwd.length > 12) {
                            create_box(args.error_len, input_len_new);
                            clear_value([input_equal_old, input_len_new, input_unlike_sure]);
                            check = false
                        }
                        // 验证确认密码是否一致
                        if (args.error_unlike !== '' && newpwd !== surepwd) {
                            create_box(args.error_unlike, input_unlike_sure);
                            clear_value([input_equal_old, input_len_new, input_unlike_sure]);

                            check = false
                        }
                        // ajax请求
                        if (check) {
                            ajax.post({
                                'url': '/cms/resetpwd/',
                                'data': {
                                    'oldpwd': oldpwd,
                                    'newpwd': newpwd,
                                    'surepwd': surepwd
                                },
                                'success': function (data) {
                                    if (data.code === 200) {
                                        m_alert.alertSuccessToast(data.message, 1500)
                                    } else {
                                        m_alert.alertError(data.message,)
                                    }
                                    clear_value([input_equal_old, input_len_new, input_unlike_sure]);
                                    $('.sweet-alert').css('margin-top', '')
                                },
                                'error': function () {
                                    m_alert.alertNetworkError(1500);
                                    clear_value([input_equal_old, input_len_new, input_unlike_sure]);
                                    $('.sweet-alert').css('margin-top', '')
                                }
                            });
                        }
                    }
                }
            )
        }
    )
}

ShowMsg.prototype.args = {
    error_len: "",  //验证密码长度
    error_unlike: "",   //验证确认密码一致
    error_equal: "",  //验证新旧密码是否相同
    input_unlike_sure: "",   //密码一致错误显示位置
    input_len_new: "",  //密码长度错误显示位置
    input_equal_old: ""  //新旧密码相同显示位置
};

new ShowMsg("#submit", {
    error_unlike: '密码不一致,请重新输入',
    error_len: '新密码长度不正确,应在6-12位之间',
    error_equal: '新密码不能与旧密码相同',
    input_len_new: "newpwd",
    input_unlike_sure: 'surepwd',
    input_equal_old: "oldpwd",
},);
