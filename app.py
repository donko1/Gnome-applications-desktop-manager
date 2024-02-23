
import customtkinter as ctk
import json
import os
from PIL import ImageTk
from manager import ApplicationManager

def restart_application():
    app.destroy()  
    main()  

def chooseTextByLanguage(ruText: str, enText: str, lang: str):
    if lang == "Русский":
        return ruText
    return enText

class Settings:
    def __init__(self):
        if not os.path.isfile('settings.json'):
            with open("settings.json", "w") as file:
                json.dump({"Language":"English", "ExtendedSettings": False}, file, indent=4)

        with open('settings.json', 'r') as file:
            self.data = json.load(file)
    
    def write_data(self, key, value):
        self.data[key] = value
        with open('settings.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_data(self, key):
        return self.data.get(key)

class MakeApplication(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()
        self.label = ctk.CTkLabel(self, text="Here u will make ur applications")
        self.label.pack()

class AllLocalApplications(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()
        self.label = ctk.CTkLabel(self, text="All Local Applications")
        self.label.pack()

class AllGlobalApplications(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()
        self.label = ctk.CTkLabel(self, text="All Global Applications")
        self.label.pack()

class Guide(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()
        self.label = ctk.CTkLabel(self, text="Guide")
        self.label.pack()

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()

        parent_frame = ctk.CTkFrame(self)
        parent_frame.pack(fill="both", padx=10, pady=10)
        
        self.language_frame = ctk.CTkFrame(parent_frame)
        self.language_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        self.label = ctk.CTkLabel(self.language_frame, text=chooseTextByLanguage("Язык", "Language", self.settings.get_data("Language")))
        self.label.pack(side="left", padx=30, pady=10)
        self.option_menu = ctk.CTkOptionMenu(self.language_frame, values=["English", "Русский"], command=self.changeLanguage)
        self.option_menu.pack(side="left", padx=5)
        self.option_menu.set(self.settings.get_data("Language"))

        self.checkbox_frame = ctk.CTkFrame(parent_frame)
        self.checkbox_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsw")
        self.checkbox_1 = ctk.CTkCheckBox(self.checkbox_frame, text=chooseTextByLanguage("Расширенные настройки(только для продвинутых пользователей)", "Extended settings(advanced users only)", self.settings.get_data("Language")), command=self.changeSettings)
        if self.settings.get_data("ExtendedSettings"):
            self.checkbox_1.select()
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def changeLanguage(self, arg):
        self.settings.write_data("Language", arg)
        restart_application()

    def changeSettings(self):
        self.settings.write_data("ExtendedSettings", bool(self.checkbox_1.get()))
        restart_application()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.language = "Ru"
        self.settings = Settings()

        self.title("Gnome applications manager")
        self.geometry("800x400") 

        menubar = ctk.CTkFrame(self)
        menubar.pack(side="top", fill="x")
        menubar.columnconfigure([0, 1, 2, 3, 4] if self.settings.get_data("ExtendedSettings") else [0, 1, 2, 3], weight=1)

        button_guide = ctk.CTkButton(menubar, text=chooseTextByLanguage("Гайд", "Guide", self.settings.get_data("Language")), command=self.open_guide)
        button_guide.grid(row=0, column=0, padx=10, pady=5)

        button_local = ctk.CTkButton(menubar, text=chooseTextByLanguage("Локальные\nприложения" if self.settings.get_data("ExtendedSettings") else "Приложения", "Local\napplications" if self.settings.get_data("ExtendedSettings") else "Applications", self.settings.get_data("Language")), command=self.open_local)
        button_local.grid(row=0, column=1, padx=10, pady=5)

        button_global = ctk.CTkButton(menubar, text=chooseTextByLanguage("Глобальные\nприложения", "Global\napplications", self.settings.get_data("Language")), command=self.open_global)
        if self.settings.get_data("ExtendedSettings"):
            button_global.grid(row=0, column=2, padx=10, pady=5)


        button_maker = ctk.CTkButton(menubar, text=chooseTextByLanguage("Создать\nсвоё приложение", "Make your\nown application", self.settings.get_data("Language")), command=self.open_maker)
        button_maker.grid(row=0, column=3 if self.settings.get_data("ExtendedSettings") else 2, padx=10, pady=5)


        button_settings = ctk.CTkButton(menubar, text=chooseTextByLanguage("Настройки", "Settings", self.settings.get_data("Language")), command=self.open_settings)
        button_settings.grid(row=0, column=4 if self.settings.get_data("ExtendedSettings") else 3, padx=10, pady=5)


        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        self.open_guide()

    def open_guide(self):
        self.frame.pack_forget()
        self.frame = Guide(self)
        self.frame.pack(fill="both", expand=True)

    def open_local(self):
        self.frame.pack_forget()
        self.frame = AllLocalApplications(self)
        self.frame.pack(fill="both", expand=True)

    def open_global(self):
        self.frame.pack_forget()
        self.frame = AllGlobalApplications(self)
        self.frame.pack(fill="both", expand=True)

    def open_settings(self):
        self.frame.pack_forget()
        self.frame = SettingsFrame(self)
        self.frame.pack(fill="both", expand=True)

    def open_maker(self):
        self.frame.pack_forget()
        self.frame = MakeApplication(self)
        self.frame.pack(fill="both", expand=True)

    def update_settings(self):
        pass

def main():
    global app
    app = App()
    manager = ApplicationManager()
    app.iconphoto(False, ImageTk.PhotoImage(file='assets/icon.png'))
    app.mainloop()

if __name__ == '__main__':
    main()
