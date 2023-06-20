from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db.models.base import Model
from django.forms import Textarea, TextInput, DateInput, ModelChoiceField, CheckboxInput, CheckboxSelectMultiple, EmailField, BooleanField, FileInput, ModelMultipleChoiceField, URLInput
from .models import DB_ShareConnection, DB_Report, DB_Settings, DB_Finding, DB_Customer, DB_Product, DB_Finding_Template, DB_Appendix, DB_CWE, DB_OWASP, DB_AttackTree, DB_Custom_field, DB_FTSModel
from django.utils.translation import gettext_lazy as _
import preport.utils.fts as ufts
from preport.utils.sharing import shares_deliverable, shares_finding
from dal import autocomplete

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
            'tags': autocomplete.TaggitSelect2('tag_autocomplete'),
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
            'tags': autocomplete.TaggitSelect2('tag_autocomplete'),
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

class ShareChoiceField(ModelChoiceField):
    def label_from_instance(self, obj: Model) -> str:
        return f"{obj.title}"

class NewReportForm(forms.ModelForm):

    product_placeholder = _('(Select a product)')
    product = CustomModelChoiceField(queryset=DB_Product.objects.all(), empty_label=product_placeholder, widget=forms.Select(attrs={'class': 'form-control'}))

    share_deliverable = ShareChoiceField(queryset=DB_ShareConnection.objects.all().filter(type="deliverable"), empty_label=_("None"), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    share_finding = ShareChoiceField(queryset=DB_ShareConnection.objects.all().filter(type="finding"), empty_label=_("None"), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    class Meta:
        today = datetime.date.today().strftime('%Y-%m-%d')
        nowformat = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        model = DB_Report
        fields = ('product', 'report_id', 'title', 'report_date', 'audit_start', 'audit_end', 'share_deliverable', 'share_finding', 'executive_summary', 'audit_objectives', 'scope', 'outofscope', 'methodology', 'recommendation', 'tags')
        widgets = {
            'report_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _('Report Name')}),
            'report_date': DateInput(attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'YYYY-MM-DD'", 'data-mask':'', 'required': "required"}),
            'audit_start': DateInput(attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'YYYY-MM-DD'", 'data-mask':''}),
            'audit_end': DateInput(attrs={'class': 'form-control', 'type': "text", 'data-inputmask': "'alias': 'YYYY-MM-DDd'", 'data-mask':''}),
            'tags': autocomplete.TaggitSelect2('tag_autocomplete'),
        }

class NewShareForm(forms.ModelForm):
    type_choice = (
        ('deliverable', _('Deliverable')),
        ('findings', _('Findings'))
    )
    type=forms.ChoiceField(choices=type_choice, required=True, widget=forms.Select(attrs={'class': 'form-control', 'id':'selecttype', 'onchange':'TypeChange(this.value);', 'type': "text", 'required': "required", 'placeholder': _("Deliverable/Findings")}))
    func_choice = ((x,_(x)) for l in [['none'],shares_finding,shares_deliverable] for x in l)
    func=forms.ChoiceField(choices=func_choice, required=True, widget=forms.Select(attrs={'class': 'form-control', 'id':'selectfunc', 'type': "text", 'required': "required"}))
    class Meta:
        today = datetime.date.today().strftime('%Y-%m-%d')
        nowformat = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        model = DB_ShareConnection
        fields = ('title', 'type', 'func', 'url', 'credentials', 'tags')
        widgets = {
            'url': URLInput(),
            'tags': autocomplete.TaggitSelect2('tag_autocomplete')
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
        fields = ('title', 'status', 'severity', 'cvss_score', 'cvss_base_score', 'description', 'poc', 'location', 'impact', 'recommendation', 'ref', 'cwe', 'owasp', 'tags')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Finding title")}),
            'cvss_base_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("CVSS Base Score")}),
            'tags': autocomplete.TaggitSelect2('tag_autocomplete'),
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
    cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label=_("(Select a CWE ID)"), widget=forms.Select(attrs={'class': 'form-control select2CWE'}))
    owasp = OWASPModelChoiceField(queryset=DB_OWASP.objects.all(), empty_label=_("(Select an OWASP ID)"), widget=forms.Select(attrs={'class': 'form-control select2OWASP'}))

    class Meta:
        model = DB_Finding_Template
        fields = ('title', 'severity', 'cvss_score', 'cvss_base_score', 'description', 'location', 'impact', 'recommendation', 'ref', 'cwe', 'owasp', 'tags')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("Finding title")}),
            'cvss_base_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("CVSS Base Score")}),
            'tags': autocomplete.TaggitSelect2('tag_autocomplete')
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

class NewFTSForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewFTSForm, self).__init__(*args, **kwargs)
        self.fields['models'] = ModelMultipleChoiceField(
                                    widget = CheckboxSelectMultiple(),
                                    queryset=DB_FTSModel.objects.all().order_by("model_name"))
        self.fields['models'].initial = DB_FTSModel.objects.all()
        self.fields['q'] = forms.CharField(
                widget = forms.TextInput(
                    attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': _("FTS Query")}),)
    class Meta:
        fields = ('models', 'q')

class CustomDeliverableReportForm(forms.Form):
    pass