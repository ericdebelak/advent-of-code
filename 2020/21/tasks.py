def _get_allergens_and_ingredients(filename):
    allergens_dict = {}
    all_ingredients = []
    for line in open(filename):
        ingredients, allergens = line.split(' (contains ')
        ingredients = ingredients.split(' ')
        all_ingredients += ingredients
        allergens = allergens.strip(')\n')
        for allergen in allergens.split(', '):
            if allergen in allergens_dict:
                old_allergens = allergens_dict[allergen]
                allergens_dict[allergen] = [x for x in old_allergens if x in ingredients]
            else:
                allergens_dict[allergen] = ingredients
    return allergens_dict, all_ingredients


def test_task_one():
    assert task_one('test-data.txt') == 5
    assert task_one('real-data.txt') == 1685


def task_one(filename):
    allergens_dict, all_ingredients = _get_allergens_and_ingredients(filename)
    all_allergens = []
    for allergens in allergens_dict.values():
        all_allergens += allergens
    return len([ingredient for ingredient in all_ingredients if ingredient not in all_allergens])


def test_task_two():
    assert task_two('test-data.txt') == 'mxmxvkd,sqjhc,fvjkl'
    assert task_two('real-data.txt') == 'ntft,nhx,kfxr,xmhsbd,rrjb,xzhxj,chbtp,cqvc'


def task_two(filename):
    allergens_dict, all_ingredients = _get_allergens_and_ingredients(filename)
    found_ingredients = []
    while len(found_ingredients) < len(allergens_dict.keys()):
        for allergen, ingredients in allergens_dict.items():
            if len(ingredients) == 1:
                found_ingredients.append(ingredients[0])
            else:
                allergens_dict[allergen] = [x for x in ingredients if x not in found_ingredients]
                if len(allergens_dict[allergen]) == 1:
                    found_ingredients.append(ingredients[0])
    allergens = [allergens_dict[x][0] for x in sorted(allergens_dict)]
    return ','.join(allergens)
