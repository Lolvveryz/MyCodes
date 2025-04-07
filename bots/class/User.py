class User:
    memory = set()

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.saved_recipes = set()
        User.memory.add(self)
        print(f"Створено нового користувача : {self.name}")

    def save_recipe(self, recipe):
        self.saved_recipes.add(recipe)
        print(f"Рецепт '{recipe.name}' збережено для користувача {self.name}")

    @classmethod
    def add_user(cls, *users):
        for user in users:
            cls.memory.add(user)

    def __repr__(self):
        return f"{self.name} ({self.email})"