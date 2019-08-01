import requests
from lxml import html
import json
import urllib.parse
import execjs

"""
使用基于 Token 的身份验证方法，大概的流程是这样的：
  1. 客户端使用用户名跟密码请求登录 
  2. 服务端收到请求，去验证用户名与密码 
  3. 验证成功后，服务端会签发一个 Token，再把这个 Token 发送给客户端 
  4. 客户端收到 Token 以后可以把它存储起来，比如放在 Cookie 里或者 Local Storage 里 
  5. 客户端每次向服务端请求资源的时候需要带着服务端签发的 Token 
  6. 服务端收到请求，然后去验证客户端请求里面带着的 Token，如果验证成功，就向客户端返回请求的数据

  总的来说就是客户端在首次登陆以后，服务端再次接收http请求的时候，就只认token了，请求只要每次把token带上就行了，
    服务器端会拦截所有的请求，然后校验token的合法性，合法就放行，不合法就返回401（鉴权失败）。
"""
cookies = {
    ' PDDAccessToken': 'TS3PENFODKSZRTJVRK6MJ6INWF6WYXWLV2TDIUVUSQIINQJ5TKGQ102e177',
    ' _nano_fp': 'Xpdjn0Tolp9JnqTqXT_00tbGBlJQr7tqieXhl6_1',
    'api_uid': 'rBQFFF09DZ2SYjQcFPR2Ag==',
    ' goods_detail': 'goods_detail_xvWOXv',
    ' goods_detail_mall': 'goods_detail_mall_Omt5sQ',
    ' msec': '1800000',
    ' pdd_user_id': '4277963319009',
    ' pdd_user_uin': 'BWJHWNDA2V7EQQJNZTBKD7HSLA_GEXDA',
    ' ua': 'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F75.0.3770.142%20Safari%2F537.36',
    ' webp': '1',
}


def get_anticontent(q):  # 只需要传一个 搜索页的 url 即可
    # ctx = execjs.compile(js)
    # anti_content = ctx.call('result', q)
    anti_content = input("输入anti_content: ")
    return anti_content


def query_second_page(session, req_params):
    url = "http://mobile.yangkeduo.com/proxy/api/search"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'AccessToken': 'TS3PENFODKSZRTJVRK6MJ6INWF6WYXWLV2TDIUVUSQIINQJ5TKGQ102e177',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': 'mobile.yangkeduo.com',
        'Referer': 'http://mobile.yangkeduo.com/search_result.html?search_key=' + urllib.parse.quote(req_params['q']),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'VerifyAuthToken': 'c0dZLte5V81nRIainPtbRw',
    }
    flip_temp = ''
    anti_content = get_anticontent(headers['Referer'])
    for page in range(2, 3):
        # print('anti_content', anti_content)
        params = dict(req_params, **{"anti_content": anti_content})
        params['page'] = page
        if page != 2:
            params['flip'] = flip_temp
        print('params', params)
        res = session.get(url, headers=headers, params=params)
        print(res.status_code, res.text)
        flip_temp = res.json()['flip']
        with open('res_json.json', 'a', encoding='GBK') as f:
            f.write(res.text)
            f.write('\n\n')


def query_first_page():
    session = requests.session()
    url = 'http://mobile.yangkeduo.com/search_result.html?search_key=月饼'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'mobile.yangkeduo.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    session.cookies.update(cookies)
    res = session.get(url, headers=headers)
    tree = html.fromstring(res.text)
    # with open('first_page.html', 'w', encoding='utf-8') as f:
    #     f.write(res.text)
    data = json.loads(tree.xpath('//script[@id="__NEXT_DATA__"]/text()')[0])
    req_params, flip = data['props']['pageProps']['data']['ssrListData']['loadSearchResultTracking']['req_params'], \
                       data['props']['pageProps']['data']['ssrListData']['flip']
    req_params = dict(json.loads(req_params), **{"flip": flip})
    query_second_page(session, req_params)


if __name__ == '__main__':
    query_first_page()
    # with open('get_anticontent.js', encoding='utf-8') as f:
    #     js = f.read()
    # ctx = execjs.compile(js)
    # anti_content = ctx.call('start')
