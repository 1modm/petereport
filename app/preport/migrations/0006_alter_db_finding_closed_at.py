# Generated by Django 3.2.16 on 2023-01-04 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preport', '0005_auto_20230104_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_finding',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]