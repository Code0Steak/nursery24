# Generated by Django 3.0.4 on 2020-03-20 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('provider', '0001_initial'),
        ('courier', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('user_type', models.CharField(max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('D', 'Delivered'), ('S', 'Shipped'), ('P', 'Placed')], default='P', max_length=1)),
                ('total_price', models.IntegerField()),
                ('date_last_tracked', models.DateField()),
                ('date_delivered', models.DateField()),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
                ('last_tracked_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courier.Courier')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=250, null=True)),
                ('rating', models.FloatField()),
                ('consumer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='provider.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.Order')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='provider.Product')),
                ('provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='provider.Provider')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.TextField(max_length=100, null=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
            ],
        ),
    ]
