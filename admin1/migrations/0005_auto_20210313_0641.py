# Generated by Django 3.1.7 on 2021-03-13 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0004_auto_20210313_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='categoryPic',
            field=models.ImageField(upload_to=''),
        ),
    ]
