# Generated by Django 3.0.4 on 2020-04-17 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_category_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]