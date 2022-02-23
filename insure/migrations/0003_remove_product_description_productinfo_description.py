# Generated by Django 4.0.1 on 2022-02-21 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("insure", "0002_alter_productinfo_duration"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="description",
        ),
        migrations.AddField(
            model_name="productinfo",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
