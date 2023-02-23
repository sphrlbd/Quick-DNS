import customtkinter
import os
import sys
import pyuac
import wmi
from PIL import Image


dns = {
    "Electro": ("78.157.42.100" ,"78.157.42.101"),
    "Shecan": ("178.22.122.100" ,"185.51.200.2"),
    "Radar Game": ("10.202.10.10" ,"10.202.10.11"),
    "403": ("10.202.10.202" ,"10.202.10.202"),
    "Cloud Flare": ("1.1.1.1" ,"1.0.0.1"),
    "Google": ("8.8.8.8" ,"8.8.4.4"),
    "Open DNS": ("208.67.222.222" ,"208.67.220.220"),
    "Comodo Group": ("8.26.56.26" ,"8.20.247.20"),
    "Quad9": ("9.9.9.9" ,"49.112.112.112"),
    "Verisign": ("64.6.64.6" ,"64.6.65.6"),
    "Alternate": ("76.76.19.19" ,"76.223.122.150"),
    "Clean browsing": ("185.228.168.9" ,"185.228.169.9"),
    "Neustar": ("156.154.70.5" ,"156.154.71.5"),
    "Safe DNS": ("195.46. 39.39" ,"195.46. 39.40"),
    "DYN": ("216.146.35.35" ,"216.146.36.36"),
    # "": ("" ,"")
}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = resource_path("Logo.png")

