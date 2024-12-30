# 🚀 Gnome Applications Desktop Manager

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange)

A convenient graphical manager for creating and managing `.desktop` files in Linux. Easily create, edit, and delete application shortcuts in both user and system directories.

## ✨ Features

- 📱 **Local Applications Management**
  - View and edit `.desktop` files in your home directory
  - No administrator rights required
  - Instant changes application
  - Safe and user-friendly interface

- 🌐 **Global Applications Management**
  - Access to system applications (requires root privileges)
  - Support for Snap and Flatpak applications
  - Automatic application discovery in all standard directories
  - Secure system-wide modifications

- 🎨 **User-Friendly Interface**
  - Modern design with theme support (light/dark)
  - English and Russian language support
  - Intuitive controls and navigation
  - Real-time updates

## 📸 Screenshots

![example image](https://github.com/donko1/Gnome-applications-desktop-manager/raw/main/assets/example.png)

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/donko1/Gnome-applications-desktop-manager.git
   cd Gnome-applications-desktop-manager
   ```

2. **Init the manager:**
   ```bash
   sudo bash init.sh
   ```
   The application will automatically install all requirements

3. **Start the app:**
   ```bash
   gnome_applications_manager
   ```
   The application will automatically add itself to your applications list.


## 💻 Usage

### Basic Usage
- Launch the application from your applications menu or terminal:
  ```bash
  gnome_applications_manager
  ```

### Advanced Features
1. Enable "Advanced Settings" in the application settings
2. For global applications access, run with administrator privileges:
   ```bash
   sudo gnome_applications_manager
   ```
   or
   ```bash
   cd Gnome-applications-desktop-manager
   sudo bash start.sh
   ```

## ⚙️ Configuration

- **Language**: English/Russian
- **Theme**: Light/Dark
- **Advanced Settings**: Access to additional features
- **Custom Paths**: Add your own application directories

## 🔍 Requirements

- Linux-based OS
- Python 3.10+
- CustomTkinter
- PIL (Pillow)
- Root privileges (for global applications)
- Standard Linux desktop environment

## 🛠️ Technical Details

- Built with Python and CustomTkinter
- Uses threading for responsive UI
- Implements caching for faster application loading
- Follows XDG Base Directory Specification

## 🔒 Security

- Safe handling of system files
- Proper permission management
- Secure root privilege handling
- Backup creation for critical operations

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- CustomTkinter team for the modern UI toolkit
- Linux community for inspiration