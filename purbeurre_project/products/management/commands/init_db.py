# Update true parse arg :
    # ne pas supprimer les produits qui sont en favoris

    # supprimer les produits qui ne sont plus dans ooff 

    # compter les produits en favoris

# importer 90 produits par categories
    # avec une limite de 9000 produits en tout

    # les enregistrer dans la base

import requests
from json import load, dump
from django.core.management.base import BaseCommand, CommandError
from products.models import Product, Category

API_URL = 'https://fr-en.openfoodfacts.org/category/'
SEARCH_HEADER = {"user-agent": "Purbeurre - https://github.com/finevine/Projet8"}

class Command(BaseCommand):
    help = 'Create DB and populate it'

    def handle(self, *args, **options):
        # ouvrir json
        with open('products/management/commands/categories_cleaned.json', 'r') as json_file:
            categories = load(json_file)
            for category in categories:
                category_DB, created = Category.objects.update_or_create(
                    id = category,
                    defaults = {
                        "id" : category,
                        "name" : categories[category]
                    }
                )
                
                req = requests.get(
                    API_URL + category + ".json",
                    headers=SEARCH_HEADER)
                # output of request as a json file
                req_output = req.json()
                # get 90 first results
                products = req_output["products"][:90]

                for item in products:
                    product_DB, created = Product.objects.update_or_create(
                        code=item["code"],
                        defaults={
                            "code" : item["code"],
                            "name" : item.get("product_name", item.get("product_name_fr")),
                            "nutritionGrade" : item.get("nutriscore_grade"),
                            "image" : item.get("selected_images", {}).get("front", {}).get("display", {}).get("fr"),
                            "sugar" : item["nutriments"].get("sugars_100g", 0),
                            "satFat" : item["nutriments"].get("saturated-fat_100g", 0),
                            "salt" : item["nutriments"].get("salt_100g", 0),
                            "fat" : item["nutriments"].get("fat_100g", 0),
                            "category" : category_DB
                        },
                    )


        # list of product of the output
        # products_output = req_output['products']

        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))