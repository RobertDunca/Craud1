# Generated by Django 4.0.6 on 2022-07-28 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_restaurant_thingstodo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ThingsToDo',
            new_name='ThingToDo',
        ),
    ]
