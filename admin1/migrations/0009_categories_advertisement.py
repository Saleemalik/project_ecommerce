# Generated by Django 3.1.7 on 2021-04-04 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0008_auto_20210404_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='Advertisement',
            field=models.CharField(default='Best Deals For this category', max_length=200),
        ),
    ]
