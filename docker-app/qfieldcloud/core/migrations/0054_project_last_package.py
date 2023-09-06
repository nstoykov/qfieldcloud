# Generated by Django 3.2.12 on 2022-03-09 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0053_auto_20220505_1948"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="last_package_job",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="last_job_of",
                to="core.packagejob",
            ),
        ),
        migrations.AddField(
            model_name="delta",
            name="jobs_to_apply",
            field=models.ManyToManyField(
                through="core.ApplyJobDelta", to="core.ApplyJob"
            ),
        ),
        migrations.RunSQL(
            sql=r'CREATE UNIQUE INDEX "core_user_username_uppercase" ON "core_user" (UPPER("username"));',
            reverse_sql=r'DROP INDEX IF EXISTS "core_user_username_uppercase";',
        ),
    ]
