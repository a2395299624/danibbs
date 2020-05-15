$(function () {
    let highlight_btn = $('.highlight-post-btn');
    let recommend_btn = $('.recommend-post-btn');
    highlight_btn.click(function () {
        let post_id = $(this).parent().parent().attr('data-id');
        let url = '';
        if ($(this).text().trim() === '置顶') {
            url = '/cms/tpost/'
        } else {
            url = '/cms/notpost/'
        }
        ajax.post({
                url: url,
                data: {
                    id: post_id
                },
                success: function (data) {
                    if (data.code === 200) {
                        window.location.href = ''
                    } else {
                        m_alert.alertError(data.message)
                    }
                },
                error: function () {
                    m_alert.alertErrorTitle('网络错误')
                }
            }
        )
    });
    recommend_btn.click(function () {
        let post_id = $(this).parent().parent().attr('data-id');
        let url = '';
        if ($(this).text().trim() === '加推') {
            url = '/cms/rpost/'
        } else {
            url = '/cms/norpost/'
        }
        ajax.post({
                url: url,
                data: {
                    id: post_id
                },
                success: function () {
                    window.location.href = ''
                },
                error: function () {
                    m_alert.alertErrorTitle('网络错误')
                }
            }
        )
    });
    delete_btn({
        btn: '.delete-post-btn',
        mes: '确定要删除这个帖子吗',
        url: "/cms/dpost/"
    })
});