/**
 * Created by Administrator on 2017/3/24.
 */

let dnparam = {
    setParam: function (href, key, value) {
        //url拼接参数
        // 重新加载整个页面
        let isReplaced = false;
        let urlArray = href.split('?');
        if (urlArray.length > 1) {
            let queryArray = urlArray[1].split('&');
            for (let i = 0; i < queryArray.length; i++) {
                let paramsArray = queryArray[i].split('=');
                if (paramsArray[0] === key) {
                    paramsArray[1] = value;
                    queryArray[i] = paramsArray.join('=');
                    isReplaced = true;
                    break;
                }
            }

            if (!isReplaced) {
                let params = {};
                params[key] = value;
                if (urlArray.length > 1) {
                    href = href + '&' + $.param(params);
                } else {
                    href = href + '?' + $.param(params);
                }
            } else {
                urlArray[1] = queryArray.join('&');
                href = urlArray.join('?');
            }
        } else {
            let param = {};
            param[key] = value;
            if (urlArray.length > 1) {
                href = href + '&' + $.param(param);
            } else {
                href = href + '?' + $.param(param);
            }
        }
        return href;
    }
};
