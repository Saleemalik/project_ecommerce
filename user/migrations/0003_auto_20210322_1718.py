# Generated by Django 3.1.7 on 2021-03-22 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shippingName', models.CharField(max_length=50)),
                ('Address', models.CharField(max_length=100)),
                ('landMark', models.CharField(max_length=50)),
                ('pincode', models.PositiveIntegerField()),
                ('phoneNo', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userphone')),
            ],
        ),
    ]
