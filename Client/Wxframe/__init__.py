import wx
import wx.xrc
import wx.html
import wx.html2 as webview
import gettext
from env import *
_ = gettext.gettext

class MyFrame1 ( wx.Frame ):

	def __init__(self, parent):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = _(u"ukey生成器 v3.0"), pos = wx.DefaultPosition, size = wx.Size( 969,710 ), style = wx.DEFAULT_FRAME_STYLE|wx.BORDER_DEFAULT|wx.BORDER_SIMPLE|wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		self.SetForegroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ))
		self.SetBackgroundColour(wx.Colour( 181, 219, 164 ))

		bSizer2 = wx.BoxSizer(wx.VERTICAL)

		bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, _(u"服务器IP地址"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText1.Wrap(-1)

		bSizer6.Add(self.m_staticText1, 0, wx.ALL, 5)

		self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, _(u"http://192.168.100.125:5000"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer6.Add(self.m_textCtrl3, 1, wx.ALL, 5)

		self.m_button2 = wx.Button(self, wx.ID_ANY, _(u"保存"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer6.Add(self.m_button2, 0, wx.ALL, 5)

		self.m_checkBox1 = wx.CheckBox(self, wx.ID_ANY, _(u"浏览器代理"), wx.Point( -1,-1 ), wx.DefaultSize, 0)
		bSizer6.Add(self.m_checkBox1, 0, wx.ALL, 5)

		self.m_checkBox11 = wx.CheckBox(self, wx.ID_ANY, _(u"备用节点"), wx.Point( -1,-1 ), wx.DefaultSize, 0)
		bSizer6.Add(self.m_checkBox11, 0, wx.ALL, 5)


		bSizer2.Add(bSizer6, 0, wx.EXPAND, 5)

		bSizer61 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_searchCtrl1 = wx.SearchCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_searchCtrl1.ShowSearchButton(False)
		self.m_searchCtrl1.ShowCancelButton(True)
		bSizer61.Add(self.m_searchCtrl1, 1, wx.ALL, 5)

		self.m_button7 = wx.Button(self, wx.ID_ANY, _(u"泛搜索"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer61.Add(self.m_button7, 0, wx.ALL, 5)

		self.m_button8 = wx.Button(self, wx.ID_ANY, _(u"精准搜索"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer61.Add(self.m_button8, 0, wx.ALL, 5)

		self.m_button9 = wx.Button(self, wx.ID_ANY, _(u"清除搜索结果"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer61.Add(self.m_button9, 0, wx.ALL, 5)

		self.m_button10 = wx.Button(self, wx.ID_ANY, _(u"工具"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer61.Add(self.m_button10, 0, wx.ALL, 5)


		bSizer2.Add(bSizer61, 0, wx.EXPAND, 5)

		bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_button1 = wx.Button(self, wx.ID_ANY, _(u"获取ukey列表"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer3.Add(self.m_button1, 1, wx.ALL, 5)

		self.m_button4 = wx.Button(self, wx.ID_ANY, _(u"获取cookies"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer3.Add(self.m_button4, 1, wx.ALL, 5)

		self.m_button6 = wx.Button(self, wx.ID_ANY, _(u"复制"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer3.Add(self.m_button6, 1, wx.ALL, 5)

		self.m_button61 = wx.Button(self, wx.ID_ANY, _(u"打开浏览器"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer3.Add(self.m_button61, 1, wx.ALL, 5)


		bSizer2.Add(bSizer3, 0, wx.EXPAND, 5)

		self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		bSizer2.Add(self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5)

		bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

		m_listBox1Choices = []
		self.m_listBox1 = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox1Choices, 0)
		bSizer4.Add(self.m_listBox1, 1, wx.ALL|wx.EXPAND, 5)

		self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_RICH)
		bSizer4.Add(self.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5)


		bSizer2.Add(bSizer4, 1, wx.EXPAND, 5)

		bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)
		self.m_staticText2.Wrap(-1)

		bSizer9.Add(self.m_staticText2, 1, wx.ALL, 5)


		bSizer2.Add(bSizer9, 0, wx.EXPAND, 5)


		self.SetSizer( bSizer2 )
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.m_button2.Bind(wx.EVT_BUTTON, self.saveip)
		self.m_checkBox1.Bind(wx.EVT_CHECKBOX, self.openproxy)
		self.m_checkBox11.Bind(wx.EVT_CHECKBOX, self.openwhilte)
		self.m_button7.Bind(wx.EVT_BUTTON, self.fsearch)
		self.m_button8.Bind(wx.EVT_BUTTON, self.jzsearch)
		self.m_button9.Bind(wx.EVT_BUTTON, self.clearsearch)
		self.m_button10.Bind(wx.EVT_BUTTON, self.shuom)
		self.m_button1.Bind(wx.EVT_BUTTON, self.getukeylist)
		self.m_button4.Bind(wx.EVT_BUTTON, self.getukeyck)
		self.m_button6.Bind(wx.EVT_BUTTON, self.copylist)
		self.m_button61.Bind(wx.EVT_BUTTON, self.openbrower)

	def __del__( self ):
		# Disconnect Events
		self.m_button2.Unbind(wx.EVT_BUTTON, None)
		self.m_checkBox1.Unbind(wx.EVT_CHECKBOX, None)
		self.m_checkBox11.Unbind(wx.EVT_CHECKBOX, None)
		self.m_button7.Unbind(wx.EVT_BUTTON, None)
		self.m_button8.Unbind(wx.EVT_BUTTON, None)
		self.m_button9.Unbind(wx.EVT_BUTTON, None)
		self.m_button10.Unbind(wx.EVT_BUTTON, None)
		self.m_button1.Unbind(wx.EVT_BUTTON, None)
		self.m_button4.Unbind(wx.EVT_BUTTON, None)
		self.m_button6.Unbind(wx.EVT_BUTTON, None)
		self.m_button61.Unbind(wx.EVT_BUTTON, None)


	# Virtual event handlers, overide them in your derived class
	def saveip( self, event ):
		event.Skip()

	def openproxy( self, event ):
		event.Skip()

	def openwhilte( self, event ):
		event.Skip()

	def fsearch( self, event ):
		event.Skip()

	def jzsearch( self, event ):
		event.Skip()

	def clearsearch( self, event ):
		event.Skip()

	def shuom( self, event ):
		event.Skip()

	def getukeylist( self, event ):
		event.Skip()

	def getukeyck( self, event ):
		event.Skip()

	def copylist( self, event ):
		event.Skip()

	def openbrower( self, event ):
		event.Skip()



class MyFrame3 ( wx.Frame ):

	def __init__(self, parent):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = _(u"工具列表"), pos = wx.DefaultPosition, size = wx.Size( 641,582 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		self.SetBackgroundColour(wx.Colour( 181, 219, 164 ))

		bSizer10 = wx.BoxSizer(wx.VERTICAL)

		bSizer17 = wx.BoxSizer(wx.HORIZONTAL)

		bSizer18 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticline7 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		bSizer18.Add(self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5)

		bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_button15 = wx.Button(self, wx.ID_ANY, _(u"交易中心瑞数检测"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer20.Add(self.m_button15, 1, wx.ALL, 5)

		self.m_button16 = wx.Button(self, wx.ID_ANY, _(u"交易中心公告获取"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer20.Add(self.m_button16, 1, wx.ALL, 5)


		bSizer18.Add(bSizer20, 0, wx.EXPAND, 5)

		self.m_staticline8 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		bSizer18.Add(self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5)

		bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_button18 = wx.Button(self, wx.ID_ANY, _(u"休息一下"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer21.Add(self.m_button18, 1, wx.ALL, 5)

		self.m_button19 = wx.Button(self, wx.ID_ANY, _(u"说明"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer21.Add(self.m_button19, 1, wx.ALL, 5)


		bSizer18.Add(bSizer21, 0, wx.EXPAND, 5)

		self.m_staticline9 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		bSizer18.Add(self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5)

		bSizer22 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_button20 = wx.Button(self, wx.ID_ANY, _(u"清除"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer22.Add(self.m_button20, 1, wx.ALL, 5)

		self.m_button201 = wx.Button(self, wx.ID_ANY, _(u"更新日志"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer22.Add(self.m_button201, 1, wx.ALL, 5)


		bSizer18.Add(bSizer22, 0, wx.EXPAND, 5)

		self.m_staticline10 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		bSizer18.Add(self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5)


		bSizer17.Add(bSizer18, 1, wx.EXPAND, 5)

		bSizer19 = wx.BoxSizer(wx.VERTICAL)

		self.m_textCtrl5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_RICH)
		bSizer19.Add(self.m_textCtrl5, 1, wx.ALL|wx.EXPAND, 5)


		bSizer17.Add(bSizer19, 1, wx.EXPAND, 5)


		bSizer10.Add(bSizer17, 1, wx.EXPAND, 5)


		self.SetSizer( bSizer10 )
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.m_button15.Bind(wx.EVT_BUTTON, self.ruishu)
		self.m_button16.Bind(wx.EVT_BUTTON, self.gonggao)
		self.m_button18.Bind(wx.EVT_BUTTON, self.xiuxi)
		self.m_button19.Bind(wx.EVT_BUTTON, self.shuoming)
		self.m_button20.Bind(wx.EVT_BUTTON, self.qingchu)
		self.m_button201.Bind(wx.EVT_BUTTON, self.rizhi)

	def __del__( self ):
		# Disconnect Events
		self.m_button15.Unbind(wx.EVT_BUTTON, None)
		self.m_button16.Unbind(wx.EVT_BUTTON, None)
		self.m_button18.Unbind(wx.EVT_BUTTON, None)
		self.m_button19.Unbind(wx.EVT_BUTTON, None)
		self.m_button20.Unbind(wx.EVT_BUTTON, None)
		self.m_button201.Unbind(wx.EVT_BUTTON, None)


	# Virtual event handlers, overide them in your derived class
	def ruishu( self, event ):
		event.Skip()

	def gonggao( self, event ):
		event.Skip()

	def xiuxi( self, event ):
		event.Skip()

	def shuoming( self, event ):
		event.Skip()

	def qingchu( self, event ):
		event.Skip()

	def rizhi( self, event ):
		event.Skip()