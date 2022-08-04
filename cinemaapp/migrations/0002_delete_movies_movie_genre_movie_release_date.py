# Generated by Django 4.0.6 on 2022-08-03 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemaapp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Movies',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.DateField(null=True),
        ),
    ]