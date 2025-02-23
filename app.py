# -*- coding: utf-8 -*-

import customtkinter as ctk
import tkinter as tk
import os
from PIL import ImageTk, Image
from manager import ApplicationManager
import pyperclip
from typing import Callable
import ctypes
from settings import Settings
from icon_finder import IconFinder
from loading_indicator import LoadingIndicator
import threading

ctk.set_default_color_theme("dark-blue")

icon_finder = IconFinder()

def is_admin():
   try:
     return os.getuid() == 0
   except AttributeError:
     return ctypes.windll.shell32.IsUserAnAdmin() != 0

def restart_application():
    app.reboot_app()  

def chooseTextByLanguage(ruText: str, enText: str, lang: str) -> str:
    if lang == "Русский":
        return ruText
    return enText


class Application(ctk.CTkFrame):
    def __init__(self, master, name: str, image_path: str, command: callable):
        super().__init__(master)
        
        # Try to find the icon using IconFinder
        icon_path = icon_finder.find_icon(image_path)
        if icon_path and os.path.isfile(icon_path):
            try:
                my_image = ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    dark_image=Image.open(icon_path),
                    size=(48, 48)
                )
            except:
                my_image = ctk.CTkImage(
                    light_image=Image.open("assets/default.png"),
                    dark_image=Image.open("assets/default.png"),
                    size=(48, 48)
                )
        else:
            my_image = ctk.CTkImage(
                light_image=Image.open("assets/default.png"),
                dark_image=Image.open("assets/default.png"),
                size=(48, 48)
            )
        
        self.image_of_app = ctk.CTkButton(
            self,
            image=my_image,
            text="",
            fg_color="transparent",
            command=lambda: app.open_edit(command)
        )
        self.image_of_app.grid(row=0, column=0, pady=(20, 3))

        self.label = ctk.CTkLabel(self, text=name)
        self.label.grid(pady=(3, 10))

