from ingredient import Ingredient
from recipe import Recipe

class ShoppingList:

    def __init__(self):
        self._items = []
    
    def add_recipe(self, recipe:Recipe, portions:float):
        if portions<=0:
            raise ValueError("Количество порций должно быть положительным")
        new_recipe = recipe.scale(portions)
        for ingredient in new_recipe.ingredients:
            self._items.append((ingredient,recipe.title))

    def remove_recipe(self, title:str):
        new_items = []
        for item in self._items:
            if item[1] != title:
                new_items.append(item)
        _items = new_items

    def get_list(self):
        totals_dict = {}
        for ingredient, _ in self._items:
            key = (ingredient.name,ingredient.unit)
            totals_dict[key] = totals_dict.get(key, 0.0) + ingredient.quantity

        result = [Ingredient(name,quantity,unit) for (name,unit),quantity in totals_dict.items()]
        result.sort(key=lambda ing: ing.name)
        return result
    
    def __add__(self, other:ShoppingList):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list