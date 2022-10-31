# Generated by Django 3.2.16 on 2022-10-28 16:06

import qfieldcloud.core.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0058_auto_20220914_2049"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "base_manager_name": "objects",
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        ),
        migrations.AlterModelManagers(
            name="team",
            managers=[
                ("objects", qfieldcloud.core.models.UserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", qfieldcloud.core.models.UserManager()),
            ],
        ),
    ]