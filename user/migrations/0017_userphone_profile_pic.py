# Generated by Django 3.1.7 on 2021-04-01 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_orders_date_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='userphone',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='user'),
        ),
    ]
