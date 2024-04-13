# from scraping import *
from extraction import *
import customtkinter
import os
import threading
import subprocess

# Absolute path to the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        self.appearance_mode_label.grid(row=25, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=25, column=0, padx=(20, 20), pady=(100, 20))

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

        # Set default values
        # self.map_widget.set_address("Dhaka")
        # self.map_option_menu.set("Google normal") 
        # self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        # self.appearance_mode_optionemenu.set("Dark")

    # Search bar
    def search_event(self, event=None):
        # self.map_widget.set_address(self.entry.get())
        pass
    
    def raw_load(self):
        target_location = os.path.join(BASE_DIR, "raw")     # Define the target directory path
        if os.path.exists(target_location):
            contents = os.listdir(target_location)
            merged_data = pd.DataFrame()
            dataframes = []     # Initialize an empty list to store DataFrames
            
            # Iterate over files in the directory
            for file_name in contents:
                print(file_name)
                file_path = os.path.join(target_location, file_name)
                df = pd.read_csv(file_path)
                dataframes.append(df)           # Append the DataFrame to the list   
                    
            merged_data = pd.concat(dataframes, ignore_index=True)      # Concatenate all DataFrames into one
            output_file = os.path.join(BASE_DIR, 'optimizer', 'final_data.csv')
            merged_data.to_csv(output_file, index=False, header=['lat', 'lng', 'csq'])
            
            filter()        # Filter the data
            
            # Enable other 3 buttons
            self.button_2.configure(state="normal")
            self.button_3.configure(state="normal")
            self.button_4.configure(state="normal")
        else:
            print(f"The location {target_location} does not exist.")
            
    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # def change_map(self, new_map: str):
    #     # Set the tile server URL for three maps
    #     if new_map == "OpenStreetMap":          
    #         self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    #     elif new_map == "Google normal":
    #         self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    #     elif new_map == "Google satellite":
    #         self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
     
    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    t = threading.Thread()
    t.start()
    app.start()