#!/usr/bin/env python
"""
PlayStation BIOS ROM Editor, programmed with love.

Helpful resources used:
"wxPython API Documentation" by The wxPython Team: https://docs.wxpython.org/index.html

"Overview of wxPython" by The wxPython Team: https://wxpython.org/pages/overview/
"Sizers Overview" by The wxPython Team: https://docs.wxpython.org/sizers_overview.html

"Layout management in wxPython" by Jan Bodnar: https://zetcode.com/wxpython/layout/
"""

import json

import wx
import wx.lib.dialogs


def insert_by_sorted_key(listToModify, dictToAdd, keyToSortBy):
	"""
	Used to insert a dictionary into a list of
	similar dictionaries while keeping the list
	sorted based on 
	"""
	start = 0
	end = len(listToModify)-1
	currPos = (start+end)//2
	
	if end == -1:
		listToModify.append(dictToAdd)
		return
	
	#Perform binary search
	while start != end:
		if listToModify[currPos][keyToSortBy] >= dictToAdd[keyToSortBy]:
			end = currPos - 1 if end == currPos else currPos
		else:
			start = currPos + 1 if start == currPos else currPos
			
		currPos = (start+end)//2

	#Once here, determine if dictToAdd is before or after currPos
	if listToModify[currPos][keyToSortBy] >= dictToAdd[keyToSortBy]:
		listToModify.insert(currPos, dictToAdd)
	else:
		listToModify.insert(currPos+1, dictToAdd)


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
			Mods    - For "Check" type. Says what values to swap into the address when checkbox is checked.
			Bounds  - For "Range" type. Defines the range of values that can be entered by the user to set the address values to.
			Label   - Text displayed on the window for each option
			Type    - The type of option it is (e.g. radio button, check button, text input, etc.)
			Choices - What options are given to the user
			Values  - Keeps track of the actual values entered by the user
		
		As an example, with the checkbox option
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
		
		As another example, for the range option, 
		{
			"Addrs":   ["289FC", "289FD", "28A0C", "28A0D"],
			"Bounds":  [{"Min": "00", "Max": "11"},
						{"Min": "22", "Max": "33"},
						{"Min": "44", "Max": "55"},
						{"Min": "66", "Max": "77"}],
			"Label":   "Sony Logo's Position",
			"Type":    "Range",
			"Choices": ["Y Position (1/2)", "Y Position (2/2)", "X Position (1/2)", "X Position (2/2)"],
			"Values":  ["00", "22", "45", "70"]
		},
		the "Y Position (1/2)" slider can set the value of address 289FC from 00 to 11 and has a default value of 00. The
		"Y Position (2/2)" slider can set the value of address 289FD from 22 to 33 and has a default value of 22. The
		"X Position (1/2)" slider can set the value of address 28A0C from 44 to 55 and has a default value of 45. Finally, the
		"X Position (2/2)" slider can set the value of address 28A0D from 66 to 77 and has a default value of 70.
		'''
		self.BIOSproperties = {
			"0x28000 - Logo Positioning": [
				{
					"Addrs":   ["289FC", "289FD", "28A0C", "28A0D"],
					"Bounds":  [{"Min": "00", "Max": "FF"},
								{"Min": "00", "Max": "FF"},
								{"Min": "00", "Max": "FF"},
								{"Min": "00", "Max": "FF"}],
					"Label":   "Sony Logo's Position",
					"Type":    "Range",
					"Choices": ["Y Position (1/2)", "Y Position (2/2)", "X Position (1/2)", "X Position (2/2)"],
					"Values":  ["00", "00", "00", "00"]
				}
			],
			
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
		
		#Read from settings.json, if it exists
		self.load_settings()
		
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
					
					tempSizer.Add(tempCheckBox, border=15, flag=wx.RIGHT)
			
			elif option["Type"] == "Range": #A slider option
				#Box/sizer to surround checkboxes
				tempBigSizer = wx.StaticBoxSizer(wx.VERTICAL, self, option["Label"])
				self.optionsSizer.Add(tempBigSizer, border=5, flag=wx.TOP)
				
				#The actual sliders
				for choiceIndex, choice in enumerate(option["Choices"]):
					tempSmallSizer = wx.BoxSizer(wx.HORIZONTAL)
					
					#Add label text for each slider
					tempLabelPanel = wx.Panel(self)
					tempSmallSizer.Add(tempLabelPanel, border=15, flag=wx.RIGHT)
					tempLabelText = wx.StaticText(tempLabelPanel, label=choice)
					
					#Add Slider
					tempSlider = wx.Slider(self, value=int(option["Values"][choiceIndex], 16),
					                       minValue=int(option["Bounds"][choiceIndex]["Min"], 16),
										   maxValue=int(option["Bounds"][choiceIndex]["Max"], 16),
										   size=wx.Size(200, 25))
					tempSmallSizer.Add(tempSlider, border=5, flag=wx.RIGHT)
					
					#Add textbox holding the slider's value
					tempTextCtrl = wx.TextCtrl(self, value=option["Values"][choiceIndex],
					                           size=wx.Size(25, 20))
					tempTextCtrl.SetMaxLength(2)
					tempSmallSizer.Add(tempTextCtrl, border=5, flag=wx.RIGHT)
					
					tempBigSizer.Add(tempSmallSizer, border=5, flag=wx.TOP|wx.BOTTOM)
					
					self.Bind(wx.EVT_TEXT, 
					          lambda e, f={"TextCtrl": tempTextCtrl, 
							               "Slider": tempSlider, 
										   "MinValue": option["Bounds"][choiceIndex]["Min"],
										   "Option": option,
										   "OptionIndex": optionIndex,
										   "ChoiceIndex": choiceIndex}: 
							  self.manage_text_entry(e, f), 
							  tempTextCtrl)
							  
					self.Bind(wx.EVT_SCROLL,
							  lambda e, f={"Slider": tempSlider,
										   "TextCtrl": tempTextCtrl,
							               "Option": option,
										   "OptionIndex": optionIndex,
										   "ChoiceIndex": choiceIndex}:
							  self.manage_slider(e, f),
							  tempSlider)

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
				
		elif extraData["Option"]["Type"] == "Range":
			self.BIOSproperties[self.currentCategory][extraData["OptionIndex"]]["Values"][extraData["ChoiceIndex"]] = extraData["TextCtrl"].GetValue()
		
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
			
		elif self.oldBIOS == self.newBIOS:
			wx.lib.dialogs.alertDialog(message="The modified BIOS file is the same as the BIOS file \
			to read from. Please choose a different file to output BIOS modifications to.",
			title="Modified BIOS Same As Source BIOS")
			
		#Once we get here, attempt the modification!
		else:
			readBIOS = None
			writeBIOS = None
			try:
				readBIOS = open(self.oldBIOS, "rb")
				writeBIOS = open(self.newBIOS, "wb")
				
				#Maximum number of bytes to copy at once.
				#This was chosen arbitrarily and can safely be changed.
				MAXCHUNK = 1024
				
				#Get the size of readBIOS
				MAXPOS = readBIOS.seek(0, 2)
				readBIOS.seek(0, 0)
				
				#Now, perform some preprocessing so that we know beforehand
				# which values need to be modified in the BIOS.
				modifications = []
				
				#Loop over all modified sections of the BIOS and record whatever changes are needed
				for optionList in self.BIOSproperties.values():
					for option in optionList:
						for addrIndex, addr in enumerate(option["Addrs"]):
							if option["Type"] == "Check":
								if option["Values"][addrIndex] == wx.CHK_CHECKED:
									insert_by_sorted_key(modifications, {"Addr": addr, "Value": option["Mods"][addrIndex]}, "Addr")
									
							elif option["Type"] == "Range":
								insert_by_sorted_key(modifications, {"Addr": addr, "Value": option["Values"][addrIndex]}, "Addr")
									
							else:
								raise ValueError(f"Attempted to modify BIOS using unknown option type {option['Type']}.")
								
							'''
							"0x28000 - Logo Positioning": [
								{
									"Addrs":   ["289FC", "289FD", "28A0C", "28A0D"],
									"Bounds":  [{"Min": "00", "Max": "FF"},
												{"Min": "00", "Max": "FF"},
												{"Min": "00", "Max": "FF"},
												{"Min": "00", "Max": "FF"}],
									"Label":   "Sony Logo's Position",
									"Type":    "Range",
									"Choices": ["Y Position (1/2)", "Y Position (2/2)", "X Position (1/2)", "X Position (2/2)"],
									"Values":  ["00", "00", "00", "00"]
								}
							],
							'''

				#Now, with all modifications accounted for, actually
				# modify the BIOS
				for mod in modifications:
					while readBIOS.tell() < int(mod["Addr"], 16):
						amountToCopy = 1
						if int(mod["Addr"], 16) - readBIOS.tell() >= MAXCHUNK:
							amountToCopy = MAXCHUNK
						writeBIOS.write(readBIOS.read(amountToCopy))
					
					writeBIOS.write(int(mod["Value"], 16).to_bytes())
					readBIOS.read(1) #Keeps the two files in sync
					
				#Now, copy the rest of the file
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
		openFileItem     = fileMenu.Append(-1, "Open BIOS File...\tCtrl-O")
		replaceFileItem  = fileMenu.Append(-1, "Save Modified BIOS File As...\tCtrl-H")
		fileMenu.AppendSeparator()
		saveSettingsItem = fileMenu.Append(-1, "Save Settings\tCtrl-S")
		
		aboutMenu = wx.Menu()
		aboutItem = aboutMenu.Append(wx.ID_ABOUT)
		
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "&File")
		menuBar.Append(aboutMenu, "&About")
		
		self.SetMenuBar(menuBar)
		
		self.Bind(wx.EVT_MENU, self.on_about, aboutItem)
		self.Bind(wx.EVT_MENU, self.on_open_file, openFileItem)
		self.Bind(wx.EVT_MENU, self.on_replace_file, replaceFileItem)
		self.Bind(wx.EVT_MENU, self.on_save_settings, saveSettingsItem)
		
		
	def manage_text_entry(self, event, extra):
		"""
		Called whenever a TextCtrl needs to be managed.
		"""
		#This makes sure no invalid characters are entered
		#Sloppy, but it works
		currentEntry = extra["TextCtrl"].GetValue()
		for c in currentEntry:
			if c not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
					 "A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f"]:
				extra["TextCtrl"].Undo()
				break
				
		#Now, we need to update the relevant slider
		currentEntry = extra["TextCtrl"].GetValue()
		if currentEntry == "":
			currentEntry = 0
		else:
			currentEntry = int(currentEntry, 16)
			
		extra["Slider"].SetValue(currentEntry)
		
		#Finally, update the stored value for this option
		# so it's reflected in the modified BIOS
		self.update_BIOS_property(None, extra)
		
		
	def manage_slider(self, event, extra):
		"""
		Called whenever a Slider needs to be managed.
		"""
		#First, update the associated TextCtrl
		hexValue = hex(extra["Slider"].GetValue())[2:]
		if len(hexValue) == 1:
			hexValue = "0" + hexValue
		extra["TextCtrl"].Replace(0, 2, hexValue)
		
		#Now, update the stored value so that
		# changes are reflected in the modified BIOS
		self.update_BIOS_property(None, extra)
		
		
	def on_about(self, event):
		"""
		Called when the "About" menu option is clicked.
		"""
		wx.MessageBox("Diamond\nCreated by Cocoatwix.", "About Diamond", wx.OK|wx.ICON_INFORMATION)
		
		
	def on_open_file(self, event):
		"""
		Called when the user wants to choose the BIOS file to use.
		"""
		self.oldBIOS = wx.lib.dialogs.openFileDialog(title="Open BIOS File to Modify...").paths
		if self.oldBIOS != None:
			self.oldBIOS = self.oldBIOS[0]
		
		
	def on_replace_file(self, event):
		"""
		Called when the user wants to give the modified BIOS file a name.
		"""
		self.newBIOS = wx.lib.dialogs.saveFileDialog(title="Choose BIOS File to Replace/Save As...").paths
		if self.newBIOS != None:
			self.newBIOS = self.newBIOS[0]
			
			
	def on_save_settings(self, event):
		"""
		Called whenever the user would like to save their settings.
		"""
		settingsObject = {}
		
		if self.oldBIOS == None:
			settingsObject["oldBIOS"] = ""
		else:
			settingsObject["oldBIOS"] = self.oldBIOS
			
		if self.newBIOS == None:
			settingsObject["newBIOS"] = ""
		else:
			settingsObject["newBIOS"] = self.newBIOS
			
		#Now, store all of the user's given settings
		for option in self.BIOSproperties.keys():
			settingsObject[option] = {}
			for panel in self.BIOSproperties[option]:
				settingsObject[option][panel["Label"]] = panel["Values"]
			
		#Actually save the settings
		with open("settings.json", "w") as settingsFile:
			json.dump(settingsObject, settingsFile, indent="\t")
			
			
	def load_settings(self):
		"""
		Called on frame initialization to load files, if they exist.
		"""
		try:
			with open("settings.json", "r") as settingsFile:
				settingsObject = json.load(settingsFile)
				
				self.oldBIOS = settingsObject["oldBIOS"]
				self.newBIOS = settingsObject["newBIOS"]
				
				#Now, load all the user's settings
				for option in settingsObject.keys():
					if option not in ["oldBIOS", "newBIOS"]:
						for panelIndex, panel in enumerate(self.BIOSproperties[option]):
							self.BIOSproperties[option][panelIndex]["Values"] = settingsObject[option][panel["Label"]]
				
		except FileNotFoundError:
			#Probably a more elegant way to do this using
			# pathlib, but this is good enough for now.
			print("settings.json file not found. Continuing with default settings.")
		
		
if __name__ == "__main__":
	app = wx.App()
	frame = Diamond(None, title="Diamond")
	frame.Show()
	app.MainLoop()
