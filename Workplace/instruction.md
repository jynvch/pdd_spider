# 拼多多js解密

const getContent = (search_key, cookie_arr, user_agent, _nano_fp, P, F, next_scrollTop_timestamp) => {

### search_key
搜索关键词. e.g. '月饼'

### cookie_arr
传入格式: 
[" _nano_fp=Xpdjn0mqlpdYnqdynT_d6emNmFhxcEOldPDixU_L"]
只需要传入cookie里的_nano_fp即可, 注意_nano_fp前有个空格

### user_agent
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
传入请求头里的user_agent即可

### _nano_fp
"Xpdjn0mqlpdYnqdynT_d6emNmFhxcEOldPDixU_L"
传入cookie里_nano_fp的值

### P
1564808831636
当前时间的时间戳, 13位数字

### F
另一个时间戳, 在P的基础上加20秒, 13位数字

### next_scrollTop_timestamp
这是python实现的next_scrollTop_timestamp参数的值, 其中E是另一个时间戳, 在P的基础上加10秒, 13位数字
P E F 的值不随翻页而改变

def yield_scrollTop_timestamp():
    data = [
        {'scrollTop': 0, 'timestamp': int(time.time() * 1000) - E},
        {'scrollTop': 100, 'timestamp': int(time.time() * 1000) - E},
    ]
    while True:
        yield data
        data = data[-1:]  # 截取最后一个,作为下一次的第一个值
        data.append({'scrollTop': data[0]['scrollTop'] + 3000, 'timestamp': int(time.time() * 1000) - E})

第一次请求 传入下面这个数组即可
[{'scrollTop': 0, 'timestamp': int(time.time() * 1000) - E},
 {'scrollTop': 100, 'timestamp': int(time.time() * 1000) - E}]
 
以后每次请求, 数组第一个值为上一次的最后一个值, 第二个值的scrollTop加3000, timestamp用当前时间戳-E即可


    