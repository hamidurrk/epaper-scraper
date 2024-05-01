from tkcalendar import Calendar
import customtkinter as ctk
from tkinter import ttk
# from datetime import date
# import ttkbootstrap as tb
# from ttkbootstrap.dialogs import Querybox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("550x400")
# Function to update the label with selected date
def update_date(event):
    selected_date = cal.get_date()
    day, month, year = map(int, selected_date.split('/'))
    # Update label text with selected date
    date_label.configure(text=f"Selected Date: {day}-{month}-{year}")

frame = ctk.CTkFrame(root)
frame.pack(fill="both", padx=10, pady=10, expand=True)

style = ttk.Style(root)
style.theme_use("default")

cal = Calendar(frame, selectmode='day', locale='en_US', disabledforeground='red',
               cursor="hand2", background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
               selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1], date_pattern="d/m/y")
cal.pack(fill="both", expand=True, padx=10, pady=10)

# Bind callback function to the CalendarSelected event
cal.bind("<<CalendarSelected>>", update_date)

# Label to display selected date
date_label = ctk.CTkLabel(frame, text="Selected Date: ")
date_label.pack()
root.mainloop()