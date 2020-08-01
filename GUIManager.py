from tkinter import *
from tkinter import ttk

class GUIManager(object):
	"""
	Class created to make my life easier when creating a GUI for Python applications.
	"""
	
	__elements_dict = {}		# grouping of all the elements with variables attached to them
	
	def __init__(self, title = 'Application', size = (None, None), resizable = (True, True)):
		"""
		Initialisation.
		:param title: title for the main window
		:param size: (optional) size of the window, in pixels: (size-x, size-y)
		:param resizable: enabled by default; (x-resizable, y-resizable)
		"""
		self.__root = Tk()
		self.__root.title(title)
		window_size = ''
		if size[0] and size[1]: window_size += str(size[0]) + "x" + str(size[1])
		window_size += "+50+20"
		print(self.__root.geometry())
		self.__root.geometry(window_size)
		self.__root.resizable(width = resizable[0], height = resizable[1])
		
	@classmethod
	def create_frame(cls, parent, pos, relief='flat', borderwidth=0, **kwargs):
		"""
		Creates a frame.
		:param parent: ttk parent
		:param relief: ttk relief: FLAT, RIDGE, GROOVE, RAISED, SUNKEN
		:param borderwidth: width of the border, min. 2 if relief is used
		:param pos: (x, y)-- x - column
							 y - row
		:param kwargs: optional arguments:
				main=True - if this argument is used, the frame will be packed to fill entire window; value of other arguments is ignored)
				xs - columnspan
				ys - rowspan
				px - padx
				py - pady
				ix - ipadx
				iy - ipady
				s - sticky
		:return frame:  generated frame
		"""
		frame = ttk.Frame(parent, borderwidth = borderwidth, relief = relief)
		# print(kwargs)
		try:
			if kwargs['main']:
				frame.pack(expand = YES, fill = BOTH, padx = 1, pady = 1)
		except KeyError:
			cls.place_element(frame, pos[0], pos[1], options = kwargs)
		
		return frame
	
	@staticmethod
	def set_columns(frame, col_weight, size = None):
		"""
		Sets the weights and minimal size of the columns.
		
		:param frame: frame the columns are being set for
		:param col_weight: weight of the columns, passed as a list
		:param size: (optional) minimum size of the columns, passed as a list in the same order as col_weight
		:return: None
		"""
		# print(col_weight)
		for col in range(len(col_weight)):
			frame.columnconfigure(col, weight = col_weight[col])
			if size and size[col]:
				frame.columnconfigure(col, minsize = size[col])
	
	@staticmethod
	def set_rows(frame, row_weight, size = None):
		"""
		Sets the weights and minimal size of the rows.
		
		:param frame: frame the columns are being set for
		:param row_weight: weight of the rows, passed as a list
		:param size: (optional) minimum size of the rows, passed as a list in the same order as row_weight
		:return: None
		"""
		# print(row_weight)
		for row in range(len(row_weight)):
			frame.rowconfigure(row, weight = row_weight[row])
			if size and size[row]:
				frame.rowconfigure(row, minsize = size[row])
	
	@classmethod
	def create_label(cls, parent, pos, text, command = None, state = 'n', **kwargs):
		"""
		Creates and places a label.
		
		:param parent: ttk parent
		:param text: text on the label
		:param command: (optional) if set, the widget will have the .bind assigned to it which will launch the command
		:param pos: (x, y)-- x - column
							 y - row
		:param state: (optional) state of the label: NORMAL - used if other not given, DISABLED
		:param kwargs: optional arguments:
				xs - columnspan
				ys - rowspan
				px - padx
				py - pady
				ix - ipadx
				iy - ipady
				s - sticky
		:return button: generated label
		"""

		label = ttk.Label(parent, text = text, state = cls.get_state(state))
		cls.place_element(label, pos[0], pos[1], options = kwargs)
		if command:
			label.bind('<Button-1>', lambda e: command())

		return label
	
	@classmethod
	def create_button(cls, parent, pos, text = 'Button', command = None,  state='n', width=None, **kwargs):
		"""
		Inserts a button into frame
		:param parent: ttk parent
		:param text: text on the button
		:param command: command after button click
		:param state: state of the button: NORMAL, DISABLED
		:param pos: (x, y)-- x - column
							 y - row
		:param kwargs: optional arguments:
				xs - columnspan
				ys - rowspan
				px - padx
				py - pady
				ix - ipadx
				iy - ipady
				s - sticky
		:return button: generated button
		"""
		button = ttk.Button(parent, text = text, width = width, state = cls.get_state(state), command = command)
		cls.place_element(button, pos[0], pos[1], options = kwargs)
		return button
	
	@classmethod
	def create_entry(cls, parent, pos, text = None, command=None, state='n', entry_type='t', width = None, **kwargs):
		"""
		Inserts an entry field into frame
		:param parent: ttk parent
		:param pos: (x, y)-- x - column
							 y - row
		:param text: value the widget will initialise to
		:param entry_type: 't' - text input
						   'n' - number input
		:param width: width of widget, in characters; if not used, default values will be used
		:param state: state of the entry field:
		 	'n' - normal,
		 	'd' - disabled,
		 	'r' - read only
		:param command: (optional) command to be executed
		:param kwargs: optional arguments:
				xs - columnspan
				ys - rowspan
				px - padx
				py - pady
				ix - ipadx
				iy - ipady
				s - sticky
		:return entry: generated entry field
		"""
		validate_command = parent.register(cls.validate_entry)
		default_width = width
		if entry_type == 't':
			variable = StringVar(value = text)
			if not width: default_width = 25
		elif entry_type == 'n':
			variable = IntVar(value = text)
			if not width: default_width = 10
			
		entry = ttk.Entry(
				parent,
				textvariable = variable,
				width = default_width,
				state=cls.get_state(state),
				command = command,
				validate = 'all',
				validatecommand = (validate_command, entry_type, '%S')
		)
		cls.place_element(entry, pos[0], pos[1], options = kwargs)
		
		# def end_of_typing(e):
		# 	entry.event_generate('<FocusOut>')
		#
		# entry.bind('<Return>', end_of_typing)
		
		cls.__elements_dict[entry] = variable
		
		return entry
	
	@classmethod
	def create_checkbox(cls, parent, pos, text = None, command = None, state = 'n', check=0, width = 12, **kwargs):
		"""
		Generates an checkbox and places it on the screen.
		
		:param parent: ttk parent
		:param pos: (x, y)--
		 		x - column
				y - row
		:param text: checkbox text
		:param width: (optional) width of widget, in characters; default is 12
		:param command: (optional) command to be executed when checkbox changes its state
		:param state: (optional) state of the entry field; default is NORMAL
		 		'n' - normal,
		 		'd' - disabled
		:param check: (optional) if 1, the checkbox will be 'check' when generated; 0 by default
		:param kwargs: (optional) placing arguments:
				xs - columnspan
				ys - rowspan
				px - padx
				py - pady
				ix - ipadx
				iy - ipady
				s - sticky
		:return checkbox: generated checkbox
		"""
		variable = IntVar(value = check)
		checkbox = ttk.Checkbutton(
				parent,
				text = text,
				width = width,
				state = cls.get_state(state),
				command = command,
				variable = variable
		)
		cls.place_element(checkbox, pos[0], pos[1], options = kwargs)
		
		cls.__elements_dict[checkbox] = variable
		
		return checkbox
	
	@classmethod
	def create_combobox(cls, parent, pos, values, text = None, command=None, state='n', cbox_type='t', width = None, **kwargs):
		"""
		Inserts an entry field into frame.
		If 'command' is used, it will be executed AFTER the combobox value is changed and will return the 'event' attribute.
		:param parent: ttk parent
		:param pos: position (x, y):
			x - column
			y - row
		:param values: values to choose from
		:param text: value the widget will initialise to
		:param cbox_type: type of the combobox:
			't' - text input
			'n' - number input
		:param width: width of widget, in characters; if not used, default values will be used
		:param state: state of the entry field:
		 	'n' - normal,
		 	'd' - disabled,
		 	'r' - read only
		:param command: (optional) command to be executed
		:param kwargs: optional arguments:
			xs - columnspan
			ys - rowspan
			px - padx
			py - pady
			ix - ipadx
			iy - ipady
			s - sticky
		:return entry: generated entry field
		:return variable: a variable connected to generated combobox
		"""
		
		validate_command = parent.register(cls.validate_entry)
		default_width = width
		if cbox_type == 't':
			variable = StringVar(value = text)
			if not width: default_width = 25
		else:
			variable = IntVar(value = text)
			if not width: default_width = 10
			
		cbox = ttk.Combobox(
				parent,
				textvariable = variable,
				values = values,
				width = default_width,
				state = cls.get_state(state),
				# postcommand = command,
				validate = 'all',
				validatecommand = (validate_command, cbox_type, '%S')
		)
		cbox.bind("<<ComboboxSelected>>", lambda e:[command()])
		cls.place_element(cbox, pos[0], pos[1], options = kwargs)
		cls.__elements_dict[cbox] = variable
		
		return cbox
	
	@classmethod
	def create_listbox(cls, parent, pos, text = None, command = None, state = 'n', mode = 'extended', width=40, height=10, **kwargs):
		"""
		Inserts listbox with a right-hand-side scroll.
		Selection is by default stored to be retrieved with a .get_element_value() command.
		Right mouse click clears whole selection.
		
		:param parent: ttk parent
		:param text: if used, the Listbox will initiate with the text
		:param command: if set, the widget will have the .bind assigned to it which will launch the command
		:param pos: (x, y)-- x - column
							 y - row
		:param state: (optional) state of the listbox:
			'n' - Normal
			'd' - Disabled
		:param mode: (optional):
			'browse' - click&drag will make the selection following the mouse, does not expand selection
			'single' - only one line can be selected at a time, used as default
			'multiple' - many lines can be selected at once
			'extended' - clik&drag will expand the selection
		:param width: width of listbox - in characters, default is 40
		:param height: height of listbox - in lines, default is 10
		:param kwargs: optional arguments:
				xs - columnspan
				ys - rowspan
				px - padx
				py - pady
				ix - ipadx
				iy - ipady
				s - sticky
		:return button: generated label
		"""
		variable = StringVar()
		frame = ttk.Frame(parent)
		cls.place_element(frame, pos[0], pos[1], options=kwargs)
		listbox = Listbox(frame, listvariable = variable, state = cls.get_state(state), selectmode = mode, width = width, height = height)
		yscroll = Scrollbar(frame, orient = VERTICAL, command = listbox.yview)
		# self.scroll.grid(column = 4, row = 9, sticky = N+E+S, pady = (10, 0))
		listbox.configure(yscrollcommand = yscroll.set)
		cls.place_element(listbox, 0, 0, options={'s': 'news'})
		cls.place_element(yscroll, 0, 0, options = {'py': 1, 's': 'nes'})
		
		if text:
			for line in text:
				listbox.insert(END, line)
				
		def get_selection():
			cls.__elements_dict[listbox] = listbox.curselection()
			
		def clear_selection(e):
			listbox.selection_clear(0, END)
			
		if command:
			listbox.bind('<ButtonRelease>', lambda e:[get_selection(), command()])		# releasing the mouse button will store the selected line(s)
		else:
			listbox.bind('<ButtonRelease>', lambda e: get_selection())
		
		listbox.bind('<Button-3>', clear_selection)
		
		return listbox
	
	@classmethod
	def create_radiobutton(cls, parent, pos, arr, count, text, label = (None, None), command = None, state = 'n', width = 12, **kwargs):
		"""
		Inserts a number of radio buttons in a row or columns.

		:param parent: ttk parent
		:param pos: (x, y)--
				x - column
				y - row
		:param arr: arrangement of the radio buttons--
				'h' - horizontal
				'v' - vertical
		:param count: how many radio buttons
		:param text: text to appear next to radio buttons, given as a list
		:param label: (optional) (text, location) if given, the label will be attached to the radio buttons group--
				text - text of the label
				l or t - l: for label to the left of the group, t: for label on the top of the group
		:param command: (optional) command to be launch every time the state of this radiobutton changes
		:param state: (optional) state of the listbox:
			'n' - normal
			'd' - disabled
		:param width: width of text on a radio buttons - in characters, default is 12
		:param kwargs: optional arguments:
				xs - columnspan
				ys - rowspan
				px - padx
				py - pady
				ix - ipadx
				iy - ipady
				s - sticky
		:return r_button: returns a list of all created radio buttons
		"""
		variable = StringVar(value = text[0])
		r_button = []
		col = 0
		row = 0
		frame = ttk.Frame(parent)
		cls.place_element(frame, pos[0], pos[1], options = kwargs)
		if label[0]:
			if label[1] == 'l':
				col = 1
				st = 'e'
			elif label[1] == 't':
				row = 1
				st = 'n'
				
		cls.create_label(frame, (0, 0), label[0], s=st, px=(0, 2)),
			
		for r in range(count):
			r_button.append(ttk.Radiobutton(
					frame,
					state = cls.get_state(state),
					width = width,
					variable = variable,
					value = text[r],
					text = text[r],
					command = command
			))
			cls.place_element(r_button[r], col, row, options = {'s': 'w'})
			if arr == 'h':
				col += 1
			elif arr == 'v':
				row += 1
		
		cls.__elements_dict[r_button[0]] = variable
		
		return r_button
		
	@staticmethod
	def validate_entry(entry_type, char):
		# print(char)
		is_valid = False
		if entry_type == 't':
			invalid_characters = '"~\\\''
			if char not in invalid_characters: is_valid = True
		else:
			is_valid = char.isnumeric()
			
		return is_valid

	@staticmethod
	def place_element(element, x, y, options = None):
		"""
		Takes the tk element and places it into a tk grid
		:param element: tk element
		:param x: column (taken from parent function)
		:param y: row (taken from parent function)
		:param options: additional arguments (taken from parent function)
		:return:
		"""
		arg = {
			'xs': 1,
			'ys': 1,
			'px': None,
			'py': None,
			'ix': None,
			'iy': None,
			's':  'w',
		}
		for key in arg.keys():
			if key in options:
				arg[key] = options[key]
		
		element.grid(
				column = x,
				row = y,
				columnspan = arg['xs'],
				rowspan = arg['ys'],
				padx = arg['px'],
				pady = arg['py'],
				ipadx = arg['ix'],
				ipady = arg['iy'],
				sticky = arg['s']
		)
	
	def start_program(self):
		self.__root.mainloop()
	
	def get_root(self):
		return self.__root
	
	def get_element_value(self, element):
		value = ''
		try:
			e = self.__elements_dict[element[0]]
		except TypeError:
			e = self.__elements_dict[element]
			
		try:
			value = e.get()
		except AttributeError:
			l = len(e)
			for r in range(l):
				value += str(e[r]) + ':'
				value += element.get(e[r])
				# print(item, l)
				if r + 1 != l:
					value += '|'
		
		return value
	
	def set_element_value(self, element, value):
		self.__elements_dict[element].set(value = value)
	
	@staticmethod
	def insert_value(element, value):
		if value != '' and value is not None:
			if isinstance(element, ttk.Combobox):
				v = []
				for item in element.cget('values'):
					v.append(item)
				v.append(value)
				element['values'] = v
				return True
			elif isinstance(element, Listbox):
				element.insert(END, value)
				return True
		else:
			return False
	
	@classmethod
	def change_element_state(cls, element, state):
		"""
		Changes state of the element to requested.
		:param state: desired state--
			'a' - active
			'n' - normal
			'r' - read only
			'd' - disabled
		:param element: tk widget
		"""
		
		try:
			# e = element[0]
			for e in range(len(element)):
				element[e].configure(state = cls.get_state(state))
		except TypeError:
			element.configure(state = cls.get_state(state))
	
	@staticmethod
	def get_state(shortcut):
		"""
		Helper method to act as ashortcut for widget states
		:param shortcut:
		:return:
		"""
		states = {
			'd': 'disabled',
			'n': 'normal',
			'r': 'readonly',
			'a': 'active'
		}
		return states[shortcut]
	
	def close_program(self):
		"""
		Closes the root window and therefore the application.
		"""
		self.__root.destroy()