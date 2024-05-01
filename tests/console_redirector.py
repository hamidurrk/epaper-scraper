import customtkinter as ctk
import sys

def redirect_stdout_to_text_widget(text_widget):
    class StdoutRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, message):
            self.text_widget.insert("end", message)
            self.text_widget.see("end")

    sys.stdout = StdoutRedirector(text_widget)

# Create a CustomTkinter application
root = ctk.CTk()
root.geometry("600x400")

# Create a Text widget to display terminal output
output_text = ctk.CTkTextbox(root, wrap="word")
output_text.pack(fill="both", expand=True)

# Redirect stdout to the Text widget
redirect_stdout_to_text_widget(output_text)

for _ in range(400):  
    print("Hello World")
# Run the application
root.mainloop()