class App(customtkinter.CTk):
    width = 520
    height = 400

    def __init__(self):
        super().__init__()

        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        self.title("Quick DNS")
        self.iconbitmap(os.path.join(image_path, "app_icon.ico"))
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # status
        self.isConnect = False

        # current dns
        self.currentDns = list(dns.keys())[0]

        network_config = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
        for config in network_config:
            for key, value in dns.items():
                if config.DNSServerSearchOrder == value:
                    self.currentDns = key
                    self.isConnect = True

        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        # load images with light and dark mode image
        self.app_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "app_icon.png")), size=(26, 26))
        self.home_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")), dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(25, 25))
        self.about_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "about_dark.png")), dark_image=Image.open(os.path.join(image_path, "about_light.png")), size=(25, 25))

        self.power_disconnected_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "power_disconnected.png")), size=(150, 150))
        self.power_connecting_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "power_connecting.png")), size=(150, 150))
        self.power_connected_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "power_connected.png")), size=(150, 150))


        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" Quick DNS", image=self.app_icon, compound="left", font=customtkinter.CTkFont(family= "gg sans Bold",size=15))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.home_icon, anchor="w", command=self.home_button_event, font=customtkinter.CTkFont(family= "gg sans Bold",size=13))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.about_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="About", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.about_icon, anchor="w", command=self.about_button_event, font=customtkinter.CTkFont(family= "gg sans Bold",size=13))
        self.about_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event, font=customtkinter.CTkFont(family= "gg sans Bold",size=13))
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")


        # create home frame
        self.home_frame = customtkinter.CTkFrame(self)
        self.home_frame.grid_columnconfigure(2, weight=1)


        if self.isConnect:
            self.set_dns_button = customtkinter.CTkButton(self.home_frame, text="", image=self.power_connected_icon, anchor="center", hover=False, fg_color= "transparent", width=150, height=150, command=self.set_dns_event)
            self.set_dns_button.grid(row=1, column=0, columnspan=2, padx=20, pady=30)

            self.state_label = customtkinter.CTkLabel(self.home_frame, text=f"Connected to {self.currentDns}", font=customtkinter.CTkFont(family= "gg sans Bold",size=16))
            self.state_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

            self.progressbar = customtkinter.CTkProgressBar(self.home_frame, progress_color="#77e171", mode="determinate")
            self.progressbar.grid(row=3, column=0, columnspan=2, padx=(20, 10), pady=(10, 10), sticky="ew")

        else:
            self.set_dns_button = customtkinter.CTkButton(self.home_frame, text="", image=self.power_disconnected_icon, anchor="center", hover=False, fg_color= "transparent", width=150, height=150, command=self.set_dns_event)
            self.set_dns_button.grid(row=1, column=0, columnspan=2, padx=20, pady=30)

            self.state_label = customtkinter.CTkLabel(self.home_frame, text="Disconnected", font=customtkinter.CTkFont(family= "gg sans Bold",size=16))
            self.state_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

            self.progressbar = customtkinter.CTkProgressBar(self.home_frame, progress_color="#c13c44", mode="determinate")
            self.progressbar.grid(row=3, column=0, columnspan=2, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.appearance_dns_menu = customtkinter.CTkOptionMenu(self.home_frame, values=list(dns.keys()), command=self.select_dns_event, width=250, height=35, dropdown_font=customtkinter.CTkFont(family= "gg sans Bold", size=15, weight="bold"), font=customtkinter.CTkFont(family= "gg sans Bold", size=15, weight="bold"))
        self.appearance_dns_menu.grid(row=4, column=0, padx=20, pady=20, sticky="s")
        
        self.progressbar.set(1)


        # create about frame
        self.about_frame = customtkinter.CTkFrame(self)
        self.about_frame.grid_columnconfigure(0, weight=1)
        
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.about_frame, text="Version: 1.2 \nGitHub: github.com/1SPHR1/Quick-DNS", font=customtkinter.CTkFont(family= "gg sans Bold", size=14))
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=60)
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.about_frame, text="Developed with 💗 by SLaSH", font=customtkinter.CTkFont(family= "gg sans Bold", size=16, weight="bold"))
        self.home_frame_large_image_label.grid(row=1, column=0, padx=20, pady=(100, 20))
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.about_frame, text="Discord: SLaSH#4474 \nGitHub: github.com/1SPHR1", font=customtkinter.CTkFont(family= "gg sans Bold", size=14))
        self.home_frame_large_image_label.grid(row=2, column=0, padx=20, pady=10)

        # select default frame
        self.select_frame_by_name("home")



    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.about_button.configure(fg_color=("gray75", "gray25") if name == "about" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "about":
            self.about_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        else:
            self.about_frame.grid_forget()



    def home_button_event(self):
        self.select_frame_by_name("home")

    def about_button_event(self):
        self.select_frame_by_name("about")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def select_dns_event(self, selectedDns):
        self.currentDns = selectedDns


    def connect(self):
            self.set_dns_button.configure(image=self.power_connected_icon)
            self.state_label.configure(text=f"Connected to {self.currentDns}")
            self.progressbar.configure(progress_color="#77e171", mode="determinate")
            self.progressbar.stop()
            
            network_config = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
            for config in network_config:
                config.SetDNSServerSearchOrder(dns[self.currentDns])
                
            self.isConnect = True
    def disconnect(self):
            self.set_dns_button.configure(image=self.power_disconnected_icon)
            self.state_label.configure(text="Disconnected")
            self.progressbar.configure(progress_color="#c13c44", mode="determinate")
            self.progressbar.stop()

            network_config = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
            for config in network_config:
                config.SetDNSServerSearchOrder([])

            self.isConnect = False

    def connecting(self):
            self.set_dns_button.configure(image=self.power_connecting_icon)
            self.state_label.configure(text="Connecting")
            self.progressbar.configure(progress_color="#f99627", mode="indeterminnate")
            self.progressbar.start()

    def disconnecting(self):
            self.set_dns_button.configure(image=self.power_connecting_icon)
            self.state_label.configure(text="Disconnecting")
            self.progressbar.configure(progress_color="#f99627", mode="indeterminnate")
            self.progressbar.start()



    def set_dns_event(self):
        if self.isConnect :
            self.disconnecting()
            self.after(1500, self.disconnect)
        else:
            self.connecting()
            self.after(3000, self.connect)
    


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        app = App()
        app.mainloop()
