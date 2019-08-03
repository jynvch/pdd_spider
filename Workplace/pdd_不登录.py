"""
不登陆
"""
import os
import time

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
    '_nano_fp': 'Xpdjn0EylpgxX0TblT_Ck2gblydHufJpSZGHsEc7',
    # 'api_uid': 'rBRc111Csa6Kz0pCFMyNAg==',
    'ua': 'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F75.0.3770.142%20Safari%2F537.36',
    'webp': '1',
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'mobile.yangkeduo.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}


def get_anticontent(search_key, cookie_dict, user_agent):
    with open('get_anticontent.js', encoding='utf-8') as f:
        js = f.read()
    ctx = execjs.compile(js)
    # 处理cookie_dict, 转为cookie_arr
    cookie_arr = []
    for key, value in cookie_dict.items():
        cookie_arr.append(' ' + key + '=' + value)
    print('传入js的参数', 'search_key:', search_key)
    print('传入js的参数', 'cookie_arr:', cookie_arr)
    print('传入js的参数', 'user_agent:', user_agent)
    anti_content = ctx.call('getContent', search_key, cookie_arr, user_agent)
    return anti_content


def query_second_page(key, session, req_params):
    headers.update({
        'Accept': '*/*',
        'AccessToken': '',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Referer': 'http://mobile.yangkeduo.com/search_result.html?search_key=' + urllib.parse.quote(key),
        'VerifyAuthToken': 'rKx3sBDN7CtHa3-bn--g_A',
    })
    session.cookies.update(cookies)
    flip_temp = ''
    for page in range(2, 10):
        anti_content = get_anticontent(key, dict(session.cookies), headers['User-Agent'])
        # anti_content = input("请输入anti_content:")
        req_params.update({"anti_content": anti_content})
        req_params['page'] = page
        if page != 2:
            req_params['flip'] = flip_temp
        print('第 {} 页的请求头          '.format(page), req_params)
        url = "http://mobile.yangkeduo.com/proxy/api/search"
        while True:
            try:
                res = session.get(url, headers=headers, params=req_params)
            except Exception as e:
                print('出现异常')
                print(e)
                time.sleep(5)
            else:
                if res.status_code != 200:
                    print(res.status_code, res.json())
                    time.sleep(5)
                else:
                    break

        print('第 {} 页的cookies         '.format(page), res.request.headers['Cookie'])
        print('第 {} 页的状态码和响应体  '.format(page), res.status_code, res.text)
        flip_temp = res.json()['flip']
        # with open('res_json.json', 'a', encoding='GBK') as f:
        #     f.write(res.text)
        #     f.write('\n\n')
        time.sleep(5)


def query_first_page(key):
    session = requests.session()
    url = 'http://mobile.yangkeduo.com/search_result.html?search_key={}'.format(key)
    res = session.get(url, headers=headers)
    tree = html.fromstring(res.text)
    data = json.loads(tree.xpath('//script[@id="__NEXT_DATA__"]/text()')[0])
    req_params, flip = data['props']['pageProps']['data']['ssrListData']['loadSearchResultTracking']['req_params'], \
                       data['props']['pageProps']['data']['ssrListData']['flip']
    req_params = dict(json.loads(req_params), **{"flip": flip, 'pdduid': 0})
    return session, req_params


def query(key):
    session, req_params = query_first_page(key)
    query_second_page(key, session, req_params)


if __name__ == '__main__':
    search_key = "月饼"
    query(search_key)

    # with open('get_anticontent.js', encoding='utf-8') as f:
    #     js = f.read()
    # os.environ['EXECJS_RUNTIME'] = "Node"
    # ctx = execjs.compile(js)
    # anti_content = ctx.call('start')
