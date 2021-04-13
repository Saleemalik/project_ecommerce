# Generated by Django 3.1.7 on 2021-04-04 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0009_categories_advertisement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='Advertisement',
            new_name='advertisement',
        ),
        migrations.AddField(
            model_name='products',
            name='offered_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='categories',
            name='categoryDiscount',
            field=models.FloatField(default=0),
        ),
    ]