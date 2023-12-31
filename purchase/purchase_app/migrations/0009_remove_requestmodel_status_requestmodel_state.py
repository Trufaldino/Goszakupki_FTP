# Generated by Django 4.2.3 on 2023-07-15 08:56

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_app', '0008_alter_requestmodel_registry_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestmodel',
            name='status',
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (1, 'Manually Filtered'), (2, 'Automatically Filtered'), (3, 'In Progress'), (4, 'Not Participating (Objective)'), (5, 'Not Participating (Subjective)'), (6, 'Bid Submission'), (7, 'Bid Submitted'), (8, 'Auction'), (9, 'Auction Completed (Return Security)'), (10, 'Auction Completed'), (11, 'Contract Signing'), (12, 'Contract Signed'), (13, 'Contract Executed')], default=0),
        ),
    ]
