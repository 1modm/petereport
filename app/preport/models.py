# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from martor.models import MartorField

import datetime
import re

import pathlib

cvss_regex = re.compile('.+ \((CVSS:.+)\)$')


# ---------- CWE ------------

class DB_CWE(models.Model):
	cwe_id = models.IntegerField(blank=False, unique=True)
	cwe_name = models.CharField(max_length=255, blank=True)
	cwe_description = models.TextField(blank=True)
	class Meta:
		verbose_name_plural = "CWEs"
	def __str__(self):
		return str(self.cwe_id)
	def get_label (self):
		return "%s - %s" % (self.cwe_id, self.cwe_name)
	
# ---------- OWASP ------------

class DB_OWASP(models.Model):
	owasp_id = models.IntegerField(blank=False, unique=True)
	owasp_year = models.IntegerField(blank=False, unique=False)
	owasp_name = models.CharField(max_length=255, blank=True)
	owasp_description = models.TextField(blank=True)
	owasp_url = models.CharField(max_length=255, blank=True)
	owasp_full_id = models.CharField(max_length=20, blank=True)
	class Meta:
		verbose_name_plural = "OWASPs"
	def __str__(self):
		return str(self.owasp_id)
	def save(self, *args, **kwargs):
		prefix = 'A'
		if self.owasp_id < 0:
			self.owasp_full_id = "-1"
		elif self.owasp_id < 10:
			prefix += '0'
		self.owasp_full_id = prefix + str(self.owasp_id) + ':' + str(self.owasp_year)
		super().save(*args, **kwargs)
	def get_label (self):
		return "%s - %s" % (self.owasp_full_id, self.owasp_name)

# ---------- Customer ------------

class DB_Customer(models.Model):
	name = models.CharField(max_length=255, blank=False)
	contact = models.EmailField(max_length=255, blank=True)
	description = MartorField(blank=True)
	class Meta:
		verbose_name_plural = "Customers"
	def __str__(self):
		return self.name
	def get_label (self):
		return self.name

# ---------- Settings ------------

def logo_dst(instance, filename):
    return 'images/company_picture{}'.format(pathlib.Path(filename).suffix)

class DB_Settings(models.Model):
	company_name = models.CharField(max_length=255, blank=False)
	company_website = models.CharField(max_length=255, blank=True)
	company_address = models.CharField(max_length=255, blank=True)
	report_subject = models.CharField(max_length=255, blank=True)
	# File will be uploaded to MEDIA_ROOT/images/<filename>
	company_picture = models.ImageField(upload_to=logo_dst, blank=True)

	def save(self, *args, **kwargs):
		if self.__class__.objects.count():
			self.pk = self.__class__.objects.first().pk
		super().save(*args, **kwargs)
	class Meta:
		verbose_name_plural = "Settings"
	def get_label (self):
		return self.company_name


# ---------- Product ------------

class DB_Product(models.Model):
	customer = models.ForeignKey(DB_Customer, default=1, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, blank=False)
	description = MartorField(blank=True)
	class Meta:
		verbose_name_plural = "Products"
	def __str__(self):
		return self.name
	def get_label (self):
		return self.name

# ---------- Report ------------

class DB_Report(models.Model):
	product = models.ForeignKey(DB_Product, on_delete=models.CASCADE)
	report_id = models.CharField(max_length=255, blank=False, unique=True)
	title = models.CharField(max_length=255, blank=False)
	executive_summary_image = models.TextField(blank=True, null=True)
	cwe_categories_summary_image = models.TextField(blank=True)
	owasp_categories_summary_image = models.TextField(blank=True)
	executive_summary = MartorField()
	scope = MartorField()
	outofscope = MartorField()
	methodology = MartorField()
	recommendation = MartorField()
	creation_date = models.DateTimeField(auto_now_add=True)
	report_date = models.DateTimeField(blank=False)
	audit_start = models.DateField(blank=True, null=True)
	audit_end = models.DateField(blank=True, null=True)
	def __str__(self):
		return self.title
	def get_label (self):
		return self.title
	class Meta:
		verbose_name_plural = "Reports"


# ---------- Finding ------------

