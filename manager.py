
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
		self.folder_path = os.path.expanduser('~/.local/share/applications')
		if not self.folder_path:
			raise CannotReadApplicationsFolder
		self.form = """[Desktop Entry]
Version=1.0
Terminal={3}
Type=Application
Name={0}
Exec={1}
Icon={2}
"""

	@staticmethod
	def format_desktop_to_dict(desktop_content: str) -> dict:
		out = {}
		split_text = tuple(desktop_content.split("\n"))
		for text in split_text:
			if text[0:4] in ["Name", "Exec", "Icon"]:
				out[text[0:4]] = text[5:]
		return out

	def get_all_applications(self) -> list:
		out = []
		files = os.listdir(self.folder_path)
		for file in files:
			path_to_file = f"{self.folder_path}/{file}"
			with open(path_to_file, "r") as f:
				text = f.read()
				out.append(self.format_desktop_to_dict(text))
		return out

	def create_desktop_file(
		self,
		name_of_app: str,
		icon_path: str,
		command: str,
		terminal: bool,
		do_write_in_file: bool = True,
		move_file_to_application: bool = True
	) -> None | str:
		if not do_write_in_file and move_file_to_application:
			raise CannotMoveNotExistingFileError("File is not exists!")
			return

		code = self.form.format(name_of_app, command, icon_path, str(terminal).lower())
		if do_write_in_file:
			with open(f"{name_of_app}.desktop", "w") as f:
				f.write(code)
			if move_file_to_application:
				
				os.rename(f"{name_of_app}.desktop", f"{self.folder_path}/{name_of_app}.desktop")
		else:
			return code

def main():
	manager = ApplicationManager()
	manager.get_all_applications()
	# manager.create_desktop_file("test", "test", "test", True)

if __name__ == '__main__':
	main()
