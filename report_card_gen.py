
import functions
from functions import *
#import time
import subprocess
import socket

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
msg_pending = ''

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
	file_dropdown.add_option(option="About rcg", command=lambda: print("mr sam is the coolest on the planet"))


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
	cb_emailtch.configure(state="disabled")
	checkbox("cb_gen_pdfs", "Generate PDFs", 0, cb_y_pad,
		'Generate PDFs of all report cards')
	cb_emailfams = checkbox("cb_emailfams", "Email report cards to families",
	0, cb_y_pad,
		'Email report cards to families')
	cb_emailfams.configure(state="disabled")

	global button
	button = ctk.CTkButton(master=app, text="Process report cards", command=process_report_card_button)
	button.pack(padx=200, pady=30)

	msgbox = ctk.CTkTextbox(app, width=window_w - 50, height=250)
	msgbox.pack(padx=10, pady=10, anchor='s')

	set_msg_callback()

	if not is_connected():
		response = CTkMessagebox(title="Failed to connect",
			message="Unable to connect to internet!", icon="warning", option_focus=1)
		response.get()
		quit()

	authenticate_google_services()

	check_current_drive_folders()

	app.after(10, update_textbox)

	#Start the application loop
	# This method runs the application and waits for user interaction until the window is closed
	app.mainloop()


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
	process = subprocess.Popen([notepad_path, 'directory_ids'])
	process.wait()
	print('closed notepad')
	check_current_drive_folders()

def check_current_drive_folders():
	folders_set = False

	load_directory_ids()
	folder_names = get_all_folder_names()
	msgbox_clear()
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

def msgbox_clear():
	msgbox.delete("1.0", "end")

def update_textbox():
	global msgbox, msg_pending
	#textbox.see("end")



	#print('yeah!')
	#msgbox.delete("1.0", "end")
	msgbox.insert("end", msg_pending)
	msgbox.see("end")
	msg_pending = ''

	app.update()

	# Re-schedule the function to run again after 1000ms (1 second)
	app.after(10, update_textbox)

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

def msg(text):
	global msgbox
	text += '\n'
	msgbox.configure(state="normal")
	msgbox.insert("end", text)

def message_cb_func(text):
	global msg_pending

	mystr = text + '\n'
	msg_pending += mystr


def set_msg_callback():
	#global message
	functions.message = message_cb_func
	#return message_cb

def process_report_card_button():
	global checkbox_settings
	msgbox_clear()
	msg('Scanning all report cards...')
	reports_ready = process_all_report_cards(
		checkbox_settings["cb_fixfonts"].get(),
		checkbox_settings["cb_missing"].get())

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
		#print(f'doitanyway = {doitanyway}')
		if doitanyway:
			make_all_pdfs()

	CTkMessagebox(title="Info",
		message="Done!", icon="info", option_focus=1)
	msg('Report PDFs saved to /generated/PDFs')

def main():
	run_gui()
	exit()

if __name__ == "__main__":
	main()