class MakeApplication(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()
        self.path_to_icon = None

        self.frame_frame = ctk.CTkFrame(self)
        self.form_frame = ctk.CTkFrame(self.frame_frame)
        self.parent_frame = ctk.CTkFrame(self.form_frame)

        self.name_frame = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.name_frame_label = ctk.CTkLabel(self.name_frame, text=chooseTextByLanguage("Название:", "Name:", self.settings.get_data("Language")))
        self.name_frame_label.grid(row=0, column=0, padx=(10, 0), pady=20)
        self.name_frame_input = ctk.CTkEntry(self.name_frame, height=30, placeholder_text=chooseTextByLanguage("Моё приложение", "My app", self.settings.get_data("Language")))
        self.name_frame_input.grid(row=0, column=1, padx=(5, 10), pady=20)
        self.name_frame.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        
        self.icon_path = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.icon_path_label = ctk.CTkLabel(self.icon_path, text=chooseTextByLanguage("Иконка:", "Icon:", self.settings.get_data("Language")))
        self.icon_path_label.grid(row=0, column=0, padx=(10, 0), pady=20)
        self.icon_path_button = ctk.CTkButton(self.icon_path, text=chooseTextByLanguage("Открыть", "Open", self.settings.get_data("Language")), command=self.selectfile) 
        self.icon_path_button.grid(row=0, column=1, padx=(5, 10), pady=20)
        self.icon_path.grid(row=2, column=0, padx=(20, 10), sticky="nsew")

        self.terminalComand_frame = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.terminalComand_frame_label = ctk.CTkLabel(self.terminalComand_frame, text=chooseTextByLanguage("Команда:", "Command:", self.settings.get_data("Language")))
        self.terminalComand_frame_label.grid(row=0, column=0, padx=(10, 0), pady=20)
        self.terminalComand_frame_input = ctk.CTkEntry(self.terminalComand_frame, height=30, width=200, placeholder_text="neofetch")
        self.terminalComand_frame_input.grid(row=0, column=1, padx=(5, 10), pady=20)
        self.terminalComand_frame.grid(row=3, column=0, padx=(20, 10), sticky="nsew")

        self.terminal_frame = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.terminal_frame_checkbox = ctk.CTkCheckBox(self.terminal_frame, text=chooseTextByLanguage("Открывать терминал", "Open terminal", self.settings.get_data("Language")))
        self.terminal_frame_checkbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.move_frame = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.move_frame_checkbox = ctk.CTkCheckBox(self.move_frame, text=chooseTextByLanguage("Перемещать файл", "Move file", self.settings.get_data("Language")), command=self.move_checkbox)
        self.move_frame_checkbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.move_frame_checkbox.select()

        self.folder_frame = ctk.CTkFrame(self.parent_frame)
        self.label = ctk.CTkLabel(self.folder_frame, text=chooseTextByLanguage("Папка назначения:", "Destination folder:", self.settings.get_data("Language")))
        self.label.pack(side="left", padx=(10, 0), pady=10)
        self.option_menu = ctk.CTkOptionMenu(self.folder_frame, values=[chooseTextByLanguage("Локальная", "Local", self.settings.get_data("Language")), chooseTextByLanguage("Глобальная", "Global", self.settings.get_data("Language"))])
        self.option_menu.pack(side="left", padx=(5, 10), pady=10)
        self.option_menu.set(chooseTextByLanguage("Локальная", "Local", self.settings.get_data("Language")))

        if self.settings.get_data("ExtendedSettings"):
            self.label = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage("Создать приложение/.desktop файл", "Create application/.desktop file", self.settings.get_data("Language")))
            self.terminal_frame.grid(row=4, column=0, padx=(20, 10), sticky="nsew")
            self.move_frame.grid(row=5, column=0, padx=(20, 10), sticky="nsew")
            self.folder_frame.grid(row=6, column=0, padx=(20, 10), sticky="nsew")

        else:
            self.label = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage("Создать приложение", "Create application", self.settings.get_data("Language")))            

        self.label.grid(row=0, column=0)

        self.parent_frame.grid(row=0, column=0)
        self.form_frame.grid(row=1, column=0, pady=10, sticky="nsew")

        self.submit_button = ctk.CTkButton(self.frame_frame, text=chooseTextByLanguage("Создать приложеине", "Create application", self.settings.get_data("Language")), command=self.submit)
        self.submit_button.grid(row=2, column=0, pady=0, sticky="nsew")

        self.frame_frame.pack()

    def selectfile(self):
        filename = ctk.filedialog.askopenfilename()
        self.path_to_icon = filename
        if filename:
            self.icon_path_button.grid_forget()
            self.icon_path_button = ctk.CTkLabel(self.icon_path, text=chooseTextByLanguage("Иконка выбрана.\nНажмите на иконку что бы изменить её", "Icon selected.\nClick on icon to change it.", self.settings.get_data("Language")))
            self.icon_path_button.grid(row=0, column=1, padx=(10, 10), pady=20)
            my_image = ctk.CTkImage(light_image=Image.open(filename),
                                  dark_image=Image.open(filename),
                                  size=(200, 200))

            self.image_of_app = ctk.CTkButton(self.form_frame, image=my_image, text="", command=self.selectfile, fg_color="transparent")
            self.image_of_app.grid(row=0, column=1, pady=(20, 10))

    def move_checkbox(self):
        if self.move_frame_checkbox.get():
            self.option_menu.set(chooseTextByLanguage("Локальная", "Local", self.settings.get_data("Language")))
            self.folder_frame.grid(row=6, column=0, padx=(20, 10), sticky="nsew")
            return

        self.folder_frame.grid_forget()

    def submit(self):
        if hasattr(self, "message"):
            self.message.grid_forget()
        if not("" in [self.terminalComand_frame_input.get(), self.path_to_icon, self.name_frame_input.get()] or None in [self.terminalComand_frame_input.get(), self.path_to_icon, self.name_frame_input.get()]):
            self.submit_button.grid_forget()
            if self.move_frame_checkbox.get():
                pyperclip.copy(os.getcwd())
                pyperclip.paste()
            try:
                manager.create_desktop_file(
                    name_of_app=self.name_frame_input.get(),
                    icon_path=self.path_to_icon,
                    command=self.terminalComand_frame_input.get(),
                    terminal=self.terminal_frame_checkbox.get(),
                    move_file_to_application=self.move_frame_checkbox.get(),
                    localFolder=self.option_menu.get() == "Локальная" or self.option_menu.get() == "Local"
                    )
            except PermissionError:
                self.message = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage(f"Ошибка доступа! Для пермещения файла в глоабльную папку откройте это приложение от лица администратора", f"PermissionError! To move file to global folder open this app as admin", self.settings.get_data("Language")))
            else:
                self.message = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage("Успешно создано приложение!", "Application successfully created!", self.settings.get_data("Language")) if self.move_frame_checkbox.get() else chooseTextByLanguage(f"Успешно создано приложение!\nПуть до директории с .desktop файлом в буфере обмена", f"Application successfully created!\nPath to folder with .desktop file in your clipboard", self.settings.get_data("Language")))
            self.message.grid(row=3, column=0, pady=10, sticky="nsew")
            return

        self.message = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage("Заполните все поля!", "Fill in all the fields!", self.settings.get_data("Language")))
        self.message.grid(row=3, column=0, pady=10, sticky="nsew")


