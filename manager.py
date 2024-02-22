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

	@staticmethod
	def __format_desktop_to_dict(desktop_content: str) -> dict:
		out: dict = {}
		split_text: tuple = tuple(desktop_content.split("\n"))
		for text in split_text:
			if text[0:4] in ["Name", "Exec", "Icon"]: # if we see Name, Exec or Icon setting
				out[text[0:4]] = text[5:]
		return out

	@classmethod
	def __get_all_applications_from_folder(cls, folder: str) -> list:
		out: list = []
		files: list = os.listdir(folder)
		for file in files:
			path_to_file: str = f"{folder}/{file}" 
			with open(path_to_file, "r") as f:
				text: str = f.read()
				out.append(cls.__format_desktop_to_dict(text))
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

		code: str = self.form.format(name_of_app, command, icon_path, str(terminal).lower()) # Making code of desktop file
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

def main():
	manager = ApplicationManager()
	manager.get_all_applications()[1]
	# manager.create_desktop_file("test", "test", "test", True)

if __name__ == '__main__':
	main()