# Generated by Django 4.1.7 on 2023-04-04 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("roster", "0004_deaninfo"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deaninfo", old_name="name", new_name="name_first",
        ),
        migrations.AddField(
            model_name="deaninfo",
            name="name_last",
            field=models.CharField(default="na", max_length=20),
            preserve_default=False,
        ),
    ]
