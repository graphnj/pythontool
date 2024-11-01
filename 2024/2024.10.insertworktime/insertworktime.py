import time

import requests
import json

# 定义请求的URL
url = 'https://pmsystem.cestc.cn/gsgl/gsApply/insertGsPCList'

# 要发送的JSON数据
data = [
    {"xmId": "YF202403150001",
     "gslx": "YF",
     "sbgs": 8,
     "sbrq": "2024-10-16",
     "gznr": "助手事件录入研发",
     "tbCxdm": "0",
     "sfbt": "Y",
     "id": None}]

cookie="token=09fd2c9e5ee44133be74839373e65b64!3543d00e9c544cadaa473105a9ff9153; cestcToken=070d079b44984302b19c53148014025f; route=1bd6bc481ca6f48caafcd8d7251f277c|1730090229|1730089653"
token="09fd2c9e5ee44133be74839373e65b64!3543d00e9c544cadaa473105a9ff9153"
# 请求头（Header），包含Token和Cookie
headers = {
"Accept": "application/json, text/plain, */*",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cache-Control": "no-cache",
"Connection": "keep-alive",
"Content-Length": "136",
"Content-Type": "application/json;charset=UTF-8",
"Cookie": cookie,
"token": token,
"Host": "pmsystem.cestc.cn",
"Origin": "https://pmsystem.cestc.cn",
"Pragma": "no-cache",
"Referer": "https://pmsystem.cestc.cn/app-vue/workingHourManage/workingHours/filling",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
"sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "macOS",

}

for i in [17,18,21,22,23,24,25]:
    data[0]['sbrq']=f'2024-10-{i}'
    print(data[0]['sbrq'])
    time.sleep(5)
    # 发送POST请求
    response = requests.post(url, json=data, headers=headers)

    # 打印响应的状态码
    print(f'Status code: {response.status_code}')

    # 如果响应状态码为200，打印响应体
    if response.status_code == 200:
        print('Response JSON:')
        print(response.json())
    else:
        print(f'Request failed with status code {response.status_code}.')