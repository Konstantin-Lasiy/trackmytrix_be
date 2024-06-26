# Generated by Django 5.0.3 on 2024-04-23 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0008_trickdefinition_restrictions"),
    ]

    operations = [
        migrations.CreateModel(
            name="Restriction",
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
                ("code", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name="trickdefinition",
            name="restrictions",
        ),
        migrations.AddField(
            model_name="trickdefinition",
            name="restrictions",
            field=models.ManyToManyField(
                blank=True, default=None, to="myapi.restriction"
            ),
        ),
    ]
