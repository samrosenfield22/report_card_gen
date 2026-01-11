
#import functions
from functions import *

#gui
import customtkinter as ctk

app = None
checkbox_settings = []
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



	#global checkbox_settings
	#checkbox_settings = [
	#	ctk.BooleanVar(value=True),
	#	ctk.BooleanVar(value=True),
	#	ctk.BooleanVar(value=True)
	#]
	cb_y_pad = 10
	checkbox("Fix fonts", cb_y_pad)
	checkbox("Prepare missing writeup report", cb_y_pad)
	checkbox("Generate PDFs", cb_y_pad)

	button = ctk.CTkButton(master=app, text="Process report cards", command=process_report_card_buttons)
	button.pack(padx=200, pady=30)


	#Start the application loop
	# This method runs the application and waits for user interaction until the window is closed
	app.mainloop()

def checkbox(text, y):
	global app
	global checkbox_settings
	global CB_COUNT

	checkbox_settings.append(ctk.BooleanVar(value=True))

	checkbox = ctk.CTkCheckBox(
	    master=app,
	    text=text,
	    command=None,
	    variable=checkbox_settings[CB_COUNT],
	    onvalue=True,
	    offvalue=False
	)
	checkbox.pack(padx=100, pady=y, anchor='w')
	CB_COUNT+=1

def process_report_card_buttons():
	global checkbox_settings
	process_all_report_cards(checkbox_settings[0].get(),
		checkbox_settings[1].get(),
		checkbox_settings[2].get())

	#for i, cb in enumerate(checkbox_settings):
	#	print(f'check box {i} set to {checkbox_settings[i].get()}')

def main():
	run_gui()
	exit()

if __name__ == "__main__":
	main()
