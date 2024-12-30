# -*- coding: utf-8 -*-

import os
import locale
import glob
from collections import namedtuple
from settings import Settings
from functools import lru_cache
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class CannotMoveNotExistingFileError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class CannotReadApplicationsFolder(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class ApplicationManager:
    def __init__(self):
        self.folder_path: str = os.path.expanduser('~/.local/share/applications')
        self.folder_path_global: str = '/usr/share/applications'
        self.settings = Settings()
        
        # Предопределенные глобальные директории
        self.global_dirs = [
            "/var/lib/snapd/desktop/applications/",
            "/var/lib/flatpak/exports/share/applications",
            "/usr/local/share/applications",
            "/usr/share/app-install/desktop",
            "/var/lib/snapd/desktop",
            "/usr/share/gnome/applications",
            "/usr/share/kde4/applications",
        ]
        
        # Расширяем пути с wildcards при инициализации
        self.expanded_global_dirs = []
        for directory in self.global_dirs:
            if "*" in directory:
                self.expanded_global_dirs.extend(glob.glob(directory))
            elif os.path.exists(directory):
                self.expanded_global_dirs.append(directory)
        
        if not os.path.exists(self.folder_path):
            self.folder_path = None
        if not self.folder_path or not self.folder_path_global:
            raise CannotReadApplicationsFolder

        self.form: str = """[Desktop Entry]
Version=1.0
Terminal={3}
Type=Application
Name={0}
Exec={1}
Icon={2}
"""
        # Инициализация приложения происходит в отдельном методе
        self._initialize_app()

    def _initialize_app(self):
        path_to_app = os.path.abspath("app.py")
        apps = self.get_all_applications()
        names = [el["Name"] for el in apps.local_apps]
        Exec = any(el["Exec"] == f"bash {os.path.abspath('start.sh')}" for el in apps.local_apps)
        
        if not any(name in names for name in ["Gnome applications manager", "Менеджер приложений gnome"]) and not Exec:
            name = "Менеджер приложений gnome" if locale.getlocale()[0] == "ru_RU" else "Gnome applications manager"
            self.create_desktop_file(
                name,
                os.path.abspath("assets/icon.png"),
                f"bash {os.path.abspath('start.sh')}",
            )
            # with open("/bin/gnome_applications_manager", "w") as f: # Now this thing is making by bash.
            #     f.write("sudo bash /home/donkol/Gnome-applications-desktop-manager/start.sh")

    @staticmethod
    def __format_desktop_to_dict(desktop_content: str, language: str) -> dict:
        out = {}
        for line in desktop_content.splitlines():
            if not line.startswith(("Name", "Exec", "Icon", "Term")):
                continue
            try:
                if line.startswith("Name["):
                    if line.startswith("Name[ru") and language == "Русский":
                        out["Name"] = line[9:]
                    continue
                elif line.startswith(("Name", "Exec", "Icon")):
                    key = line[:4]
                    out[key] = line[5:]
                elif line.startswith("Term"):
                    out["Terminal"] = line[9:] == "true"
            except:
                continue
        
        return out if all(k in out for k in ["Name", "Exec", "Terminal"]) else None

    def _get_applications_from_folder(self, folder: str) -> list:
        if not folder or not os.path.exists(folder):
            return []
            
        applications = []
        try:
            files = [f for f in os.listdir(folder) if f.endswith(".desktop")]
            for file in files:
                path_to_file = os.path.join(folder, file)
                try:
                    with open(path_to_file, "r") as f:
                        text = f.read()
                        info = self.__format_desktop_to_dict(text, self.settings.get_data("Language"))
                        if info:
                            info["file"] = path_to_file
                            applications.append(info)
                except:
                    continue
                    
            return applications
        except:
            return []

    def get_all_applications(self):
        # Получаем локальные приложения
        local_applications = self._get_applications_from_folder(self.folder_path)
        
        # Получаем глобальные приложения параллельно
        glob_applications = []
        with ThreadPoolExecutor(max_workers=min(8, len(self.expanded_global_dirs))) as executor:
            future_to_dir = {
                executor.submit(self._get_applications_from_folder, directory): directory
                for directory in [self.folder_path_global] + self.expanded_global_dirs
            }
            
            for future in as_completed(future_to_dir):
                apps = future.result()
                if apps:
                    glob_applications.extend(apps)
        
        # Удаляем дубликаты
        seen = set()
        unique_apps = []
        for app in glob_applications:
            key = (app.get('Name', ''), app.get('Exec', ''))
            if key not in seen:
                seen.add(key)
                unique_apps.append(app)
        
        # Сортируем приложения
        local_applications = sorted(local_applications, key=lambda x: locale.strxfrm(x['Name']))
        glob_applications = sorted(unique_apps, key=lambda x: locale.strxfrm(x['Name']))
        
        Apps = namedtuple("Apps", "local_apps global_apps")
        return Apps(local_applications, glob_applications)

    def __format_dict_to_desktop(self, d: dict) -> str:
        return self.form.format(d["Name"], d["Exec"], d["Icon"], str(d["Terminal"]).lower())

    def create_desktop_file(
        self,
        name_of_app: str,
        icon_path: str,
        command: str,
        terminal: bool=False,
        do_write_in_file: bool=True,
        move_file_to_application: bool=True,
        localFolder: bool=True
    ) -> None | str:
        if not do_write_in_file and move_file_to_application:
            raise CannotMoveNotExistingFileError("File is not exists!")
            return

        code: str = self.__format_dict_to_desktop({
            "Name": name_of_app, 
            "Icon":icon_path, 
            "Terminal": terminal, 
            "Exec": command},
        )

        if do_write_in_file:
            with open(f"{name_of_app}.desktop", "w") as f:
                f.write(code)
            if move_file_to_application:
                if localFolder:
                    os.rename(f"{name_of_app}.desktop", f"{self.folder_path}/{name_of_app}.desktop") # Replace to local folder
                    return
                os.rename(f"{name_of_app}.desktop", f"{self.folder_path_global}/{name_of_app}.desktop") # Replace to global folder
            return None
        
        return code

    def edit_application(self, application_path: str, new_data: dict) -> None:
        if os.path.isfile(application_path):
            code = self.__format_dict_to_desktop(new_data) 
            with open(application_path, "w") as f:
                f.write(code)
            name = new_data["Name"]
            path = application_path.split("/")[0:-1]
            path.append(f"{name}.desktop")
            new_path = "/".join(path)
            os.rename(application_path, new_path)
            return

        raise FileExistsError("Editing file is not exists")

    def delete_application(self, application_path) -> None:
        if os.path.isfile(application_path):
            os.remove(application_path)
            return

        new_path1 = f"{self.folder_path}/{application_path}"
        new_path2 = f"{self.folder_path_global}/{application_path}"
        if os.path.isfile(new_path2) or os.path.isfile(new_path1):
            os.remove(new_path1 if os.path.isfile(new_path1) else new_path2)
        raise FileExistsError("File is not exists now")

def main():
    manager = ApplicationManager()
    # Ur tests here

if __name__ == '__main__':
    main()
