
import time, requests
from typing import Optional
from LogRecord.record import logger


class ProxyMiddleware:

    def __init__(self, api_url: Optional[str] = None, max_retry_get: int = 5):
        self.api_url = api_url
        self._proxy: Optional[str] = None           # 当前可用的 ip:port 字符串
        self._bad_proxies: set[str] = set()         # 已判定不可用的 ip:port
        self._max_retry_get = max_retry_get         # 连续取 IP 的最大尝试次数

    def as_requests_proxies(self) -> dict:

        p = self._get_proxy()
        return {"http": f"http://{p}", "https": f"http://{p}"}

    def mark_bad(self):
        if self._proxy:
            self._bad_proxies.add(self._proxy)
            logger.info(f"[Proxy] mark bad → {self._proxy}")
            self._proxy = None

    def _get_proxy(self) -> str:

        if self._proxy is None:
            self._refresh()
        return self._proxy

    def _refresh(self):
        for attempt in range(1, self._max_retry_get + 1):
            try:
                resp = requests.get(self.api_url, timeout=5)
                data = resp.json()
            except Exception as e:
                raise RuntimeError(f"获取代理接口错误: {e}")

            if data.get("code") != 1000 or not data.get("data"):
                raise RuntimeError(f"获取代理失败: {data}")

            ip_info   = data["data"][0]
            candidate = f"{ip_info['ip']}:{ip_info['port']}"

            if candidate in self._bad_proxies:          # 拒绝已失效 IP
                logger.warning(
                    f"[Proxy] 拿到已失效 IP({candidate})，重试 {attempt}/{self._max_retry_get}"
                )
                time.sleep(1)
                continue

            self._proxy = candidate
            logger.info(f"[Proxy] use {self._proxy}")
            return

        raise RuntimeError("连续获取到不可用代理，放弃")

# ===================== demo =====================
if __name__ == "__main__":
    proxy = ProxyMiddleware()
    ppp=proxy.as_requests_proxies()
    print(ppp)
    print(type(ppp))# {'http': 'http://IP:port', 'https': 'http://IP:port'}
    # print(proxy._refresh())         # {'http': 'http://IP:port', 'https': 'http://IP:port'}

