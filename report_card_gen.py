
import functions
from functions import *

import emails
from emails import *

import shared
from shared import *

#import time
import subprocess
import stat
import socket
import sys
import threading

#gui
import customtkinter as ctk
#from tkinter import messagebox
from CTkMenuBar import *
from CTkMessagebox import CTkMessagebox
from CTkToolTip import CTkToolTip

app = None
msgbox = None
button = None
checkbox_settings = {}
CB_COUNT = 0

def run_gui():
	window_w = 600
	window_h = 600

	#Set the appearance mode and default color theme
	# Options: "Light", "Dark", "System" (default)
	ctk.set_appearance_mode("Dark")
	# Options: "blue" (default), "dark-blue", "green"
	ctk.set_default_color_theme("blue")

	#Create the main application window
	global app
	global msgbox

	app = ctk.CTk()
	app.title("Report card generator")
	geometry_str = str(window_w) + "x" + str(window_h) + "+450+50"
	app.geometry(geometry_str) # Set the window size and location

	menubar = CTkMenuBar(app)

	# Add a "File" button and a dropdown menu
	file_button = menubar.add_cascade("File")
	file_dropdown = CustomDropdownMenu(widget=file_button)
	file_dropdown.add_option(option="Set google drive folder IDs...", command=lambda: open_notepad_dir_ids())
	#file_dropdown.add_option(option="Open File", command=lambda: print("Open File"))
	file_dropdown.add_separator()
	file_dropdown.add_option(option="Exit", command=app.quit)

	file_button = menubar.add_cascade("Help")
	file_dropdown = CustomDropdownMenu(widget=file_button)
	file_dropdown.add_option(option="How to use", command=lambda: display_readme())
	file_dropdown.add_option(option="About this program", command=lambda: display_about())


	#Add a label widget to the window
	label = ctk.CTkLabel(app, text="Report card generator", font=("Helvetica", 15))
	label.pack(pady=20) # Use pack() to place the label in the window and add vertical padding


	cb_y_pad = 10
	cb_x_indent = 20
	checkbox("cb_fixfonts", "Fix fonts", 0, cb_y_pad,
		'Fix fonts and font sizes in all grades boxes')
	checkbox("cb_missing", "Prepare missing writeup report", 0, cb_y_pad,
		'Find all grade boxes with missing \'Notes\' sections, generate a report')
	cb_emailtch = checkbox("cb_emailtch", "Email teachers with missing reports",
	cb_x_indent, cb_y_pad,
		'Email all teachers which reports are missing')
	#cb_emailtch.deselect()
	#cb_emailtch.configure(state="disabled")
	checkbox("cb_gen_pdfs", "Generate PDFs", 0, cb_y_pad,
		'Generate PDFs of all report cards')
	'''cb_emailfams = checkbox("cb_emailfams", "Email report cards to families",
	0, cb_y_pad,
		'Email report cards to families')
	cb_emailfams.configure(state="disabled")
	cb_emailfams.deselect()
	'''

	global button
	button = ctk.CTkButton(master=app, text="Process report cards", command=process_report_card_button)
	button.pack(padx=200, pady=30)

	msgbox = ctk.CTkTextbox(app, width=window_w - 50, height=250)
	msgbox.pack(padx=10, pady=10, anchor='s')
	msgbox.configure(state="disabled")

	set_msg_callbacks()

	if not is_connected():
		response = CTkMessagebox(title="Failed to connect",
			message="Unable to connect to internet!", icon="warning", option_focus=1)
		response.get()
		sys.exit()

	authenticate_google_services()

	check_current_drive_folders()

	#Start the application loop
	# This method runs the application and waits for user interaction until the window is closed
	app.mainloop()



def email_wizard():
	global app

	window_w = 400
	window_h = 550
	emwiz = ctk.CTkToplevel(app)
	geometry_str = str(window_w) + "x" + str(window_h) + "+200+50"
	emwiz.geometry(geometry_str) # Set the window size and location
	#emwiz.geometry("400x300")
	emwiz.title("Email Config Wizard")

	#label = ctk.CTkLabel(emwiz, text="Auto emailer")
	#label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

	#add textboxes and labels
	box_x_off = 25
	box_w = window_w - (2*box_x_off)
	subjtxt = ctk.CTkLabel(emwiz, text="Subject:")
	subjtxt.pack(anchor='w', padx=box_x_off, pady=(20,5))
	subjbox = ctk.CTkTextbox(emwiz, width=box_w, height=30)
	subjbox.pack(padx=box_x_off, pady=(0,20), anchor='w')
	default_subject = shared.file_read_ifnot_create('user/default_email_subject.txt')
	subjbox.insert("0.0", default_subject)

	bodytxt = ctk.CTkLabel(emwiz, text="Body:")
	bodytxt.pack(anchor='w', padx=box_x_off, pady=(20,5))
	bodybox = ctk.CTkTextbox(emwiz, width=box_w, height=280)
	bodybox.pack(padx=box_x_off, pady=(0,12), anchor='w')
	default_body = shared.file_read_ifnot_create('user/default_email_body.txt')
	bodybox.insert("0.0", default_body)

	def save_to_template():
		shared.file_write('user/default_email_subject.txt', subjbox.get("0.0", "end"))
		shared.file_write('user/default_email_body.txt', bodybox.get("0.0", "end"))

	save_to_template_button = ctk.CTkButton(
		emwiz,
		text="Save to template",
		command=lambda: save_to_template()
	)
	save_to_template_button.pack(padx=10, pady=8)

	#function to populate text boxes
	subject = [None]
	body = [None]
	def wiz_close():
		subject[0] = subjbox.get("0.0", "end")
		body[0] = bodybox.get("0.0", "end")
		emwiz.destroy()

	close_button = ctk.CTkButton(
		emwiz,
		text="Confirm",
		command=lambda: wiz_close()
	)
	close_button.pack(anchor='s', pady=15)



	emwiz.wait_window()
	#print(f'subject: {subject[0]}')
	#sys.exit()
	return (subject[0], body[0])
	#return text from (subject, body)


