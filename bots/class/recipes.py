from Recipe import Recipe
from ingredients import *
from categories import *
from difficulties import *

pancake_recipe = Recipe(
    name="Млинці",
    description="Смачні млинці на сніданок.",
    category=breakfast,
    time=15,
    difficulty=easy,
    ingredients=[flour, sugar, eggs],
    instructions="Змішай інгредієнти і підсмаж на сковороді.")

lunch_recipe = Recipe(
    name="Смажене куряче філе з овочами",
    description="Здорова та смачна страва з курячого філе з овочами.",
    category=dinner,
    time=30,
    difficulty=medium,
    ingredients=[chicken_fillet, bell_pepper, carrot, onion, olive_oil, garlic, salt, black_pepper, herbs],
    instructions=(
        "  1. Наріжте куряче філе на тонкі смужки.\n"
        "  2. Розігрійте оливкову олію на сковороді.\n"
        "  3. Додайте подрібнений часник і смажте протягом 1 хвилини.\n"
        "  4. Додайте куряче філе та смажте до золотистого кольору.\n"
        "  5. Наріжте болгарський перець, моркву і цибулю, потім додайте до сковороди.\n"
        "  6. Смажте все разом ще 10 хвилин.\n"
        "  7. Приправте сіллю, чорним перцем і травами. Подавати гарячим.")
    )

snack_recipe = Recipe(
    name="Пластівці на молоці",
    description="Простий рецепт пластівців на молоці, ідеальний для легкого підвечірка.",
    category=breakfast,
    time=10,
    difficulty=easy,
    ingredients=[oats, milk, salt],
    instructions=(
        "1. Налийте молоко в каструлю і доведіть до кипіння.\n"
        "2. Додайте пластівці та дрібку солі.\n"
        "3. Варіть на повільному вогні протягом 5-7 хвилин, постійно помішуючи.\n"
        "4. Подавайте гарячими.")
    )
new_recipe = Recipe(
    name="Грандіозний рецепт"
)

print()
Recipe.add_recipe(pancake_recipe, lunch_recipe, snack_recipe, new_recipe)