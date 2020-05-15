function ShowMsg(btn, args) {
    $(function () {
            let telephone = $("input[name=" + args.telephone + "]");
            let username = $("input[name=" + args.username + "]");
            let remember = $('input[name=remember]');
            let password1 = $(args.password1);
            let password2 = $(args.password2);
            let submit = $(btn);
            let mobilelogin = $('#mobilelogin');
            let namelogin = $('#namelogin');

            // 表单验证数据提交
            function from_check() {
                let check = true;
                if (namelogin.hasClass('active')) {
                    if (username.val() === '') {
                        check = false;
                        username.next().text('昵称不能为空');
                    } else {
                        username.next().text('');
                    }

                    if (password2.val() === '') {
                        check = false;
                        password2.css('border', 'solid 1px red');
                        password2.next().text('请输入密码');
                    } else {
                        password2.css('border', '');
                        password2.next().text('');
                    }
                }
                if (mobilelogin.hasClass('active')) {
                    if (telephone.val() === '') {
                        check = false;
                        telephone.next().text('请输入手机号');
                    } else {
                        telephone.next().text('');
                    }

                    if (password1.val() === '') {
                        check = false;
                        password1.css('border', 'solid 1px red');
                        password1.next().text('请输入密码');
                    } else {
                        password1.css('border', '');
                        password1.next().text('');
                    }
                }
                if (mobilelogin.hasClass('active')) {
                    if (check) {
                        ajax.post({
                                url: "/login/",
                                data: {
                                    telephone: telephone.val(),
                                    password1: password1.val(),
                                    remember: remember.is(':checked') ? "true" : "false"
                                },
                                success: function (data) {
                                    if (data.code === 200) {
                                        let url_go = submit.attr('url-go');
                                        if (url_go !== 'None') {
                                            window.location.href = url_go
                                        } else {
                                            window.location.href = '/'
                                        }
                                    }
                                    if (data.code === 400) {
                                        $('.form-error').children().text('账号或密码错误')
                                    }
                                },
                                error: function (error) {
                                    $('.form-error').children().text('网络错误');
                                }
                            }
                        )
                    }
                }

                if (namelogin.hasClass('active')) {
                    if (check) {
                        ajax.post({
                            url: "/login/",
                            data: {
                                username: username.val(),
                                password2: password2.val(),
                                remember: remember.is(':checked') ? "true" : "false"
                            },
                            success: function (data) {
                                if (data.code === 200) {
                                    if (data.data.url_go) {
                                        window.location.href = data.data.url_go
                                    } else {
                                        window.location.href = '/'
                                    }
                                }
                                if (data.code === 400) {
                                    $('.form-error').children().text('账号或密码错误')
                                }
                            },
                            error: function (error) {
                                $('.form-error').children().text('网络错误');
                            }
                        })
                    }
                }
            }

            function password_check(parm) {
                parm.keyup(function () {
                    if (parm.val() === '') {
                        parm.next().text('请输入密码');
                        parm.css('border', 'solid 1px red');
                    } else {
                        parm.css('border', '');
                        parm.next().text('');
                    }
                });
            }

            // 登录按钮
            submit.click(function () {
                from_check()
            });

            // 回车按钮
            $(document).keyup(function (event) {
                if (event.keyCode === 13) {
                    from_check()
                }
            });

            // 表单验证
            password_check(password1);
            password_check(password2);
            telephone.keyup(function () {
                telephone.val(telephone.val().replace(/\D/g, ''));
                if (telephone.val() === '') {
                    telephone.next().text('请输入手机号')
                    telephone.css('border', 'solid 1px red');
                } else {
                    telephone.css('border', '');
                    telephone.next().text('')
                }
            });
            username.keyup(function () {
                if (username.val() === '') {
                    username.next().text('昵称不能为空')
                    username.css('border', 'solid 1px red');
                } else {
                    username.css('border', '');
                    username.next().text('')
                }
            })
        }
    )
}

ShowMsg.prototype.args = {
    telephone: "",
    password: "",
    password1: "",
    password2: "",
    username: "",
};

new ShowMsg("#signin", {
    telephone: "telephone",
    password: "password",
    password1: ".password1",
    password2: ".password2",
    username: "username",
},);

