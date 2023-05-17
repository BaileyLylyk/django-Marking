# Generated by Django 4.1.7 on 2023-04-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markingApp', '0010_alter_criterialevel_criterialevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='criteria',
            name='criteriaTotalMark',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='criterialevel',
            name='criteriaLevel',
            field=models.IntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4')], default=0),
        ),
    ]