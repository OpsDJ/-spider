import execjs
import requests
import time
t = time.time()

ssess = requests.session()

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Length": "0",
    "Origin": "https://www.ciweimao.com",
    "Referer": "https://www.ciweimao.com/chapter/110694165",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie":f"get_task_type_sign=1; Hm_lvt_1dbadbc80ffab52435c688db7b756e3a={t},1692444576,1692459049,1692463473; ci_session=0f73f1cdea2ee1f475f4ececd46397974abd71cc; Hm_lpvt_1dbadbc80ffab52435c688db7b756e3a=1692493096; readPage_visits=42; user_id=18263008;"}

url_main = 'https://www.ciweimao.com/chapter/110694165'

res1 = ssess.get(url_main, headers=headers)

url = 'https://www.ciweimao.com/chapter/ajax_get_image_session_code'


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Length": "0",
    "Origin": "https://www.ciweimao.com",
    "Referer": "https://www.ciweimao.com/chapter/110694165",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "X-Requested-With": "XMLHttpRequest"}


res = ssess.post(url, headers=headers)
# print(res.cookies)
# for key, value in ssess.cookies.items():
#     cookie = (key + "=" + value)
#     print(cookie)

js = res.json()

image_code = js['image_code']
encryt_keys = js['encryt_keys']
access_key = js['access_key']

js_code = """
base64 = function() {
    var _PADCHAR = "="
        , _ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        , _VERSION = "1.0";
    function _getbyte64(s, i) {
        var idx = _ALPHA.indexOf(s.charAt(i));
        if (idx === -1) {
            throw "Cannot decode base64"
        }
        return idx
    }
    function _decode(s) {
        var pads = 0, i, b10, imax = s.length, x = [];
        s = String(s);
        if (imax === 0) {
            return s
        }
        if (imax % 4 !== 0) {
            throw "Cannot decode base64"
        }
        if (s.charAt(imax - 1) === _PADCHAR) {
            pads = 1;
            if (s.charAt(imax - 2) === _PADCHAR) {
                pads = 2
            }
            imax -= 4
        }
        for (i = 0; i < imax; i += 4) {
            b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12) | (_getbyte64(s, i + 2) << 6) | _getbyte64(s, i + 3);
            x.push(String.fromCharCode(b10 >> 16, (b10 >> 8) & 255, b10 & 255))
        }
        switch (pads) {
            case 1:
                b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12) | (_getbyte64(s, i + 2) << 6);
                x.push(String.fromCharCode(b10 >> 16, (b10 >> 8) & 255));
                break;
            case 2:
                b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12);
                x.push(String.fromCharCode(b10 >> 16));
                break
        }
        return x.join("")
    }
    function _getbyte(s, i) {
        var x = s.charCodeAt(i);
        if (x > 255) {
            throw "INVALID_CHARACTER_ERR: DOM Exception 5"
        }
        return x
    }
    function _encode(s) {
        if (arguments.length !== 1) {
            throw "SyntaxError: exactly one argument required"
        }
        s = String(s);
        var i, b10, x = [], imax = s.length - s.length % 3;
        if (s.length === 0) {
            return s
        }
        for (i = 0; i < imax; i += 3) {
            b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8) | _getbyte(s, i + 2);
            x.push(_ALPHA.charAt(b10 >> 18));
            x.push(_ALPHA.charAt((b10 >> 12) & 63));
            x.push(_ALPHA.charAt((b10 >> 6) & 63));
            x.push(_ALPHA.charAt(b10 & 63))
        }
        switch (s.length - imax) {
            case 1:
                b10 = _getbyte(s, i) << 16;
                x.push(_ALPHA.charAt(b10 >> 18) + _ALPHA.charAt((b10 >> 12) & 63) + _PADCHAR + _PADCHAR);
                break;
            case 2:
                b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8);
                x.push(_ALPHA.charAt(b10 >> 18) + _ALPHA.charAt((b10 >> 12) & 63) + _ALPHA.charAt((b10 >> 6) & 63) + _PADCHAR);
                break
        }
        return x.join("")
    }
    return {
        decode: _decode,
        encode: _encode,
        VERSION: _VERSION
    }
}
function decrypt(g) {
    var CryptoJS = require("crypto-js");
    var s = g;
    var n = s.content;
    var r = s.keys;
    var t = s.keys.length;
    var q = s.accessKey;
    var o = q.split("");
    var m = o.length;
    var k = new Array();
    k.push(r[(o[m - 1].charCodeAt(0)) % t]);
    k.push(r[(o[0].charCodeAt(0)) % t]);
    for (i = 0; i < k.length; i++) {
        n = base64().decode(n);
        var p = k[i];
        var j = base64().encode(n.substr(0, 16));
        var f = base64().encode(n.substr(16));
        var h = CryptoJS.format.OpenSSL.parse(f);
        n = CryptoJS.AES.decrypt(h, CryptoJS.enc.Base64.parse(p), {
            iv: CryptoJS.enc.Base64.parse(j),
            format: CryptoJS.format.OpenSSL
        });
        if (i < k.length - 1) {
            n = n.toString(CryptoJS.enc.Base64);
            n = base64().decode(n)
        }
    }
    return n.toString(CryptoJS.enc.Utf8)
}

"""

g = {
    "content": image_code,
    "keys":encryt_keys,
    "accessKey":access_key
}

ctx = execjs.compile(js_code)
result = ctx.call("decrypt", g)


url_2 = 'https://www.ciweimao.com/chapter/book_chapter_image'



params = {
    "chapter_id": 110694165,
    'area_width': 870.99,
    'font': 'undefined',
    'font_size': 14,
    'image_code': f'{result}',
    'bg_color_name': 'default',
    'text_color_name': 'default'
}


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Length": "0",
    "Origin": "https://www.ciweimao.com",
    "Referer": "https://www.ciweimao.com/chapter/110607780",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "X-Requested-With": "XMLHttpRequest"}

res2 = ssess.get(url_2, headers=headers, params=params)


with open('book_image.png', mode='wb') as f:
    f.write(res2.content)

print('ok')
