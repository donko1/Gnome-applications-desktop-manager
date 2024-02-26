
# -*- coding: utf-8 -*-
 
import os
import locale
from collections import namedtuple
from settings import Settings
from pprint import pprint as print # This line is for debug

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

		path_to_app = os.path.abspath("app.py")
		names = [el["Name"] for el in self.get_all_applications().local_apps]
		Exec = False
		for el in self.get_all_applications().local_apps:
			if el["Exec"] == f"bash {os.path.abspath('start.sh')}":
				Exec = True
		if not "Gnome applications manager" in names and not "Менеджер приложений gnome" in names and not Exec:
			self.create_desktop_file("Gnome applications manager" if not locale.getlocale()[0] == "ru_RU" else "Менеджер приложений gnome",  os.path.abspath("assets/icon.png"), f"bash {os.path.abspath('start.sh')}")
			with open(os.path.expanduser("~/.bashrc"), "r") as f:
				if not f"alias gnome_applications_manager=\"sudo bash {os.path.abspath('start.sh')}\"" in f.read():
					with open(os.path.expanduser("~/.bashrc"), "a") as f2:
						f2.write(f"\nalias gnome_applications_manager=\"sudo bash {os.path.abspath('start.sh')}\"")

	def __format_dict_to_desktop(self, d: dict) -> str:
		return self.form.format(d["Name"], d["Exec"], d["Icon"], str(d["Terminal"]).lower())


	@staticmethod
	def __format_desktop_to_dict(desktop_content: str, language: str) -> dict:
		out: dict = {}
		split_text: tuple = tuple(desktop_content.split("\n"))

		for text in split_text:
			try:
				if text[0:4] in ["Name", "Exec", "Icon", "Term"]: # if we see Name, Exec or Icon setting
					if text[0:4] != "Term":
						if text[0:5] == "Name[":
							if text[0:7] == "Name[ru" and language == "Русский":
								out[text[0:4]] = text[9:] 
							continue
						out[text[0:4]] = text[5:]
						continue
					out[text[0:8]] = True if text[9:] == "true" else False
			except:
				continue

		if "Name" in out.keys() and "Exec" in out.keys() and "Terminal" in out.keys():
			return out


	@classmethod
	def __get_all_applications_from_folder(cls, folder: str, language: str) -> list:
		out: list = []
		if not folder:
			return []
		files: list = os.listdir(folder)
		for file in files:
			path_to_file: str = f"{folder}/{file}" 
			if path_to_file.endswith(".desktop"):
				with open(path_to_file, "r") as f:
					text: str = f.read()
					info: dict = cls.__format_desktop_to_dict(text, language)
					if info:
						info["file"] = path_to_file
						out.append(info)

		return out


	def get_all_applications(self):
		local_applications: list = list(self.__get_all_applications_from_folder(self.folder_path, self.settings.get_data("Language")))
		glob_applications: list = [*self.__get_all_applications_from_folder(self.folder_path_global, self.settings.get_data("Language"))]
		if os.path.exists("/var/lib/snapd/desktop/"):
			snapd: tuple = (self.__get_all_applications_from_folder("/var/lib/snapd/desktop/applications/", self.settings.get_data("Language")))
			if snapd:
				glob_applications.extend(snapd)

		glob_applications = glob_applications
		local_applications = sorted(local_applications, key=lambda x: locale.strxfrm(x['Name']))
		glob_applications = sorted(glob_applications, key=lambda x: locale.strxfrm(x['Name']))

		outC = namedtuple("Apps", "local_apps global_apps")
		out = outC(local_applications, glob_applications) 

		return out


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

		newPath1 = f"{self.folder_path}/{application_path}"
		newPath2 = f"{self.folder_path_global}/{application_path}"
		if os.path.isfile(newPath2) or os.path.isfile(newPath1):
			os.remove(newPath1 if os.path.isfile(newPath1) else newPath2)
		raise FileExistsError("File is not exists now")

def main():
	manager = ApplicationManager()
	# Ur tests here

if __name__ == '__main__':
	main()