# Generated by Django 4.2.3 on 2023-07-11 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_app', '0005_remove_requestmodel_auction_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmodel',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
    ]
