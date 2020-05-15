function clear_value(values) {
    for (let i = 0; i <= values.length; i++) {
        $(values[i]).val('')
    }
}

function countdown(args) {
    let time = 60;
    let t = setInterval(function () {
        time -= 1;
        let get_sms = $(args.get_sms);
        get_sms.text(time + "S后获取");
        get_sms.attr('disabled', 'disabled');
        if (time === 0) {
            time = 60;
            get_sms.text("点击获取");
            get_sms.removeAttr('disabled');
            clearInterval(t);
        }
    }, 1000);
}

function ShowMsg(btn, args) {
    $(function () {
        let telephone = $("input[name=" + args.telephone + "]");
        let agree = $("input[name=" + args.agree + "]");
        let password = $("input[name=" + args.password + "]");
        let username = $("input[name=" + args.username + "]");
        let smscaptcha = $("input[name=" + args.smscaptcha + "]");
        let submit = $(btn);
        // 同意
        if (!agree.is(':checked')) {
            submit.attr('disabled', 'disabled')
        }
        agree.click(function () {
            if (submit.is(':disabled')) {
                submit.removeAttr('disabled')
            } else {
                submit.attr('disabled', 'disabled')
            }
        });

        // 行为验证码
        new YpRiddler({
            expired: 10,
            mode: 'dialog',
            winWidth: 350,
            noButton: true,
            lang: 'zh-cn', // 界面语言, 目前支持: 中文简体 zh-cn, 英语 en
            // langPack: LANG_OTHER, // 你可以通过该参数自定义语言包, 其优先级高于lang
            container: document.getElementById('span_sms'),
            appId: 'e452fd6b22734687aa5698511b0c8852',
            version: 'v1',
            onError: function (param) {
                if (param.code === 429) {
                    console.warn('请求过于频繁，请稍后再试');
                }
            },
            onSuccess: function (validInfo, close, useDefaultSuccess) {
                // 成功回调
                m_alert.alertSuccessToast('验证成功', 1500);
                ajax.post({
                    'url': '/common/sms/',
                    'data': {
                        'telephone': telephone.val(),
                        "token": validInfo.token,
                        "authenticate": validInfo.authenticate,
                    },
                    'success': function (data) {
                        if (data.code === 200) {
                            smscaptcha.parent().next().text('验证码已发送');
                        }
                        if (data.code === 400) {
                            smscaptcha.parent().next().text('手机号已被注册');
                        }
                        if (data.code === 401) {
                            smscaptcha.parent().next().text('请输入正确的手机号');
                        }
                        if (data.code === 500) {
                            smscaptcha.parent().next().text('验证失败,请稍后再试');
                        }
                    },
                    'error': function (error) {
                        smscaptcha.parent().next().text('网络错误');
                    }
                });
                close()
            },
            beforeStart: function (next) {
                telephone.next().text('');
                if (telephone.val() === '') {
                    telephone.next().text('请输入手机号');
                    telephone.css('border', 'solid 1px red');
                    let t = setTimeout(function () {
                        telephone.css('border', '');
                        clearTimeout(t)
                    }, 2000)
                } else {
                    next()
                }
            },
            onFail: function (code, msg, retry) {
                // 失败回调
                retry()
            },

        });

        // 注册按钮
        submit.click(function () {
            let check = true;
            if (username.val() === '') {
                check = false;
                username.next().text('昵称不能为空');
            } else {
                username.next().text('');
            }
            if (password.val().length < 5) {
                check = false;
                password.next().text('密码不能小于6位');
            } else if (password.val().length > 16) {
                check = false;
                password.next().text('密码不能大于16位');
            } else {
                password.next().text('');
            }
            if (telephone.val() === '') {
                check = false;
                telephone.next().text('请输入手机号');
            } else {
                telephone.next().text('');
            }
            if (smscaptcha.val() === '') {
                check = false;
                smscaptcha.parent().next().text('请输入验证码');
            } else {
                smscaptcha.parent().next().text('');
            }
            if (check) {
                ajax.post({
                    url: "/register/",
                    data: {
                        username: username.val(),
                        password: password.val(),
                        telephone: telephone.val(),
                        smscaptcha: smscaptcha.val()
                    },
                    success: function (data) {
                        if (data.code === 400) {
                            username.next().text(data.message);
                        }
                        if (data.code === 401) {
                            smscaptcha.parent().next().text(data.message);
                        }
                        if (data.code === 200) {
                            clear_value([username, password, telephone, smscaptcha]);
                            m_alert.alertSuccessToast('注册成功3秒后跳转到首页', 1000000);
                            let t = setTimeout(function () {
                                window.location.href = "http://127.0.0.1:8000/cms/login/";
                                clearTimeout(t)
                            }, 3000);
                        }
                    },
                    error: function (error) {
                        clear_value([username, password, telephone, smscaptcha]);
                        smscaptcha.parent().next().text('网络错误');
                    }
                })
            }
        });

        password.keyup(function () {
            if (password.val().length < 6) {
                password.next().text('密码不能小于6位');
            } else if (password.val().length > 16) {
                password.next().text('密码不能大于16位');
            } else {
                password.next().text('');
            }
        });

        telephone.keyup(function () {
            telephone.val(telephone.val().replace(/\D/g, ''));
        });
    })
}

ShowMsg.prototype.args = {
    get_sms: "",
    agree: "",
    telephone: "",
    password: "",
    username: "",
    smscaptcha: "",
};

new ShowMsg("#submit", {
    get_sms: "#get_sms",
    agree: "agree",
    telephone: "telephone",
    password: "password",
    username: "username",
    smscaptcha: "smscaptcha"
},);

