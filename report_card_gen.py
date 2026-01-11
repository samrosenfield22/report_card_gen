
#import functions
from functions import *

#gui
import customtkinter as ctk

def run_gui():
	import customtkinter as ctk

	#Set the appearance mode and default color theme
	# Options: "Light", "Dark", "System" (default)
	ctk.set_appearance_mode("Dark")
	# Options: "blue" (default), "dark-blue", "green"
	ctk.set_default_color_theme("blue")

	#Create the main application window
	app = ctk.CTk()
	app.title("Report card generator")
	app.geometry("600x600") # Set the window size

	#Add a label widget to the window
	label = ctk.CTkLabel(app, text="Report card generator", font=("Helvetica", 20))
	label.pack(pady=30) # Use pack() to place the label in the window and add vertical padding

	button = ctk.CTkButton(master=app, text="Process report cards", command=process_report_card_buttons)
	button.pack(padx=200, pady=40)

	#Start the application loop
	# This method runs the application and waits for user interaction until the window is closed
	app.mainloop()

def process_report_card_buttons():
	process_report_cards()

def main():
	run_gui()
	exit()

if __name__ == "__main__":
	main()