class EditApp(ctk.CTkFrame):
    def __init__(self, master, application_data: dict):
        super().__init__(master)
        self.settings = Settings()
        self.path_to_icon = None
        self.application_data = application_data

        self.frame_frame = ctk.CTkFrame(self)
        self.form_frame = ctk.CTkFrame(self.frame_frame)
        self.parent_frame = ctk.CTkFrame(self.form_frame)

        self.name_frame = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.name_frame_label = ctk.CTkLabel(self.name_frame, text=chooseTextByLanguage("Название:", "Name:", self.settings.get_data("Language")))
        self.name_frame_label.grid(row=0, column=0, padx=(10, 0), pady=20)
        v = ctk.StringVar(self.name_frame, value=self.application_data["Name"])
        self.name_frame_input = ctk.CTkEntry(self.name_frame, height=30, textvariable=v, placeholder_text=self.application_data["Name"])
        self.name_frame_input.grid(row=0, column=1, padx=(5, 10), pady=20)
        self.name_frame.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        
        self.icon_path = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.icon_path_label = ctk.CTkLabel(self.icon_path, text=chooseTextByLanguage("Иконка:", "Icon:", self.settings.get_data("Language")))
        self.icon_path_label.grid(row=0, column=0, padx=(10, 0), pady=20)
        self.icon_path_button = ctk.CTkButton(self.icon_path, text=chooseTextByLanguage("Открыть", "Open", self.settings.get_data("Language")), command=self.selectfile) 
        self.icon_path_button.grid(row=0, column=1, padx=(5, 10), pady=20)
        self.icon_path.grid(row=2, column=0, padx=(20, 10), sticky="nsew")

        self.terminalComand_frame = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.terminalComand_frame_label = ctk.CTkLabel(self.terminalComand_frame, text=chooseTextByLanguage("Команда:", "Command:", self.settings.get_data("Language")))
        self.terminalComand_frame_label.grid(row=0, column=0, padx=(10, 0), pady=20)
        v = ctk.StringVar(self.terminalComand_frame, value=self.application_data["Exec"])
        self.terminalComand_frame_input = ctk.CTkEntry(self.terminalComand_frame, height=30, width=600, textvariable=v)
        self.terminalComand_frame_input.grid(row=0, column=1, padx=(5, 10), pady=20)
        self.terminalComand_frame.grid(row=3, column=0, padx=(20, 10), sticky="nsew")

        self.terminal_frame = ctk.CTkFrame(self.parent_frame, width=400, corner_radius=0)
        self.terminal_frame_checkbox = ctk.CTkCheckBox(self.terminal_frame, text=chooseTextByLanguage("Открывать терминал", "Open terminal", self.settings.get_data("Language")))
        self.terminal_frame_checkbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        if self.application_data["Terminal"]:
            self.terminal_frame_checkbox.select()

        if self.settings.get_data("ExtendedSettings"):
            self.label = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage("Изменить приложение", "Edit application", self.settings.get_data("Language")))
            self.terminal_frame.grid(row=4, column=0, padx=(20, 10), sticky="nsew")
    
        else:
            self.label = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage("Изменить приложение", "Edit application", self.settings.get_data("Language")))            
        if os.path.isfile(self.application_data["Icon"]):
            self.icon_path_button.grid(row=0, column=1, padx=(10, 10), pady=20)
            my_image = ctk.CTkImage(light_image=Image.open(self.application_data["Icon"]),
                                  dark_image=Image.open(self.application_data["Icon"]),
                                  size=(200, 200))

            self.image_of_app = ctk.CTkButton(self.form_frame, image=my_image, text="", command=self.selectfile, fg_color="transparent")
            self.image_of_app.grid(row=0, column=1, pady=(20, 10))

        self.label.grid(row=0, column=0)

        self.parent_frame.grid(row=0, column=0)
        self.form_frame.grid(row=1, column=0, pady=10, sticky="nsew")

        self.submit_button = ctk.CTkButton(self.frame_frame, text=chooseTextByLanguage("Сохранить", "Save", self.settings.get_data("Language")), command=self.submit)
        self.submit_button.grid(row=2, column=0, pady=0, sticky="nsew")

        self.delete_button = ctk.CTkButton(self.frame_frame, text=chooseTextByLanguage("Удалить приложеине", "Delete application", self.settings.get_data("Language")), command=self.delete, fg_color="#ec5f66")
        self.delete_button.grid(row=3, column=0, pady=0, sticky="nsew")

        self.frame_frame.pack()

    def delete(self):
        manager.delete_application(self.application_data["file"])
        app.open_local()

    def selectfile(self):
        filename = ctk.filedialog.askopenfilename()
        self.path_to_icon = filename
        if filename:
            self.icon_path_button.grid(row=0, column=1, padx=(10, 10), pady=20)
            my_image = ctk.CTkImage(light_image=Image.open(filename),
                                  dark_image=Image.open(filename),
                                  size=(200, 200))

            self.image_of_app = ctk.CTkButton(self.form_frame, image=my_image, text="", command=self.selectfile)
            self.image_of_app.grid(row=0, column=1, pady=(20, 10))

    def submit(self):
        if hasattr(self, "message"):
            self.message.grid_forget()
        self.submit_button.grid_forget()
        self.delete_button.grid_forget()
        try:

            manager.edit_application(
                application_path=self.application_data["file"],
                new_data={
                    "Name":self.name_frame_input.get() if self.name_frame_input.get() else self.application_data["Name"],
                    "Exec":self.terminalComand_frame_input.get() if self.terminalComand_frame_input.get() else self.application_data["Exec"],
                    "Icon":self.path_to_icon if self.path_to_icon else self.application_data["Icon"],
                    "Terminal":bool(self.terminal_frame_checkbox.get())
                }
                )
        except PermissionError:
            self.message = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage(f"Ошибка доступа! Для пермещения файла в глоабльную папку откройте это приложение от лица администратора", f"PermissionError! To move file to global folder open this app as admin", self.settings.get_data("Language")))
        else:
            self.message = ctk.CTkLabel(self.frame_frame, text=chooseTextByLanguage("Успешно изменено приложение!", "Application successfully edited!", self.settings.get_data("Language")))
        self.message.grid(row=3, column=0, pady=10, sticky="nsew")


