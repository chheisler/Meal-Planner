import app
from datetime import date
from food import Food, Ingredient
from mock import patch
from nutrition import Diet, Person
from pytest import approx


class TestFood(object):

    def test_load_food(self):
        f = Food.load('brown rice')
        assert f.name == 'brown rice'
        assert f.unit == 'g'
        assert f.size == 100
        assert f.carbs == 76
        assert f.protein == 8
        assert f.fat == 2.7

    def test_parse_ingredient(self):
        f = Ingredient.parse('brown_rice:200g')
        assert f.carbs == 152
        assert f.protein == 16
        assert f.fat == 5.4


class TestNutrition(object):

    def test_load_person(self):
        p = Person.load('Test')
        assert p.sex == 'male'
        assert p.dob == date(year=1988, month=12, day=24)
        assert p.weight == 230
        assert p.height == 69

    @patch('nutrition.Person.age', 30)
    def test_get_bmr(self):
        p = Person.load('Test')
        assert p.bmr == approx(1993, 1)

    def test_load_diet(self):
        d = Diet.load('test')


class TestApp(object):
    pass
    #def test_parse_args(self):
    #    args = app.parse_args(['Charles', 'cut', 'chicken breast', 'brown rice', 'olive oil'])
    def gen_args(self):
        return app.parse_args(['Charles', 'cut', 'chicken  breast', 'brown rice', 'olive oil',
                               '--add-total', 'zuchinni:500g', '--add-daily', 'carrot:100g',
                               '--days', 5])