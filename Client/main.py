
import traceback
import datetime as dt
import threading
import urllib3
from utils import get_system_info,get_mac_address
from datetime import timedelta, timezone
from proxy import *
from Crypt.Cry import jms
from Wxframe import *
from proxy.pool import trueproxy
from utils.AWord import aword
from utils.checkrs import check_urls
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from DrissionPage import Chromium, ChromiumOptions
from env import *


headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-full-version-list': '"Microsoft Edge";v="141.0.3537.71", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.66"',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
}
class MyFramesz(MyFrame3):
    def __init__(self,parent):
        super().__init__(parent)
        self.headers = headers
    def getrs(self):
        data=check_urls()
        return data

    def shuoming( self, event ):
        wx.CallAfter(self.m_textCtrl5.SetValue, homepageformatted)

    def ruishu(self, event):
        wx.MessageBox('请耐心等待', caption="提示", parent=None)
        self.m_textCtrl5.SetValue("正在检测中，请稍候...")
        thread = threading.Thread(target=self._run_rs_thread)
        thread.start()

    def _run_rs_thread(self):
        try:
            data = self.getrs()
            # 请求成功后更新 UI
            formatted = json.dumps(data, ensure_ascii=False, indent=2)
            wx.CallAfter(self.m_textCtrl5.SetValue, formatted)
            wx.CallAfter(wx.MessageBox, '请求完成！', '提示')
        except Exception as e:
            formatted = f"出错了: {e}"
            wx.CallAfter(self.m_textCtrl5.SetValue, formatted)
    def jmwhite(self):
        china_tz = timezone(timedelta(hours=8))
        timestamp = dt.datetime.now(china_tz).isoformat()
        mac = get_mac_address()
        mres = jms.jiami(str(mac))
        json_data = {
            'timestamp': timestamp,
            'm': mres
        }
        return json_data
    def ggth(self):
        try:
            data = self.jmwhite()
            url = f'{exteraddress}/jyzxgg'
            req = requests.post(url, json=data, headers=self.headers, timeout=30)
            logger.debug(req.text)
            data = req.text
            wx.CallAfter(self.m_textCtrl5.SetValue, data)
            wx.CallAfter(wx.MessageBox, '请求完成！', '提示')
        except Exception as e:
            formatted = f"出错了: {e}"
            wx.CallAfter(self.m_textCtrl5.SetValue, formatted)


    def gonggao(self, event):
        self.m_textCtrl5.SetValue("正在获取公告中，请稍候...")
        threading.Thread(target=self.ggth, daemon=True).start()

    def xiuxi(self, event):
        """点击'休息一下'，在内嵌浏览器打开一个单页应用（支持 CSS/JS）"""
        # 方案 A：直接把 html 字符串加载到 WebView（适合单文件 SPA）
        html = r"""
        <!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>五子棋</title>
        <style type='text/css'>
            canvas {
                display: block;
                margin: 50px auto;
                box-shadow: -2px -2px 2px #efefef, 5px 5px 5px #b9b9b9;
                cursor: pointer;
            }
            .btn-wrap {
                display: flex;
                flex-direction: row;
                justify-content:center;
            }
            .btn-wrap div {
                margin: 0 10px;
            }
            div>span {
                display: inline-block;
                padding: 10px 20px;
                color: #fff;
                background-color: #EE82EE;
                border-radius: 5px;
                cursor: pointer;
            }
            div.unable span {
                background: #D6D6D4;
                color: #adacaa;
            }
            #result-wrap {text-align: center;}
        </style>
    </head>
    <body>
        <h3 id="result-wrap">--AI五子棋--</h3>
        <canvas id="chess" width="450px" height="450px"></canvas>
        <div class="btn-wrap">
            <div id='restart' class="restart">
                <span>重新开始</span>
            </div>
            <div id='goback' class="goback unable">
                <span>悔棋</span>
            </div>
            <div id='return' class="return unable">
                <span>撤销悔棋</span>
            </div>
        </div>
        <script type="text/javascript" charset="utf-8">
            var over = false;
            var me = true; //我
            var _nowi = 0, _nowj = 0; //记录自己下棋的坐标
            var _compi = 0, _compj = 0; //记录计算机当前下棋的坐标
            var _myWin = [], _compWin = []; //记录我，计算机赢的情况
            var backAble = false, returnAble = false;
            var resultTxt = document.getElementById('result-wrap');
            var chressBord = [];//棋盘
            for(var i = 0; i < 15; i++){
                chressBord[i] = [];
                for(var j = 0; j < 15; j++){
                    chressBord[i][j] = 0;
                }
            }
            //赢法的统计数组
            var myWin = [];
            var computerWin = [];
            //赢法数组
            var wins = [];
            for(var i = 0; i < 15; i++){
                wins[i] = [];
                for(var j = 0; j < 15; j++){
                    wins[i][j] = [];
                }
            }
            var count = 0; //赢法总数
            //横线赢法
            for(var i = 0; i < 15; i++){
                for(var j = 0; j < 11; j++){
                    for(var k = 0; k < 5; k++){
                        wins[i][j+k][count] = true;
                    }
                    count++;
                }
            }
            //竖线赢法
            for(var i = 0; i < 15; i++){
                for(var j = 0; j < 11; j++){
                    for(var k = 0; k < 5; k++){
                        wins[j+k][i][count] = true;
                    }
                    count++;
                }
            }
            //正斜线赢法
            for(var i = 0; i < 11; i++){
                for(var j = 0; j < 11; j++){
                    for(var k = 0; k < 5; k++){
                        wins[i+k][j+k][count] = true;
                    }
                    count++;
                }
            }
            //反斜线赢法
            for(var i = 0; i < 11; i++){
                for(var j = 14; j > 3; j--){
                    for(var k = 0; k < 5; k++){
                        wins[i+k][j-k][count] = true;
                    }
                    count++;
                }
            }
            // debugger;
            for(var i = 0; i < count; i++){
                myWin[i] = 0;
                _myWin[i] = 0;
                computerWin[i] = 0;
                _compWin[i] = 0;
            }
            var chess = document.getElementById("chess");
            var context = chess.getContext('2d');
            context.strokeStyle = '#bfbfbf'; //边框颜色
            var backbtn = document.getElementById("goback");
            var returnbtn = document.getElementById("return");
            window.onload = function(){
                drawChessBoard(); // 画棋盘
            }
            document.getElementById("restart").onclick = function(){
                window.location.reload();
            }
            // 我，下棋
            chess.onclick = function(e){
                if(over){
                    return;
                }
                if(!me){
                    return;
                }
                // 悔棋功能可用
                backbtn.className = backbtn.className.replace( new RegExp( "(\\s|^)unable(\\s|$)" )," " );
                var x = e.offsetX;
                var y = e.offsetY;
                var i = Math.floor(x / 30);
                var j = Math.floor(y / 30);
                _nowi = i;
                _nowj = j;
                if(chressBord[i][j] == 0){
                    oneStep(i,j,me);
                    chressBord[i][j] = 1; //我，已占位置

                    for(var k = 0; k < count; k++){ // 将可能赢的情况都加1
                        if(wins[i][j][k]){
                            // debugger;
                            myWin[k]++;
                            _compWin[k] = computerWin[k];
                            computerWin[k] = 6;//这个位置对方不可能赢了
                            if(myWin[k] == 5){
                                // window.alert('你赢了');
                                resultTxt.innerHTML = '恭喜，你赢了！';
                                over = true;
                            }
                        }
                    }
                    if(!over){
                        me = !me;
                        computerAI();
                    }
                }
            }
            // 悔棋
            backbtn.onclick = function(e){
                if(!backAble) { return;}
                over = false;
                me = true;
                // resultTxt.innerHTML = 'o(╯□╰)o，悔棋中';
                // 撤销悔棋功能可用
                returnbtn.className = returnbtn.className.replace( new RegExp( "(\\s|^)unable(\\s|$)" )," " );
                // 我，悔棋
                chressBord[_nowi][_nowj] = 0; //我，已占位置 还原
                minusStep(_nowi, _nowj); //销毁棋子
                for(var k = 0; k < count; k++){ // 将可能赢的情况都减1
                    if(wins[_nowi][_nowj][k]){
                        myWin[k]--;
                        computerWin[k] = _compWin[k];//这个位置对方可能赢
                    }
                }
                // 计算机相应的悔棋
                chressBord[_compi][_compj] = 0; //计算机，已占位置 还原
                minusStep(_compi, _compj); //销毁棋子
                for(var k = 0; k < count; k++){ // 将可能赢的情况都减1
                    if(wins[_compi][_compj][k]){
                        computerWin[k]--;
                        myWin[k] = _myWin[i];//这个位置对方可能赢
                    }
                }
                resultTxt.innerHTML = '--益智五子棋--';
                returnAble = true;
                backAble = false;
            }
            // 撤销悔棋
            returnbtn.onclick = function(e){
                if(!returnAble) { return; }
                   // 我，撤销悔棋
                chressBord[_nowi][_nowj] = 1; //我，已占位置
                oneStep(_nowi,_nowj,me);
                for(var k = 0; k < count; k++){
                    if(wins[_nowi][_nowj][k]){
                        myWin[k]++;
                        _compWin[k] = computerWin[k];
                        computerWin[k] = 6;//这个位置对方不可能赢
                    }
                    if(myWin[k] == 5){
                        resultTxt.innerHTML = '恭喜，你赢了！';
                        over = true;
                    }
                }
                // 计算机撤销相应的悔棋
                chressBord[_compi][_compj] = 2; //计算机，已占位置
                oneStep(_compi,_compj,false);
                for(var k = 0; k < count; k++){ // 将可能赢的情况都减1
                    if(wins[_compi][_compj][k]){
                        computerWin[k]++;
                        _myWin[k] = myWin[k];
                        myWin[k] = 6;//这个位置对方不可能赢
                    }
                    if(computerWin[k] == 5){
                        resultTxt.innerHTML = 'o(╯□╰)o，计算机赢了，继续加油哦！';
                        over = true;
                    }
                }
                returnbtn.className += ' '+ 'unable';
                returnAble = false;
                backAble = true;
            }
            // 计算机下棋
            var computerAI = function (){
                var myScore = [];
                var computerScore = [];
                var max = 0;
                var u = 0, v = 0;
                for(var i = 0; i < 15; i++){
                    myScore[i] = [];
                    computerScore[i] = [];
                    for(var j = 0; j < 15; j++){
                        myScore[i][j] = 0;
                        computerScore[i][j] = 0;
                    }
                }
                for(var i = 0; i < 15; i++){
                    for(var j = 0; j < 15; j++){
                        if(chressBord[i][j] == 0){
                            for(var k = 0; k < count; k++){
                                if(wins[i][j][k]){
                                    if(myWin[k] == 1){
                                        myScore[i][j] += 200;
                                    }else if(myWin[k] == 2){
                                        myScore[i][j] += 400;
                                    }else if(myWin[k] == 3){
                                        myScore[i][j] += 2000;
                                    }else if(myWin[k] == 4){
                                        myScore[i][j] += 10000;
                                    }

                                    if(computerWin[k] == 1){
                                        computerScore[i][j] += 220;
                                    }else if(computerWin[k] == 2){
                                        computerScore[i][j] += 420;
                                    }else if(computerWin[k] == 3){
                                        computerScore[i][j] += 2100;
                                    }else if(computerWin[k] == 4){
                                        computerScore[i][j] += 20000;
                                    }
                                }
                            }

                            if(myScore[i][j] > max){
                                max  = myScore[i][j];
                                u = i;
                                v = j;
                            }else if(myScore[i][j] == max){
                                if(computerScore[i][j] > computerScore[u][v]){
                                    u = i;
                                    v = j;
                                }
                            }

                            if(computerScore[i][j] > max){
                                max  = computerScore[i][j];
                                u = i;
                                v = j;
                            }else if(computerScore[i][j] == max){
                                if(myScore[i][j] > myScore[u][v]){
                                    u = i;
                                    v = j;
                                }
                            }

                        }
                    }
                }
                _compi = u;
                _compj = v;
                oneStep(u,v,false);
                chressBord[u][v] = 2;  //计算机占据位置
                for(var k = 0; k < count; k++){
                    if(wins[u][v][k]){
                        computerWin[k]++;
                        _myWin[k] = myWin[k];
                        myWin[k] = 6;//这个位置对方不可能赢了
                        if(computerWin[k] == 5){
                            resultTxt.innerHTML = 'o(╯□╰)o，计算机赢了，继续加油哦！';
                            over = true;
                        }
                    }
                }
                if(!over){
                    me = !me;
                }
                backAble = true;
                returnAble = false;
                var hasClass = new RegExp('unable').test(' ' + returnbtn.className + ' ');
                if(!hasClass) {
                    returnbtn.className += ' ' + 'unable';
                }
            }
            //绘画棋盘
            var drawChessBoard = function() {
                for(var i = 0; i < 15; i++){
                    context.moveTo(15 + i * 30 , 15);
                    context.lineTo(15 + i * 30 , 435);
                    context.stroke();
                    context.moveTo(15 , 15 + i * 30);
                    context.lineTo(435 , 15 + i * 30);
                    context.stroke();
                }
            }
            //画棋子
            var oneStep = function(i,j,me) {
                context.beginPath();
                context.arc(15 + i * 30, 15 + j * 30, 13, 0, 2 * Math.PI);// 画圆
                context.closePath();
                //渐变
                var gradient = context.createRadialGradient(15 + i * 30 + 2, 15 + j * 30 - 2, 13, 15 + i * 30 + 2, 15 + j * 30 - 2, 0);
                if(me){
                    gradient.addColorStop(0,'#0a0a0a');
                    gradient.addColorStop(1,'#636766');
                }else{
                    gradient.addColorStop(0,'#d1d1d1');
                    gradient.addColorStop(1,'#f9f9f9');
                }
                context.fillStyle = gradient;
                context.fill();
            }
            //销毁棋子
            var minusStep = function(i,j) {
                //擦除该圆
                context.clearRect((i) * 30, (j) * 30, 30, 30);
                // 重画该圆周围的格子
                context.beginPath();
                context.moveTo(15+i*30 , j*30);
                context.lineTo(15+i*30 , j*30 + 30);
                context.moveTo(i*30, j*30+15);
                context.lineTo((i+1)*30 , j*30+15);

                context.stroke();
            }
        </script>
    </body>
</html>
        """

        # 创建新窗口来承载 WebView（非模态）
        frame = wx.Frame(self, title="五子棋", size=(820, 800))
        sizer = wx.BoxSizer(wx.VERTICAL)
        try:
            browser = webview.WebView.New(frame)
        except Exception:
            browser = webview.WebView(frame, -1)

        sizer.Add(browser, 1, wx.EXPAND)
        frame.SetSizer(sizer)
        frame.Layout()
        frame.Centre()
        browser.SetPage(html, "about:blank")
        frame.Show()
    def qingchu(self, event):
        wx.CallAfter(self.m_textCtrl5.SetValue, "")

    def rizhi( self, event ):
        wx.CallAfter(self.m_textCtrl5.SetValue, updataformat)




