from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import ModelForm, Textarea, TextInput, DateField, DateInput, ModelChoiceField, CheckboxInput, CheckboxSelectMultiple, PasswordInput, EmailField, BooleanField, FileInput, ModelMultipleChoiceField
from .models import DB_Report, DB_Settings, DB_Finding, DB_Customer, DB_Product, DB_Finding_Template, DB_Appendix, DB_CWE, DB_OWASP, DB_AttackTree, DB_Custom_field
from martor.fields import MartorFormField
from django.utils.translation import gettext_lazy as _
from multi_email_field.forms import MultiEmailField

import datetime

class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name

class NewCustomerForm(forms.ModelForm):

    class Meta:
        model = DB_Customer
        fields = ('name', 'contact_list', 'contact_sp_mail', 'contact_dp_mail', 'description', 'tags')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Customer Name')}),
            'contact_list': Textarea(attrs={'class': 'form-control', 'type':'textarea', 'placeholder': _('Enter multiple email line by line')}),
            'contact_sp_mail': TextInput(attrs={'class': 'form-control', 'type':'email', 'aria-describedby':'emailHelp', 'placeholder': 'Enter Email'}),
            'contact_dp_mail': TextInput(attrs={'class': 'form-control', 'type':'email', 'aria-describedby':'emailHelp', 'placeholder': 'Enter Email'}),
        }


class NewProductForm(forms.ModelForm):
    customer_placeholder = _('(Select a customer)')

    customer = CustomModelChoiceField(queryset=DB_Customer.objects.all(),
                                      empty_label=customer_placeholder,
                                      widget=forms.Select(
        attrs={'class': 'form-control'}
    ))
    class Meta:
        model = DB_Product
        fields = ('name', 'description', 'customer', 'tags')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Product Name')}),
        }


class NewSettingsForm(forms.ModelForm):

    class Meta:
        model = DB_Settings
        fields = ('company_name', 'company_website', 'company_address', 'company_picture')

        widgets = {
            'company_name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Company name')}),
            'company_website': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Company website')}),
            'company_address': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Company address')}),
            'company_picture': FileInput(attrs={'class': 'form-control', 'type': "file", 'placeholder': _('Company picture')}),
        }




class NewReportForm(forms.ModelForm):

    product_placeholder = _('(Select a product)')

    product = CustomModelChoiceField(queryset=DB_Product.objects.all(), empty_label=product_placeholder, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        today = datetime.date.today().strftime('%Y-%m-%d')
        nowformat = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        model = DB_Report
        fields = ('product', 'report_id', 'title', 'report_date', 'audit_start', 'audit_end', 'executive_summary', 'scope', 'outofscope', 'methodology', 'recommendation', 'tags')

        widgets = {
            'report_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Report Name')}),
            'report_date': DateInput(attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'yyyy-mm-dd'", 'data-mask':'', 'required': "required"}),
            'audit_start': DateInput(attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'yyyy-mm-dd'", 'data-mask':''}),
            'audit_end': DateInput(attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'yyyy-mm-dd'", 'data-mask':''}),
        }

class CWEModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.cwe_id, obj.cwe_name)

class OWASPModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.owasp_full_id, obj.owasp_name)

class NewFindingForm(forms.ModelForm):

    severity_choices = (
        ('', _('(Select severity)')),
        ('Critical', _('Critical')),
        ('High', _('High')),
        ('Medium', _('Medium')),
        ('Low', _('Low')),
        ('Info', _('Info')),
        ('None', _('None')),
    )

    status_choices = (
        ('', _('(Select status)')),
        ('Opened', _('Opened')),
        ('Closed', _('Closed')),
    )

    severity = forms.ChoiceField(choices=severity_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Critical/High/Medium/Low/Info/None")}))
    status = forms.ChoiceField(choices=status_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Opened/Closed")}))
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label=_("(Select a CWE ID)"), widget=forms.Select(attrs={'class': 'form-control select2CWE'}))
    owasp = OWASPModelChoiceField(queryset=DB_OWASP.objects.all(), empty_label=_("(Select an OWASP ID)"), widget=forms.Select(attrs={'class': 'form-control select2OWASP'}))

    class Meta:
        model = DB_Finding
        fields = ('title', 'status', 'severity', 'cvss_score', 'cvss_base_score', 'description', 'poc', 'location', 'impact', 'recommendation', 'references', 'cwe', 'tags')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Finding title")}),
            'cvss_base_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("CVSS Base Score")}),
           }



