# Generated by Django 3.0.4 on 2020-03-21 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0002_product_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]