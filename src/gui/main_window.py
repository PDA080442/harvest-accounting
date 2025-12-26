"""
Графический интерфейс приложения для учета урожая.

Содержит главное окно приложения с полями ввода, кнопками
и областью отображения результатов.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

from ..models.crop import Crop
from ..utils.calculations import calculate_total_season_harvest


class HarvestApp(tk.Tk):
    """
    Главное окно приложения для учета урожая.
    
    Позволяет фермеру вводить данные по культурам,
    добавлять их в список и рассчитывать общий урожай за сезон.
    """
    
    def __init__(self):
        """Инициализация главного окна приложения."""
        super().__init__()
        
        self.crops: List[Crop] = []  # Список культур
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self) -> None:
        """Настройка параметров окна."""
        self.title("Учет урожая")
        self.geometry("700x600")
        self.resizable(True, True)
        
        # Центрирование окна
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self) -> None:
        """Создание и размещение виджетов интерфейса."""
        # Заголовок
        title_label = tk.Label(
            self,
            text="Учет урожая культур",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Фрейм для полей ввода
        input_frame = ttk.LabelFrame(self, text="Ввод данных о культуре", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Поле ввода: Название культуры
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill=tk.X, pady=5)
        tk.Label(name_frame, text="Название культуры:", width=20, anchor="w").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        # Поле ввода: Площадь посева
        area_frame = ttk.Frame(input_frame)
        area_frame.pack(fill=tk.X, pady=5)
        tk.Label(area_frame, text="Площадь посева (га):", width=20, anchor="w").pack(side=tk.LEFT)
        self.area_entry = tk.Entry(area_frame, width=30)
        self.area_entry.pack(side=tk.LEFT, padx=5)
        
        # Поле ввода: Урожайность
        yield_frame = ttk.Frame(input_frame)
        yield_frame.pack(fill=tk.X, pady=5)
        tk.Label(yield_frame, text="Урожайность (т/га):", width=20, anchor="w").pack(side=tk.LEFT)
        self.yield_entry = tk.Entry(yield_frame, width=30)
        self.yield_entry.pack(side=tk.LEFT, padx=5)
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        # Кнопка "Добавить культуру"
        add_button = tk.Button(
            button_frame,
            text="Добавить культуру",
            command=self._add_crop,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            width=18,
            height=2
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка "Рассчитать общий урожай"
        calculate_button = tk.Button(
            button_frame,
            text="Рассчитать общий урожай",
            command=self._calculate_total,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            width=18,
            height=2
        )
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка "Очистить список"
        clear_button = tk.Button(
            button_frame,
            text="Очистить список",
            command=self._clear_list,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            width=18,
            height=2
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Фрейм для списка культур
        list_frame = ttk.LabelFrame(self, text="Список культур", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar для списка
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox для отображения культур
        self.crops_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Courier", 10),
            height=10
        )
        self.crops_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.crops_listbox.yview)
        
        # Метка для отображения общего урожая
        self.total_label = tk.Label(
            self,
            text="Общий урожай за сезон: 0.00 т",
            font=("Arial", 12, "bold"),
            fg="#2196F3",
            pady=10
        )
        self.total_label.pack()
    
    def _validate_input(self) -> tuple[bool, str, float, float]:
        """
        Валидация введенных пользователем данных.
        
        Returns:
            tuple: (is_valid, name, area, yield_per_hectare)
        """
        name = self.name_entry.get().strip()
        area_str = self.area_entry.get().strip()
        yield_str = self.yield_entry.get().strip()
        
        # Проверка названия
        if not name:
            messagebox.showerror("Ошибка", "Введите название культуры!")
            return False, "", 0.0, 0.0
        
        # Проверка площади
        try:
            area = float(area_str)
            if area <= 0:
                messagebox.showerror("Ошибка", "Площадь посева должна быть положительным числом!")
                return False, "", 0.0, 0.0
        except ValueError:
            messagebox.showerror("Ошибка", "Площадь посева должна быть числом!")
            return False, "", 0.0, 0.0
        
        # Проверка урожайности
        try:
            yield_per_hectare = float(yield_str)
            if yield_per_hectare <= 0:
                messagebox.showerror("Ошибка", "Урожайность должна быть положительным числом!")
                return False, "", 0.0, 0.0
        except ValueError:
            messagebox.showerror("Ошибка", "Урожайность должна быть числом!")
            return False, "", 0.0, 0.0
        
        return True, name, area, yield_per_hectare
    
    def _add_crop(self) -> None:
        """Добавление новой культуры в список."""
        is_valid, name, area, yield_per_hectare = self._validate_input()
        
        if not is_valid:
            return
        
        try:
            # Создание объекта культуры
            crop = Crop(name=name, area=area, yield_per_hectare=yield_per_hectare)
            
            # Добавление в список
            self.crops.append(crop)
            
            # Добавление в Listbox
            crop_info = f"{crop.name}: {crop.area} га × {crop.yield_per_hectare} т/га = {crop.total_harvest:.2f} т"
            self.crops_listbox.insert(tk.END, crop_info)
            
            # Очистка полей ввода
            self.name_entry.delete(0, tk.END)
            self.area_entry.delete(0, tk.END)
            self.yield_entry.delete(0, tk.END)
            
            # Фокус на первое поле
            self.name_entry.focus()
            
            messagebox.showinfo("Успех", f"Культура '{name}' успешно добавлена!")
            
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def _calculate_total(self) -> None:
        """Расчет и отображение общего урожая за сезон."""
        if not self.crops:
            messagebox.showwarning("Предупреждение", "Список культур пуст!")
            return
        
        # Использование цикла для расчета общего урожая
        total_harvest = calculate_total_season_harvest(self.crops)
        
        # Обновление метки
        self.total_label.config(
            text=f"Общий урожай за сезон: {total_harvest:.2f} т"
        )
        
        messagebox.showinfo(
            "Результат",
            f"Общий урожай за сезон составляет {total_harvest:.2f} тонн"
        )
    
    def _clear_list(self) -> None:
        """Очистка списка культур."""
        if not self.crops:
            messagebox.showinfo("Информация", "Список уже пуст!")
            return
        
        # Подтверждение очистки
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить весь список?"):
            self.crops.clear()
            self.crops_listbox.delete(0, tk.END)
            self.total_label.config(text="Общий урожай за сезон: 0.00 т")
            messagebox.showinfo("Успех", "Список очищен!")

