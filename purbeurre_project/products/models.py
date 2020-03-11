from django.db import models

# Create your models here.

class Product(models.Model):
    nutrition_grade = models.CharField(max_length=1)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30)
    category = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
