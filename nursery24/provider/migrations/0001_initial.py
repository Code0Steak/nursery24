# Generated by Django 3.0.4 on 2020-03-20 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('verification_status', models.BooleanField(default=False)),
                ('user_type', models.CharField(max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pics')),
                ('name', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('category', models.CharField(choices=[('P', 'Plants'), ('S', 'Seeds'), ('F', 'Soils and Fertilizers'), ('D', 'Decor'), ('A', 'Accessories')], max_length=1)),
                ('rating', models.FloatField()),
                ('providers', models.ManyToManyField(to='provider.Provider')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.TextField(max_length=100, null=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.Provider')),
            ],
        ),
    ]