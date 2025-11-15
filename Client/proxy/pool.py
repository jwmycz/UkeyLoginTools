from . import ProxyMiddleware
import time,requests
from typing import Optional
from LogRecord.record import logger

class ProxyPool(ProxyMiddleware):
    # 需要根据不同的代理商api重写响应
    def _refresh(self):
        for attempt in range(1, self._max_retry_get + 1):
            try:
                resp = requests.get(self.api_url, timeout=5)
                data = resp.json()
            except Exception as e:
                raise RuntimeError(f"获取代理接口错误: {e}")

            if data.get("code") != 1000 or not data.get("data"):
                raise RuntimeError(f"获取代理失败: {data}")

            ip_info = data["data"][0]
            candidate = f"{ip_info['ip']}:{ip_info['port']}"

            if candidate in self._bad_proxies:
                logger.warning(
                    f"[Proxy] 拿到已失效 IP({candidate})，重试 {attempt}/{self._max_retry_get}"
                )
                time.sleep(1)
                continue
            self._proxy = candidate
            logger.info(f"[Proxy] use {self._proxy}")
            return

        raise RuntimeError("连续获取到不可用代理，放弃")
class CheckProxyPool:
    def __init__(self,apiurl):
        self.Proxy = ProxyPool(apiurl)
        self.proxyip = self.Proxy.as_requests_proxies()
    def checkproxy(self,proxy):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
        }
        try:
            requests.get('https://www.baidu.com/', headers=headers, proxies=proxy,timeout=30)
            logger.debug('[代理生效中]')
            return True
        except Exception as e:
            logger.debug('[代理已失效]')
            return False

    def trueproxy(self):
        """尝试返回可用代理，最多重试6次"""
        for attempt in range(6):
            try:
                if self.checkproxy(self.proxyip):
                    return self.proxyip
                else:
                    logger.info(f"第 {attempt + 1} 次检测失败，代理不可用")
                    logger.info("❌ 当前代理失效，更换新代理中...")
                    self.proxyip = self.Proxy.as_requests_proxies()  # ✅ 获取新代理并继续循环
            except Exception as e:
                logger.error(f"第 {attempt + 1} 次检测发生异常: {e}")
        return None  # 如果都失败

# 不应该直接初始化
try:
    api="http://127.0.0.1"
    check = CheckProxyPool(api)
    trueproxy=check.trueproxy()
except Exception as e:
    trueproxy="http://127.0.0.1"

