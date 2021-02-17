import re
import units
import yaml


class Food(object):

    def __init__(self, name, unit, size, carbs, protein, fat):
        self._name = name
        self._unit = unit
        self._size = size
        self._carbs = carbs
        self._protein = protein
        self._fat = fat

    @classmethod
    def load(cls, name):
        with open('foods.yml', 'r') as file:
            return cls(name, **yaml.load(file, Loader=yaml.FullLoader)[name])
      
    @property
    def name(self):
        return self._name
    
    @property
    def unit(self):
        return self._unit

    @property
    def size(self):
        return self._size
    
    @property
    def carbs(self):
        return self._carbs

    @property
    def protein(self):
        return self._protein

    @property
    def fat(self):
        return self._fat

    
class Ingredient(object):

    def __init__(self, food, servings):
        self._food = food
        self._servings = servings

    INGREDIENT_PATTERN = re.compile(r'^(?P<name>[\w ]+):(?P<amount>\d+(?:\.\d+)?)(?P<unit>[a-zA-Z])$')

    @classmethod 
    def parse(cls, raw):
        match = re.match(cls.INGREDIENT_PATTERN, raw)
        if match is None:
            raise ValueError(f'"{raw}" is not a valid ingredient string')
        food = Food.load(match.group('name').replace('_', ' '))
        amount = float(match.group('amount'))
        unit = match.group('unit')
        servings = get_servings(food, amount, unit)
        return cls(food, servings)

    @property
    def name(self):
        return self._food.name

    @property
    def carbs(self):
        return self._food.carbs * self._servings

    @property
    def protein(self):
        return self._food.protein * self._servings

    @property
    def fat(self):
        return self._food.fat * self._servings

    def __str__(self):
        return f'{self._food.name}:{self._servings * self._food.size:.2f}{self._food.unit}'

    def __mul__(self, x):
        return Ingredient(self._food, self._servings * x)

    def __truediv__(self, x):
        return Ingredient(self._food, self._servings / x)


def get_servings(food, amount, unit):
    if unit == units.SERVING:
        return amount    
    amount_grams = units.as_grams(amount, unit)
    size_grams = units.as_grams(food.size, food.unit)
    return amount_grams / size_grams