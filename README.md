# Автор

Калажокова Лиана 
Группа: БТАДБ251
lizakalazhokova@edu.hse.ru

# Название и краткое описание

Recipe Manager
Система для управления рецептами, масштабирования порций и составления списка покупок.
Проект реализован в виде 4 классов (Ingredients, Recipe, ShoppingList, DietaryRecipe),
которые позволяют создавать рецепты из ингредиентов, указывать тип диеты на рецепты, 
а также составлять список покупок на основании блюд, которые пользователь желает приготовить.

# Использование

`Установка:`

1. Клонируйте репозиторий
git clone https://github.com/Liana-K-o-0/TP-Homework2.git
2. Перейдите в папку проекта
cd TP-Homework2
3. Установите зависимости
pip install -r requierements.txt
4. Запустите тесты (опционально)
pytest

`Пример использования:`

bread = Ingredient("Хлеб", 2, "ломтик")
cheese = Ingredient("Сыр плавленый", 2, "кусочек")
sausage = Ingredient("Колбаса", 2, "ломтик")

sandwich = Recipe("Бутерброд",[bread,cheese,sausage])

sandwich_for_three = sandwich.scale(3)

shopping = ShoppingList()
shopping.add_recipe(sandwich, 2)

print("Список покупок для 2 бутербродов:")
for ing in shopping.get_list():
    print(ing)