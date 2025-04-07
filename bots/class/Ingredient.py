class Ingredient:
    memory = set()

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        Ingredient.memory.add(self)
        print(f"Створено новий інгредієнт : {name}")

    def __repr__(self):
        return f"{self.name} ({self.unit})"

    @classmethod
    def add_ingredient(cls, *ingredients):
        for ingredient in ingredients:
            cls.memory.add(ingredient)