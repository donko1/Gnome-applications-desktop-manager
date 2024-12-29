import os
import glob
from PIL import Image
from functools import lru_cache

class IconFinder:
    def __init__(self):
        self.icon_paths = [
            "/usr/share/icons/hicolor",  # Наиболее часто используемый путь
            "/usr/share/pixmaps",
            "~/.local/share/icons/hicolor",
            "/usr/local/share/icons/hicolor",
            "/var/lib/flatpak/exports/share/icons/hicolor",
            os.path.expanduser("~/.icons/hicolor"),
            "/usr/share/icons/Adwaita",
            "/usr/share/icons/gnome"
        ]
        # Сначала проверяем более популярные размеры
        self.icon_sizes = ["48x48", "64x64", "32x32", "128x128", "scalable"]
        self.categories = ["apps", "applications"]
        self.icon_extensions = [".png", ".svg", ".xpm"]
        
        # Расширяем пути сразу при инициализации
        self.expanded_paths = []
        for path in self.icon_paths:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                self.expanded_paths.append(expanded)

    @lru_cache(maxsize=1000)
    def find_icon(self, icon_name: str) -> str:
        """Поиск иконки с кэшированием результатов"""
        if not icon_name:
            return ""
            
        # Если это полный путь и файл существует
        if os.path.isfile(icon_name):
            return icon_name
            
        # Получаем базовое имя без расширения
        icon_name = os.path.splitext(os.path.basename(icon_name))[0]
        
        # Пробуем разные варианты имени
        names_to_try = {
            icon_name,
            icon_name.lower(),
            icon_name.replace("-", "_"),
            icon_name.replace("_", "-")
        }
        
        # Если это имя в стиле flatpak (org.gnome.Example)
        if "." in icon_name:
            names_to_try.add(icon_name.split(".")[-1])
        
        # Поиск по всем возможным путям
        for base_path in self.expanded_paths:
            for size in self.icon_sizes:
                for category in self.categories:
                    size_path = os.path.join(base_path, size, category)
                    if not os.path.exists(size_path):
                        continue
                        
                    for name in names_to_try:
                        for ext in self.icon_extensions:
                            icon_path = os.path.join(size_path, name + ext)
                            if os.path.isfile(icon_path):
                                return icon_path
                                
            # Проверяем корневую директорию
            for name in names_to_try:
                for ext in self.icon_extensions:
                    icon_path = os.path.join(base_path, name + ext)
                    if os.path.isfile(icon_path):
                        return icon_path
        
        return ""
