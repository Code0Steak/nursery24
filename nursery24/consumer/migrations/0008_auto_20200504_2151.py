# Generated by Django 3.0.5 on 2020-05-04 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0007_auto_20200504_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinorder',
            name='status',
            field=models.CharField(choices=[('D', 'Delivered'), ('S', 'Shipped'), ('P', 'Placed'), ('C', 'Cancelled'), ('R', 'Ready To Ship'), ('N', 'Not Returned')], default='P', max_length=1),
        ),
    ]
