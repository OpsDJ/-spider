function r() {
    var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 8;
    console.assert(e >= 8, "最少需生成8位");
    var t = (new Date).getTime()
      , n = e < 8 ? 8 : e
      , r = new Array(n).join("x")
      , o = "".concat(r, "y").replace(/[xy]/g, (function(e) {
        var n = (t + 36 * Math.random()) % 36 | 0;
        return t = Math.floor(t / 36),
        ("x" === e ? n : 3 & n | 8).toString(36)
    }
    ));
    return o
}
var randomString = r(32);
console.log(randomString);  // 输出生成的随机字符串
