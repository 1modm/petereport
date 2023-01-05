# Generated by Django 3.2.16 on 2023-01-05 09:28

from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('preport', '0006_alter_db_finding_closed_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', martor.models.MartorField()),
            ],
        ),
        migrations.AddField(
            model_name='db_product',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='preport.db_customer'),
            preserve_default=False,
        ),
    ]