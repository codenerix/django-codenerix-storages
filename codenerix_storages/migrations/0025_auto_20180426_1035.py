# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-26 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def run_migrate(apps, schema_editor):
    Inventory = apps.get_model("codenerix_storages", "Inventory")
    Storage = apps.get_model("codenerix_storages", "Storage")

    inventories = Inventory.objects.all()
    if inventories:
        storage = Storage.objects.first()
        if storage:
            for inventory in inventories:
                inventory.storage = storage
                inventory.save()
        else:
            raise IOError("Can not execute this migration, you must create at least 1 Storage")


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_storages', '0024_auto_20180426_1034'),
    ]

    operations = [
        migrations.RunPython(run_migrate),
        migrations.AlterField(
            model_name='inventory',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventorys', to='codenerix_storages.Storage', verbose_name='Storage'),
        ),
    ]
