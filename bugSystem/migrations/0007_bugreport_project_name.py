# Generated by Django 3.1.7 on 2021-03-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugSystem', '0006_auto_20210319_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='bugreport',
            name='project_name',
            field=models.CharField(default='Default Name', help_text='Enter the name of project', max_length=200),
        ),
    ]
