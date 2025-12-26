"""
Модуль для расчетов урожая.

Содержит функции для расчета общего урожая за сезон.
"""
from typing import List

from ..models.crop import Crop


def calculate_total_season_harvest(crops: List[Crop]) -> float:
    """
    Рассчитывает общий объем урожая за сезон для всех культур.
    
    Использует цикл для суммирования общего урожая каждой культуры
    из переданного списка.
    
    Args:
        crops: Список объектов Crop с информацией о культурах
    
    Returns:
        float: Общий объем урожая за сезон в тоннах
    
    Example:
        >>> crop1 = Crop("Пшеница", 10.0, 3.5)
        >>> crop2 = Crop("Ячмень", 5.0, 2.8)
        >>> total = calculate_total_season_harvest([crop1, crop2])
        >>> print(f"Общий урожай: {total} т")
    """
    total_harvest = 0.0
    
    # Цикл для суммирования урожая всех культур
    for crop in crops:
        total_harvest += crop.total_harvest
    
    return total_harvest

