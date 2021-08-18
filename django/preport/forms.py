from django import forms
from django.forms import ModelForm, Textarea, TextInput, DateField, DateInput, ModelChoiceField, CheckboxInput, CheckboxSelectMultiple
from .models import DB_Report, DB_Finding, DB_Product, DB_Finding_Template, DB_Appendix, DB_CWE
from martor.fields import MartorFormField

import datetime

class NewProductForm(forms.ModelForm):

    class Meta:
        model = DB_Product
        fields = ('name', 'description')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Product Name"}),
        }

class ProductModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class NewReportForm(forms.ModelForm):

    product = ProductModelChoiceField(queryset=DB_Product.objects.all(), empty_label="(Select a product)", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:

        today = datetime.date.today().strftime('%Y-%m-%d')
        nowformat = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        model = DB_Report
        fields = ('product', 'report_id', 'title', 'executive_summary', 'scope', 'outofscope', 'methodology', 'recommendation', 'report_date' )

        widgets = {
            'report_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'report_date': DateInput(attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'yyyy-mm-dd'", 'data-mask':'', 'required': "required"}),
        }

class CWEModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.cwe_id, obj.cwe_name)


class NewFindingForm(forms.ModelForm):

    severity_choices = (
        ('', '(Select severity)'),
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Info', 'Info'),
        ('None', 'None'),
    )

    status_choices = (
        ('', '(Select status)'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )

    severity = forms.ChoiceField(choices=severity_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Critical/High/Medium/Low/Info/None"}))
    status = forms.ChoiceField(choices=status_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Open/Close"}))
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label="(Select a CWE)", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DB_Finding
        fields = ('title', 'status', 'severity', 'cvss_score', 'cvss_base_score', 'description', 'location', 'impact', 'recommendation', 'references', 'cwe')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Finding title"}),
            'cvss_base_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "CVSS Base Score"}),
           }
        


class NewFindingTemplateForm(forms.ModelForm):

    severity_choices = (
        ('', 'Severity'),
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Info', 'Info'),
        ('None', 'None'),
    )


    severity = forms.ChoiceField(choices=severity_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Critical/High/Medium/Low/Info/None"}))
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label="(Select a CWE)", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DB_Finding_Template
        fields = ('title', 'severity', 'cvss_score', 'cvss_base_score', 'description', 'location', 'impact', 'recommendation', 'references', 'cwe')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Finding title"}),
            'cvss_base_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "CVSS Base Score"}),
        }
        



class FindingModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"({obj.report.title}) - {obj.title}"


class NewAppendixForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        reportpk = kwargs.pop('reportpk')
        super(NewAppendixForm, self).__init__(*args, **kwargs)

        DB_finding_query = DB_Finding.objects.filter(report=reportpk)

        self.fields["finding"] = FindingModelChoiceField(queryset=DB_finding_query, empty_label="(Select a finding)", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DB_Appendix
        fields = ('finding', 'title', 'description' )

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Title"}),
        }

