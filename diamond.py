#!/usr/bin/env python
"""
PlayStation BIOS ROM Editor, programmed with love.

Helpful resources used:
"wxPython API Documentation" by The wxPython Team: https://docs.wxpython.org/index.html

"Overview of wxPython" by The wxPython Team: https://wxpython.org/pages/overview/
"Sizers Overview" by The wxPython Team: https://docs.wxpython.org/sizers_overview.html

"Layout management in wxPython" by Jan Bodnar: https://zetcode.com/wxpython/layout/
"""

import wx

class Diamond(wx.Frame):
	"""
	The main window for Diamond.
	"""
	
	def __init__(self, *args, **kw):
		"""
		Initialize the program.
		"""
		super(Diamond, self).__init__(*args, **kw)
		
		'''
		self.BIOSproperties defines all the different things the
		user can control about the BIOS.
		
		Each key in the dictionary defines a
		"category" of options from which the user can
		click through. This prevents every single options
		from being on-screen at once.
		
		The data inside each inner list defines the options that'll
		be displayed on the window for the user to interact with.
		
		ID      - Used by the program to identify what options are being set
		Label   - Text displayed on the window for each option
		Type    - The type of option it is (e.g. radio button, check button, text input, etc.)
		Options - What options are given to the user, if applicable
		'''
		self.BIOSproperties = {
			"0x42000 - Main Sphere Colours": [
				{
					"ID":      "42EE0",
					"Label":   "Outer Main Sphere Colour",
					"Type":    "Check",
					"Options": ["Red", "Green", "Blue"]
				},
				{
					"ID":      "42EE4",
					"Label":   "Inner Main Sphere Colour",
					"Type":    "Check",
					"Options": ["Red", "Green", "Blue"]
				}
			],
			"Category 2": [],
			"Category 3": [],
			"Category 4": [],
			"Category 5": []
		}
		
		#Wrapper panel for everything
		self.wrapperPanel = wx.Panel(self)
		self.wrapperSizer = wx.BoxSizer(wx.VERTICAL)
		self.wrapperPanel.SetSizer(self.wrapperSizer)
		
		#Add banner image
		bannerPanel = wx.Panel(self.wrapperPanel)
		#bannerPanel.SetOwnBackgroundColour(wx.Colour(255, 0, 0))
		bannerBitmap = wx.Bitmap("banner.bmp", type=wx.BITMAP_TYPE_BMP)
		bannerImage = wx.StaticBitmap(bannerPanel, wx.ID_ANY, bannerBitmap)
		self.wrapperSizer.Add(bannerPanel, flag=wx.ALIGN_CENTRE_HORIZONTAL) #Flag aligns banner horizontally
		
		#Present options for user to choose from 
		# (i.e. which properties of the BIOS to change)
		categoryPanel = wx.Panel(self.wrapperPanel)
		categoryChoice = wx.Choice(categoryPanel, 
								   choices=list(self.BIOSproperties.keys()),
								   size=wx.Size(450, 20))
		self.wrapperSizer.Add(categoryPanel, 
		                      border=5, 
							  flag=wx.TOP|wx.ALIGN_CENTRE_HORIZONTAL) #Flag aligns and adds margin on top

		#Set an event handler for the category choice
		self.Bind(wx.EVT_CHOICE, self.category_change, categoryChoice)
		
		#Add sizer for specific option data
		self.optionsSizer = wx.BoxSizer(wx.VERTICAL)
		
		#Temp panel for welcome info
		self.optionsPanel = wx.Panel(self.wrapperPanel)
		self.optionsSizer.Add(self.optionsPanel)
		
		welcomeText = wx.StaticText(self.optionsPanel, label="Welcome!")
		self.wrapperSizer.Add(self.optionsSizer, 
		                      border=5, 
							  flag=wx.TOP|wx.ALIGN_CENTRE_HORIZONTAL)
							  
		#self.optionsPanel.SetOwnBackgroundColour(wx.Colour(255, 0, 0))
		
		
		#Fit window to size of sizer
		self.wrapperSizer.SetSizeHints(self)
		
		#Add menu bar
		self.make_menu_bar()
		
		
	def category_change(self, event):
		"""
		Called when the user changes the selected category of BIOS options.
		"""
		#Clear options panel for new options
		self.optionsSizer.Clear(True)
		
		#Now, use event data to make new options
		for option in self.BIOSproperties[event.GetString()]:
			print(option)
			if option["Type"] == "Check": #A checkbox option
				pass
				#Box to surround checkboxes
				#tempStaticBox = wx.StaticBox(self.optionsSizer, label=option["Label"])
		
		#Calling this forces the window to recalculate all sizes
		# related to the sizer, making sure nothing "clips"
		self.wrapperSizer.Layout()
		
		#Fit window to size of sizer
		self.wrapperSizer.SetSizeHints(self)
		
	def make_menu_bar(self):
		"""
		Makes the menu bar for the application.
		"""
		print("Not implemented yet!")
		
		
	def on_about(self, event):
		"""
		Called when the "about" menu option is clicked.
		"""
		ex.MessageBox("About info goes here.")
		
		
if __name__ == "__main__":
	app = wx.App()
	frame = Diamond(None, title="Diamond", size=(800, 500))
	frame.Show()
	app.MainLoop()