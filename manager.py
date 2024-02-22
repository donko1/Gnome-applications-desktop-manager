import os
# from pprint import pprint as print # This line is for debug

class CannotMoveNotExistingFileError(Exception):
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)

class CannotReadApplicationsFolder(Exception):
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)

class ApplicationManager:
	def __init__(self):
		self.folder_path: str = os.path.expanduser('~/.local/share/applications')
		self.folder_path_global: str = os.path.expanduser('/usr/share/applications')
		
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


	def __format_dict_to_desktop(self, d: dict) -> str:
		return self.form.format(d["Name"], d["Exec"], d["Icon"], str(d["Terminal"]).lower())


	@staticmethod
	def __format_desktop_to_dict(desktop_content: str) -> dict:
		out: dict = {}
		split_text: tuple = tuple(desktop_content.split("\n"))

		for text in split_text:
			if text[0:4] in ["Name", "Exec", "Icon", "Term"]: # if we see Name, Exec or Icon setting
				if text[0:4] != "Term":
					out[text[0:4]] = text[5:]
					continue
				out[text[0:8]] = True if text[9:] == "true" else False

		return out


	@classmethod
	def __get_all_applications_from_folder(cls, folder: str) -> list:
		out: list = []
		files: list = os.listdir(folder)
		for file in files:
			path_to_file: str = f"{folder}/{file}" 

			with open(path_to_file, "r") as f:
				text: str = f.read()
				info: dict = cls.__format_desktop_to_dict(text)
				info["file"] = path_to_file
				out.append(info)

		return out


	def get_all_applications(self):
		local_applications: tuple = tuple(self.__get_all_applications_from_folder(self.folder_path))
		glob_applications: tuple = tuple(self.__get_all_applications_from_folder(self.folder_path_global))

		return (local_applications, glob_applications)


	def create_desktop_file(
		self,
		name_of_app: str,
		icon_path: str,
		command: str,
		terminal: bool,
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
			"Exec": command}
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
			return

		raise FileExistsError("Editing file is not exists")

	def delete_application(self, application_path) -> None:
		if os.path.isfile(application_path):
			os.remove(application_path)
			return

		raise FileExistsError("File is not exists now")

def main():
	manager = ApplicationManager()
	# print(manager.get_all_applications())
	# manager.delete_application("test.desktop")
	# manager.create_desktop_file("test", "test", "test", True)

if __name__ == '__main__':
	main()