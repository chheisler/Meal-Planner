from constants import *
from argparse import ArgumentParser
from json import load
from datetime import date
from math import floor
from numpy import array
from numpy.linalg import solve

def main():
	parser = ArgumentParser()
	parser.add_argument('--fixed', nargs='+')
	parser.add_argument('--servings', type=float, nargs='+')
	parser.add_argument('--variable', nargs='+')
	args = parser.parse_args()
	
	# get food and configuration information
	config = load(open('config.json', 'r'))
	foods = load(open('foods.json', 'r'))
	
	# calculate base metabolic rate
	person = config['person']
	if person['sex'] == 'male':
		sex_bias = BMR_MALE_BIAS
	elif person['sex'] == 'female':
		sex_bias = BMR_FEMALE_BIAS
	else:
		raise ConfigException('"sex" must be either "male" or "female"')
	dob = person['dob']
	dob = date(year=dob['year'], month=dob['month'], day=dob['day'])
	age = floor((date.today() - dob).days / DAYS_PER_YEAR)
	calories = BMR_WEIGHT_FACTOR * person['weight'] \
		+ BMR_HEIGHT_FACTOR * person['height'] \
		- BMR_AGE_FACTOR * age + sex_bias
	
	# calculate nutritional requirements
	diet = config['diet']
	calories *= diet['factor']
	if diet['carbs'] + diet['protein'] + diet['fat'] != 1.0:
		raise ConfigException('carbs, protein and fat must sum to 1')
	carbs = calories * diet['carbs'] / CARBS_CAL_PER_G
	protein = calories * diet['protein'] / PROTEIN_CAL_PER_G
	fat = calories * diet['fat'] / FAT_CAL_PER_G
	print int(carbs), int(protein), int(fat)
	
	# subtract flat dietary intakes
	for food, servings in zip(args.fixed, args.servings):
		carbs -= foods[food]['carbs'] * servings
		protein -= foods[food]['protein'] * servings
		fat -= foods[food]['fat'] * servings
	
	# calculate servings for each food
	nutrition = array([
		[foods[food]['carbs'] for food in args.variable],
		[foods[food]['protein'] for food in args.variable],
		[foods[food]['fat'] for food in args.variable]
	])
	needs = array([carbs, protein, fat])
	servings = solve(nutrition, needs)
	print servings
	
if __name__ == '__main__':
	main()