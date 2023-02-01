from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import Textarea, TextInput, DateInput, ModelChoiceField, EmailField, BooleanField
from .models import DB_Report, DB_Finding, DB_Product, DB_Finding_Template, DB_Appendix, DB_CWE, DB_AttackTree, DB_Custom_field, DB_Engagement
from django.utils.translation import gettext_lazy as _

import datetime

class NewProductForm(forms.ModelForm):

    class Meta:
        model = DB_Product
        fields = ('name', 'description')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Product Name')}),
        }

class ProductModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class NewReportForm(forms.ModelForm):

    product_placeholder = _('(Select a product)')

    product = ProductModelChoiceField(queryset=DB_Product.objects.all(), empty_label=product_placeholder, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        today = datetime.date.today().strftime('%Y-%m-%d')
        nowformat = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        model = DB_Report
        fields = ('product', 'report_id', 'title', 'executive_summary', 'scope', 'outofscope', 'methodology', 'recommendation', 'report_date' )

        widgets = {
            'report_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Report Name')}),
            'report_date': DateInput(attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'yyyy-mm-dd'", 'data-mask':'', 'required': "required"}),
        }

class CWEModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.cwe_id, obj.cwe_name)


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
        ('Open', _('Open')),
        ('Closed', _('Closed')),
    )

    severity = forms.ChoiceField(choices=severity_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Critical/High/Medium/Low/Info/None")}))
    status = forms.ChoiceField(choices=status_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Open/Close")}))
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label=_("(Select a CWE)"), widget=forms.Select(attrs={'class': 'form-control select2CWE'}))

    class Meta:
        model = DB_Finding
        fields = ('title', 'status', 'severity', 'cvss_score', 'cvss_base_score', 'description', 'location', 'impact', 'recommendation', 'references', 'cwe')

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
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label=_("(Select a CWE)"), widget=forms.Select(attrs={'class': 'form-control select2CWE'}))

    class Meta:
        model = DB_Finding_Template
        fields = ('title', 'severity', 'cvss_score', 'cvss_base_score', 'description', 'location', 'impact', 'recommendation', 'references', 'cwe')

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


class NewFieldForm(forms.ModelForm):

    class Meta:
        model = DB_Custom_field
        fields = ('title', 'description')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Title")}),
        }

class NewEngagementForm(forms.ModelForm):
    class Meta:
        model = DB_Engagement
        fields = ('name', 'description', 'start_date', 'end_date')

        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Name")}),
            'description': TextInput(
                attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Engagement Description")}),
            'start_date': DateInput(
                attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'yyyy-mm-dd'",'data-mask': '', 'required': "required"}),
            'end_date': DateInput(
                attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'yyyy-mm-dd'",'data-mask': '', 'required': "required"}),
        }