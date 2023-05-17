# Generated by Django 4.1.7 on 2023-03-28 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markingApp', '0009_alter_criterialevel_criterialevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterialevel',
            name='criteriaLevel',
            field=models.CharField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4')], default=0, max_length=100),
        ),
    ]
