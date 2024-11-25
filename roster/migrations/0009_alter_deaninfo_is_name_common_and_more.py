# Generated by Django 4.1.7 on 2023-04-19 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("roster", "0008_deaninfo_university_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deaninfo",
            name="is_name_common",
            field=models.CharField(choices=[("1", "是"), ("0", "否")], max_length=20),
        ),
        migrations.AlterField(
            model_name="deaninfo",
            name="whether_oversea_phd",
            field=models.CharField(
                choices=[("1", "是"), ("0", "否")], default="na", max_length=3
            ),
        ),
    ]
