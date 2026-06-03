from recipe import Recipe

class DietaryRecipe(Recipe):

    def __init__(self,title:str,diet_type,ingredients=None):
        self.diet_type = diet_type
        if ingredients == None:
            ingredients = []
        super().__init__(title,ingredients)
    
    def scale(self,ratio:float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть положительным")
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(scaled_recipe.title,self.diet_type,scaled_recipe.ingredients)
    
    def __str__(self):
        text = super().__str__()
        return f"[{self.diet_type}] {text}"