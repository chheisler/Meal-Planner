#!/usr/bin/env python3


from argparse import ArgumentParser
from datetime import date
from food import Food, Ingredient
from numpy import array
from numpy.linalg import solve
from nutrition import Diet, Person


def main():
    args = parse_args()
    macros = args.person.macros(args.diet)
    print_macros(args.person, macros)
    supps = get_supplements(args.diet, args.add_daily, args.add_total, args.days)
    macros = adjust_macros(macros, supps)
    ingrds = solve_ingredients(args.foods, macros, args.days)
    for i in ingrds:
        print(i)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('person', type=Person.load)
    parser.add_argument('diet', type=Diet.load)
    parser.add_argument('foods', nargs='+', type=Food.load)
    parser.add_argument('--add-total', '-t', nargs='+', type=Ingredient.parse, default=[])
    parser.add_argument('--add-daily', '-d', nargs='+', type=Ingredient.parse, default=[])
    parser.add_argument('--days', '-D', type=float, default=1.0)
    return parser.parse_args()


def get_supplements(diet, dailies, totals, days):
    return diet.supplements + dailies + [t / days for t in totals]


def adjust_macros(macros, supps):
    carbs, protein, fat = macros
    for supp in supps:
        carbs -= supp.carbs
        protein -= supp.protein
        fat -= supp.fat
    return carbs, protein, fat


def solve_ingredients(foods, macros, days):
    nutrition = array([
        [f.carbs for f in foods],
        [f.protein for f in foods],
        [f.fat for f in foods]
    ])
    carbs, protein, fat = macros
    servings = solve(nutrition, array([carbs, protein, fat]))
    return [Ingredient(f, s) * days for f, s in zip(foods, servings)]


def print_macros(person, macros):
    carbs, protein, fat = macros
    print(person.weight)
    print(f'carbs: {carbs:.2f}g')
    print(f'protein: {protein:.2f}g ({protein / person.weight:.2f}g/lb)')
    print(f'fat: {fat:.2f}g')


if __name__ == '__main__':
    main()
