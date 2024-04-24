# Generated by Django 5.0.3 on 2024-04-24 02:21

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0011_trickdefinition_technical_coefficient_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="trickdefinition",
            name="devil_twist_stall_bonus",
            field=models.DecimalField(
                decimal_places=2, default=Decimal("0.00"), max_digits=5
            ),
        ),
        migrations.AddField(
            model_name="trickdefinition",
            name="full_twisted_bonus",
            field=models.DecimalField(
                decimal_places=2, default=Decimal("0.00"), max_digits=5
            ),
        ),
        migrations.AddField(
            model_name="trickdefinition",
            name="hardcore_enty_bonus",
            field=models.DecimalField(
                decimal_places=2, default=Decimal("0.00"), max_digits=5
            ),
        ),
    ]