import requests
from json import load, dump
from django.core.management.base import BaseCommand, CommandError
from products.models import Product, Category

API_URL = 'https://fr-en.openfoodfacts.org/category/'
SEARCH_HEADER = {"user-agent": "Purbeurre - https://github.com/finevine/Projet8"}

class Command(BaseCommand):
    help = 'Create DB and populate it'

    def handle(self, *args, **options):
        # open json of all categories
        with open('products/management/commands/categories_cleaned.json', 'r') as json_file:
            categories = load(json_file)
            for category in categories:
                category_DB, created = Category.objects.update_or_create(
                    id=category,
                    defaults={
                        "id": category,
                        "name": categories[category]
                    }
                )
                
                req = requests.get(
                    API_URL + category + ".json",
                    headers=SEARCH_HEADER)
                # output of request as a json file
                req_output = req.json()
                # get 90 first results
                products = req_output["products"]
                count = 0

                for item in products:
                    # assign attributes to product
                    sugar = item["nutriments"].get("sugars_100g", 0)
                    satFat = item["nutriments"].get("saturated-fat_100g", 0)
                    salt = item["nutriments"].get("salt_100g", 0)
                    fat = item["nutriments"].get("fat_100g", 0)
                    if item.get("nutriscore_grade") and float(sugar) + float(satFat) + float(salt) + float(fat) != 0:
                        product_DB, created = Product.objects.update_or_create(
                            code=item["code"],
                            defaults={
                                "code": item["code"],
                                "name": item.get("product_name", item.get("product_name_fr")),
                                "nutritionGrade": item.get("nutriscore_grade"),
                                "image": item.get("selected_images", {}).get("front", {}).get("display", {}).get("fr"),
                                "sugar": sugar,
                                "satFat": satFat,
                                "salt"  salt,
                                "fat": fat,
                                "category": category_DB
                            },
                        )
                        count += 1
                    if count >= 90:
                        count = 0
                        break
