# Generated by Django 3.1.7 on 2021-04-27 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_food_type_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='food_type',
            field=models.ManyToManyField(related_name='recipes', to='core.Food_Type'),
        ),
    ]