class AllLocalApplications(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()
        
        # Create main frame that fills the window
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show loading indicator
        self.loading = LoadingIndicator(
            self.main_frame,
            text=chooseTextByLanguage("Загрузка приложений", "Loading applications", self.settings.get_data("Language"))
        )
        self.loading.pack(expand=True)
        
        # Load applications in a separate thread
        self.load_thread = threading.Thread(target=self._load_applications)
        self.load_thread.daemon = True
        self.load_thread.start()
    
    def _load_applications(self):
        # Create scrollable frame
        self.app_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=1200,
            height=800,
            label_text=chooseTextByLanguage("Локальные приложения", "Local Applications", self.settings.get_data("Language"))
        )
        
        # Get applications
        applications, _ = manager.get_all_applications()
        
        # Display applications in grid
        for i, elem in enumerate(applications):
            row, col = self.__get_addr(i)            
            try:
                app = Application(self.app_frame, elem["Name"], elem["Icon"], elem)
            except KeyError:
                app = Application(self.app_frame, elem["Name"], "", elem)
            app.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
        # Configure grid columns to be equal width
        for i in range(4):  # 4 columns
            self.app_frame.grid_columnconfigure(i, weight=1)
        
        # Enable mouse wheel scrolling for Linux
        self.app_frame.bind_all("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.app_frame.bind_all("<Button-5>", self._on_mousewheel)  # Linux scroll down
        
        # Remove loading indicator and show applications
        self.loading.stop()
        self.app_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _on_mousewheel(self, event):
        if event.num == 4:  # scroll up
            self.app_frame._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # scroll down
            self.app_frame._parent_canvas.yview_scroll(1, "units")
        
    @staticmethod
    def __get_addr(n: int) -> tuple:
        return (n // 4, n % 4)  # 4 columns layout

class AllGlobalApplications(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()
        
        # Create main frame that fills the window
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show loading indicator
        self.loading = LoadingIndicator(
            self.main_frame,
            text=chooseTextByLanguage("Загрузка приложений", "Loading applications", self.settings.get_data("Language"))
        )
        self.loading.pack(expand=True)
        
        # Load applications in a separate thread
        self.load_thread = threading.Thread(target=self._load_applications)
        self.load_thread.daemon = True
        self.load_thread.start()
    
    def _load_applications(self):
        # Create scrollable frame
        self.app_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=1200,
            height=800,
            label_text=chooseTextByLanguage("Глобальные приложения", "Global Applications", self.settings.get_data("Language"))
        )
        
        # Get applications
        _, applications = manager.get_all_applications()
        
        # Display applications in grid
        for i, elem in enumerate(applications):
            row, col = self.__get_addr(i)            
            try:
                app = Application(self.app_frame, elem["Name"], elem["Icon"], elem)
            except KeyError:
                app = Application(self.app_frame, elem["Name"], "", elem)
            app.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
        # Configure grid columns to be equal width
        for i in range(4):  # 4 columns
            self.app_frame.grid_columnconfigure(i, weight=1)
        
        # Enable mouse wheel scrolling for Linux
        self.app_frame.bind_all("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.app_frame.bind_all("<Button-5>", self._on_mousewheel)  # Linux scroll down
        
        # Remove loading indicator and show applications
        self.loading.stop()
        self.app_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _on_mousewheel(self, event):
        if event.num == 4:  # scroll up
            self.app_frame._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # scroll down
            self.app_frame._parent_canvas.yview_scroll(1, "units")
        
    @staticmethod
    def __get_addr(n: int) -> tuple:
        return (n // 4, n % 4)  # 4 columns layout

class Guide(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = Settings()

        # Основной фрейм с прокруткой
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 30))
        
        title = ctk.CTkLabel(
            title_frame,
            text=chooseTextByLanguage(
                "Добро пожаловать в Gnome Applications Manager!",
                "Welcome to Gnome Applications Manager!",
                self.settings.get_data("Language")
            ),
            font=("TkDefaultFont", 24, "bold")
        )
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text=chooseTextByLanguage(
                "Простой способ управления вашими приложениями",
                "An easy way to manage your applications",
                self.settings.get_data("Language")
            ),
            font=("TkDefaultFont", 16)
        )
        subtitle.pack()

        # Карточки с разделами
        sections = [
            {
                "title": chooseTextByLanguage("🚀 Начало работы", "🚀 Getting Started", self.settings.get_data("Language")),
                "content": chooseTextByLanguage(
                    "• Измените язык и тему в настройках\n"
                    "• Для полного доступа запустите от администратора\n"
                    "• Приложение уже добавлено в ваш список!",
                    
                    "• Change language and theme in settings\n"
                    "• Run as administrator for full access\n"
                    "• The app is already in your list!",
                    self.settings.get_data("Language")
                )
            },
            {
                "title": chooseTextByLanguage("📱 Локальные приложения", "📱 Local Applications", self.settings.get_data("Language")),
                "content": chooseTextByLanguage(
                    "• Приложения в вашей домашней папке\n"
                    "• Нажмите для изменения или удаления\n"
                    "• Доступны без прав администратора",
                    
                    "• Apps in your home folder\n"
                    "• Click to modify or delete\n"
                    "• Available without admin rights",
                    self.settings.get_data("Language")
                )
            },
            {
                "title": chooseTextByLanguage("🌐 Глобальные приложения", "🌐 Global Applications", self.settings.get_data("Language")),
                "content": chooseTextByLanguage(
                    "• Системные приложения и snap/flatpak\n"
                    "• Нажмите для изменения или удаления\n"
                    "• Требуются права администратора",
                    
                    "• System apps and snap/flatpak\n"
                    "• Click to modify or delete\n"
                    "• Requires administrator rights",
                    self.settings.get_data("Language")
                )
            },
            {
                "title": chooseTextByLanguage("✏️ Редактирование", "✏️ Editing", self.settings.get_data("Language")),
                "content": chooseTextByLanguage(
                    "• Название: имя программы\n"
                    "• Иконка: выберите новое изображение\n"
                    "• Команда: как запускать программу\n"
                    "• Терминал: открывать ли консоль\n"
                    "• Сохранить или удалить приложение",
                    
                    "• Name: program title\n"
                    "• Icon: choose new image\n"
                    "• Command: how to launch\n"
                    "• Terminal: open console or not\n"
                    "• Save or delete the app",
                    self.settings.get_data("Language")
                )
            },
            {
                "title": chooseTextByLanguage("➕ Создание приложения", "➕ Creating Application", self.settings.get_data("Language")),
                "content": chooseTextByLanguage(
                    "• Заполните те же поля\n"
                    "• Выберите место установки\n"
                    "• Или сохраните путь в буфер обмена",
                    
                    "• Fill in the same fields\n"
                    "• Choose installation location\n"
                    "• Or save path to clipboard",
                    self.settings.get_data("Language")
                )
            }
        ]

        # Создаем карточки
        for section in sections:
            card = ctk.CTkFrame(self.main_frame)
            card.pack(fill="x", pady=10, padx=5, ipady=10)
            
            # Заголовок карточки
            title = ctk.CTkLabel(
                card,
                text=section["title"],
                font=("TkDefaultFont", 18, "bold")
            )
            title.pack(pady=(10, 5), padx=15, anchor="w")
            
            # Содержимое карточки
            content = ctk.CTkLabel(
                card,
                text=section["content"],
                justify="left",
                anchor="w"
            )
            content.pack(pady=(0, 10), padx=15, anchor="w")

        # Финальное сообщение
        final_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        final_frame.pack(fill="x", pady=(20, 0))
        
        final_message = ctk.CTkLabel(
            final_frame,
            text=chooseTextByLanguage(
                "🎉 Приятного использования!",
                "🎉 Enjoy using the app!",
                self.settings.get_data("Language")
            ),
            font=("TkDefaultFont", 18, "bold")
        )
        final_message.pack(pady=10)

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

        self.theme_frame = ctk.CTkFrame(parent_frame)
        self.theme_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")
        self.theme_label = ctk.CTkLabel(self.theme_frame, text=chooseTextByLanguage("Тема", "Theme", self.settings.get_data("Language")))
        self.theme_label.pack(side="left", padx=30, pady=10)
        theme_values = ["dark", "light"] if self.settings.get_data("Language") == "English" else ["черная", "белая"]
        self.theme_menu = ctk.CTkOptionMenu(self.theme_frame, values=theme_values, command=self.changeTheme)
        self.theme_menu.pack(side="left", padx=5)
        current_theme = self.settings.get_data("Theme")
        # Convert theme value for display
        display_theme = current_theme
        if self.settings.get_data("Language") == "Русский":
            display_theme = "черная" if current_theme == "dark" else "белая"
        self.theme_menu.set(display_theme)

        self.checkbox_frame = ctk.CTkFrame(parent_frame)
        self.checkbox_frame.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsw")
        self.checkbox_1 = ctk.CTkCheckBox(self.checkbox_frame, text=chooseTextByLanguage("Расширенные настройки(только для продвинутых пользователей)", "Extended settings(advanced users only)", self.settings.get_data("Language")), command=self.changeSettings)
        if self.settings.get_data("ExtendedSettings"):
            self.checkbox_1.select()
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def changeLanguage(self, arg):
        # Update theme menu text when language changes
        current_theme = self.settings.get_data("Theme")
        self.settings.write_data("Language", arg)
        theme_values = ["dark", "light"] if arg == "English" else ["черная", "белая"]
        self.theme_menu.configure(values=theme_values)
        display_theme = current_theme
        if arg == "Русский":
            display_theme = "черная" if current_theme == "dark" else "белая"
        self.theme_menu.set(display_theme)
        restart_application()

    def changeTheme(self, new_theme):
        # Convert Russian theme names to English for storage
        if new_theme == "черная":
            new_theme = "dark"
        elif new_theme == "белая":
            new_theme = "light"
        self.settings.write_data("Theme", new_theme)
        ctk.set_appearance_mode(new_theme)

    def changeSettings(self):
        self.settings.write_data("ExtendedSettings", bool(self.checkbox_1.get()))
        restart_application()

class App(ctk.CTk):
    def __init__(self, create_window: bool=True):
        if create_window:
            super().__init__()
            self.settings = Settings()

            # Set theme from settings with fallback to dark theme
            theme = self.settings.get_data("Theme") or "dark"
            ctk.set_appearance_mode(theme)

            self.title("Gnome applications manager")
            self.geometry("1300x990") 

        self.menubar = ctk.CTkFrame(self)
        self.menubar.pack(side="top", fill="x")
        self.menubar.columnconfigure([0, 1, 2, 3, 4] if self.settings.get_data("ExtendedSettings") and is_admin() else [0, 1, 2, 3], weight=1)

        self.button_guide = ctk.CTkButton(self.menubar, text=chooseTextByLanguage("Гайд", "Guide", self.settings.get_data("Language")), command=self.open_guide)
        self.button_guide.grid(row=0, column=0, padx=10, pady=5)

        self.button_local = ctk.CTkButton(self.menubar, text=chooseTextByLanguage("Локальные\nприложения" if self.settings.get_data("ExtendedSettings") else "Приложения", "Local\napplications" if self.settings.get_data("ExtendedSettings") else "Applications", self.settings.get_data("Language")), command=self.open_local)
        self.button_local.grid(row=0, column=1, padx=10, pady=5)

        self.button_global = ctk.CTkButton(self.menubar, text=chooseTextByLanguage("Глобальные\nприложения", "Global\napplications", self.settings.get_data("Language")), command=self.open_global)
        if self.settings.get_data("ExtendedSettings") and is_admin():
            self.button_global.grid(row=0, column=2, padx=10, pady=5)


        self.button_maker = ctk.CTkButton(self.menubar, text=chooseTextByLanguage("Создать\nсвоё приложение", "Make your\nown application", self.settings.get_data("Language")), command=self.open_maker)
        self.button_maker.grid(row=0, column=3 if self.settings.get_data("ExtendedSettings") and is_admin() else 2, padx=10, pady=5)


        self.button_settings = ctk.CTkButton(self.menubar, text=chooseTextByLanguage("Настройки", "Settings", self.settings.get_data("Language")), command=self.open_settings)
        self.button_settings.grid(row=0, column=4 if self.settings.get_data("ExtendedSettings") and is_admin() else 3, padx=10, pady=5)


        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)
        if create_window:
            self.open_guide()
            return
        self.open_settings()

    def open_edit(self, data):
        self.frame.pack_forget()
        self.frame = EditApp(self, data)
        self.frame.pack(fill="both", expand=True)

    def reboot_app(self):
        self.frame.pack_forget()
        self.menubar.pack_forget()
        self.__init__(create_window=False)

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
    global app, manager
    app = App()
    manager = ApplicationManager()
    try:
        os.remove("assets/example.png")
    except: pass
    app.iconphoto(False, ImageTk.PhotoImage(file='assets/icon.png'))
    app.mainloop()

if __name__ == '__main__':
    main()
