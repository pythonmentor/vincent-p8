from json import load, dump


# filter categories from https://world.openfoodfacts.org/categories.json
filtered = {}
with open('categories.json', 'r') as json_file:
    # load a json and get category list ('tags')
    categories = load(json_file)['tags']

    for category in categories:
        # if more than X products
        if category.get("products", 0) > 500:
            filtered[category['id']] = category['products']

JSON_file = open('categories_cleaned.json', 'w')
dump(filtered, JSON_file, indent=4)
JSON_file.close()
