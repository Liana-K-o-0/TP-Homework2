import pytest
from ingredient import Ingredient

def test_initialization():
    ingredient = Ingredient("Мука",500.0,"г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"

    ingredient2 = Ingredient("Мука",500,"г")
    assert ingredient2.quantity == 500.0

    with pytest.raises(ValueError,match="Количество должно быть положительным"):
        Ingredient("Соль", -5, "г")
    with pytest.raises(ValueError,match="Количество должно быть положительным"):
        Ingredient("Соль", 0, "г")


def test_str():
    ingredient = Ingredient("Мука",500.0,"г")
    assert str(ingredient) == "Мука: 500.0 г"

    ingredient2 = Ingredient("Яйца",3,"шт")
    assert str(ingredient2) == "Яйца: 3.0 шт"

def test_eq():
    assert Ingredient("Молоко",2,"литра") == Ingredient("Молоко",3,"литра")
    assert Ingredient("Вода",2,"литра") != Ingredient("Молоко",2,"литра")
    assert Ingredient("Молоко",2,"литра") != Ingredient("Молоко",2,"кг")