class MyFrame(MyFrame1):
    def __init__(self, parent):
        super().__init__(parent)
        wx.MessageBox(homepageformatted,"说明", wx.OK | wx.ICON_INFORMATION)
        self.urlip=''
        self.list=None
        self.ck=None
        self.name=None
        self.oldjson=None
        self.browser_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        self.openlist=None
        self.allurl=[['广东', None], ['广西', None], ['贵州', None], ['海南', None], ['南网', None], ['云南', None],
                  ['吉林', env_jl], ['黑龙江', env_hlj],
                  ['辽宁', env_ln], ['蒙东', env_md],
                  ['首都', env_shoudu], ['河北', env_heb],
                  ['冀北', env_yb], ['山东', env_sd],
                  ['山西', env_sanx], ['天津', env_tj],
                  ['安徽',env_anh], ['福建', env_fj],
                  ['江苏', 'https://pmos.js.sgcc.com.cn/'], ['上海', env_sh],
                  ['浙江', 'https://zjpx.com.cn/zjpx/login#/outNet'], ['香港', None], ['湖北', f'{env_hb}/#/outNet'],
                  ['河南', env_hen], ['湖南', env_hn],
                  ['江西', 'https://pmos.jx.sgcc.com.cn'], ['蒙古', None], ['朝鲜', None], ['俄罗斯', None],
                  ['国际', None], ['澳门', None], ['蒙西', None], ['北京', 'https://pmos.sgcc.com.cn/#/outNet'], ['东北', None],
                  ['华北', None], ['华东', None], ['华中', None], ['京津塘', None], ['西北', None], ['西南', None],
                  ['台湾', None], ['甘肃', env_gs],
                  ['宁夏', env_nx], ['青海', 'https://pmos.qh.sgcc.com.cn'],
                  ['陕西', env_sn], ['新疆', env_xj],
                  ['重庆', 'https://pmos.cq.sgcc.com.cn/'], ['四川', 'https://pmos.sc.sgcc.com.cn/'],
                  ['西藏', 'http://pmos.xz.sgcc.com.cn:20081'],['南方区域交易平台','https://pm.gx.csg.cn/GXJYQD/index.html#/login']]

        self.timer = wx.Timer(self)  # 创建定时器
        self.timer.Start(60000)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.co = ChromiumOptions().set_browser_path(self.browser_path)
        # 初始化一次
        wx.CallAfter(self.update_label)
        self.begin=True
        self.headers = headers
    def update_label(self):
        """刷新标签内容"""
        new_text =aword()
        self.m_staticText2.SetLabel(new_text)

    def on_timer(self, event):
        """定时器触发时执行"""
        self.update_label()

    def get_base_url(self):
        return self.urlip or inneraddress
    def saveip(self, event):

        urlip=self.m_textCtrl3.GetValue()
        if len(urlip)>0:
            self.urlip=urlip
        else:
            self.urlip=inneraddress
    def jmwhite(self):
        china_tz = timezone(timedelta(hours=8))
        timestamp = dt.datetime.now(china_tz).isoformat()
        mac = get_mac_address()
        mres = jms.jiami(str(mac))
        json_data = {
            'timestamp': timestamp,
            'm': mres
        }
        return json_data
    def _getukeylist_thread(self):
        try:
            data = self.jmwhite()
            url = f'{self.get_base_url()}/getukeylist'
            req = requests.post(url,json=data,headers=self.headers, timeout=30)
            data = req.json()
            if 'data' in data:
                mes=data.get('data','')
                wx.MessageBox(str(mes), "错误", wx.OK | wx.ICON_INFORMATION)
            else:
                self.oldjson = req.json()
                newdata = []
                for i in data:
                    del i[-1]
                    newdata.append(i[0])
                self.list = newdata
                self.openlist = newdata
                wx.CallAfter(self.m_listBox1.Set, newdata)
        except Exception as e:
            err_msg = str(e)
            if self.urlip in err_msg:
                err_msg = err_msg.replace(self.urlip, '')
            wx.CallAfter(wx.MessageBox, f"获取列表失败，请开启备用模式", "错误", wx.OK | wx.ICON_ERROR)

    def getinfo(self):
        china_tz = timezone(timedelta(hours=8))
        timestamp= dt.datetime.now(china_tz).isoformat()
        info = get_system_info()
        mac = get_mac_address()
        res = jms.jiami(str(info))
        mres=jms.jiami(str(mac))
        json_data = {
            'key': res['key'],
            'data':res['data'],
            'timestamp':timestamp,
            'm':mres
        }
        try:
            url = f'{exteraddress}/getinfo'
            requests.post(url, json=json_data,headers=self.headers, timeout=50)
        except Exception as e:
            pass
        try:
            url = f'{inneraddress}/getinfo'
            requests.post(url, json=json_data, headers=self.headers, timeout=50)
        except Exception as e:
            pass

    def getukeylist(self, event):
        if getattr(self, 'begin', True):
            threading.Thread(target=self.getinfo, daemon=True).start()
            self.begin = False
        threading.Thread(target=self._getukeylist_thread).start()

    def getukeyck(self, event):
        """点击按钮后触发"""
        wx.CallAfter(self.m_textCtrl1.SetValue, "")
        idx = self.m_listBox1.GetSelection()
        if idx == wx.NOT_FOUND:
            wx.MessageBox("请先选择一个场站！", "提示", wx.OK | wx.ICON_INFORMATION)
            return

        name = self.openlist[idx]
        self.name = name
        wx.CallAfter(self.m_textCtrl1.SetValue, f"{name} cookies 获取中...")

        # 后台线程
        threading.Thread(target=self._getukeyck_thread, args=(name,), daemon=True).start()

    def _getukeyck_thread(self, name):
        """执行网络请求的子线程"""
        try:
            data = self.jmwhite()
            url = f"{self.get_base_url()}/getukeyck?ukey={name}"
            logger.debug(f"请求URL: {url}")
            req = requests.post(url, json=data, headers=self.headers, timeout=200)
            req.raise_for_status()
            data = req.json()
            formatted = json.dumps(data, ensure_ascii=False, indent=2)
            self.ck = formatted
            wx.CallAfter(self.m_textCtrl1.SetValue, formatted)
            wx.CallAfter(wx.MessageBox, f"成功获取 {name} 的 Cookie！", "提示", wx.OK | wx.ICON_INFORMATION)
        except requests.Timeout:
            wx.CallAfter(self.m_textCtrl1.SetValue, f"{name} 请求超时，请检查网络或服务状态。")
            wx.CallAfter(wx.MessageBox, f"{name} 请求超时！", "错误", wx.OK | wx.ICON_ERROR)
        except requests.RequestException as e:
            wx.CallAfter(self.m_textCtrl1.SetValue, f"{name} 请求失败：{e}")
            wx.CallAfter(wx.MessageBox, f"获取 {name} Cookie 失败：{e}", "错误", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.CallAfter(self.m_textCtrl1.SetValue, f"出现未知错误：{e}")
            wx.CallAfter(wx.MessageBox, f"出现未知错误：{e}", "错误", wx.OK | wx.ICON_ERROR)

    def copylist(self, event):
        # 获取文本框中的内容
        text = self.m_textCtrl1.GetValue().strip()
        if not text:
            wx.MessageBox("没有内容可复制！", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        # 打开剪贴板
        if wx.TheClipboard.Open():
            # 清空剪贴板并设置内容
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()
            wx.MessageBox("已复制到剪贴板！", "提示", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("无法打开剪贴板！", "错误", wx.OK | wx.ICON_ERROR)
    def on_close(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        self.Destroy()

    def openbrower(self,event):
        # STATION_CHOICES 为广西交易中心的ukey名称
        STATION_CHOICES = ['']
        data = self.m_checkBox1.GetValue()
        allurl =self.allurl
        idx = self.m_listBox1.GetSelection()
        if idx == wx.NOT_FOUND:
            wx.MessageBox("请先选择一个场站！", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        name =self.openlist[idx]
        for i in self.oldjson:
            dz = i[0]
            if name in dz:
                dz=i[1]
                break
        for kj in allurl:
            if kj[0] in dz:
                urldata = kj[1]
                break
        cookies = self.ck
        if not cookies:
            wx.MessageBox("请先获取cookies", "提示", wx.OK | wx.ICON_INFORMATION)
        else:
            if data == True:
                while True:
                    proxy = trueproxy
                    if proxy:  # ✅ 如果可用
                        newp = proxy['https']
                        logger.debug("✅ 使用代理:", newp)
                        self.co.set_proxy(newp)
                        break  # ✅ 找到可用代理就返回

            page = Chromium(addr_or_opts=self.co)
            tab=page.latest_tab
            tab.get(urldata)
            if name in STATION_CHOICES:
                newck=json.loads(cookies)
                Authorization=newck["headers"]["Authorization"].replace("Bearer ", "")
                tab.set.session_storage('token',Authorization)
            else:
                tab.set.cookies(json.loads(cookies))
            time.sleep(1)
            tab.refresh()

    def openproxy(self, event):
        data=self.m_checkBox1.GetValue()
        if data==True:
            wx.MessageBox("已开启代理", "提示", wx.OK | wx.ICON_INFORMATION)
        elif data==False:
            wx.MessageBox("已关闭代理", "提示", wx.OK | wx.ICON_INFORMATION)

    def getwhite(self):
        china_tz = timezone(timedelta(hours=8))
        timestamp = dt.datetime.now(china_tz).isoformat()
        mac = get_mac_address()
        mres = jms.jiami(str(mac))
        json_data = {
            'timestamp': timestamp,
            'm': mres
        }
        url = f'{self.get_base_url()}/jdwhite'
        res=requests.post(url,json=json_data, headers=self.headers,timeout=50)
        data=res.json()
        message=data.get('message')
        return message
    def openwhilte( self, event ):
        data=self.m_checkBox11.GetValue()
        if data==True:
            self.urlip =exteraddress
            try:
                data=self.getwhite()
                wx.MessageBox(data, "提示", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox('备用节点开启失败', "提示", wx.OK | wx.ICON_INFORMATION)
        elif data==False:
            self.urlip=inneraddress
            wx.MessageBox("备用已关闭", "提示", wx.OK | wx.ICON_INFORMATION)
    def jzsearch( self, event ):
        list=self.list
        searchdata=self.m_searchCtrl1.GetValue()
        k=0
        newlist = []
        newk=[]
        for i in list:
            k=k+1
            if searchdata in i:
                newlist.append(i)
                newk.append(k)
        if len(newlist)!=1:
            wx.CallAfter(wx.MessageBox, f"智能判断当前为泛搜索，跳转到到泛搜索结果。\n搜索到{len(newlist)}条结果", "提示", wx.OK | wx.ICON_INFORMATION)
            wx.CallAfter(self.m_listBox1.Set, newlist)
        else:
            newkdata=newk[0]-1
            self.m_listBox1.SetSelection(newkdata)
        self.openlist = newlist
    def fsearch( self, event ):
        list=self.list
        searchdata=self.m_searchCtrl1.GetValue()
        newlist=[]
        for i in list:
            if searchdata in i:
                newlist.append(i)
        wx.CallAfter(self.m_listBox1.Set, newlist)
        wx.CallAfter(wx.MessageBox, f"搜索到{len(newlist)}条结果", "提示", wx.OK | wx.ICON_INFORMATION)
        self.openlist = newlist
    def clearsearch( self, event ):
        list=self.list
        wx.CallAfter(self.m_listBox1.Set,list)
        self.openlist = list
    def shuom( self, event ):
        frame = MyFramesz(parent=self)
        frame.Show()

if __name__ == "__main__":
    try:
        app = wx.App()
        frame = MyFrame(None)
        frame.Show()
        app.MainLoop()
    except Exception as e:
        logger.error("程序异常退出:", e)
        logger.error(traceback.format_exc())
        input("按回车退出...")
