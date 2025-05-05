#!/usr/bin/env python
"""
PlayStation BIOS ROM Editor, programmed with love.
"""

import wx
import wx.media

class Diamond(wx.Frame):
	"""
	The main window for Diamond.
	"""
	
	def __init__(self, *args, **kw):
		"""
		Making sure the wxPython stuff initializes properly.
		"""
		super(Diamond, self).__init__(*args, **kw)
		
		#Wrapper panel for everything
		wrapperPanel = wx.Panel(self)
		wrapperSizer = wx.BoxSizer(wx.VERTICAL)
		wrapperPanel.SetSizer(wrapperSizer)
		
		#Add banner image
		bannerPanel = wx.Panel(wrapperPanel)
		#bannerPanel.SetOwnBackgroundColour(wx.Colour(255, 0, 0))
		bannerBitmap = wx.Bitmap("banner.bmp", type=wx.BITMAP_TYPE_BMP)
		bannerImage = wx.StaticBitmap(bannerPanel, wx.ID_ANY, bannerBitmap)
		wrapperSizer.Add(bannerPanel, flag=wx.ALIGN_CENTRE_HORIZONTAL) #Flag aligns banner horizontally
		
		#Fit window to size of sizer
		wrapperSizer.SetSizeHints(self)
		
		#Add menu bar
		self.make_menu_bar()
		
		
	def make_menu_bar(self):
		"""Makes the menu bar for the application."""
		print("Not implemented yet!")
		
		
	def on_about(self, event):
		"""Called when the "about" menu option is clicked."""
		ex.MessageBox("About info goes here.")
		
		
if __name__ == "__main__":
	app = wx.App()
	frame = Diamond(None, title="Diamond", size=(800, 500))
	frame.Show()
	app.MainLoop()