# Generated by Django 4.1.7 on 2023-05-02 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markingApp', '0015_alter_criterialevel_criterialevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='mark',
            field=models.IntegerField(blank=True),
        ),
    ]