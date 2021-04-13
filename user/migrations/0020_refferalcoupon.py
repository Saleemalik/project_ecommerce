# Generated by Django 3.1.7 on 2021-04-08 11:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_couponuse'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefferalCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couponName', models.CharField(max_length=100)),
                ('couponCode', models.CharField(max_length=50, unique=True)),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField(default=True)),
                ('userK', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.userphone')),
            ],
        ),
    ]