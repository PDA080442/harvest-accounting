"""
Главный файл запуска приложения "Учет урожая".

Точка входа в приложение для ведения учета урожая различных культур.
"""
import sys

# Проверка наличия tkinter
try:
    import tkinter as tk
except ImportError:
    print("Ошибка: tkinter не установлен!")
    print("\nДля установки tkinter на macOS выполните:")
    print("  brew install python-tk")
    print("\nИли используйте Python с официального сайта python.org,")
    print("который включает tkinter по умолчанию.")
    sys.exit(1)

from src.gui import HarvestApp


def main():
    """Главная функция запуска приложения."""
    app = HarvestApp()
    app.mainloop()


if __name__ == "__main__":
    main()

