class Difficulty:
    memory = set()

    def __init__(self, value):
        self.value = value
        Difficulty.memory.add(self)
        print(f"Додано новий рівень складності : {self.value}")

    def __repr__(self):
        return self.value

    @classmethod
    def add_difficulty(cls, *difficulties):
        for difficulty in difficulties:
            cls.memory.add(difficulty)