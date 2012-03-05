#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import wx
import sqlite3

## just the UI CODE
## Logic crap below
class NavigatorWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.ayatText = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_RIGHT|wx.TE_WORDWRAP )
		bSizer1.Add( self.ayatText, 1, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer1 = wx.FlexGridSizer( 2, 3, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableCol( 2 )
		fgSizer1.SetFlexibleDirection( wx.VERTICAL )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.txtSurahNum = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.txtSurahNum, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.txtAyatNum = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.txtAyatNum, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.btnGo = wx.Button( self, wx.ID_ANY, u"Go", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.btnGo, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.btnPrev = wx.Button( self, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.btnPrev, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.btnNext = wx.Button( self, wx.ID_ANY, u">", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.btnNext, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.btnCommit = wx.Button( self, wx.ID_ANY, u"Commit", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.btnCommit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer1.Add( fgSizer1, 0, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.ayatText.Bind( wx.EVT_TEXT, self.onAyatChange )
		self.btnGo.Bind( wx.EVT_BUTTON, self.onGobtnClick )
		self.btnPrev.Bind( wx.EVT_BUTTON, self.onPrevClick )
		self.btnNext.Bind( wx.EVT_BUTTON, self.onNextClick )
		self.btnCommit.Bind( wx.EVT_BUTTON, self.onCommit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onAyatChange( self, event ):
		event.Skip()
	
	def onGobtnClick( self, event ):
		event.Skip()
	
	def onPrevClick( self, event ):
		event.Skip()
	
	def onNextClick( self, event ):
		event.Skip()
	
	def onCommit( self, event ):
		event.Skip()
		
		
if __name__ == "__main__":
	wxapp = wx.App()
	navigator = NavigatorWindow(None)
	navigator.Show()
	wxapp.MainLoop()