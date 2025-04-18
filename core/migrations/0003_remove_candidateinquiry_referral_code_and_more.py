# Generated by Django 5.1.7 on 2025-04-03 23:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_customuser_managers_remove_customuser_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="candidateinquiry",
            name="referral_code",
        ),
        migrations.AddField(
            model_name="candidateinquiry",
            name="referrer_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.referrercode",
            ),
        ),
    ]
