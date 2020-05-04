# Generated by Django 3.0.5 on 2020-05-03 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0006_remove_courier_delivery'),
        ('deliveryPersonnel', '0002_auto_20200503_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverypersonnel',
            name='user',
        ),
        migrations.AddField(
            model_name='deliverypersonnel',
            name='courier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courier.Courier'),
        ),
    ]
