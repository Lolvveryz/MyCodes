class Recipe:
    memory = set()

    def __init__(self, name=None, description=None, category=None, time=None, difficulty=None, ingredients=None, instructions=None, photo=None):
        self.name = name if name else "Без назви"
        self.description = description if description else "Немає опису"
        self.category = category
        self.time = time if time else "Невідомо"
        self.difficulty = difficulty
        self.ingredients = ingredients if ingredients else []
        self.instructions = instructions if instructions else "Інструкції відсутні"
        self.photo = photo if photo else "Відсутнє"
        self.ratings = []
        self.comments = []
        
        Recipe.memory.add(self)
        print(f"Створено новий рецепт : {self.name}")

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.ratings.append(rating)
        else:
            print("Оцінка має бути від 1 до 5")

    def add_comment(self, comment):
        self.comments.append(comment)

    def avg_rating(self):
        if self.ratings:
            avg = sum(self.ratings) / len(self.ratings)
            return round(avg, 1)
        return "Поки немає"

    def get_recipe_details(self):
        details = {
            "Назва": self.name,
            "Опис": self.description,
            "Категорія": self.category.name if self.category else 'Невідома',
            "Час приготування": self.time,
            "Складність": self.difficulty.value if self.difficulty else 'Не визначено',
            "Список інгредієнтів": ', '.join([i.name for i in self.ingredients]) if self.ingredients else 'Відсутні',
            "Інструкції приготування": self.instructions,
            "Коментарі": ', '.join(self.comments) if self.comments else 'Відсутні',
            "Середній рейтинг": self.avg_rating(),
            "Посилання на фото": self.photo
        }
        return details

    @classmethod
    def add_recipe(cls, *recipes):
        for recipe in recipes:
            cls.memory.add(recipe)

    def __repr__(self):
        return f"{self.name} ({self.category.name if self.category else 'Невідома категорія'})"
