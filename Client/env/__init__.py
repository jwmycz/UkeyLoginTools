import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # env/ 目录
ENV_PATH = os.path.join(BASE_DIR, "env.json")

with open(ENV_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)
# 开屏日志
homepageformatted=config.get("homepageformatted",'')
# 更新日志
updataformat=config.get("updataformat",'')
# 内网地址
inneraddress=config.get("inneraddress",'http://127.0.0.1:5000')
# 外网地址
exteraddress=config.get("exteraddress",'http://127.0.0.1:5000')
# 网站
env_hlj=config.get("黑龙江","https://pmos.hl.sgcc.com.cn/#/outNet")
env_jl=config.get("吉林","https://pmos.jl.sgcc.com.cn/#/outNet")
env_ln=config.get("辽宁","https://pmos.ln.sgcc.com.cn/#/outNet")
env_md=config.get("蒙东","https://pmos.md.sgcc.com.cn/#/outNet")
env_shoudu=config.get("首都","https://pmos.bj.sgcc.com.cn/#/outNet")
env_heb=config.get("河北","https://pmos.he.sgcc.com.cn/#/outNet")
env_yb=config.get("冀北","https://pmos.jibei.sgcc.com.cn/")
env_sd=config.get("山东","https://pmos.sd.sgcc.com.cn/#/outNet")
env_sanx=config.get("山西","https://pmos.sx.sgcc.com.cn/#/outNet")
env_tj=config.get("天津","https://pmos.tj.sgcc.com.cn")
env_anh=config.get("安徽","https://pmos.ah.sgcc.com.cn:20080/#/outNet")
env_fj=config.get("福建","https://pmos.fj.sgcc.com.cn/#/outNet")
env_sn=config.get("陕西","https://pmos.sn.sgcc.com.cn/#/outNet")
env_xj=config.get("新疆","https://pmos.xj.sgcc.com.cn:20080")
env_gs=config.get("甘肃","https://pmos.gs.sgcc.com.cn")
env_nx=config.get("宁夏","https://pmos.nx.sgcc.com.cn:10443")
env_hen=config.get("河南","https://pmos.ha.sgcc.com.cn")
env_hb=config.get("湖北","https://newpmos.hb.sgcc.com.cn")
env_hn=config.get("湖南","https://pmos.hn.sgcc.cn/#/outNet")
env_sh=config.get("上海","https://pmos.sh.sgcc.com.cn:20080")