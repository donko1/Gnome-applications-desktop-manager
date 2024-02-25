# Hello! This porgramm will alow you to
## - edit applications
## - deleting applications
## - making new applications
## Example:
![example image](https://github.com/donko1/Gnome-applications-desktop-manager/raw/main/assets/example.png)
## Requires:
- Donwload and install
```bash
sudo apt-get install xclip
sudo apt-get install python3-tk
sudo apt install git
sudo apt install python3.$-venv # For example python-3.10-venv
```
Replace $ with your version of python. 
```bash
python3 -V # Will return your version of python
```
## Installing:

- Download repo with this command:
```bash
git clone https://github.com/donko1/Gnome-applications-desktop-manager.git
```

- Now u can start installing with this command:
```bash
cd Gnome-applications-desktop-manager
python3 -m venv venv
bash start.sh
```
Here u enter ur password and programm will start installing. After programm will open itself and it will be adding to your list of applications.
- If u want see global applications too just enable extended settings and run programm from root with this command
```bash
gnome_applications_manager
```
If u get some problems with this method u can try
```bash
cd Gnome-applications-desktop-manager
sudo bash start.sh
```