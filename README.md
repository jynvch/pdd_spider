# pdd_spider
通过requests方式请求获得拼多多h5页面异步加载的信息, 
http://mobile.yangkeduo.com/search_result.html?search_key=%E6%9C%88%E9%A5%BC

查找加密位置:

[找加密位置](https://sergiojune.com/2019/03/26/pinduoduo_anti_content/)

[通过F11逐步查找](https://www.cnblogs.com/pupilheart/p/11065797.html)

在GoodList.js下搜 getAntiContent, 
在case 0到case 4之间他已经加密完成了，
接下来就再一次在case 0到case 4之间一直按F11观察情况了。
在GoodList.js的第482行, 进入RiskControl.js
case 3:
    return t = e.sent,
    e.abrupt("return", t.messagePackSync());
此时e的值为
e = {
    arg: Dt {}
    delegate: null
    done: false
    method: "next"
    next: 3
    prev: 3
    sent: Dt {}
    tryEntries: (2) [{…}, {…}]
    _sent: Dt {}
    __proto__: Object
}
然后按着按着就来到了RiskControl.js的1260行
Dt[v("0x108", "([hh")][v("0x109", "*B)d")] = function() {   // v("0x108", "([hh")为prototype, v("0x109", "*B)d")为messagePackSync
    var t = {};
    return t[v("0x10a", "Tadf")] = function(t, n) {
        return t(n)
    }

RiskControl.js里
13个变量大部分都是在第一页的时候执行了初始化, 翻页的时候不再初始化, 
有几个变量是每次都初始化一次, 
Dt[v("0xff", "%ilK")][v("0x100", "@!cA")] = function(t) { // v("0xff", "%ilK")为prototype,v("0x100", "@!cA")为updateServerTime 
    F = G[m](),
    P = t
}

涉及到js解密, 主要解决anti_content参数
简单说一下 这个算法： 它获取了href，push，屏幕宽高，打开网页的时间，当前时间戳，使用math随机生成一个与时间有关的字符串，Referer，User-Agent 等等，

拼多多策略修改, 列表页及搜索页都需要在请求头中加 'AccessToken': "登录后的 token", 才可以访问!!!
或者 IP 质量较好,直接访问也是可以获取数据的!!!
拼多多对请求的请求头检查比较严格
如图 ，我见过拼多多所有系列都是用的同一套加密方式，有个0a开头。加密是他自己写的一套加密方式，涉及到的加密参数有：鼠标点击位置、href、ua、cookie和时间戳

{
    key: "initRiskController",
        value: function() {
            this.riskControlCrawler || (this.riskControlCrawler = new n.a({
                serverTime: this.serverTime,
                _2827c887a48a351a: !1
            }),
            this.riskControlCrawler.init())
        }
    }
爬虫控制风险,看名字就知道不简单,这里先做了一次初始化,初始化的时候记录了一个serverTime的时间戳,而且以后的每一次下拉页面都有拿时间作比较.等等…

js破解之再战pdd（搜索商品列表页anti_content参数破解）（不是吧，好像历时一天多就凉了？）
2019-07-01 测试发现，单个ip若首次使用示例py代码调用为不成功时，此时使用浏览器访问搜索链接则需要登录，此时用户完成登录，后再使用py示例代码调用则正确返回数据。（猜测ip与用户登录态存在某些权重绑定，欢迎大家测试）（测试环境为本机ip，本机chrome浏览器）
2019-07-05 测试发现，首先用浏览器成功访问一下pdd的搜索，不管是登录也好，滑块也罢，只要浏览器能成功展示页面，此时使用py代码调用亦可成功。（还是猜测ip存在某些权重绑定，需要验证一下）（测试环境为本机ip，本机chrome浏览器）
特殊说明：本人测试同一anti_content有效调用次数为2次，目前ip限制较为严重，但代理不在本文讨论之列，请合理安排策略

嗯，最近跟风在看pdd的那个anti参数，扣代码的各位有没有头大😂。大致看了一下，随便说两句，仿照webpackJsonp打包的方式，去处理模块，保留那个i函数和数组内好像大约19个函数，这样就不用考虑模块间的引用问题，处理下异常就好了，也就是url，cookie和一个浏览器宽高的数值，然后找到目标模块，把目标函数的返回值return出来，也就达到所谓的秒破效果了。

增加浏览器scrollTop和一个timestamp检测，scrollTop就不说了，稍微提一下timestamp，timestamp是触发ajax时的一个Date.now()-J的差值（ps：J的值为js加载的时候记录的一个时间戳也是由Date.now()得到），类似于这样
var st = {};
st['data'] = [
    {"scrollTop": 1.5, "timestamp": 954},
    {"scrollTop": 13.5, "timestamp": 966},
    {"scrollTop": 43.5, "timestamp": 1015},
    {"scrollTop": 174, "timestamp": 1029},
    {"scrollTop": 457.5, "timestamp": 1055}];


参考文章: 
https://zhuanlan.zhihu.com/p/64242695
https://blog.csdn.net/weixin_44472296/article/details/92181707
[Js解密](https://sergiojune.com/2019/04/10/how_to_code/)

