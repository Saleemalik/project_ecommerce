# Generated by Django 3.1.7 on 2021-03-14 05:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0006_auto_20210313_0643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='productImg',
            new_name='productImg1',
        ),
        migrations.AddField(
            model_name='products',
            name='productImg2',
            field=models.ImageField(default=0, upload_to='img'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='productImg3',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='img'),
            preserve_default=False,
        ),
    ]
