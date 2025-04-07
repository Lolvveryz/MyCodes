from Category import Category
from Recipe import Recipe
from Ingredient import Ingredient
from Difficulty import Difficulty
from User import User
from rich import print

import categories, ingredients, difficulties, recipes
class RecipeManagementSystem:
    memory = {
        "ingredients": set(),
        "categories": set(),
        "difficulties": set(),
        "recipes": set(),
        "users": set()
    }

    def pre_reload(self):
        # Preloading memory from existing static data
        for category in Category.memory:
            self.add_category(category)
        for ingredient in Ingredient.memory:
            self.add_ingredient(ingredient)
        for difficulty in Difficulty.memory:
            self.add_difficulty(difficulty)
        for recipe in Recipe.memory:
            self.add_recipe(recipe)

        print(f"\n{'*' * 34}\nЗавантаження бази даних завершено!\n{'*' * 34}\n")


    # ---------------------- MENU ---------------------
    def start_menu(self):
        while True:
            print(
                "\n\n########  ########  ######  #### ########  ########    ##     ##    ###    ##    ##    ###     ######   ######## ########\n"
                "##     ## ##       ##    ##  ##  ##     ## ##          ###   ###   ## ##   ###   ##   ## ##   ##    ##  ##       ##     ##\n"
                "##     ## ##       ##        ##  ##     ## ##          #### ####  ##   ##  ####  ##  ##   ##  ##        ##       ##     ##\n"
                "########  ######   ##        ##  ########  ######      ## ### ## ##     ## ## ## ## ##     ## ##   #### ######   ########  \n"
                "##   ##   ##       ##        ##  ##        ##          ##     ## ######### ##  #### ######### ##    ##  ##       ##   ##   \n"
                "##    ##  ##       ##    ##  ##  ##        ##          ##     ## ##     ## ##   ### ##     ## ##    ##  ##       ##    ##  \n"
                "##     ## ########  ######  #### ##        ########    ##     ## ##     ## ##    ## ##     ##  ######   ######## ##     ##\n"
            )

            try:
                choice = int(input("1-Створити щось нове \n2-Переглянути каталог існуючого \n3-Редагувати каталог\n0-Вийти з програми\n Виберіть опцію : "))
            except ValueError:
                print("Будь ласка, введіть коректний номер.")
                continue

            if choice == 0:
                print("Вихід з програми.")
                break
            elif choice == 1:
                self.create_menu()
            elif choice == 2:
                self.view_menu()
            elif choice == 3:
                self.edit_menu()
            else:
                print("Невірний вибір. Спробуйте ще раз.")

    def create_menu(self):
        try:
            option = int(input("\n1-Створити рецепт\n2-Створити інгредієнт\n3-Створити категорію\n4-Створити користувач\n Виберіть опцію : "))
        except ValueError:
            print("Невірний вибір.")
            return

        match option:
            case 1:
                self.add_recipe()
            case 2:
                self.add_ingredient()
            case 3:
                self.add_category()
            case 4:
                self.register_user()
            case _:
                print("Такого варіанту відповіді немає")

    def view_menu(self):
        try:
            option = int(input("\n1-Список всіх рецептів\n2-Список всіх інгредієнтів\n3-Список всіх категорій\n Виберіть опцію : "))
        except ValueError:
            print("Невірний вибір.")
            return

        match option:
            case 1:
                for num, recipe_name in enumerate(self.show_all_recipes(), start=1):
                    print(f"{num} - {recipe_name}")
                dtails = int(input("\nДетальніше про рецепт (Введіть номер рецепту) або 0 для виходу : "))
                if dtails:  
                    recipe_details = list(self.memory["recipes"])[dtails - 1].get_recipe_details()
                    for key, value in recipe_details.items():
                        print(f"[red]{key}[/red] - {value}")
            case 2:
                for num, ingredient_name in enumerate(self.show_all_ingredients(), start=1):
                    print(f"{num} - {ingredient_name}")
            case 3:
                for num, category_name in enumerate(self.show_all_categories(), start=1):
                    print(f"{num} - {category_name}")

    def edit_menu(self):
        try:
            option = int(input("\n1-Редагувати рецепт\n2-Редагувати користувача\n Виберіть опцію : "))
        except ValueError:
            print("Невірний вибір.")
            return

        match option:
            case 1:
                self.edit_recipe()
            case 2:
                self.edit_user()
            case _:
                print("Невірний вибір.")

        
    # ---------------------- MENU ---------------------


    # ---------------------- ADD ---------------------
    def add_recipe(self, recipe=None):
        if recipe:
            self.memory["recipes"].add(recipe)
            print(f"{recipe.name} успішно додано в систему")
        else:
            print("\nВведіть дані для нового рецепту:")
            name = input("Назва рецепту: ")
            description = input("Опис рецепту: ")
            category = self.select_category()
            time = input("Час приготування (у хвилинах): ")
            difficulty = self.select_difficulty()
            ingredients = self.select_ingredients()
            instructions = input("Інструкції для приготування: ")
            photo = input("Посилання на фото (необов'язково): ")

            new_recipe = Recipe(name, description, category, time, difficulty, ingredients, instructions, photo)
            self.memory["recipes"].add(new_recipe)
            print(f"Рецепт '{name}' успішно створено!")

    def add_category(self, category=None):
        if category:
            self.memory["categories"].add(category)
            print(f"{category.name} успішно додано в систему")
        else:
            print("\nВведіть дані для нової категорії:")
            name = input("Назва категорії: ")
            description = input("Опис категорії: ")

            new_category = Category(name, description)
            self.memory["categories"].add(new_category)
            print(f"Категорію '{name}' успішно створено!")

    def add_ingredient(self, ingredient=None):
        if ingredient:
            self.memory["ingredients"].add(ingredient)
            print(f"{ingredient.name} успішно додано в систему")
        else:
            print("\nВведіть дані для нового інгредієнта:")
            name = input("Назва інгредієнта: ")
            unit = input("Одиниця виміру (кг, л, шт. тощо): ")

            new_ingredient = Ingredient(name, unit)
            self.memory["ingredients"].add(new_ingredient)
            print(f"Інгредієнт '{name}' успішно створено!")

    def add_difficulty(self, difficulty):
        self.memory["difficulties"].add(difficulty)

    def register_user(self, user=None):
        if user:
            self.memory["users"].add(user)
            print(f"{user.name} успішно зареєстровано в систему")
        else:
            print("\nРеєстрація нового користувача:")
            name = input("Ім'я користувача: ")
            email = input("Email користувача: ")
            password = input("Пароль: ")

            new_user = User(name, email, password)
            self.memory["users"].add(new_user)
            print(f"Користувача '{name}' успішно зареєстровано в систему")
    # ---------------------- ADD ---------------------


    # ---------------------- EDIT ---------------------
    def delete_recipe(self, name):
        for recipe in self.memory["recipes"]:
            if recipe.name == name:
                self.memory["recipes"].discard(recipe)
                print(f"{name} видалено")
                break
        else:
            print("Такого рецепту немає в списку")

    def edit_recipe(self):
        if not self.memory["recipes"]:
            print("Немає рецептів для редагування.")
            return

        print("\nВиберіть рецепт для редагування:")
        for index, recipe in enumerate(self.memory["recipes"], start=1):
            print(f"{index} - {recipe.name}")

        try:
            choice = int(input("Введіть номер рецепту: ")) - 1
            recipe_to_edit = list(self.memory["recipes"])[choice]
        except (ValueError, IndexError):
            print("Неправильний вибір.")
            return

        new_name = input("Нова назва рецепту (залиште порожнім, щоб не змінювати): ")
        new_description = input("Новий опис рецепту (залиште порожнім, щоб не змінювати): ")
        new_category = self.select_category() if input("Змінити категорію? (y/n): ").lower() == 'y' else None
        new_time = input("Новий час приготування (залиште порожнім, щоб не змінювати): ")
        new_difficulty = self.select_difficulty() if input("Змінити складність? (y/n): ").lower() == 'y' else None
        new_ingredients = self.select_ingredients() if input("Змінити інгредієнти? (y/n): ").lower() == 'y' else None
        new_instructions = input("Нові інструкції (залиште порожнім, щоб не змінювати): ")

        if new_name:
            recipe_to_edit.name = new_name
        if new_description:
            recipe_to_edit.description = new_description
        if new_category:
            recipe_to_edit.category = new_category
        if new_time:
            recipe_to_edit.time = new_time
        if new_difficulty:
            recipe_to_edit.difficulty = new_difficulty
        if new_ingredients:
            recipe_to_edit.ingredients = new_ingredients
        if new_instructions:
            recipe_to_edit.instructions = new_instructions

        print(f"Рецепт '{recipe_to_edit.name}' успішно відредаговано!")

    def edit_user(self):
        if not self.memory["users"]:
            print("Немає користувачів для редагування.")
            return

        print("\nВиберіть користувача для редагування:")
        for index, user in enumerate(self.memory["users"], start=1):
            print(f"{index} - {user.name}")

        try:
            choice = int(input("Введіть номер користувача: ")) - 1
            user_to_edit = list(self.memory["users"])[choice]
        except (ValueError, IndexError):
            print("Неправильний вибір.")
            return

        new_name = input("Нове ім'я користувача (залиште порожнім, щоб не змінювати): ")
        new_email = input("Новий email користувача (залиште порожнім, щоб не змінювати): ")
        new_password = input("Новий пароль (залиште порожнім, щоб не змінювати): ")

        if new_name:
            user_to_edit.name = new_name
        if new_email:
            user_to_edit.email = new_email
        if new_password:
            user_to_edit.password = new_password

        print(f"Користувача '{user_to_edit.name}' успішно відредаговано!")
    # ---------------------- EDIT ---------------------


    # ---------------------- SEARCH ---------------------
    def search_recipes(self, name=None, category=None, time=None):
        results = self.memory["recipes"]
        if name:
            results = [recipe for recipe in results if name.lower() == recipe.name.lower()]
        elif category:
            results = [recipe for recipe in results if recipe.category == category]
        elif time:
            results = [recipe for recipe in results if recipe.time == time]
        print(f"За запитом {name if name else category.name if category else time} знайдено : {', '.join([i.name for i in results])}")
        return results
    # ---------------------- SEARCH ---------------------


    # ---------------------- SHOW ---------------------

    def show_all_recipes(self):
        return [recipe.name for recipe in self.memory["recipes"]]

    def show_all_categories(self):
        return [category.name for category in self.memory["categories"]]

    def show_all_ingredients(self):
        return [ingredient.name for ingredient in self.memory["ingredients"]]

    def show_all_difficulties(self):
        return [difficulty.value for difficulty in self.memory["difficulties"]]
    # ---------------------- SHOW ---------------------

    
    # ---------------------- SELECT ---------------------
    def select_category(self):
        print("\nОберіть категорію:")
        for num, category in enumerate(self.show_all_categories(), start=1):
            print(f"{num} - {category}")
        choice = int(input("Введіть номер категорії або 0 для створення нової: "))
        if choice == 0:
            self.add_category()
            return list(self.memory["categories"])[-1]
        return list(self.memory["categories"])[choice - 1]

    def select_ingredients(self):
        ingredients = []
        while True:
            print("\nОберіть інгредієнт:")
            for num, ingredient in enumerate(self.show_all_ingredients(), start=1):
                print(f"{num} - {ingredient}")
            choice = int(input("Введіть номер інгредієнта або 0 для створення нового: "))
            if choice == 0:
                self.add_ingredient()
                ingredients.append(list(self.memory["ingredients"])[-1])
            else:
                ingredients.append(list(self.memory["ingredients"])[choice - 1])

            more = input("Додати ще інгредієнт? (y/n): ").strip().lower()
            if more != 'y':
                break
        return ingredients

    def select_difficulty(self):
        print("\nОберіть складність:")
        for num, difficulty in enumerate(self.show_all_difficulties(), start=1):
            print(f"{num} - {difficulty}")
        choice = int(input("Введіть номер складності або 0 для створення нової: "))
        if choice == 0:
            value = input("Введіть назву складності (наприклад, Легко, Середньо, Важко): ")
            new_difficulty = Difficulty(value)
            self.memory["difficulties"].add(new_difficulty)
            return new_difficulty
        return list(self.memory["difficulties"])[choice - 1]
    # ---------------------- SELECT ---------------------


    def __init__(self):
        self.pre_reload()
        self.start_menu()
