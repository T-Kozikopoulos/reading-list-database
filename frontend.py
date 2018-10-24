from tkinter import *
from backend import Database


# Load the data.
database = Database("books.db")


# Creating the window class.
class Window(object):

	def __init__(self, window):
		self.window = window
		self.window.wm_title("BookStore")

		# Labels.
		l1 = Label(window, text='Title')
		l1.grid(row=0, column=0)

		l2 = Label(window, text='Author')
		l2.grid(row=0, column=2)

		l3 = Label(window, text='Year')
		l3.grid(row=1, column=0)

		l4 = Label(window, text='ISBN')
		l4.grid(row=1, column=2)

		# Entries.
		self.title_text = StringVar()
		self.e1 = Entry(window, textvariable=self.title_text)
		self.e1.grid(row=0, column=1)

		self.author_text = StringVar()
		self.e2 = Entry(window, textvariable=self.author_text)
		self.e2.grid(row=0, column=3)

		self.year_text = StringVar()
		self.e3 = Entry(window, textvariable=self.year_text)
		self.e3.grid(row=1, column=1)

		self.isbn_text = StringVar()
		self.e4 = Entry(window, textvariable=self.isbn_text)
		self.e4.grid(row=1, column=3)

		# List box and scroll bar for it.
		self.lb = Listbox(window, height=8, width=40)
		self.lb.grid(row=2, column=0, rowspan=8, columnspan=2)

		sb = Scrollbar(window)
		sb.grid(row=2, column=2, rowspan=8)

		self.lb.configure(yscrollcommand=sb.set)
		sb.configure(command=self.lb.yview)

		self.lb.bind('<<ListboxSelect>>', self.get_selected_row)

		# Buttons.
		b1=Button(window, text='View All', width=14, command=self.view_command)
		b1.grid(row=2, column=3)

		b2=Button(window, text='Search', width=14, command=self.search_command)
		b2.grid(row=3, column=3)

		b3=Button(window, text='Add New', width=14, command=self.add_command)
		b3.grid(row=4, column=3)

		b4=Button(window, text='Update Selected', width=14, command=self.update_command)
		b4.grid(row=5, column=3)

		b4=Button(window, text='Delete Selected', width=14, command=self.delete_command)
		b4.grid(row=6, column=3)

		b5=Button(window, text='Close', width=14, command=window.destroy)
		b5.grid(row=7, column=3)

	# Helper for when selecting items from the list is needed.
	def get_selected_row(self, event):
		try:
			index = self.lb.curselection()[0]
			self.selected_tuple = self.lb.get(index)
			self.e1.delete(0, END)
			self.e1.insert(END, self.selected_tuple[1])
			self.e2.delete(0, END)
			self.e2.insert(END, self.selected_tuple[2])
			self.e3.delete(0, END)
			self.e3.insert(END, self.selected_tuple[3])
			self.e4.delete(0, END)
			self.e4.insert(END, self.selected_tuple[4])
		# Bypass useless index error.
		except IndexError:
			pass

	# Adding functionality to the buttons.
	def view_command(self):
		self.lb.delete(0 ,END)
		for row in database.view():
			self.lb.insert(END,row)

	def search_command(self):
		self.lb.delete(0, END)
		for row in database.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
			self.lb.insert(END, row)

	def add_command(self):
		database.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
		self.lb.delete(0, END)
		self.lb.insert(END, (self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()))

	def delete_command(self):
		database.delete(self.selected_tuple[0])

	def update_command(self):
		database.update(self.selected_tuple[0], self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())


# Creating the window object.
window = Tk()
Window(window)

# All done!
window.mainloop()
