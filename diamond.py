#!/usr/bin/env python
"""
PlayStation BIOS ROM Editor, programmed with love.

Resources used:
"Overview of wxPython" by The wxPython Team: https://wxpython.org/pages/overview/
"Sizers Overview" by The wxPython Team: https://docs.wxpython.org/sizers_overview.html

"wx.Choice" by The wxPython Team: https://docs.wxpython.org/wx.Choice.html#wx-choice

"Layout management in wxPython" by Jan Bodnar: https://zetcode.com/wxpython/layout/
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
		
		'''
		This defines all the different things the
		user can control about the BIOS.
		
		Each dictionary in the dictionary defines a
		"category" of options from which the user can
		click through. This prevents every single options
		from being on-screen at once.
		'''
		BIOSproperties = {
			"Category 1": {},
			"Category 2": {},
			"Category 3": {},
			"Category 4": {},
			"Category 5": {}
		}
		
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
		
		#Present options for user to choose from 
		# (i.e. which properties of the BIOS to change)
		categoryPanel = wx.Panel(wrapperPanel)
		categoryChoice = wx.Choice(categoryPanel, 
								   choices=list(BIOSproperties.keys()),
								   size=wx.Size(500, 20))

		wrapperSizer.Add(categoryPanel, border=5, flag=wx.TOP|wx.ALIGN_CENTRE_HORIZONTAL)
		
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