class Category:
    memory = set()

    def __init__(self, name, description):
        self.name = name
        self.description = description
        Category.memory.add(self)
        print(f"Створено нову категорію : {name}")

    def __repr__(self):
        return f"{self.name} - {self.description}"

    @classmethod
    def add_category(cls, *categories):
        for category in categories:
            cls.memory.add(category)