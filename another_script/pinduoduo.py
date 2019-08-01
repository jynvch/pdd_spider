import requests
import re
import execjs
from urllib.request import quote  # py3: from urllib import quote 会失败

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
with open('get_anticontent.js', 'r', encoding='utf-8') as f:
    js = f.read()

key_name = quote('情侣衣服')  # 搜索的关键字
url = 'http://yangkeduo.com/search_result.html?search_key=' + key_name

response = requests.get(url, headers=headers)
list_id = re.search('"listID":"([^"]+)"', response.text).group(1)
flip = re.search('"flip":"([^"]+)"', response.text).group(1)

ctx = execjs.compile(js)
anti_content = ctx.call('get_anti', url)
# 获取下一页
next_url = 'http://apiv3.yangkeduo.com/search?page={0}&size=50&sort=default&requery=0&list_id={1}&q={2}&flip={3}&anti_content={4}&pdduid=0'
# 获取下一页的参数有这几个，其中第一个参数为页数，最后一个参数为加密参数，其他的从搜索页第一页获取，上面代码获取，都是不变的
r = requests.get(next_url.format(2, list_id, key_name, flip, anti_content), headers=headers)
print(r.text)

# 不断获取下一页
# def get_next_page(page, url):
#     ctx = execjs.compile(js)
#     anti_content = ctx.call('get_anti', url)  # 每一页的anti-content 都不一样
#     url = next_url.format(page, list_id, key_name, flip, anti_content)
#     r = requests.get(url, headers=headers)
#     for item in r.json()['items']:
#         print(item)
#
#
# for i in range(2, 11):
#     get_next_page(i, url)
