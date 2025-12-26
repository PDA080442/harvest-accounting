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
    
    # Современная цветовая палитра
    COLORS = {
        'bg_main': '#F8F9FA',           # Светло-серый фон
        'bg_card': '#FFFFFF',           # Белый для карточек
        'bg_input': '#FFFFFF',          # Белый для полей ввода
        'accent_green': '#28A745',      # Зеленый для добавления
        'accent_blue': '#007BFF',       # Синий для расчетов
        'accent_red': '#DC3545',        # Красный для удаления
        'accent_orange': '#FF6B35',    # Оранжевый для итогов
        'text_primary': '#212529',      # Темный текст
        'text_secondary': '#6C757D',    # Серый текст
        'border': '#DEE2E6',            # Светлая граница
        'hover_green': '#218838',
        'hover_blue': '#0056B3',
        'hover_red': '#C82333',
    }
    
    def __init__(self):
        """Инициализация главного окна приложения."""
        super().__init__()
        
        self.crops: List[Crop] = []  # Список культур
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self) -> None:
        """Настройка параметров окна."""
        self.title("🌾 Учет урожая")
        self.geometry("850x750")
        self.resizable(True, True)
        self.configure(bg=self.COLORS['bg_main'])
        
        # Центрирование окна
        self.update_idletasks()
        width = 850
        height = 750
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_styled_button(self, parent, text, command, color, hover_color):
        """Создание стилизованной кнопки с эффектом hover."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="black",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            bd=0,
            padx=20,
            pady=10,
            activebackground=hover_color,
            activeforeground="black"
        )
        
        # Эффект hover
        def on_enter(e):
            btn['bg'] = hover_color
        
        def on_leave(e):
            btn['bg'] = color
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def _create_card(self, parent):
        """Создание карточки с тенью (визуальный эффект через рамку)."""
        card = tk.Frame(
            parent,
            bg=self.COLORS['bg_card'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.COLORS['border'],
            highlightthickness=1
        )
        return card
    
    def _create_widgets(self) -> None:
        """Создание и размещение виджетов интерфейса."""
        # Главный контейнер
        main_container = tk.Frame(self, bg=self.COLORS['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # ========== ЗАГОЛОВОК ==========
        header_frame = tk.Frame(main_container, bg=self.COLORS['bg_main'])
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        title_label = tk.Label(
            header_frame,
            text="🌾 Учет урожая культур",
            font=("Segoe UI", 28, "bold"),
            fg=self.COLORS['text_primary'],
            bg=self.COLORS['bg_main'],
            pady=5
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Введите данные о культурах и рассчитайте общий урожай за сезон",
            font=("Segoe UI", 11),
            fg=self.COLORS['text_secondary'],
            bg=self.COLORS['bg_main'],
            pady=3
        )
        subtitle_label.pack()
        
        # ========== КАРТОЧКА ВВОДА ДАННЫХ ==========
        input_card = self._create_card(main_container)
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        input_inner = tk.Frame(input_card, bg=self.COLORS['bg_card'])
        input_inner.pack(fill=tk.BOTH, padx=30, pady=25)
        
        # Заголовок секции
        section_title = tk.Label(
            input_inner,
            text="Ввод данных о культуре",
            font=("Segoe UI", 14, "bold"),
            fg=self.COLORS['text_primary'],
            bg=self.COLORS['bg_card'],
            anchor="w"
        )
        section_title.pack(fill=tk.X, pady=(0, 20))
        
        # Поле: Название культуры
        self._create_input_field(
            input_inner,
            "Название культуры:",
            "name_entry"
        )
        
        # Поле: Площадь посева
        self._create_input_field(
            input_inner,
            "Площадь посева (га):",
            "area_entry"
        )
        
        # Поле: Урожайность
        self._create_input_field(
            input_inner,
            "Урожайность (т/га):",
            "yield_entry"
        )
        
        # ========== КНОПКИ ДЕЙСТВИЙ ==========
        button_frame = tk.Frame(main_container, bg=self.COLORS['bg_main'])
        button_frame.pack(pady=20)
        
        add_btn = self._create_styled_button(
            button_frame,
            "➕ Добавить культуру",
            self._add_crop,
            self.COLORS['accent_green'],
            self.COLORS['hover_green']
        )
        add_btn.pack(side=tk.LEFT, padx=8)
        
        calc_btn = self._create_styled_button(
            button_frame,
            "📊 Рассчитать урожай",
            self._calculate_total,
            self.COLORS['accent_blue'],
            self.COLORS['hover_blue']
        )
        calc_btn.pack(side=tk.LEFT, padx=8)
        
        clear_btn = self._create_styled_button(
            button_frame,
            "🗑️ Очистить список",
            self._clear_list,
            self.COLORS['accent_red'],
            self.COLORS['hover_red']
        )
        clear_btn.pack(side=tk.LEFT, padx=8)
        
        # ========== КАРТОЧКА СПИСКА КУЛЬТУР ==========
        list_card = self._create_card(main_container)
        list_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        list_inner = tk.Frame(list_card, bg=self.COLORS['bg_card'])
        list_inner.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # Заголовок списка
        list_title = tk.Label(
            list_inner,
            text="Список культур",
            font=("Segoe UI", 14, "bold"),
            fg=self.COLORS['text_primary'],
            bg=self.COLORS['bg_card'],
            anchor="w"
        )
        list_title.pack(fill=tk.X, pady=(0, 15))
        
        # Контейнер для списка
        listbox_container = tk.Frame(list_inner, bg=self.COLORS['bg_card'])
        listbox_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(
            listbox_container,
            bg=self.COLORS['bg_input'],
            troughcolor=self.COLORS['bg_main'],
            activebackground=self.COLORS['accent_blue'],
            width=14,
            relief=tk.FLAT
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.crops_listbox = tk.Listbox(
            listbox_container,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
            height=12,
            bg=self.COLORS['bg_input'],
            fg=self.COLORS['text_primary'],
            selectbackground=self.COLORS['accent_blue'],
            selectforeground="white",
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.COLORS['border'],
            activestyle='none'
        )
        self.crops_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.crops_listbox.yview)
        
        # ========== ИТОГОВАЯ ИНФОРМАЦИЯ ==========
        total_frame = tk.Frame(main_container, bg=self.COLORS['bg_main'])
        total_frame.pack(fill=tk.X, pady=10)
        
        self.total_label = tk.Label(
            total_frame,
            text="🌾 Общий урожай за сезон: 0.00 т",
            font=("Segoe UI", 16, "bold"),
            fg=self.COLORS['accent_orange'],
            bg=self.COLORS['bg_main'],
            pady=8
        )
        self.total_label.pack()
    
    def _create_input_field(self, parent, label_text, entry_attr):
        """Создание поля ввода с меткой."""
        field_frame = tk.Frame(parent, bg=self.COLORS['bg_card'])
        field_frame.pack(fill=tk.X, pady=10)
        
        # Метка
        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Segoe UI", 10),
            fg=self.COLORS['text_primary'],
            bg=self.COLORS['bg_card'],
            width=22,
            anchor="w"
        )
        label.pack(side=tk.LEFT)
        
        # Поле ввода
        entry = tk.Entry(
            field_frame,
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            bd=1,
            bg=self.COLORS['bg_input'],
            fg=self.COLORS['text_primary'],
            highlightthickness=1,
            highlightbackground=self.COLORS['border'],
            highlightcolor=self.COLORS['accent_blue'],
            insertbackground=self.COLORS['accent_blue']
        )
        entry.pack(side=tk.LEFT, padx=(10, 0), ipadx=10, ipady=8, fill=tk.X, expand=True)
        
        # Сохранение ссылки на поле ввода
        setattr(self, entry_attr, entry)
    
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
            
            # Форматирование для отображения
            crop_info = (
                f"{crop.name:20s} │ "
                f"{crop.area:>7.2f} га × "
                f"{crop.yield_per_hectare:>6.2f} т/га = "
                f"{crop.total_harvest:>8.2f} т"
            )
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
            text=f"🌾 Общий урожай за сезон: {total_harvest:.2f} т"
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
            self.total_label.config(text="🌾 Общий урожай за сезон: 0.00 т")
            messagebox.showinfo("Успех", "Список очищен!")
