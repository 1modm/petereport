from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import ModelForm, Textarea, TextInput, DateField, DateInput, ModelChoiceField, CheckboxInput, CheckboxSelectMultiple, PasswordInput, EmailField, BooleanField
from .models import DB_Report, DB_Finding, DB_Product, DB_Finding_Template, DB_Appendix, DB_CWE, DB_AttackTree, DB_Custom_field
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
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Report Name"}),
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
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label="(Select a CWE)", widget=forms.Select(attrs={'class': 'form-control select2CWE'}))

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
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label="(Select a CWE)", widget=forms.Select(attrs={'class': 'form-control select2CWE'}))

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




class AddUserForm(UserCreationForm):

    group = ModelChoiceField(queryset=Group.objects.all(), empty_label="(Select a group)", widget=forms.Select(attrs={'class': 'form-control'}))
    email = EmailField(max_length=254, help_text='Require a valid email address.', widget=forms.TextInput(
                                attrs={'type': 'email', 'class': 'form-control',
                                'placeholder': 'E-mail address'}))
    superadmin = BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'group', 'superadmin', 'email', 'password1', 'password2')

        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Username"}),
            #'password1': PasswordInput(attrs={'class': 'form-control', 'required': "required", 'placeholder': "P@ssW0rd"}),
        }

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Username"})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Secret P@ssW0rd'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Secret P@ssW0rd'})



class NewAttackTreeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        reportpk = kwargs.pop('reportpk')
        super(NewAttackTreeForm, self).__init__(*args, **kwargs)

        DB_finding_query = DB_Finding.objects.filter(report=reportpk)

        self.fields["finding"] = FindingModelChoiceField(queryset=DB_finding_query, empty_label="(Select a finding)", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DB_AttackTree
        fields = ('finding', 'title', 'attacktree', 'svg_file')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Title"}),
            'attacktree': Textarea(attrs={'class': 'form-control', 'rows': "20", 'required': "required", 'placeholder': "Attack Tree"}),
        }


class NewCWEForm(forms.ModelForm):

    class Meta:
        model = DB_CWE
        fields = ('cwe_id', 'cwe_name', 'cwe_description')

        widgets = {
            'cwe_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "CWE ID"}),
            'cwe_name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "CWE Name"}),
            'cwe_description': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "CWE Description"}),
        }


class NewFieldForm(forms.ModelForm):

    class Meta:
        model = DB_Custom_field
        fields = ('title', 'description')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "Title"}),
        }