from GUIManager import GUIManager

class MainWindow(object):
	def __init__(self):
		# some test variables
		v = []
		for i in range(12): v.append('Line number ' + str(i + 1))

		self.gm = GUIManager("Senemedar's GUIManager Demo", resizable=(True, False))		# initialise the main window
		self.myParent = GUIManager.get_root(self.gm)		# main window as a parent for all the widgets
		
		self.mainContainer1 = self.gm.create_frame(self.myParent, (0, 0), 'groove', 3, main=True, s='ns')
		self.quit_button = self.gm.create_button(
				self.mainContainer1, (0, 0), 'Quit', self.gm.close_program, py=(2, 0))
		self.awesome_button = self.gm.create_button(
				self.mainContainer1, (1, 1), 'Awesome', self.disable_button, state='d', py=(0,2), iy=10)
		self.frame1 = self.gm.create_frame(self.mainContainer1, (0, 2), 'raised', 2, px=10, py=10, xs=2, s='news')
		self.awesome_label = self.gm.create_label(
				self.frame1, (0 , 0), 'This label closes the window!', self.gm.close_program, xs=2, ix=10, iy=5, s= 'news')
		self.awesome_button1 = self.gm.create_button(
				self.frame1, (0, 1), 'Even awesomer!', self.enable_button, xs=2, px=3, py=5, s='ew')
		self.awesome_entry_label1 = self.gm.create_label(
				self.frame1, (0, 2), 'Numbers entry', None, px=3, s='e')
		self.awesome_entry1 = self.gm.create_entry(
				self.frame1, (1, 2), text = 123, state = 'n', entry_type = 'n', px = 3)
		self.awesome_entry_label3 = self.gm.create_label(
				self.frame1, (0, 3), 'Magical Combobox', None, px = 3, s = 'e')
		self.awesome_combobox = self.gm.create_combobox(
				self.frame1, (1, 3), v, text = v[0], state = 'r', cbox_type = 't', command = self.update_entry, width = 20, px = 3, py=3)
		self.awesome_entry_label2 = self.gm.create_label(
				self.frame1, (0, 4), 'Combobox selection', None, px = 3, s = 'e')
		self.awesome_entry2 = self.gm.create_entry(
				self.frame1, (1, 4), text = 'Entry', state = 'r', entry_type = 't', width = 20, px = 3, py=3)
		self.awesome_listbox = self.gm.create_listbox(
				self.frame1, (2, 0), text = v, command=self.update_entry2, ys=5, s='news', height = 10)
		self.awesome_entry_label4 = self.gm.create_label(
				self.frame1, (0, 5), 'Listbox selection', None, px = 3, s = 'e')
		self.awesome_entry3 = self.gm.create_entry(
				self.frame1, (1, 5), text = 'Entry3', state = 'r', entry_type = 't', width = 60, xs = 2, px = 3, py=3)
		self.frame2 = self.gm.create_frame(self.mainContainer1, (0, 4), px=10, py=10, xs=2, s='news')
		self.label5 = self.gm.create_label(self.frame2, (0, 0), 'Text entry', py=3, px=(5, 1), s='e')
		self.entry4 = self.gm.create_entry(self.frame2, (1, 0), entry_type = 't')
		self.button2 = self.gm.create_button(self.frame2, (2, 0), 'Insert into Combobox', lambda: self.gm.insert_value(
				self.awesome_combobox, self.gm.get_element_value(self.entry4)), width = 20, px=5)
		self.button3 = self.gm.create_button(self.frame2, (3, 0), 'Insert into Listbox', lambda: self.gm.insert_value(
				self.awesome_listbox, self.gm.get_element_value(self.entry4)), width = 20, px=(0,5))
		self.radio_button = self.gm.create_radiobutton(
				self.frame2,
				(0,5),
				'v',
				3,
				('First', 'Second', 'Third'),
				('Choose one:', 'l'),
				command = lambda: self.gm.set_element_value(self.entry4, self.gm.get_element_value(self.radio_button)),
				xs=2
		)
		self.radio_button[0].invoke()
		self.checkbox = self.gm.create_checkbox(self.frame2, (2, 5), 'Disable radio buttons', width = 20, command = self.toggle_radio_buttons, check=0, s='nw', py=5)
		
		# print(len(self.radio_button))
		self.gm.set_columns(self.mainContainer1, (0, 1))
		self.gm.set_columns(self.frame1, [0, 0])
		self.gm.set_rows(self.mainContainer1, [False, False, 1])
		self.gm.set_rows(self.frame1, [0, 0, 0, 0])

		# =======================================================================
		# ------ end of drawing the GUI -----------------------------------------
		# =======================================================================
		
		# Start application
		self.gm.start_program()
		
	def insert_value(self, widget):
		self.gm.insert_value(widget, self.gm.get_element_value(self.entry4))
	
	def update_entry(self):
		self.gm.set_element_value(self.awesome_entry2, self.gm.get_element_value(self.awesome_combobox))

	def update_entry2(self):
		self.gm.set_element_value(self.awesome_entry3, self.gm.get_element_value(self.awesome_listbox))
	
	def disable_button(self):
		self.gm.change_element_state(self.awesome_button, 'd')
		
	def enable_button(self):
		self.gm.change_element_state(self.awesome_button, 'a')
		
	def toggle_radio_buttons(self):
		if not self.gm.get_element_value(self.checkbox):
			self.gm.change_element_state(self.radio_button, 'n')
		else:
			self.gm.change_element_state(self.radio_button, 'd')

app = MainWindow()

