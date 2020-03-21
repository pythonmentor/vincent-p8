from django.db import models
from django.utils.text import slugify

# Create your models here.

class Product(models.Model):
    '''
    code, name, nutritionGrade, image (url), fat, satFat, sugar, salt, compared_to_category
    '''
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100, null= True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null= True)
    nutritionGrade = models.CharField(max_length=1, null= True)
    image = models.URLField(null= True)
    fat = models.DecimalField("Fat in 100g", max_digits=5, decimal_places=2, default=0)
    satFat = models.DecimalField("Saturated fat in 100g", max_digits=5, decimal_places=2, default=0)
    sugar = models.DecimalField("Sugar in 100g", max_digits=5, decimal_places=2, default=0)
    salt = models.DecimalField("Salt in 100g", max_digits=5, decimal_places=2, default=0)
    compared_to_category = models.ForeignKey('ProductCategories', on_delete=models.CASCADE, null= True)

    def __str__(self):
        return self.name + self.code
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

class ProductCategories(models.Model):
    '''
    code, name
    '''
    code = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField('Category name', max_length=100)

class Favourite(models.Model):
    '''
    codeHealthy, codeUnhealthy
    '''
    codeHealthy = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="healthy")
    codeUnhealthy = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="unhealthy")
    # user = models.ForeignKey()
