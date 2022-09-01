# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from martor.models import MartorField


# ---------- CWE ------------

class DB_CWE(models.Model):
	cwe_id = models.IntegerField(blank=False, unique=True)
	cwe_name = models.CharField(max_length=255, blank=True)
	cwe_description = models.TextField(blank=True)
	
# ---------- Product ------------

class DB_Product(models.Model):
	name = models.CharField(max_length=255, blank=False)
	description = MartorField()

# ---------- Report ------------

class DB_Report(models.Model):
	product = models.ForeignKey(DB_Product, on_delete=models.CASCADE)
	report_id = models.CharField(max_length=255, blank=False, unique=True)
	title = models.CharField(max_length=255, blank=False)
	executive_summary_image = models.TextField(blank=True, null=True)
	categories_summary_image = models.TextField(blank=True, null=True)
	executive_summary = MartorField()
	scope = MartorField()
	outofscope = MartorField()
	methodology = MartorField()
	recommendation = MartorField()
	creation_date = models.DateTimeField(auto_now_add=True)
	report_date = models.DateTimeField(blank=False)


# ---------- Finding ------------

class DB_Finding(models.Model):
	report = models.ForeignKey(DB_Report, on_delete=models.CASCADE)
	finding_id = models.CharField(blank=True, max_length=200)
	status = models.CharField(blank=True, max_length=200, default="Open")
	title = models.CharField(blank=True, max_length=200)
	severity = models.CharField(blank=True, max_length=200)
	cvss_base_score = models.CharField(blank=True, max_length=200)
	cvss_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
	description = MartorField()
	location = MartorField()
	impact = MartorField()
	recommendation = MartorField()
	references = MartorField()
	cwe = models.ForeignKey(DB_CWE, on_delete=models.CASCADE)

# ---------- Finding templates ------------

class DB_Finding_Template(models.Model):
	finding_id = models.CharField(blank=False, max_length=200)
	title = models.CharField(blank=False, max_length=200)
	severity = models.CharField(blank=True, max_length=200)
	cvss_base_score = models.CharField(blank=True, max_length=200)
	cvss_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
	description = MartorField()
	location = MartorField()
	impact = MartorField()
	recommendation = MartorField()
	references = MartorField()
	cwe = models.ForeignKey(DB_CWE, on_delete=models.CASCADE)

# ---------- Appendix ------------

class DB_Appendix(models.Model):
	finding = models.ManyToManyField(DB_Finding, related_name='appendix_finding', blank=True)
	title = models.CharField(blank=False, max_length=200)
	description = MartorField()


# ---------- Attack Tree ------------

class DB_AttackTree(models.Model):
	finding = models.ManyToManyField(DB_Finding, related_name='attacktree_finding', blank=True)
	title = models.CharField(blank=False, max_length=200)
	attacktree = models.TextField(blank=True, null=True)
	svg_file = models.TextField(blank=True, null=True)
