$(function () {
    let url = window.location.href;
    let sidebar_menu = $('.sidebar-menu');
    if (url.indexOf("banners") >= 0) {
        sidebar_menu.children().eq(2).addClass('active');
        sidebar_menu.children().eq(0).removeClass('active')
    }
    if (url.indexOf("profile") >= 0) {
        $('.treeview').addClass('active');
        sidebar_menu.children().eq(0).removeClass('active');
        $('.treeview-menu').children('li').children().eq(0).css('color', 'red')
    }
    if (url.indexOf("resetpwd") >= 0) {
        $('.treeview').addClass('active');
        $('.sidebar-menu').children().eq(0).removeClass('active')
        $('.treeview-menu').children('li').children().eq(1).css('color', 'red')
    }
    if (url.indexOf("resetemail") >= 0) {
        $('.treeview').addClass('active');
        $('.sidebar-menu').children().eq(0).removeClass('active')
        $('.treeview-menu').children('li').children().eq(2).css('color', 'red')
    }
    if (url.indexOf("post") >= 0) {
        sidebar_menu.children().eq(3).addClass('active');
        sidebar_menu.children().eq(0).removeClass('active')
    }
    if (url.indexOf("comment") >= 0) {
        sidebar_menu.children().eq(4).addClass('active');
        sidebar_menu.children().eq(0).removeClass('active')
    }
    if (url.indexOf("plate") >= 0) {
        sidebar_menu.children().eq(5).addClass('active');
        sidebar_menu.children().eq(0).removeClass('active')
    }
    if (url.indexOf("webuser") >= 0) {
        sidebar_menu.children().eq(6).addClass('active');
        sidebar_menu.children().eq(0).removeClass('active')
    }
    if (url.indexOf("cmsuser") >= 0) {
        sidebar_menu.children().eq(7).addClass('active');
        sidebar_menu.children().eq(0).removeClass('active')
    }
    if (url.indexOf("cmsgroup") >= 0) {
        sidebar_menu.children().eq(8).addClass('active');
        sidebar_menu.children().eq(0).removeClass('active')
    }
});