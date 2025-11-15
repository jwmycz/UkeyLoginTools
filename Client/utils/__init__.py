"""
get_system_info.py

用途：采集当前电脑的大量信息（系统、CPU、内存、磁盘、网络、用户、GPU……）
注意：需要 psutil，其他库可选以获取更详细信息。
"""
from datetime import datetime, timedelta, timezone
import platform
import re
import socket
import uuid
import getpass
import os
import time
import shutil
import subprocess

# 第三方库（非必须，但建议安装）
try:
    import psutil
except Exception:
    psutil = None

try:
    import cpuinfo  # py-cpuinfo
except Exception:
    cpuinfo = None

try:
    import GPUtil  # GPU 信息
except Exception:
    GPUtil = None

# Windows 专用更深信息（可选）
try:
    import wmi  # 仅 Windows，下同
except Exception:
    wmi = None


def _safe_run(cmd):
    """安全运行命令并返回 stdout（用于获取一些系统命令信息），失败返回 None。"""
    try:
        res = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True, encoding='utf-8')
        return res.strip()
    except Exception:
        return None


def bytes2human(n):
    """把字节数转成人可读格式（简易）"""
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i * 10)
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return "%s B" % n


def get_system_info():
    info = {}
    # -------------------------
    # 基本信息
    # -------------------------
    from datetime import datetime, timezone, timedelta
    import platform, socket, getpass, os, uuid

    china_tz = timezone(timedelta(hours=8))
    info['timestamp'] = datetime.now(china_tz).isoformat()
    info['platform'] = platform.system()
    info['platform_release'] = platform.release()
    info['platform_version'] = platform.version()
    info['architecture'] = platform.machine()
    info['hostname'] = socket.gethostname()
    try:
        info['fqdn'] = socket.getfqdn()
    except:
        info['fqdn'] = None
    info['current_user'] = getpass.getuser()
    info['login_shell'] = os.environ.get('SHELL') or os.environ.get('COMSPEC')
    info['machine_uuid'] = str(uuid.getnode())
    # -------------------------
    # 网络接口
    # -------------------------
    net_if_addrs = {}
    if psutil:
        for ifname, addrs in psutil.net_if_addrs().items():
            net_if_addrs[ifname] = []
            for a in addrs:
                net_if_addrs[ifname].append({
                    'family': str(a.family),
                    'address': a.address,
                    'netmask': a.netmask
                })
    info['network_interfaces'] = net_if_addrs

    # -------------------------
    # 磁盘信息
    # -------------------------
    disks = []
    if psutil:
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    'device': part.device,
                    'mountpoint': part.mountpoint,
                    'fstype': part.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except:
                pass
    info['disks'] = disks

    return info

def get_mac_address():
    # 执行命令并获取输出
    data = subprocess.check_output(
        'wmic nic where "NetEnabled=true" get Name,MACAddress',
        shell=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    # 用正则提取 MAC 地址
    macs = re.findall(r'([0-9A-F]{2}(?::[0-9A-F]{2}){5})', data, re.I)

    if macs:
        return macs[0]  # 取第一个
    return None
# def get_mac_address():
#     mac_int = uuid.getnode()
#     mac_str = ':'.join(f'{(mac_int >> ele) & 0xff:02X}' for ele in range(40, -8, -8))
#     return mac_str
# 简单示例：打印 JSON 样式的输出（你可以把返回值转成 JSON 存文件或通过 API 返回）
if __name__ == '__main__':
    # pip install psutil py-cpuinfo GPUtil wmi
    import json
    info = get_system_info()
    # print(info)
    print(json.dumps(info, indent=2, ensure_ascii=False))
