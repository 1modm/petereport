# Generated by Django 4.1.7 on 2023-03-20 18:53

from django.db import migrations, models
import django.db.models.deletion
import martor.models
import multi_email_field.fields
import preport.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_list', multi_email_field.fields.MultiEmailField(default=[])),
                ('contact_sp_mail', models.EmailField(blank=True, max_length=255)),
                ('contact_dp_mail', models.EmailField(blank=True, max_length=255)),
                ('description', martor.models.MartorField(blank=True)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='DB_CWE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cwe_id', models.IntegerField(unique=True)),
                ('cwe_name', models.CharField(blank=True, max_length=255)),
                ('cwe_description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'CWEs',
            },
        ),
        migrations.CreateModel(
            name='DB_FTSModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=64)),
                ('fts_fields', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='DB_OWASP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owasp_id', models.IntegerField(unique=True)),
                ('owasp_year', models.IntegerField()),
                ('owasp_name', models.CharField(blank=True, max_length=255)),
                ('owasp_description', models.TextField(blank=True)),
                ('owasp_url', models.CharField(blank=True, max_length=255)),
                ('owasp_full_id', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'verbose_name_plural': 'OWASPs',
            },
        ),
        migrations.CreateModel(
            name='DB_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', martor.models.MartorField(blank=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preport.db_customer')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='DB_Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_website', models.CharField(blank=True, max_length=255)),
                ('company_address', models.CharField(blank=True, max_length=255)),
                ('company_picture', models.ImageField(blank=True, upload_to=preport.models.logo_dst)),
            ],
            options={
                'verbose_name_plural': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='DB_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_id', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('executive_summary_image', models.TextField(blank=True)),
                ('cwe_categories_summary_image', models.TextField(blank=True)),
                ('owasp_categories_summary_image', models.TextField(blank=True)),
                ('executive_summary', martor.models.MartorField(blank=True)),
                ('scope', martor.models.MartorField(blank=True)),
                ('outofscope', martor.models.MartorField(blank=True)),
                ('methodology', martor.models.MartorField(blank=True)),
                ('recommendation', martor.models.MartorField(blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('report_date', models.DateTimeField()),
                ('audit_start', models.DateTimeField(blank=True, null=True)),
                ('audit_end', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preport.db_product')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Reports',
            },
        ),
        migrations.CreateModel(
            name='DB_Finding_Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finding_id', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('severity', models.CharField(blank=True, max_length=200)),
                ('cvss_base_score', models.CharField(blank=True, max_length=200)),
                ('cvss_score', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('description', martor.models.MartorField(blank=True)),
                ('location', martor.models.MartorField(blank=True)),
                ('impact', martor.models.MartorField(blank=True)),
                ('recommendation', martor.models.MartorField(blank=True)),
                ('ref', martor.models.MartorField(blank=True)),
                ('cwe', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='preport.db_cwe')),
                ('owasp', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='preport.db_owasp')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='DB_Finding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finding_id', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(blank=True, default='Opened', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('severity', models.CharField(blank=True, max_length=200)),
                ('cvss_base_score', models.CharField(blank=True, max_length=200)),
                ('cvss_score', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('description', martor.models.MartorField(blank=True)),
                ('location', martor.models.MartorField(blank=True)),
                ('impact', martor.models.MartorField(blank=True)),
                ('recommendation', martor.models.MartorField(blank=True)),
                ('ref', martor.models.MartorField(blank=True)),
                ('poc', martor.models.MartorField(blank=True)),
                ('cwe', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='preport.db_cwe')),
                ('owasp', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='preport.db_owasp')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preport.db_report')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Findings',
            },
        ),
        migrations.CreateModel(
            name='DB_Deliverable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=2048)),
                ('generation_date', models.DateTimeField()),
                ('filetype', models.CharField(max_length=32)),
                ('filetemplate', models.CharField(max_length=64)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preport.db_report')),
            ],
            options={
                'verbose_name_plural': 'Deliverables',
            },
        ),
        migrations.CreateModel(
            name='DB_Custom_field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', martor.models.MartorField(blank=True)),
                ('finding', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_field_finding', to='preport.db_finding')),
            ],
        ),
        migrations.CreateModel(
            name='DB_AttackTree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('attacktree', models.TextField(blank=True)),
                ('svg_file', models.TextField(blank=True)),
                ('finding', models.ManyToManyField(blank=True, related_name='attacktree_finding', to='preport.db_finding')),
            ],
        ),
        migrations.CreateModel(
            name='DB_AttackFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('attackflow_afb', models.TextField(blank=True)),
                ('attackflow_png', models.TextField(blank=True)),
                ('finding', models.ManyToManyField(blank=True, related_name='attackflow_finding', to='preport.db_finding')),
            ],
        ),
        migrations.CreateModel(
            name='DB_Appendix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', martor.models.MartorField()),
                ('finding', models.ManyToManyField(blank=True, related_name='appendix_finding', to='preport.db_finding')),
            ],
        ),
    ]
