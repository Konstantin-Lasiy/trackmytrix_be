# Generated by Django 5.0.3 on 2024-04-22 14:14

import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TrickDefinition",
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
                ("name", models.CharField(max_length=100)),
                ("has_orientation", models.BooleanField(default=False)),
                (
                    "reverse_bonus",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=5
                    ),
                ),
                (
                    "twisted_bonus",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=5
                    ),
                ),
                (
                    "twisted_exit_bonus",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=5
                    ),
                ),
                (
                    "flipped_bonus",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=5
                    ),
                ),
                (
                    "double_flipped_bonus",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=5
                    ),
                ),
                (
                    "devil_twist_bonus",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=5
                    ),
                ),
                (
                    "cab_slide_bonus",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=5
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Run",
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
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("wing", models.CharField(max_length=100)),
                ("site", models.CharField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="runs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TrickInstance",
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
                ("name", models.CharField(max_length=100)),
                ("orientation", models.CharField(max_length=20)),
                ("reverse", models.BooleanField(default=False)),
                ("twisted", models.BooleanField(default=False)),
                ("twisted_exit", models.BooleanField(default=False)),
                ("flipped", models.BooleanField(default=False)),
                ("double_flipped", models.BooleanField(default=False)),
                ("devil_twist", models.BooleanField(default=False)),
                ("cab_slide", models.BooleanField(default=False)),
                ("successful", models.BooleanField(default=True)),
                (
                    "run",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tricks",
                        to="myapi.run",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tricks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
