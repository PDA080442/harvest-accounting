"""
Модель данных для культуры.

Содержит структуру данных для хранения информации о культуре:
название, площадь посева, урожайность и общий объем урожая.
"""
from dataclasses import dataclass


@dataclass
class Crop:
    """
    Структура данных для хранения информации о культуре.
    
    Attributes:
        name: Название культуры
        area: Площадь посева в гектарах
        yield_per_hectare: Урожайность в тоннах на гектар
        total_harvest: Общий объем урожая в тоннах (рассчитывается автоматически)
    """
    name: str
    area: float
    yield_per_hectare: float
    total_harvest: float = 0.0
    
    def __post_init__(self):
        """
        Валидация данных и расчет общего урожая после инициализации.
        
        Raises:
            ValueError: Если площадь или урожайность отрицательные или равны нулю
        """
        self._validate_data()
        self.total_harvest = self.calculate_total_harvest()
    
    def _validate_data(self) -> None:
        """
        Проверяет корректность введенных данных.
        
        Raises:
            ValueError: Если данные некорректны
        """
        if self.area <= 0:
            raise ValueError("Площадь посева должна быть положительным числом")
        if self.yield_per_hectare <= 0:
            raise ValueError("Урожайность должна быть положительным числом")
        if not self.name or not self.name.strip():
            raise ValueError("Название культуры не может быть пустым")
    
    def calculate_total_harvest(self) -> float:
        """
        Рассчитывает общий объем урожая.
        
        Формула: Общий урожай = Площадь посева × Урожайность
        
        Returns:
            float: Общий объем урожая в тоннах
        """
        return self.area * self.yield_per_hectare
    
    def __str__(self) -> str:
        """
        Строковое представление объекта для удобного вывода.
        
        Returns:
            str: Форматированная строка с информацией о культуре
        """
        return (f"Культура: {self.name}, "
                f"Площадь: {self.area} га, "
                f"Урожайность: {self.yield_per_hectare} т/га, "
                f"Общий урожай: {self.total_harvest:.2f} т")