def is_connected():
	try:
		# Connect to a public DNS server (1.1.1.1) on port 53 (DNS port)
		# using a short timeout to prevent hanging.
		socket.create_connection(("1.1.1.1", 53), timeout=3)
		return True
	except OSError:
		# If the connection fails, an OSError is raised.
		return False

def open_notepad_dir_ids():
	notepad_path = r"C:\Windows\System32\notepad.exe"
	process = subprocess.Popen([notepad_path, 'user/directory_ids'])
	process.wait()
	check_current_drive_folders()

def display_readme():
	notepad_path = r"C:\Windows\System32\notepad.exe"
	readme_path = 'docs/readme.txt'
	os.chmod(readme_path, stat.S_IREAD)
	process = subprocess.Popen([notepad_path, readme_path])
	process.wait()
	return

def display_about():
	about_msg = "Report card fixer/generator\nBy Mr. Sam, the dopest math/science teacher on the planet"
	response = CTkMessagebox(title="About",
		message=about_msg, icon="info", option_focus=1)
	response.get()

def check_current_drive_folders():
	folders_set = False

	load_directory_ids()
	folder_names = get_all_folder_names()
	msg_clear()
	if not folder_names:
		msg('No folders added.\nGet each folder ID by opening it in Google Drive, then copy the long string of characters after\nhttps://drive.google.com/drive/u/0/folders/\nThen go to File > Set google drive folder IDs to add those folder IDs\n')
	else:
		folders_set = True
		msg('Using google drive folders:')
		for fname in folder_names:
			msg(fname)
			msg('\nIf these are not the correct folders, Go to File > Set google drive folder IDs to add\nthe current folders')

	global button
	if folders_set:
		button.configure(state="normal")
	else:
		button.configure(state="disabled")



def checkbox(name, text, x, y, infotext):
	global app
	global checkbox_settings
	global CB_COUNT

	#checkbox_settings.append(ctk.BooleanVar(value=True))
	checkbox_settings[name] = ctk.BooleanVar(value=True)


	checkbox = ctk.CTkCheckBox(
		master=app,
		text=text,
		command=None,
		variable=checkbox_settings[name],
		onvalue=True,
		offvalue=False
	)
	checkbox.pack(padx=x+100, pady=y, anchor='w')
	CB_COUNT+=1

	#CustomTooltipLabel(anchor=checkbox, text="This is the information you asked for!", delay=0.5)
	tooltip = CTkToolTip(checkbox, message=infotext,
					 #delay=0,  # Optional: time delay in seconds before showing (default is 1)
					 #follow=True
	) # Optional: tooltip follows the mouse cursor (default is False)

	return checkbox

def msg(text, line="end"):
	global msgbox
	text += '\n'
	msgbox.configure(state="normal")

	#print(f'deleting from {line} to end')
	msgbox.insert(line, text)
	if not line == 'end':
		ln = float(line) + 1
		line = str(ln)
		#line = f'\"{ln}.0\"'
	msgbox.delete(line, "end")
	msgbox.configure(state="disabled")

def msg_overwrite_last(text):
	global msgbox
	lcnt = msgbox._textbox.count("1.0", "end", "displaylines")[0]
	#cntstr = f'\"{lcnt}.0\"'
	msg(text, int(lcnt))

def msg_clear():
	msgbox.configure(state="normal")
	msgbox.delete("1.0", "end")
	msgbox.configure(state="disabled")

'''def msg_clear(clearfrom="3.0"):
	print(f'clearing from {clearfrom} to end')
	#msgbox.configure(state="normal")
	if not clearfrom == "end":
		msgbox.delete(clearfrom, "end")
	#msgbox.configure(state="disabled")'''


def set_msg_callbacks():
	#global message
	functions.message = msg
	functions.message_clear = msg_clear
	functions.message_overwrite_last = msg_overwrite_last
	#return message_cb

def process_report_card_button():


	def task_wrapper():
		global checkbox_settings
		msg_clear()
		msg('Scanning all report cards...')
		(reports_ready, missing_entries) = process_all_report_cards(
			checkbox_settings["cb_fixfonts"].get(),
			checkbox_settings["cb_missing"].get())

		if checkbox_settings["cb_emailtch"].get():
			(subject, body) = email_wizard()
			emails.email_all_teachers(missing_entries, subject, body)

		#if we're trying to generate pdfs but we didn't
		#check for missing entries, prompt user
		if checkbox_settings["cb_gen_pdfs"].get():
			doitanyway = True
			if not checkbox_settings["cb_missing"].get():
				response = CTkMessagebox(title="Are you sure?",
					message='You didn\'t check for missing writeups.\nAre you sure you still want to generate PDFs?',
					icon="question", option_1="No", option_2="Yes")
				doitanyway = response.get()
			elif not reports_ready:
				response = CTkMessagebox(title="Are you sure?",
					message='Some report cards are missing writeups.\n(See generated/missing entries report.xlsx for details)\nAre you sure you still want to generate PDFs?',
					icon="question", option_1="No", option_2="Yes")
				doitanyway = response.get()
			print(f'doitanyway = {doitanyway}')

			if doitanyway == 'Yes':
				make_all_pdfs()

		CTkMessagebox(title="Info",
			message="Done!", icon="info", option_focus=1)

	# Create and start a new thread for the task
	thread = threading.Thread(target=task_wrapper)
	thread.start()

def main():
	run_gui()
	sys.exit()

if __name__ == "__main__":
	main()
