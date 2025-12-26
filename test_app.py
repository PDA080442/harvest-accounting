"""
Тестовый скрипт для проверки функциональности приложения.

Проверяет работу модели данных и функций расчета без GUI.
"""
from src.models import Crop
from src.utils import calculate_total_season_harvest


def test_crop_creation():
    """Тест создания культуры."""
    print("Тест 1: Создание культуры...")
    crop = Crop(name="Пшеница", area=10.0, yield_per_hectare=3.5)
    assert crop.name == "Пшеница"
    assert crop.area == 10.0
    assert crop.yield_per_hectare == 3.5
    assert crop.total_harvest == 35.0
    print("✓ Тест пройден: культура создана корректно")
    print(f"  {crop}\n")


def test_crop_calculation():
    """Тест расчета урожая."""
    print("Тест 2: Расчет урожая культуры...")
    crop = Crop(name="Ячмень", area=5.0, yield_per_hectare=2.8)
    expected = 5.0 * 2.8
    assert crop.total_harvest == expected
    print(f"✓ Тест пройден: урожай рассчитан корректно ({expected} т)\n")


def test_multiple_crops():
    """Тест добавления нескольких культур."""
    print("Тест 3: Добавление нескольких культур...")
    crops = [
        Crop("Пшеница", 10.0, 3.5),
        Crop("Ячмень", 5.0, 2.8),
        Crop("Овес", 8.0, 2.5)
    ]
    assert len(crops) == 3
    print("✓ Тест пройден: добавлено 3 культуры")
    for crop in crops:
        print(f"  - {crop.name}: {crop.total_harvest:.2f} т")
    print()


def test_total_season_harvest():
    """Тест расчета общего урожая за сезон."""
    print("Тест 4: Расчет общего урожая за сезон...")
    crops = [
        Crop("Пшеница", 10.0, 3.5),   # 35.0 т
        Crop("Ячмень", 5.0, 2.8),     # 14.0 т
        Crop("Овес", 8.0, 2.5)        # 20.0 т
    ]
    total = calculate_total_season_harvest(crops)
    expected = 35.0 + 14.0 + 20.0
    assert total == expected
    print(f"✓ Тест пройден: общий урожай = {total:.2f} т (ожидалось {expected:.2f} т)\n")


def test_validation():
    """Тест валидации данных."""
    print("Тест 5: Валидация данных...")
    
    # Тест отрицательной площади
    try:
        Crop("Пшеница", -10.0, 3.5)
        assert False, "Должна быть ошибка для отрицательной площади"
    except ValueError as e:
        print(f"✓ Отрицательная площадь обработана: {e}")
    
    # Тест нулевой урожайности
    try:
        Crop("Пшеница", 10.0, 0.0)
        assert False, "Должна быть ошибка для нулевой урожайности"
    except ValueError as e:
        print(f"✓ Нулевая урожайность обработана: {e}")
    
    # Тест пустого названия
    try:
        Crop("", 10.0, 3.5)
        assert False, "Должна быть ошибка для пустого названия"
    except ValueError as e:
        print(f"✓ Пустое название обработано: {e}")
    
    print("✓ Тест пройден: валидация работает корректно\n")


def main():
    """Запуск всех тестов."""
    print("=" * 50)
    print("Запуск тестов приложения 'Учет урожая'")
    print("=" * 50)
    print()
    
    try:
        test_crop_creation()
        test_crop_calculation()
        test_multiple_crops()
        test_total_season_harvest()
        test_validation()
        
        print("=" * 50)
        print("✓ Все тесты пройдены успешно!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n✗ Ошибка теста: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Неожиданная ошибка: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

