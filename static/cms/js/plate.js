$(function () {
    let plate_add = $('#plate-add');
    let edit_plate_btn = $('.edit-plate-btn');
    let input_name = $("input[name='name']");

    plate_add.click(function () {
        m_alert.alertOneInput({
            title: "添加板块",
            text: "请输入板块名称",
            placeholder: '板块名称',
            confirmCallback: function (inputValue) {
                ajax.post({
                    url: '/cms/aplate/',
                    data: {
                        name: inputValue
                    },
                    success: function (data) {
                        if (data.code === 200) {
                            window.location.reload();
                        } else {
                            m_alert.alertInfo(data.message)
                        }
                    },
                    error: function () {
                        m_alert.alertErrorTitle('网络错误',)
                    }
                })
            }
        });

    });
    edit_plate_btn.click(function () {
        let tr = $(this).parent().parent();
        let id = tr.attr('data-id');
        m_alert.alertOneInput({
            title: "修改板块",
            text: "请输入新的板块名称",
            placeholder: '板块名称',
            confirmCallback: function (inputValue) {
                ajax.post({
                    url: '/cms/uplate/',
                    data: {
                        name: inputValue,
                        id: id
                    },
                    success: function (data) {
                        if (data.code === 200) {
                            window.location.reload();
                        } else {
                            m_alert.alertInfo(data.message)
                        }
                    },
                    error: function () {
                        m_alert.alertErrorTitle('网络错误',)
                    }
                })
            }
        });
    });
    delete_btn({
        btn: '.delete-plate-btn',
        mes: '确定要删除这个板块吗',
        url: "/cms/dplate/"
    })
});