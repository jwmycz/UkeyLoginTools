import time

import requests
from env import *
from LogRecord.record import logger
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-full-version-list': '"Microsoft Edge";v="141.0.3537.71", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.66"',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
}
def get_allurl(max_retries=3):
    url = f'{env_hb}/px-common-authority/marketMapping/selectByCondition'
    payload = {
        'data': {
            'marketName': '',
            'newMarketCode': '',
            'newUrl': '',
            'oldUrl': '',
        },
        'pageInfo': {
            'pageSize': 100,
            'pageNum': 1,
        },
    }

    for retry in range(1, max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get('data', {}).get('list', [])
                return [{'网站': item['marketName'], '链接': item['newDomainName']} for item in data if
                        item['newDomainName']]
            else:
                logger.warning(f"请求失败，状态码：{resp.status_code}")
        except Exception as e:
            logger.error(f"获取 URL 异常: {e}")


def check_urls():
    start = time.time()
    all_url = get_allurl()
    if len(all_url) > 0:
        allurl = all_url
    else:
        allurl = [{'网站': '吉林', '链接': env_jl},
                  {'网站': '黑龙江', '链接': env_hlj},
                  {'网站': '辽宁', '链接': env_ln},
                  {'网站': '蒙东', '链接': env_md},
                  {'网站': '首都', '链接': env_shoudu},
                  {'网站': '河北', '链接': env_heb},
                  {'网站': '冀北', '链接': env_yb},
                  {'网站': '山东', '链接': env_sd},
                  {'网站': '山西', '链接': env_sanx},
                  {'网站': '天津', '链接': env_tj},
                  {'网站': '安徽', '链接': env_anh},
                  {'网站': '福建', '链接': env_fj},
                  {'网站': '江苏', '链接': 'https://pmos.js.sgcc.com.cn/'},
                  {'网站': '上海', '链接': env_sh},
                  {'网站': '浙江', '链接': 'https://zjpx.com.cn'},
                  {'网站': '湖北', '链接': env_hb},
                  {'网站': '河南', '链接': env_hen},
                  {'网站': '湖南', '链接': env_hn},
                  {'网站': '江西', '链接': 'https://pmos.jx.sgcc.com.cn/#/outNet'},
                  {'网站': '北京', '链接': 'http://pmos.sgcc.com.cn'},
                  {'网站': '甘肃', '链接': env_gs},
                  {'网站': '宁夏', '链接': env_nx},
                  {'网站': '青海', '链接': 'https://pmos.qh.sgcc.com.cn'},
                  {'网站': '陕西', '链接': env_sn},
                  {'网站': '新疆', '链接': env_xj},
                  {'网站': '重庆', '链接': 'https://pmos.cq.sgcc.com.cn/#/outNet'},
                  {'网站': '四川', '链接': 'https://pmos.sc.sgcc.com.cn/'}]
    # print(allurl)
    success, error, noneall, wqy = [], [], [], []

    for site in allurl:
        name = site['网站']
        url = site['链接'].strip()
        try:
            response = requests.get(url, headers=headers, timeout=30, verify=False)
            code = response.status_code
            if code == 200:
                if '$_ts.cd' in response.text:
                    wqy.append(f'{name}省 --> 响应 {code} --> 有瑞数，未启用')
                else:
                    success.append(f'{name}省 --> 响应 {code} --> 无瑞数')
            elif code == 412:
                error.append(f'{name}省 --> 响应 {code} --> 有瑞数')
            else:
                noneall.append(f'{name}省 --> 响应 {code} --> 未知响应')
        except Exception as e:
            noneall.append(f'{name}省 --> 请求异常: {e}')
        time.sleep(1)

    end = time.time()
    usetime = round(end - start, 2)

    msg = [
        f"🔍 瑞数检测完成，用时 {usetime} 秒，共检测 {len(allurl)} 个网站。",
        "",
        f"✅ 正常访问：{len(success)} 个（无瑞数）",
        *([f" - {line}" for line in success] if success else [" - 无"]),
        "",
        f"✅ 正常访问：{len(wqy)} 个（有瑞数，未启用）",
        *([f" - {line}" for line in wqy] if wqy else [" - 无"]),
        "",
        f"⚠️ 异常访问：{len(error)} 个（返回 412 - 有瑞数）",
        *([f" - {line}" for line in error] if error else [" - 无"]),
        "",
        f"❌ 错误或未知响应：{len(noneall)} 个",
        *([f" - {line}" for line in noneall] if noneall else [" - 无"]),
    ]
    return msg