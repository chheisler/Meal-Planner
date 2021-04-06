from datetime import date
from food import Food, Ingredient
import yaml


BMR_WEIGHT_FACTOR = 4.536
BMR_HEIGHT_FACTOR = 15.875
BMR_AGE_FACTOR = 5.0
BMR_MALE_BIAS = 5.0
BMR_FEMALE_BIAS = -161.0
CARBS_CAL_PER_G = 4.0
PROTEIN_CAL_PER_G = 4.0
FAT_CAL_PER_G = 9.0
DAYS_PER_YEAR = 365.2425


class Person(object):

    def __init__(self, sex, dob, weight, height):
        self._sex = sex
        self._dob = dob
        self._weight = weight
        self._height = height

    @classmethod
    def load(cls, name):
        with open('persons.yml', 'r') as file:
            return cls(**yaml.load(file, Loader=yaml.FullLoader)[name])

    @property
    def sex(self):
        return self._sex

    @property
    def dob(self):
        return self._dob

    @property
    def weight(self):
        return self._weight

    @property
    def height(self):
        return self._height

    @property
    def bmr(self):
        return BMR_WEIGHT_FACTOR * self._weight \
             + BMR_HEIGHT_FACTOR * self._height \
             - BMR_AGE_FACTOR * self.age + self.bias

    @property
    def age(self):
        return (date.today() - self._dob).days / DAYS_PER_YEAR

    @property
    def bias(self): 
        if self._sex == 'male':
            return BMR_MALE_BIAS
        elif self._sex == 'female':
            return BMR_FEMALE_BIAS
        else:
            raise ConfigException('"sex" must be either "male" or "female"')

    def calories(self, diet):
        return self.bmr * diet.factor

    def macros(self, diet):
        calories = self.calories(diet)
        carbs = calories * diet.carbs / CARBS_CAL_PER_G
        protein = calories * diet.protein / PROTEIN_CAL_PER_G
        fat = calories * diet.fat / FAT_CAL_PER_G
        return carbs, protein, fat


class Diet(object):

    def __init__(self, factor, carbs, protein, fat, supplements):
        
        self._factor = factor
        self._supplements = supplements

        total = carbs + protein + fat
        self._carbs = carbs / total
        self._protein = protein / total
        self._fat = fat / total

    @classmethod
    def load(cls, name):
        with open('diets.yml', 'r') as file:
            d = yaml.load(file, Loader=yaml.FullLoader)[name]
            d['supplements'] = [Ingredient(Food.load(n), s) for n, s in d['supplements'].items()]
            return cls(**d)

    @property
    def factor(self):
        return self._factor

    @property
    def carbs(self):
        return self._carbs

    @property
    def protein(self):
        return self._protein

    @property
    def fat(self):
        return self._fat

    @property
    def supplements(self):
        return self._supplements
    
