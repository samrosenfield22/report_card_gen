
#import functions
from functions import *

#gui
import customtkinter as ctk

app = None
checkbox_settings = None

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

	button = ctk.CTkButton(master=app, text="Process report cards", command=process_report_card_buttons)
	button.pack(padx=200, pady=40)

	global checkbox_settings
	checkbox_settings = [
		ctk.BooleanVar(value=True),
		ctk.BooleanVar(value=True)
	]
	checkbox("enable feature x", 150, checkbox_settings[0])
	checkbox("enable feature y", 180, checkbox_settings[1])


	#Start the application loop
	# This method runs the application and waits for user interaction until the window is closed
	app.mainloop()

def checkbox(text, y, var):
	global app
	# Variable to track state (on/off)
	#var = ctk.StringVar(value="on") # Default value

	checkbox = ctk.CTkCheckBox(
	    master=app,
	    text=text,
	    command=None,
	    variable=var,
	    onvalue=True,  # Value when checked
	    offvalue=False # Value when unchecked
	)
	checkbox.pack(padx=20, pady=y)

def process_report_card_buttons():
	#process_report_cards()
	global checkbox_settings
	for i, cb in enumerate(checkbox_settings):
		print(f'check box {i} set to {checkbox_settings[i].get()}')

def main():
	run_gui()
	exit()

if __name__ == "__main__":
	main()
