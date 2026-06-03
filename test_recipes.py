import pytest
from ingredient import Ingredient
from recipe import Recipe
from shopping_list import ShoppingList

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

# ТЕСТЫ ДЛЯ SHOPPING LIST

@pytest.fixture
def sample_recipe():
    ingredients = [
        Ingredient("Яйца", 2, "шт"),
        Ingredient("Молоко", 50, "мл"),
        Ingredient("Соль", 1, "щепотка")
    ]
    return Recipe("Омлет",ingredients)

@pytest.fixture
def sample_recipe2():
    ingredients = [
        Ingredient("Мука", 100, "г"),
        Ingredient("Яйца", 1, "шт"),
        Ingredient("Молоко", 150, "мл"),
        Ingredient("Сахар", 10, "г")
    ]
    return Recipe("Блины",ingredients)

def test_shoplist_addrecipe(sample_recipe):
    shop_list1 = ShoppingList()
    shop_list1.add_recipe(sample_recipe,2)
    items = shop_list1._items
    assert len(items) == 3
    expected = [
        (Ingredient("Яйца", 2, "шт"), "Омлет"),
        (Ingredient("Молоко", 50, "мл"), "Омлет"),
        (Ingredient("Соль", 1, "щепотка"), "Омлет")
    ]
    for exp_ing, exp_title in expected:
        found = any(item[0].name == exp_ing.name and 
                    item[0].unit == exp_ing.unit and 
                    item[0].quantity == exp_ing.quantity and
                    item[1] == exp_title for item in items)
        assert found
    
    shop_list2 = ShoppingList()
    with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
        shop_list2.add_recipe(sample_recipe, -1)
    with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
        shop_list2.add_recipe(sample_recipe, 0)
    
def test_shoplist_removerecipe(sample_recipe,sample_recipe2):
    shoplist = ShoppingList()
    shoplist.add_recipe(sample_recipe,2)
    shoplist.add_recipe(sample_recipe2,3)

    shoplist.remove_recipe(sample_recipe2.title)
    for item in shoplist._items:
        assert item[1] == sample_recipe.title
    assert len(shoplist._items) == len(sample_recipe.ingredients)

def test_shoplist_getlist(sample_recipe,sample_recipe2):
    shopping = ShoppingList()
    shopping.add_recipe(sample_recipe,1)
    shopping.add_recipe(sample_recipe2,1)
    result = shopping.get_list()
    expected = [
        Ingredient("Мука", 100, "г"),
        Ingredient("Яйца", 3, "шт"),
        Ingredient("Молоко", 200, "мл"),
        Ingredient("Сахар", 10, "г"),
        Ingredient("Соль", 1, "щепотка")
    ]
    expected.sort(key=lambda x: x.name)
    assert len(result) == 5
    for ing,exp in zip(result,expected):
        assert ing.name == exp.name
        assert ing.quantity == exp.quantity
        assert ing.unit == exp.unit

    names = [ing.name for ing in result]
    assert names == sorted(names) #имена отсортированы

def test_shoplist_add(sample_recipe,sample_recipe2):
    shop1 = ShoppingList()
    shop1.add_recipe(sample_recipe,1)
    shop1_items_safe_copy = shop1._items.copy()
    shop2 = ShoppingList()
    shop2.add_recipe(sample_recipe2,1)
    shop2_items_safe_copy = shop2._items.copy()

    merge = shop1 + shop2
    assert len(merge._items) == len(shop1._items) + len(shop2._items)
    for item in shop1._items:
        assert item in merge._items
    for item in shop2._items:
        assert item in merge._items
    
    assert shop1._items == shop1_items_safe_copy
    assert shop2._items == shop2_items_safe_copy