class DB_Finding(models.Model):
	report = models.ForeignKey(DB_Report, on_delete=models.CASCADE)
	finding_id = models.CharField(blank=True, max_length=200)
	status = models.CharField(blank=True, max_length=200, default="Open")
	creation_date = models.DateTimeField(auto_now_add=True, null=True)
	closed_at = models.DateTimeField(blank=True, null=True)
	title = models.CharField(blank=True, max_length=200)
	severity = models.CharField(blank=True, max_length=200)
	cvss_vector = models.CharField(blank=True, max_length=200)
	cvss_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
	description = MartorField(blank=True)
	location = MartorField(blank=True)
	impact = MartorField(blank=True)
	recommendation = MartorField(blank=True)
	references = MartorField(blank=True)
	poc = MartorField(blank=True)
	cwe = models.ForeignKey(DB_CWE, on_delete=models.CASCADE, null=True, blank=True)
	owasp = models.ForeignKey(DB_OWASP, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.title
	def get_label (self):
		return self.title

	def save(self, *args, **kwargs):
		if self.status == "Close":
			self.closed_at = datetime.datetime.now()
		super().save(*args, **kwargs)

	def get_cvss_score_anchor(self):
		m = cvss_regex.search(self.cvss_vector)
		if m:
			return m.group(1)
	class Meta:
		verbose_name_plural = "Findings"


# ---------- Finding templates ------------

class DB_Finding_Template(models.Model):
	finding_id = models.CharField(blank=False, max_length=200)
	title = models.CharField(blank=False, max_length=200)
	severity = models.CharField(blank=True, max_length=200)
	cvss_vector = models.CharField(blank=True, max_length=200)
	cvss_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
	description = MartorField(blank=True)
	location = MartorField(blank=True)
	impact = MartorField(blank=True)
	recommendation = MartorField(blank=True)
	references = MartorField(blank=True)
	poc = MartorField(blank=True)
	cwe = models.ForeignKey(DB_CWE, on_delete=models.CASCADE, null=True, blank=True)
	owasp = models.ForeignKey(DB_OWASP, on_delete=models.CASCADE, null=True, blank=True)

	def get_label (self):
		return self.title

	def get_cvss_score_anchor(self):
		m = cvss_regex.search(self.cvss_vector)
		if m:
			return m.group(1)



# ---------- Appendix ------------

class DB_Appendix(models.Model):
	finding = models.ManyToManyField(DB_Finding, related_name='appendix_finding', blank=True)
	title = models.CharField(blank=False, max_length=200)
	description = MartorField()
	def get_label (self):
		return self.title


# ---------- Attack Tree ------------

class DB_AttackTree(models.Model):
	finding = models.ManyToManyField(DB_Finding, related_name='attacktree_finding', blank=True)
	title = models.CharField(blank=False, max_length=200)
	attacktree = models.TextField(blank=True, null=True)
	svg_file = models.TextField(blank=True, null=True)
	def get_label (self):
		return self.title

# ---------- Custom Field ------------

class DB_Custom_field(models.Model):
	finding = models.ForeignKey(DB_Finding, related_name='custom_field_finding', blank=True, on_delete=models.CASCADE)
	title = models.CharField(blank=False, max_length=200)
	description = MartorField(blank=True, null=True)

	def get_label (self):
		return self.title

# ---------- Attack Flow ------------

class DB_AttackFlow(models.Model):
	finding = models.ManyToManyField(DB_Finding, related_name='attackflow_finding', blank=True)
	title = models.CharField(blank=False, max_length=200)
	attackflow_afb = models.TextField(blank=True, null=True)
	attackflow_png = models.TextField(blank=True, null=True)
	def get_label (self):
		return self.title


# ---------- Deliverable ------------
class DB_Deliverable(models.Model):
	report = models.ForeignKey(DB_Report, on_delete=models.CASCADE)
	filename = models.CharField(max_length=2048, blank=False, unique=False)
	generation_date = models.DateTimeField(blank=False)
	filetype = models.CharField(max_length=32, blank=False, unique=False)
	filetemplate = models.CharField(max_length=64, blank=False, unique=False)
	def get_label (self):
		return self.filename
	def __str__(self):
		return self.filename
	class Meta:
		verbose_name_plural = "Deliverables"
