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
import wx.lib.dialogs

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
		
		Each key in the dictionary defines a "category" of options from 
		which the user can click through. This prevents every single option
		from being on-screen at once.
		
		The dictionaries inside each inner list define the options that'll
		be displayed on the window for the user to interact with, as well
		as stored data that will be used to appropriately modify the BIOS.
		
		Each dictionary will have the following keys:
			Addrs   - Used by the program to identify what addresses are being modified
			Mods    - Says what values to swap into the address, if applicable
			Label   - Text displayed on the window for each option
			Type    - The type of option it is (e.g. radio button, check button, text input, etc.)
			Choices - What options are given to the user, if applicable
			Values  - Keeps track of the actual values entered by the user
		
		For check button options, "mods" specifies the value to set each
		relevant address to if the checkbox is checked. For example, with the option
		{
			"Addrs":   ["42EE0", "42EE1", "42EE2"],
			"Mods":    ["12", "34", "56"],
			"Label":   "Outer Main Sphere Colour",
			"Type":    "Check",
			"Choices": ["Red", "Green", "Blue"],
			"Values":  [wx.CHK_UNCHECKED, wx.CHK_UNCHECKED, wx.CHK_UNCHECKED]
		},
		checking the "Red" checkbox will set the value of address 42EE0 to 12, checking
		the "Green" checkbox will set the value of address 42EE1 to 34, and checking the
		"Blue" checkbox will set address 42EE2 to 56.
		
		IMPORTANT: the addresses in BIOSproperties must be ordered from smallest to
		greatest for the modification code to work. So, modifications that happen
		earlier in the BIOS file must be placed earlier in the dictionary.
		
		'''
		self.BIOSproperties = {
			"0x42000 - Main Sphere Colours": [
				{
					"Addrs":   ["42EE0", "42EE1", "42EE2"],
					"Mods":    ["FF", "FF", "FF"],
					"Label":   "Outer Main Sphere Colour",
					"Type":    "Check",
					"Choices": ["Red", "Green", "Blue"],
					"Values":  [wx.CHK_UNCHECKED, wx.CHK_UNCHECKED, wx.CHK_UNCHECKED]
				},
				{
					"Addrs":   ["42EE4", "42EE5", "42EE6"],
					"Mods":    ["FF", "FF", "FF"],
					"Label":   "Inner Main Sphere Colour",
					"Type":    "Check",
					"Choices": ["Red", "Green", "Blue"],
					"Values":  [wx.CHK_UNCHECKED, wx.CHK_UNCHECKED, wx.CHK_UNCHECKED]
				}
			]
		}
		
		#Holds the name of the currently-selected category
		# so that functions can utilize it.
		self.currentCategory = None
		
		#Holds the paths to the BIOS files
		self.oldBIOS = None
		self.newBIOS = None
		
		#Wrapper sizer for everything
		self.wrapperSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.wrapperSizer)
		self.SetBackgroundColour(wx.Colour(255, 255, 255))
		
		#Add banner image
		bannerPanel = wx.Panel(self)
		bannerBitmap = wx.Bitmap("banner.bmp", type=wx.BITMAP_TYPE_BMP)
		bannerImage = wx.StaticBitmap(bannerPanel, wx.ID_ANY, bannerBitmap)
		self.wrapperSizer.Add(bannerPanel, flag=wx.ALIGN_CENTRE_HORIZONTAL) #Flag aligns banner horizontally
		
		#Present options for user to choose from 
		# (i.e. which properties of the BIOS to change)
		categoryPanel = wx.Panel(self)
		categoryChoice = wx.Choice(categoryPanel, 
								   choices=list(self.BIOSproperties.keys()),
								   size=wx.Size(450, 25))
		self.wrapperSizer.Add(categoryPanel, border=5, 
							  flag=wx.TOP|wx.ALIGN_CENTRE_HORIZONTAL) #Flag aligns and adds margin on top

		#Set an event handler for the category choice
		self.Bind(wx.EVT_CHOICE, self.category_change, categoryChoice)
		
		#Add sizer for specific option data
		self.optionsSizer = wx.BoxSizer(wx.VERTICAL)
		
		#Temp panel for welcome info
		optionsPanel = wx.Panel(self)
		self.optionsSizer.Add(optionsPanel)
		
		welcomeText = wx.StaticText(optionsPanel, label="Welcome!")
		self.wrapperSizer.Add(self.optionsSizer, border=5, 
							  flag=wx.TOP|wx.ALIGN_CENTRE_HORIZONTAL)
							  
		#Add "modify" button
		#Maybe needs a better name
		modifyButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
		modifyButton = wx.Button(self, label="Modify")
		modifyButton.SetMinClientSize(wx.Size(100, 66)) #Prevents the button from being squished
		modifyButton.SetFont(wx.Font(wx.FontInfo(20)))
		self.Bind(wx.EVT_BUTTON, lambda e: self.modify_BIOS(e), modifyButton)
		
		modifyButtonSizer.Add(modifyButton, border=5,
							  flag=wx.TOP|wx.BOTTOM|wx.ALIGN_BOTTOM)
							  
		self.wrapperSizer.Add(modifyButtonSizer, proportion=1, border=5,
		                      flag=wx.TOP|wx.BOTTOM|wx.ALIGN_CENTRE_HORIZONTAL)
		
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
		
		#Set new category choice
		self.currentCategory = event.GetString()
		
		#Now, use event data to make new options
		for optionIndex, option in enumerate(self.BIOSproperties[event.GetString()]):
			if option["Type"] == "Check": #A checkbox option
				#Box/sizer to surround checkboxes
				tempSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, option["Label"])
				self.optionsSizer.Add(tempSizer, border=5, flag=wx.TOP)
				
				#The actual checkboxes
				for checkBoxIndex, name in enumerate(option["Choices"]):
					tempCheckBox = wx.CheckBox(self, label=name)
					
					#Set checkboxes to correct values
					tempCheckBox.SetValue(option["Values"][checkBoxIndex])
					
					#Allow checkboxes to store values
					self.Bind(
						wx.EVT_CHECKBOX, 
						lambda e, f={"Option": option, "CheckBoxIndex": checkBoxIndex, "OptionIndex": optionIndex}: self.update_BIOS_property(e, f), 
						tempCheckBox
					)
					
					tempSizer.Add(tempCheckBox)
		
		#Calling this forces the window to recalculate all sizes
		# related to the sizer, making sure nothing "clips"
		self.wrapperSizer.Layout()
		
		#Fit window to size of sizer
		self.wrapperSizer.SetSizeHints(self)
		
		
	def update_BIOS_property(self, event, extraData):
		"""
		Called whenever a UI element updates a BIOS property.
		"""
		#Decide what type of option this is, then update accordingly
		if extraData["Option"]["Type"] == "Check":
			if event.IsChecked():
				self.BIOSproperties[self.currentCategory][extraData["OptionIndex"]]["Values"][extraData["CheckBoxIndex"]] = wx.CHK_CHECKED
			else:
				self.BIOSproperties[self.currentCategory][extraData["OptionIndex"]]["Values"][extraData["CheckBoxIndex"]] = wx.CHK_UNCHECKED
		
		else:
			raise ValueError(f"Attempted to update BIOS property of an unknown option type {extraData['Option']['Type']}.")
			
			
	def modify_BIOS(self, event):
		"""
		Called whenever the user clicks the 'Modify' button to
		inject their changes into the BIOS.
		"""
		#First, check to see if the user has provided files
		if self.oldBIOS == None:
			wx.lib.dialogs.alertDialog(message="No BIOS file provided to modify. \
			Go to File > Open... to select a BIOS file.", title="No BIOS File Provided")
		
		elif self.newBIOS == None:
			wx.lib.dialogs.alertDialog(message="A name for the modified BIOS file hasn't been given. \
			Go to File > Save As... to choose a name for the modified BIOS file.", 
			title="No Name Given for Modified BIOS")
			
		#Once we get here, attempt the modification!
		else:
			readBIOS = None
			writeBIOS = None
			try:
				readBIOS = open(self.oldBIOS, "rb")
				writeBIOS = open(self.newBIOS, "wb")
				
				'''
				"0x42000 - Main Sphere Colours": [
					{
						"Addrs":   ["42EE0", "42EE1", "42EE2"],
						"Mods":    ["FF", "FF", "FF"],
						"Label":   "Outer Main Sphere Colour",
						"Type":    "Check",
						"Choices": ["Red", "Green", "Blue"],
						"Values":  [wx.CHK_UNCHECKED, wx.CHK_UNCHECKED, wx.CHK_UNCHECKED]
					},
					{
						"Addrs":   ["42EE4", "42EE5", "42EE6"],
						"Mods":    ["FF", "FF", "FF"],
						"Label":   "Inner Main Sphere Colour",
						"Type":    "Check",
						"Choices": ["Red", "Green", "Blue"],
						"Values":  [wx.CHK_UNCHECKED, wx.CHK_UNCHECKED, wx.CHK_UNCHECKED]
					}
				]
				'''
				
				#int("hex", 16)
				
				#Maximum number of bytes to copy at once.
				#This was chosen arbitrarily and can safely be changed.
				MAXCHUNK = 1024
				
				#Get the size of readBIOS
				MAXPOS = readBIOS.seek(0, 2)
				readBIOS.seek(0, 0)
				
				#Loop over all modified sections of the BIOS and change whatever is needed
				for optionList in self.BIOSproperties.values():
					for option in optionList:
						for addrIndex, addr in enumerate(option["Addrs"]):
							#Copy data from readBIOS to writeBIOS until we're
							# at a section that needs to be modified
							while readBIOS.tell() != int(addr, 16):
								amountToCopy = 1
								if int(addr, 16) - readBIOS.tell() >= MAXCHUNK:
									amountToCopy = MAXCHUNK
								writeBIOS.write(readBIOS.read(amountToCopy))
								
							#Once we get here, that means we're at the proper spot to modify
							if option["Type"] == "Check":
								if option["Values"][addrIndex] == wx.CHK_CHECKED:
									#Probably a better way to do this conversion, but oh well
									writeBIOS.write(int(option["Mods"][addrIndex], 16).to_bytes())
									readBIOS.read(1) #To make sure files don't fall out of sync
								else:
									writeBIOS.write(readBIOS.read(1))
									
							else:
								raise ValueError(f"Attempted to modify BIOS using unknown option type {option['Type']}.")
								
				#Once all the options have been accounted for,
				# copy the rest of the BIOS file
				while readBIOS.tell() < MAXPOS:
					amountToCopy = 1
					if MAXPOS - readBIOS.tell() >= MAXCHUNK:
						amountToCopy = MAXCHUNK
					writeBIOS.write(readBIOS.read(amountToCopy))
				
			except FileNotFoundError:
				wx.lib.dialogs.alertDialog(message="Unable to read provided BIOS file. Check to make sure \
				the file is in the correct location.", title="Unable to Read BIOS File")
			finally:
				if readBIOS != None:
					readBIOS.close()
				if writeBIOS != None:
					writeBIOS.close()
		
		
	def make_menu_bar(self):
		"""
		Makes the menu bar for the application.
		"""
		fileMenu = wx.Menu()
		openFileItem = fileMenu.Append(wx.ID_OPEN)
		replaceFileItem = fileMenu.Append(wx.ID_REPLACE)
		
		aboutMenu = wx.Menu()
		aboutItem = aboutMenu.Append(wx.ID_ABOUT)
		
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "&File")
		menuBar.Append(aboutMenu, "&About")
		
		self.SetMenuBar(menuBar)
		
		self.Bind(wx.EVT_MENU, self.on_about, aboutItem)
		self.Bind(wx.EVT_MENU, self.on_open_file, openFileItem)
		self.Bind(wx.EVT_MENU, self.on_replace_file, replaceFileItem)
		
		
	def on_about(self, event):
		"""
		Called when the "About" menu option is clicked.
		"""
		wx.MessageBox("Diamond\nCreated by Cocoatwix.", "About Diamond", wx.OK|wx.ICON_INFORMATION)
		
		
	def on_open_file(self, event):
		"""
		Called when the user selects "Open...".
		"""
		self.oldBIOS = wx.lib.dialogs.openFileDialog(title="Open BIOS File to Modify...").paths
		if self.oldBIOS != None:
			self.oldBIOS = self.oldBIOS[0]
		
		
	def on_replace_file(self, event):
		"""
		Called when the user selects "Replace...".
		"""
		self.newBIOS = wx.lib.dialogs.saveFileDialog(title="Choose BIOS File to Replace/Save As...").paths
		if self.newBIOS != None:
			self.newBIOS = self.newBIOS[0]
		
		
if __name__ == "__main__":
	app = wx.App()
	frame = Diamond(None, title="Diamond")
	frame.Show()
	app.MainLoop()
