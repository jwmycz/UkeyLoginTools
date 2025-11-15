import requests


def aword():
    cookies = {
        '_gid': 'GA1.2.1000113528.1761041387',
        '_ga_74ZZC03H3M': 'GS2.1.s1761041387$o1$g0$t1761041391$j56$l0$h0',
        '_ga': 'GA1.1.157194141.1761041387',
        '_ga_QL2J611R9Q': 'GS2.1.s1761041394$o1$g1$t1761041610$j60$l0$h0',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    }
    try:
        response = requests.get('https://v1.hitokoto.cn/', cookies=cookies, headers=headers)
        res=response.json()
        hitokoto=res.get('hitokoto','')
        fromdate=res.get('from','')
        yj=f'{hitokoto}--{fromdate}'
        return yj
    except Exception as e:
        return '用代码表达言语的魅力，用代码书写山河的壮丽。'