class NewFindingTemplateForm(forms.ModelForm):

    severity_choices = (
        ('', _('(Select severity)')),
        ('Critical', _('Critical')),
        ('High', _('High')),
        ('Medium', _('Medium')),
        ('Low', _('Low')),
        ('Info', _('Info')),
        ('None', _('None')),
    )



    severity = forms.ChoiceField(choices=severity_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Critical/High/Medium/Low/Info/None")}))
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label=_("(Select a CW ID)"), widget=forms.Select(attrs={'class': 'form-control select2CWE'}))
    owasp = OWASPModelChoiceField(queryset=DB_OWASP.objects.all(), empty_label=_("(Select an OWASP ID)"), widget=forms.Select(attrs={'class': 'form-control select2OWASP'}))

    class Meta:
        model = DB_Finding_Template
        fields = ('title', 'severity', 'cvss_score', 'cvss_base_score', 'description', 'location', 'impact', 'recommendation', 'references', 'cwe', 'tags')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Finding title")}),
            'cvss_base_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("CVSS Base Score")}),
        }




class FindingModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"({obj.report.title}) - {obj.title}"


class NewAppendixForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        reportpk = kwargs.pop('reportpk')
        super(NewAppendixForm, self).__init__(*args, **kwargs)

        DB_finding_query = DB_Finding.objects.filter(report=reportpk)

        self.fields["finding"] = FindingModelChoiceField(queryset=DB_finding_query, empty_label=_("(Select a finding)"), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DB_Appendix
        fields = ('finding', 'title', 'description' )

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Title")}),
        }




class AddUserForm(UserCreationForm):

    group = ModelChoiceField(queryset=Group.objects.all(), empty_label=_("(Select a group)"), widget=forms.Select(attrs={'class': 'form-control'}))
    email = EmailField(max_length=254, help_text='Require a valid email address.', widget=forms.TextInput(
                                attrs={'type': 'email', 'class': 'form-control',
                                'placeholder': _('E-mail address')}))
    superadmin = BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'group', 'superadmin', 'email', 'password1', 'password2')

        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Username")}),
            #'password1': PasswordInput(attrs={'class': 'form-control', 'required': "required", 'placeholder': "P@ssW0rd"}),
        }

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Username")})
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
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Title")}),
            'attacktree': Textarea(attrs={'class': 'form-control', 'rows': "20", 'required': "required", 'placeholder': _("Attack Tree")}),
        }


class NewCWEForm(forms.ModelForm):

    class Meta:
        model = DB_CWE
        fields = ('cwe_id', 'cwe_name', 'cwe_description')

        widgets = {
            'cwe_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "CWE ID"}),
            'cwe_name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("CWE Name")}),
            'cwe_description': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("CWE Description")}),
        }
class NewOWASPForm(forms.ModelForm):

    class Meta:
        model = DB_OWASP
        fields = ('owasp_id', 'owasp_year', 'owasp_name', 'owasp_description', 'owasp_url')

        widgets = {
            'owasp_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "OWASP ID"}),
            'owasp_year': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "2021"}),
            'owasp_name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("OWASP Name")}),
            'owasp_description': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("OWASP Description")}),
            'owasp_url': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("OWASP URL")}),
        }

class NewFieldForm(forms.ModelForm):

    class Meta:
        model = DB_Custom_field
        fields = ('title', 'description')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Title")}),
        }
