from ingredient import Ingredient

class Recipe:

    def __init__(self, title:str ,ingredients:list[Ingredient]):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient : Ingredient):
        for item in self.ingredients:
            if item == ingredient:
                item.quantity += ingredient.quantity
                break
        else:
            self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int,float)) and ratio>0
    
    def scale(self,ratio: float):
        new_recipe = Recipe(self.title, [Ingredient(ing.name,ing.quantity*ratio,ing.unit) for ing in self.ingredients])
        return new_recipe
    
    def __len__(self):
        return len(self.ingredients)
    
    def __str__(self):
        text = f"Блюдо '{self.title}':\n"
        for ing in self.ingredients:
            text += f"{ing}\n"
        return text