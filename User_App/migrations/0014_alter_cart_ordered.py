# Generated by Django 4.2.3 on 2023-10-04 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_App', '0013_alter_cart_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]