# Generated by Django 5.0.3 on 2024-04-23 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0004_alter_trickinstance_trick_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trickdefinition",
            name="trick_id",
        ),
        migrations.RemoveField(
            model_name="trickinstance",
            name="trick_id",
        ),
        migrations.AddField(
            model_name="trickinstance",
            name="trick_definition",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapi.trickdefinition",
            ),
            preserve_default=False,
        ),
    ]
