# Generated by Django 2.2.17 on 2021-03-21 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_auto_20210316_2056"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delta",
            name="status",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "STATUS_PENDING"),
                    (2, "STATUS_BUSY"),
                    (3, "STATUS_APPLIED"),
                    (4, "STATUS_CONFLICT"),
                    (5, "STATUS_NOT_APPLIED"),
                    (6, "STATUS_ERROR"),
                    (7, "STATUS_IGNORED"),
                    (8, "STATUS_UNPERMITTED"),
                ],
                default=1,
            ),
        ),
    ]