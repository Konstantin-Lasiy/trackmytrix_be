# Generated by Django 5.0.3 on 2024-04-23 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0005_remove_trickdefinition_trick_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trickinstance",
            name="name",
        ),
    ]
