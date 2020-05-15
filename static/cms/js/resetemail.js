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
    setTimeout(function () {
        div.remove()
    }, 3700)
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

function countdown(args) {
    let time = 60;
    $(args.captcha_btn).addClass('btn');
    let t = setInterval(function () {
        time -= 1;
        $(args.captcha_btn).text(time + "S后获取");
        if (time === 0) {
            time = 60;
            $(args.captcha_btn).text("获取验证码");
            $(args.captcha_btn).removeClass('btn');
            clearInterval(t)
        }
    }, 1000);
}

function ShowMsg(btn, args) {
    let email = "input[name=" + args.email + "]";
    let captcha = "input[name=" + args.captcha + "]";
    args = extend(this.args, args);
    let email_reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
    $(function () {
            $(btn).click(function (event) {
                    let check = true;
                    let captcha_val = $(captcha).val();
                    let email_val = $(email).val();
                    event.preventDefault();
                    if (captcha_val === "") {
                        create_box(args.error_captcha, captcha);
                        check = false
                    }
                    if (email_val === '') {
                        create_box(args.error_email, email);
                        check = false
                    } else if (!email_reg.test(email_val)) {
                        create_box(args.error_format, email);
                    }
                    if (check) {
                        ajax.post({
                            "url": "/cms/resetemail/",
                            "data": {
                                "email": email_val,
                                "captcha": captcha_val
                            },
                            "success": function (data) {
                                if (data.code === 200) {
                                    m_alert.alertSuccessToast('邮箱修改成功', 1500)
                                } else {
                                    m_alert.alertError(data.message)
                                }
                                $('.sweet-alert').css('margin-top', '');
                                clear_value([email, captcha])
                            },
                            "error": function () {
                                m_alert.alertNetworkError(1500);
                                clear_value([email, captcha]);
                                $('.sweet-alert').css('margin-top', '')
                            }
                        })
                    }
                }
            );
            $(args.captcha_btn).click(function (event) {
                    let email_val = $(email).val();
                    if (email_val === '') {
                        create_box(args.error_email, email);
                    } else if (!email_reg.test(email_val)) {
                        create_box(args.error_format, email);
                    } else {
                        countdown(args);
                        ajax.get({
                                "url": "/cms/emailcaptcha/",
                                "data": {
                                    "email": email_val
                                },
                                "success": function (data) {
                                    if (data.code === 200) {
                                        m_alert.alertSuccessToast('验证码发送成功', 1500)
                                    } else {
                                        m_alert.alertError(data.message,)
                                    }
                                    $('.sweet-alert').css('margin-top', '')
                                },
                                "error": function () {
                                    m_alert.alertNetworkError(1500);
                                    clear_value([email, captcha]);
                                    $('.sweet-alert').css('margin-top', '')
                                }
                            }
                        )
                    }

                }
            )
        }
    )
}

ShowMsg.prototype.args = {
    error_email: "",
    error_format: "",
    error_captcha: "",
    email: "",
    captcha: "",
    captcha_btn: ""
};

new ShowMsg("#submit", {
    error_format: "邮箱格式错误",
    error_email: '请输入邮箱',
    error_captcha: "请输入验证码",
    email: "email",
    captcha: "captcha",
    captcha_btn: ".get-captcha"

},);
