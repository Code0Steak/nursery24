# Generated by Django 3.0.4 on 2020-04-20 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0001_initial'),
        ('consumer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='date_delivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='date_last_tracked',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_tracked_by',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='productinorder',
            name='consumer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer'),
        ),
        migrations.AddField(
            model_name='productinorder',
            name='date_delivered',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='productinorder',
            name='date_last_tracked',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='productinorder',
            name='expected_delivery_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='productinorder',
            name='last_tracked_by',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='courier.Courier'),
        ),
        migrations.AddField(
            model_name='productinorder',
            name='status',
            field=models.CharField(choices=[('D', 'Delivered'), ('S', 'Shipped'), ('P', 'Placed'), ('C', 'Cancelled')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='productinorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='consumer.Order'),
        ),
        migrations.AlterField(
            model_name='productinorder',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='productinorder',
            name='total_price',
            field=models.IntegerField(null=True),
        ),
    ]