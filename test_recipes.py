import pytest
from ingredient import Ingredient
from recipe import Recipe

#ТЕСТЫ ДЛЯ INGREDIENT

def test_ingredient_initialization():
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


def test_ingredient_str():
    ingredient = Ingredient("Мука",500.0,"г")
    assert str(ingredient) == "Мука: 500.0 г"

    ingredient2 = Ingredient("Яйца",3,"шт")
    assert str(ingredient2) == "Яйца: 3.0 шт"

def test_ingredient_eq():
    assert Ingredient("Молоко",2,"литра") == Ingredient("Молоко",3,"литра")
    assert Ingredient("Вода",2,"литра") != Ingredient("Молоко",2,"литра")
    assert Ingredient("Молоко",2,"литра") != Ingredient("Молоко",2,"кг")

#ТЕСТЫ ДЛЯ RECIPE

def test_recipe_initialisation():
    ingredients = [
        Ingredient("Яйца", 2, "шт"),
        Ingredient("Молоко", 50, "мл"),
        Ingredient("Соль", 1, "щепотка")
    ]
    recipe = Recipe("Омлет",ingredients)
    assert recipe.title == "Омлет"
    assert recipe.ingredients == ingredients
    assert len(recipe.ingredients) == 3

def test_recipe_add_ingredient():
    ingredients = [
        Ingredient("Яйца", 2, "шт"),
        Ingredient("Молоко", 50, "мл"),
        Ingredient("Соль", 1, "щепотка")
    ]
    recipe = Recipe("Омлет",ingredients)

    new_ing = Ingredient("Мука",2,"столовых ложки")
    recipe.add_ingredient(new_ing)
    assert any(ing.name == "Мука" and ing.unit == "столовых ложки" for ing in recipe.ingredients)
    assert len(recipe.ingredients) == 4

    new_ing2 = Ingredient("Молоко",20,"мл")
    recipe.add_ingredient(new_ing2)
    assert len(recipe.ingredients) == 4
    for ing in recipe.ingredients:
        if ing.name == "Молоко" and ing.unit == "мл":
            assert ing.quantity == 70
            break
    else:
        pytest.fail("Ингредиент 'Молоко' не найден")

def test_recipe_scale():
    ingredients = [
        Ingredient("Яйца", 2, "шт"),
        Ingredient("Молоко", 50, "мл"),
        Ingredient("Соль", 1, "щепотка")
    ]
    recipe = Recipe("Омлет",ingredients)
    scaled = recipe.scale(2)
    assert scaled is not recipe
    assert scaled.title == recipe.title
    for orig_ing,scaled_ing in zip(recipe.ingredients, scaled.ingredients):
        assert scaled_ing.quantity == orig_ing.quantity * 2
    
    with pytest.raises(ValueError,match="Коэффициент масштабирования должен быть положительным"):
        recipe.scale(-2)
    with pytest.raises(ValueError,match="Коэффициент масштабирования должен быть положительным"):
        recipe.scale(0)

def test_recipe_len():
    recipe = Recipe("Тест",[])
    recipe.add_ingredient(Ingredient("Мука",500,"г"))
    recipe.add_ingredient(Ingredient("Яйца", 2, "шт"))
    recipe.add_ingredient(Ingredient("Мука",200,"г"))
    recipe.add_ingredient(Ingredient("Молоко", 100, "мл"))
    assert len(recipe) == 3