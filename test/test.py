import requests

def ck(payload):
    url = "http://111.229.124.162:9897/getck"

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    result = response.json()
    print(result)
    cookies = result.get("cookies", [])
    allcookies = {}
    for cookie in cookies:
        name = cookie.get("name")
        value = cookie.get("value")
        allcookies[name] = value

    api_url = result.get("intercepted_url")
    return {'url': api_url, 'cookies': allcookies}
def test(payload):
    cook = ck(payload)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'ClientTag': 'OUTNET_BROWSE',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'CurrentRoute': '/outNet',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0',
        'X-Ticket': 'undefined',
        'X-Token': 'null',
        'sec-ch-ua': '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    cookies = cook['cookies']

    local_session = requests.Session()
    local_session.cookies.clear()
    local_session.cookies.update(cookies)
    local_session.headers.clear()
    local_session.headers.update(headers)
    jsurl = cook['url']


    json_data = {
        'captchaType': 'blockPuzzle',
        'pointJson': 'U16hhLjxV2fnRlXxr3CbZOHiTbxwsYZZ0+j1fkGlYHs=',
        'token': '05fac46c0873471baddfac0e688029d9',
    }
    print(f'请求url-->{jsurl}')
    response = local_session.post(
        jsurl,
        json=json_data,
    )
    print(response.text)
if __name__ == '__main__':
    # 安徽
    # payload = {"name":"ah","url":"https://pmos.ah.sgcc.com.cn:20080/px-common-authcenter/auth/v2/captcha/check"}
    # 新疆
    # payload = {"name": "xj", "url": "https://pmos.xj.sgcc.com.cn:20080/px-common-authcenter/auth/v2/captcha/check"}
    # 福建
    payload = {"name": "fj", "url": "https://pmos.fj.sgcc.com.cn/px-common-authcenter/auth/v2/captcha/check"}
    # 宁夏
    # payload = {"name": "nx", "url": "https://pmos.nx.sgcc.com.cn:10443/px-common-authcenter/auth/v2/captcha/check"}
    # 河南
    # payload = {"name": "henan", "url": "https://pmos.ha.sgcc.com.cn/px-common-authcenter/auth/v2/captcha/check"}
    # 广西 废弃
    # payload = {"name": "nfgx", "url": "/GXJYHD/qctc_pm_mh/mh/mhIndex/getCenterIntroduceVld"}
    # 广东
    # payload = {"name": "nfgd", "url": "/portal/xhr/sso-company/protocol/detail/serviceAgreement"}   #get
    test(payload)