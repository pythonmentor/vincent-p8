from json import load, dump


# filter categories from https://world.openfoodfacts.org/categories.json
filtered = {}
with open('categories.json', 'r') as json_file:
    # load a json and get category list ('tags')
    categories = load(json_file)['tags']
    limit_max, count = 500, 0

    for category in categories:
        # if more than X products and count < 100
        if 500 < category.get("products", 0) < 10000 and count < limit_max:
            count += 1
            filtered[category['id']] = category['name']

JSON_file = open('categories_cleaned.json', 'w')
dump(filtered, JSON_file, indent=4)
JSON_file.close()
