# from scraping import *
from extraction import *
import customtkinter
import os
import threading
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

customtkinter.set_default_color_theme("blue")
 
PY2 = sys.version_info[0] == 2

class Reloader(object):

    RELOADING_CODE = 3
    def start_process(self):
        while True:
            print("Starting CTk application...")

            args = [sys.executable] + sys.argv
            env = os.environ.copy()
            env['TKINTER_MAIN'] = 'true'

            if os.name == 'nt' and PY2:
                for key, value in env.iteritems():
                    env[key] = value.encode('iso-8859-1')

            exit_code = subprocess.call(args, env=env,
                                        close_fds=False)
            if exit_code != self.RELOADING_CODE:
                return exit_code

    def trigger_reload(self):
        self.log_reload()
        sys.exit(self.RELOADING_CODE)

    def log_reload(self):
        print("Reloading...")

def run_with_reloader(root, *hotkeys):
    """Run the given application in an independent python interpreter."""
    import signal
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    reloader = Reloader()
    try:
        if os.environ.get('TKINTER_MAIN') == 'true':

            for hotkey in hotkeys:
                root.bind_all(hotkey, lambda event: reloader.trigger_reload())
                
            if os.name == 'nt':
                root.wm_state("iconic")
                root.wm_state("zoomed")

            root.start()
        else:
            sys.exit(reloader.start_process())
    except KeyboardInterrupt:
        pass

class App(customtkinter.CTk):
    APP_NAME = "Epaper Scraper"
    WIDTH = 1400
    HEIGHT = 800
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window properties
        self.title(App.APP_NAME)
        # INITIAL_WIDTH = self.winfo_screenwidth()
        # INITIAL_HEIGHT = self.winfo_screenheight()
        # self.geometry(str(INITIAL_WIDTH) + "x" + str(INITIAL_HEIGHT) + "+0+0")
        self.minsize(App.WIDTH, App.HEIGHT)
        self._state_before_windows_set_titlebar_color = 'zoomed'
        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(BASE_DIR, "resources")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        
        self.jugantor_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "jugantor.jpg")), size=(130, 35))
        self.jugantor_img_lg = customtkinter.CTkImage(Image.open(os.path.join(image_path, "jugantor.jpg")), size=(500, 150))
        self.prothomalo_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "prothom_alo.png")), size=(130, 35))
        self.prothomalo_img_lg = customtkinter.CTkImage(Image.open(os.path.join(image_path, "prothom_alo.png")), size=(500, 150))
        self.kalkerkantho_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "kaler_kantho.png")), size=(130, 35))
        self.kalkerkantho_img_lg = customtkinter.CTkImage(Image.open(os.path.join(image_path, "kaler_kantho.png")), size=(500, 150))
        
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

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=self.APP_NAME, 
                                                             compound="left", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        # jugantor
        self.jugantor_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.jugantor_img, anchor="w", command=self.jugantor_button_event)
        self.jugantor_button.grid(row=1, column=0, sticky="ew")

        self.prothomalo_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.prothomalo_img, anchor="w", command=self.prothomalo_button_event)
        self.prothomalo_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.kalkerkantho_img, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # ======================== jugantor frame ==============================
        self.jugantor_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.jugantor_frame.grid_columnconfigure(0, weight=1)

        self.jugantor_frame_large_image_label = customtkinter.CTkLabel(self.jugantor_frame, text="", image=self.jugantor_img_lg)
        self.jugantor_frame_large_image_label.grid(row=0, column=0, padx=20, pady=50)

        # self.jugantor_frame_button_1 = customtkinter.CTkButton(self.jugantor_frame, text="", image=self.image_icon_image)
        # self.jugantor_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.jugantor_frame_button_2 = customtkinter.CTkButton(self.jugantor_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        # self.jugantor_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.jugantor_frame_button_3 = customtkinter.CTkButton(self.jugantor_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        # self.jugantor_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.jugantor_frame_button_4 = customtkinter.CTkButton(self.jugantor_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        # self.jugantor_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # ======================== prothomalo frame ==============================
        self.prothomalo_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.prothomalo_frame.grid_columnconfigure(0, weight=1)
        self.prothomalo_frame.grid_rowconfigure((0), weight=0)
        self.prothomalo_frame.grid_rowconfigure((1), weight=1)
        self.prothomalo_frame.grid_rowconfigure((2, 3), weight=2)
        
        self.prothomalo_frame_large_image_label = customtkinter.CTkLabel(self.prothomalo_frame, text="", image=self.prothomalo_img_lg)
        self.prothomalo_frame_large_image_label.grid(row=0, column=0, padx=20, pady=50)
        
        self.prothomalo_subframe1 = customtkinter.CTkFrame(self.prothomalo_frame, corner_radius=0, fg_color="black")
        self.prothomalo_subframe1.grid(row=1, column=0, sticky="nsew")
        self.prothomalo_subframe1.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.prothomalo_subframe1.grid_rowconfigure((0), weight=1)
        
        self.test_button = customtkinter.CTkButton(self.prothomalo_subframe1)
        self.test_button.grid(row=0, column=3)
        
        self.prothomalo_subframe2 = customtkinter.CTkFrame(self.prothomalo_frame, corner_radius=0, fg_color="white")
        self.prothomalo_subframe2.grid(row=2, column=0, sticky="nsew")
        self.prothomalo_subframe3 = customtkinter.CTkFrame(self.prothomalo_frame, corner_radius=0, fg_color="black")
        self.prothomalo_subframe3.grid(row=3, column=0, sticky="nsew")


        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_large_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.kalkerkantho_img_lg)
        self.third_frame_large_image_label.grid(row=0, column=0, padx=20, pady=50)

        # select default frame
        self.select_frame_by_name("prothomalo")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.jugantor_button.configure(fg_color=("gray75", "gray25") if name == "jugantor" else "transparent")
        self.prothomalo_button.configure(fg_color=("gray75", "gray25") if name == "prothomalo" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "jugantor":
            self.jugantor_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.jugantor_frame.grid_forget()
        if name == "prothomalo":
            self.prothomalo_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.prothomalo_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def jugantor_button_event(self):
        self.select_frame_by_name("jugantor")

    def prothomalo_button_event(self):
        self.select_frame_by_name("prothomalo")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    # app = App()
    # t = threading.Thread()
    # t.start()
    run_with_reloader(App(), "<Control-R>", "<Control-r>")
    