# Generated by Django 5.1.7 on 2025-03-31 16:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ReferrerCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "referral_code",
                    models.CharField(blank=True, max_length=10, unique=True),
                ),
                ("used", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="ReferrerProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "email",
                    models.EmailField(
                        default="placeholder@example.com", max_length=254, unique=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DatingUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dating_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "referral_code",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.referrercode",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="referrercode",
            name="referrer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="referral_codes",
                to="core.referrerprofile",
            ),
        ),
    ]
