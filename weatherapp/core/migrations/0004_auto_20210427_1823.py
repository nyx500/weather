# Generated by Django 3.1.7 on 2021-04-27 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210427_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='food_type',
        ),
        migrations.AddField(
            model_name='recipe',
            name='food_type',
            field=models.CharField(blank=True, choices=[('african', 'African'), ('american', 'American'), ('british', 'British'), ('chinese', 'Chinese'), ('eastern_european', 'Eastern European'), ('french', 'French'), ('greek', 'Greek'), ('italian', 'Italian'), ('indian', 'Indian'), ('japanese', 'Japanese'), ('mexican', 'Mexican'), ('middle_eastern', 'Middle Eastern'), ('nordic', 'Nordic'), ('persian', 'Persian'), ('south_american', 'South American'), ('thai', 'Thai'), ('vietnamese', 'Vietnamese')], max_length=64, null=True),
        ),
        migrations.DeleteModel(
            name='Food_Type',
        ),
    ]
