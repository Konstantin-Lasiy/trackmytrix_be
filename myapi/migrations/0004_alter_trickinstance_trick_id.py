# Generated by Django 5.0.3 on 2024-04-22 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapi", "0003_alter_run_site_alter_run_wing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trickinstance",
            name="trick_id",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
