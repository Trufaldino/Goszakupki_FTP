# Generated by Django 4.2.3 on 2023-07-06 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_app', '0003_alter_requestmodel_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmodel',
            name='price',
            field=models.IntegerField(),
        ),
    ]
