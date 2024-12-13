# Generated by Django 3.2.25 on 2024-12-04 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0013_auto_20241125_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolinfo',
            name='school',
            field=models.CharField(default='na', max_length=100, verbose_name='学院名称'),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='school_en',
            field=models.CharField(default='na', max_length=150, verbose_name='学院英文名'),
        ),
        migrations.CreateModel(
            name='SchoolSiteMapName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitemap_name', models.CharField(default='na', max_length=150, verbose_name='学院网站sitemap名称(id)')),
                ('school_info', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='roster.schoolinfo')),
            ],
        ),
    ]
