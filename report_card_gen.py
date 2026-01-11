
#import functions
from functions import *

#gui
import customtkinter as ctk
#from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
from CTkToolTip import CTkToolTip

app = None
checkbox_settings = {}
CB_COUNT = 0

def run_gui():
	import customtkinter as ctk

	#Set the appearance mode and default color theme
	# Options: "Light", "Dark", "System" (default)
	ctk.set_appearance_mode("Dark")
	# Options: "blue" (default), "dark-blue", "green"
	ctk.set_default_color_theme("blue")

	#Create the main application window
	global app
	app = ctk.CTk()
	app.title("Report card generator")
	app.geometry("600x600") # Set the window size

	#Add a label widget to the window
	label = ctk.CTkLabel(app, text="Report card generator", font=("Helvetica", 20))
	label.pack(pady=30) # Use pack() to place the label in the window and add vertical padding


	cb_y_pad = 10
	checkbox("cb_fixfonts", "Fix fonts", cb_y_pad,
		'Fix fonts and font sizes in all grades boxes')
	checkbox("cb_missing", "Prepare missing writeup report", cb_y_pad,
		'Find all grade boxes with missing \'Notes\' sections, generate a report')
	checkbox("cb_gen_pdfs", "Generate PDFs", cb_y_pad,
		'Generate PDFs of all report cards')

	button = ctk.CTkButton(master=app, text="Process report cards", command=process_report_card_buttons)
	button.pack(padx=200, pady=30)


	#Start the application loop
	# This method runs the application and waits for user interaction until the window is closed
	app.mainloop()

def checkbox(name, text, y, infotext):
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
	checkbox.pack(padx=100, pady=y, anchor='w')
	CB_COUNT+=1

	#CustomTooltipLabel(anchor=checkbox, text="This is the information you asked for!", delay=0.5)
	tooltip = CTkToolTip(checkbox, message=infotext,
					 #delay=0,  # Optional: time delay in seconds before showing (default is 1)
					 #follow=True
	) # Optional: tooltip follows the mouse cursor (default is False)

def process_report_card_buttons():
	global checkbox_settings
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
				message='Some report cards are missing writeups.\n(See the missing entries report in /generated for details)\nAre you sure you still want to generate PDFs?',
				icon="question", option_1="No", option_2="Yes")
			doitanyway = response.get()
		print(f'doitanyway = {doitanyway}')
		if doitanyway:
			make_all_pdfs()

	msg = CTkMessagebox(title="Info",
		message="Done!", icon="info", option_focus=1)


def main():
	run_gui()
	exit()

if __name__ == "__main__":
	main()
