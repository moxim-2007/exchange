# Generated by Django 4.0.1 on 2022-02-13 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("insure", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productinfo",
            name="duration",
            field=models.IntegerField(),
        ),
    ]
