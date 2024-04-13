# from scraping import *
from extraction import *
import customtkinter
import os
import threading
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

customtkinter.set_default_color_theme("blue")
 
class App(customtkinter.CTk):
    APP_NAME = "Epaper Scraper"
    WIDTH = 1400
    HEIGHT = 800
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window properties
        INITIAL_WIDTH = self.winfo_screenwidth()
        INITIAL_HEIGHT = self.winfo_screenheight()
        self.title(App.APP_NAME)
        self.geometry(str(INITIAL_WIDTH) + "x" + str(INITIAL_HEIGHT) + "+0+0")
        self.minsize(App.WIDTH, App.HEIGHT)
        
        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)  # Left panel will not resize in the x direction when the screen is resized
        self.grid_columnconfigure(1, weight=1) # Right panel will resize in the x direction when the screen is resized
        self.grid_rowconfigure(0, weight=1)  # Both panels will resize in the y direction when the screen is resized

        # Left panel attach
        self.frame_left = customtkinter.CTkFrame(master=self, width=100, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Right panel attach
        self.frame_right = customtkinter.CTkTabview(master=self, corner_radius=10)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")
        

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(25, weight=1)
        
                # ============ frame_left optimizer ============
        self.logo_label = customtkinter.CTkLabel(self.frame_left, text=App.APP_NAME, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.subframe_optimizer = customtkinter.CTkFrame(master=self.frame_left)
        self.subframe_optimizer.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew", rowspan=5)
        self.subframe_optimizer_label = customtkinter.CTkLabel(master=self.subframe_optimizer, text="Optimizer Functions")
        self.subframe_optimizer_label.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="")
        
        # Start process button
        self.button_1 = customtkinter.CTkButton(master=self.subframe_optimizer,
                                                text="Start Loading Data")
        self.button_1.grid(pady=(0, 0), padx=(20, 20), row=2, column=0)
        
        # View Heatmap button
        self.button_2 = customtkinter.CTkButton(master=self.subframe_optimizer, state="disabled",
                                                text="View Heatmap")
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=3, column=0)
        
        # View Cluster button
        self.button_3 = customtkinter.CTkButton(master=self.subframe_optimizer, state="disabled",
                                                text="View Cluster")
        self.button_3.grid(pady=(20, 0), padx=(20, 20), row=4, column=0)
        
        # View Tower button
        self.button_4 = customtkinter.CTkButton(master=self.subframe_optimizer, state="disabled",
                                                text="View Tower")
        self.button_4.grid(pady=(20, 20), padx=(20, 20), row=5, column=0)

                # ============ frame_left misc. ============
        # Section for selecting map type
        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=22, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=[ "Google normal", "OpenStreetMap", "Google satellite"])
        self.map_option_menu.grid(row=23, column=0, padx=(20, 20), pady=(10, 0))

        # Section for selecting theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=25, column=0, padx=(20, 20), pady=(20, 0), sticky='n')
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=25, column=0, padx=(20, 20), pady=(100, 20), sticky='s')

        # ============ frame_right ============
        
        self.frame_right.add("Map")  
        self.frame_right.add("Plot")
        
        # Map tab
        self.frame_right.tab("Map").grid_rowconfigure(1, weight=1)
        self.frame_right.tab("Map").grid_rowconfigure(0, weight=0)
        self.frame_right.tab("Map").grid_columnconfigure(0, weight=1)
        self.frame_right.tab("Map").grid_columnconfigure(1, weight=0)
        self.frame_right.tab("Map").grid_columnconfigure(2, weight=1)
        
        # Plot tab
        self.frame_right.tab("Plot").grid_rowconfigure(1, weight=1)
        self.frame_right.tab("Plot").grid_rowconfigure(0, weight=0)
        self.frame_right.tab("Plot").grid_columnconfigure(0, weight=1)
        self.frame_right.tab("Plot").grid_columnconfigure(1, weight=0)
        self.frame_right.tab("Plot").grid_columnconfigure(2, weight=1)
        
        # Map widget
        # self.map_widget = TkinterMapView(self.frame_right.tab("Map"), corner_radius=0)
        # self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        # Entry field and button
        self.entry = customtkinter.CTkEntry(master=self.frame_right.tab("Map"),
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)          # Run search_event() function on enter press

        self.search = customtkinter.CTkButton(master=self.frame_right.tab("Map"),
                                                text="Search",
                                                width=90)
        self.search.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)
        
        # Reset button
        self.button_reset = customtkinter.CTkButton(master=self.frame_right.tab("Map"),
                                                text="Reset Map")
        self.button_reset.grid(pady=(0, 0), padx=(20, 20), row=0, column=2, sticky="e")

    # Search bar
    def search_event(self, event=None):
        # self.map_widget.set_address(self.entry.get())
        pass
       
    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("image_example.py")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(BASE_DIR, "resources")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    t = threading.Thread()
    t.start()
    app.start()