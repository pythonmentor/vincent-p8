from django.db import models
from django.utils.text import slugify

# Create your models here.

class Product(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    nutritionGrade = models.CharField(max_length=1)
    image = models.URLField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

class Nutition100(models.Model):
    code = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    fat = models.DecimalField("Fat in 100g", max_digits=5, decimal_places=2)
    satFat = models.DecimalField("Saturated fat in 100g", max_digits=5, decimal_places=2)
    sugar = models.DecimalField("Sugar in 100g", max_digits=5, decimal_places=2)
    salt = models.DecimalField("Salt in 100g", max_digits=5, decimal_places=2)

class Category(models.Model):
    code = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField("Category name", max_length=100, primary_key=True)

class Favourite(models.Model):
    codeHealthy = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="healthy")
    codeUnhealthy = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="unhealthy")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # user = models.ForeignKey()
