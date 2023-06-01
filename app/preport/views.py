# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, Http404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext_lazy as _
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

# Forms
from .forms import NewProductForm, NewReportForm, NewFindingForm, NewAppendixForm, NewFindingTemplateForm, AddUserForm, NewCWEForm, NewFieldForm

# Model
from .models import DB_Report, DB_Finding, DB_Product, DB_Finding_Template, DB_Appendix, DB_CWE, DB_Custom_field, DB_AttackFlow

# Decorators
from .decorators import allowed_users

# Libraries
import datetime
import textwrap
import requests
import base64
import bleach
import uuid
import json
import csv
import io
import os
from collections import Counter
import pypandoc

# Martor
from petereport.settings import MAX_IMAGE_UPLOAD_SIZE, MARTOR_UPLOAD_PATH, MEDIA_URL, MEDIA_ROOT, TEMPLATES_ROOT, REPORTS_MEDIA_ROOT, SERVER_CONF

# PeTeReport config
from config.petereport_config import PETEREPORT_MARKDOWN, PETEREPORT_TEMPLATES, DEFECTDOJO_CONFIG

# Not all Django output can be passed unmodified to json. In particular, lazy
# translation objects need a special encoder written for them.
# https://docs.djangoproject.com/en/1.8/topics/serialization/#serialization-formats-json
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)

# ----------------------------------------------------------------------
# https://github.com/agusmakmun/django-markdown-editor/wiki
# ----------------------------------------------------------------------

@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            # DJANGO 1.11: if image._size > settings.MAX_IMAGE_UPLOAD_SIZE:
            # DJANGO 2.0
            if image.size > MAX_IMAGE_UPLOAD_SIZE:
                to_MB = MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)


            if PETEREPORT_MARKDOWN['martor_upload_method'] == 'BASE64':

                image_content_base64 = base64.b64encode(image.read()).decode('utf-8')
             
                image_content_base64_final = 'data:' + image.content_type +';base64,' + image_content_base64

                data = json.dumps({
                    'status': 200,
                    'link': image_content_base64_final,
                    'name': image.name
                    })

            elif PETEREPORT_MARKDOWN['martor_upload_method'] == 'MEDIA':
                img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
                tmp_file = os.path.join(MARTOR_UPLOAD_PATH, img_uuid)
                def_path = default_storage.save(tmp_file, ContentFile(image.read()))
                # Modified to include server host and port
                MEDIA_URL_COMPLETE = PETEREPORT_MARKDOWN['media_host'] + MEDIA_URL
                img_url_complete = os.path.join(MEDIA_URL_COMPLETE, def_path)

                data = json.dumps({
                    'status': 200,
                    'link': img_url_complete,
                    'name': image.name
                })

            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))


# ----------------------------------------------------------------------
#                           index 
# ----------------------------------------------------------------------



@login_required
def index(request):

    DB_product_query = DB_Product.objects.order_by('name')

    report_number = {}
    product_findings = {}
    total_reports = 0
    total_products = DB_product_query.count()
    count_product_findings_total = 0
    count_product_findings_critical_high = 0
    count_product_findings_medium = 0

    for p in DB_product_query:
        DB_Report_query = DB_Report.objects.filter(product=p.id)
        count_product_report = DB_Report_query.count()
        report_number[p.id] = count_product_report
        total_reports += count_product_report

        for report in DB_Report_query:
            DB_finding_query = DB_Finding.objects.filter(report=report.id).order_by('cvss_score')
            count_product_findings = DB_finding_query.count()
            product_findings[report.id] = count_product_findings
            count_product_findings_total += count_product_findings
            for finding in DB_finding_query:
                if finding.severity == 'High' or finding.severity == 'Critical':
                    count_product_findings_critical_high += 1
                elif finding.severity == 'Medium':
                    count_product_findings_medium += 1

    DB_finding_query = DB_Finding.objects.order_by('cvss_score').reverse()

    cwe_rows = []

    for finding in DB_finding_query:
        finding_cwe = f"CWE-{finding.cwe.cwe_id} - {finding.cwe.cwe_name}"
        cwe_rows.append(finding_cwe)

    cwe_cat = Counter(cwe_rows)
    cwe_categories = []

    for key_cwe, value_cwe in cwe_cat.items():
        fixed_key_cwe = '\n'.join(key_cwe[i:i+60] for i in range(0, len(key_cwe), 60))
        dict_cwe = {
            "value": value_cwe,
            "name": fixed_key_cwe
        }

        cwe_categories.append(dict_cwe)



    # TOP 10 findings
    DB_finding_query = DB_finding_query[:10] 

    return render(request, 'home/index.html', {'total_reports': total_reports, 'total_products': total_products, 'count_product_findings_total': count_product_findings_total, 'count_product_findings_critical_high': count_product_findings_critical_high, 'count_product_findings_medium': count_product_findings_medium, 'DB_finding_query':DB_finding_query, 'cwe_categories': cwe_categories})


# ----------------------------------------------------------------------
#                           Configuration 
# ----------------------------------------------------------------------

@login_required
@allowed_users(allowed_roles=['administrator'])
def user_list(request):
    userList = User.objects.values()
    group_list = Group.objects.all()

    return render(request, 'configuration/user_list.html', {'userList': userList, 'group_list': group_list})



@login_required
@allowed_users(allowed_roles=['administrator'])
def user_add(request):
    
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            user_group = form.cleaned_data.get('group')
            superadmin = form.cleaned_data.get('superadmin')
            user.is_staff = superadmin
            user.is_superuser = superadmin
            user.save()

            user.groups.add(user_group)

            return redirect('user_list')
    else:
        form = AddUserForm()

    return render(request, 'configuration/user_add.html', {'form': form})


@login_required
@allowed_users(allowed_roles=['administrator'])
def user_edit(request,pk):

    DB_user_query = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = AddUserForm(request.POST, instance=DB_user_query)
        if form.is_valid():
            user = form.save(commit=False)
            
            user_group = form.cleaned_data.get('group')
            superadmin = form.cleaned_data.get('superadmin')
            user.is_staff = superadmin
            user.is_superuser = superadmin
            user.save()

            user.groups.add(user_group)

            return redirect('user_list')
    else:
        form = AddUserForm(instance=DB_user_query)

    return render(request, 'configuration/user_add.html', {'form': form})



@login_required
@allowed_users(allowed_roles=['administrator'])
def user_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        User.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')


# ----------------------------------------------------------------------
#                           Products 
# ----------------------------------------------------------------------

@login_required
def product_list(request):

    DB_product_query = DB_Product.objects.order_by('pk').all()
    report_number = {}

    for product_in_db in DB_product_query:
        count_product_report = DB_Report.objects.filter(product=product_in_db.id).count()
        report_number[product_in_db.id] = count_product_report

    return render(request, 'products/product_list.html', {'DB_product_query': DB_product_query, 'report_number': report_number})



@login_required
@allowed_users(allowed_roles=['administrator'])
def product_add(request):

    if request.method == 'POST':
        form = NewProductForm(request.POST)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.save()
            return redirect('product_list')
    else:
        form = NewProductForm()
        form.fields['description'].initial = PETEREPORT_TEMPLATES['initial_text']

    return render(request, 'products/product_add.html', {
        'form': form
    })


@login_required
@allowed_users(allowed_roles=['administrator'])
def product_edit(request,pk):

    DB_product_query = get_object_or_404(DB_Product, pk=pk)

    if request.method == 'POST':
        form = NewProductForm(request.POST, instance=DB_product_query)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.save()
            return redirect('product_list')
    else:
        form = NewProductForm(instance=DB_product_query)

    return render(request, 'products/product_add.html', {
        'form': form
    })



@login_required
@allowed_users(allowed_roles=['administrator'])
def product_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        DB_Product.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')




@login_required
def product_view(request,pk):

    DB_product_query = get_object_or_404(DB_Product, pk=pk)
    DB_report_query = DB_Report.objects.filter(product=DB_product_query).order_by('creation_date').reverse()
    count_product_report = DB_report_query.count()
    product_findings = {}
    count_product_findings_total = 0
    count_product_findings_critical_high = 0
    count_product_findings_medium = 0

    for report in DB_report_query:
        DB_finding_query = DB_Finding.objects.filter(report=report.id)
        count_product_findings = DB_finding_query.count()
        product_findings[report.id] = count_product_findings
        count_product_findings_total += count_product_findings
        for finding in DB_finding_query:
            if finding.severity == 'High' or finding.severity == 'Critical':
                count_product_findings_critical_high += 1
            elif finding.severity == 'Medium':
                count_product_findings_medium += 1

    return render(request, 'products/product_view.html', {'pk': pk, 'DB_product_query': DB_product_query, 'DB_report_query': DB_report_query, 'count_product_report': count_product_report, 'product_findings': count_product_findings_total, 'count_product_findings_critical_high': count_product_findings_critical_high, 'count_product_findings_medium': count_product_findings_medium})




# ----------------------------------------------------------------------
#                           Reports 
# ----------------------------------------------------------------------

@login_required
def report_list(request):

    DB_report_query = DB_Report.objects.order_by('pk').all()

    return render(request, 'reports/report_list.html', {'DB_report_query': DB_report_query})



@login_required
@allowed_users(allowed_roles=['administrator'])
def report_add(request):

    today = datetime.date.today().strftime('%Y-%m-%d')
    report_id_format = PETEREPORT_TEMPLATES['report_id_format'] + str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M'))

    if request.method == 'POST':
        form = NewReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            return redirect('report_view', pk=report.pk)
    else:
        form = NewReportForm()
        form.fields['report_id'].initial = report_id_format
        form.fields['executive_summary'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['scope'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['outofscope'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['methodology'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['recommendation'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['report_date'].initial = today
    return render(request, 'reports/report_add.html', {
        'form': form
    })



@login_required
@allowed_users(allowed_roles=['administrator'])
def report_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        DB_Report.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')




@login_required
@allowed_users(allowed_roles=['administrator'])
def report_edit(request,pk):

    report = get_object_or_404(DB_Report, pk=pk)

    if request.method == 'POST':
        form = NewReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_view', pk=report.pk)
    else:
        form = NewReportForm(instance=report)
    return render(request, 'reports/report_add.html', {
        'form': form
    })



@login_required
def report_view(request,pk):
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()
    count_finding_query = DB_finding_query.count()

    DB_appendix_query = DB_Appendix.objects.filter(finding__in=DB_finding_query)
    count_appendix_query = DB_appendix_query.count()

    DB_attackflow_query = DB_AttackFlow.objects.filter(finding__in=DB_finding_query)
    count_attackflow_query = DB_attackflow_query.count()

    count_findings_critical = 0
    count_findings_high = 0
    count_findings_medium = 0
    count_findings_low = 0
    count_findings_info = 0
    count_findings_none = 0

    cwe_rows = []
    
    for finding in DB_finding_query:
        # Only reporting Critical/High/Medium/Low/Info findings
        if finding.severity == 'None':
            count_findings_none += 1
        else:

            finding_cwe = f"CWE-{finding.cwe.cwe_id} - {finding.cwe.cwe_name}"
            cwe_rows.append(finding_cwe)

            if finding.severity == 'Critical':
                count_findings_critical += 1
            elif finding.severity == 'High':
                count_findings_high += 1
            elif finding.severity == 'Medium':
                count_findings_medium += 1
            elif finding.severity == 'Low':
                count_findings_low += 1
            elif finding.severity == 'Info':
                count_findings_info += 1


    cwe_cat = Counter(cwe_rows)

    cwe_categories = []

    for key_cwe, value_cwe in cwe_cat.items():
        fixed_key_cwe = '\n'.join(key_cwe[i:i+60] for i in range(0, len(key_cwe), 60))
        dict_cwe = {
            "value": value_cwe,
            "name": fixed_key_cwe
        }
        cwe_categories.append(dict_cwe)


    return render(request, 'reports/report_view.html', {'DB_appendix_query': DB_appendix_query, 'DB_report_query': DB_report_query, 'DB_finding_query': DB_finding_query, 'count_appendix_query': count_appendix_query, 'count_finding_query': count_finding_query, 'count_findings_critical': count_findings_critical, 'count_findings_high': count_findings_high, 'count_findings_medium': count_findings_medium, 'count_findings_low': count_findings_low, 'count_findings_info': count_findings_info, 'count_findings_none': count_findings_none, 'cwe_categories': cwe_categories, 'DB_attackflow_query': DB_attackflow_query, 'count_attackflow_query': count_attackflow_query})





@login_required
def uploadsummaryfindings(request,pk):
    
    DB_report_query = get_object_or_404(DB_Report, pk=pk)

    if request.method == 'POST':

        # Severitybar
        summary_finding_file_base64 = request.POST['fileSeveritybar']
        format, summary_finding_file_str = summary_finding_file_base64.split(';base64,')
        ext = format.split('/')[-1]
        dataimgSeveritybar = ContentFile(base64.b64decode(summary_finding_file_str))

        # Categories
        summary_categories_file_base64 = request.POST['file_cwe']
        format, summary_categories_finding_file_str = summary_categories_file_base64.split(';base64,')
        ext = format.split('/')[-1]
        dataCWE = ContentFile(base64.b64decode(summary_categories_finding_file_str))

        if PETEREPORT_MARKDOWN['martor_upload_method'] == 'BASE64':
            DB_report_query.executive_summary_image = summary_finding_file_base64
            DB_report_query.categories_summary_image = summary_categories_file_base64
            DB_report_query.save()


        elif PETEREPORT_MARKDOWN['martor_upload_method'] == 'MEDIA':

            # Severity chart
            file_name_severity = DB_report_query.report_id + "_severity_summary_finding." + ext
            img_url_severity = os.path.join(MARTOR_UPLOAD_PATH, file_name_severity)
            media_url_severity = os.path.join(MEDIA_ROOT, img_url_severity)

            if os.path.exists(media_url_severity):
                os.remove(media_url_severity)

            fs = FileSystemStorage()
            filename_severity = fs.save(img_url_severity, dataimgSeveritybar) 
            uploaded_file_url_severity = fs.url(filename_severity) 

            DB_report_query.report_executive_summary = uploaded_file_url_severity


            # CWE
            file_name_categories = DB_report_query.report_id + "_categories_summary_finding." + ext
            img_url_categories = os.path.join(MARTOR_UPLOAD_PATH, file_name_categories)
            media_url_categories = os.path.join(MEDIA_ROOT, img_url_categories)

            if os.path.exists(media_url_categories):
                os.remove(media_url_categories)

            fs = FileSystemStorage()
            filename_categories = fs.save(img_url_categories, dataCWE) 
            uploaded_file_url_categories = fs.url(filename_categories) 

            DB_report_query.report_categories_summary = uploaded_file_url_categories

            DB_report_query.save()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')




@login_required
def reportdownloadmarkdown(request,pk):

    # DB
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()

    # Datetime
    report_date = DB_report_query.report_date.strftime('%d-%m-%Y')

    # MD filename
    name_file = PETEREPORT_TEMPLATES['report_markdown_name'] + '_' + DB_report_query.title + '_' +  str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M')) + '.md'

    # INIT
    template_findings = template_appendix = md_finding_summary = md_finding = "\n"
    counter_finding = 0
    md_author = PETEREPORT_MARKDOWN['author']
    md_subject = PETEREPORT_MARKDOWN['subject']
    md_website = PETEREPORT_MARKDOWN['website']

    
    # IMAGES
    if PETEREPORT_MARKDOWN['martor_upload_method'] == 'BASE64':
        report_executive_summary_image = DB_report_query.executive_summary_image
        report_executive_categories_image = DB_report_query.categories_summary_image
    elif PETEREPORT_MARKDOWN['martor_upload_method'] == 'MEDIA':
        report_executive_summary_image = f"{SERVER_CONF}{DB_report_query.executive_summary_image}"
        report_executive_categories_image = f"{SERVER_CONF}{DB_report_query.categories_summary_image}"

    # Appendix
    template_appendix = _('# Additional Notes') + "\n\n"

    # FINDINGS
    for finding in DB_finding_query:

        # Custom fields
        template_custom_fields = ""

        # Only reporting Critical/High/Medium/Low/Info findings
        if finding.severity == 'None':
            pass
        else:
            counter_finding += 1
            template_appendix_in_finding = template_attackflow_in_finding = None

            # Summary table
            md_finding_summary += render_to_string('tpl/markdown/md_finding_summary.md', {'finding': finding, 'counter_finding': counter_finding})

            # Custom fields
            if finding.custom_field_finding.all():

                for field_in_finding in finding.custom_field_finding.all():
                    md_custom_fields = f"**{bleach.clean(field_in_finding.title)}**\n\n{bleach.clean(field_in_finding.description)}\n\n"

                    template_custom_fields += ''.join(md_custom_fields)


            # appendix
            if finding.appendix_finding.all():

                template_appendix_in_finding = _('**Additional notes**') + "\n"

                for appendix_in_finding in finding.appendix_finding.all():
                    md_appendix = render_to_string('tpl/markdown/md_appendix.md', {'appendix_in_finding': appendix_in_finding})

                    template_appendix += ''.join(md_appendix)
                    template_appendix_in_finding += ''.join(bleach.clean(appendix_in_finding.title) + "\n")


            # attack flows
            if finding.attackflow_finding.all():

                template_attackflow_in_finding = _('**Attack Flow**') + "\n"

                for attackflow_in_finding in finding.attackflow_finding.all():
                    md_attackflow = render_to_string('tpl/markdown/md_attackflow.md', {'attackflow_in_finding': attackflow_in_finding})

                    template_attackflow_in_finding += ''.join(md_attackflow + "\n")

            # finding
            md_finding = render_to_string('tpl/markdown/md_finding.md', {'finding': finding, 'template_appendix_in_finding': template_appendix_in_finding, 'template_attackflow_in_finding': template_attackflow_in_finding, 'template_custom_fields': template_custom_fields})

            template_findings += ''.join(md_finding)

    render_md = render_to_string('tpl/markdown/md_report.md', {'DB_report_query': DB_report_query, 'template_findings': template_findings, 'template_appendix': template_appendix, 'finding_summary': md_finding_summary, 'md_author': md_author, 'report_date': report_date, 'md_subject': md_subject, 'md_website': md_website, 'report_executive_summary_image': report_executive_summary_image, 'report_executive_categories_image': report_executive_categories_image})

    final_markdown = textwrap.dedent(render_md)
    final_markdown_output = mark_safe(final_markdown)

    # Create the HttpResponse object with the appropriate header.
    response = HttpResponse(final_markdown_output, content_type='text/markdown')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(name_file)

    return response




@login_required
def reportdownloadhtml(request,pk):

    # DB
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()

    # Datetime
    report_date = DB_report_query.report_date.strftime('%d-%m-%Y')

    # HTML filename
    name_file = PETEREPORT_TEMPLATES['report_html_name'] + '_' + DB_report_query.title + '_' +  str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M')) + '.html'

    # COLORS
    CRITICAL = 'CC0000'
    HIGH = 'FF0000'
    WARNING = 'FC7F03'
    LOW = '05B04F'
    INFO = '002060'

    # INIT
    template_findings = template_appendix = md_finding_summary = ''
    md_author = PETEREPORT_MARKDOWN['author']
    md_subject = PETEREPORT_MARKDOWN['subject']
    md_website = PETEREPORT_MARKDOWN['website']

    counter_finding = counter_finding_critical = counter_finding_high = counter_finding_medium = counter_finding_low = counter_finding_info = 0

    # Summary table
    finding_summary_table = render_to_string('tpl/html/html_finding_summary_table.html')

    # Appendix
    template_appendix = _('# Additional Notes') + "\n\n"

    # FINDINGS
    for finding in DB_finding_query:
        
        # Custom fields
        template_custom_fields = ""

        # Only reporting Critical/High/Medium/Low/Info findings
        if finding.severity == 'None':
            pass
        else:
            counter_finding += 1
            template_appendix_in_finding = template_attackflow_in_finding = None

            if finding.severity == 'Critical':
                color_text_severity = CRITICAL
                counter_finding_critical += 1 
            elif finding.severity == 'High':
                color_text_severity = HIGH
                counter_finding_high += 1 
            elif finding.severity == 'Medium':
                color_text_severity = WARNING
                counter_finding_medium += 1 
            elif finding.severity == 'Low':
                color_text_severity = LOW
                counter_finding_low += 1 
            else:
                color_text_severity = INFO
                counter_finding_info += 1 

            # Summary table
            finding_summary_table += render_to_string('tpl/html/html_finding_summary.html', {'finding': finding, 'counter_finding': counter_finding, 'color_text_severity': color_text_severity})
            
            # Custom fields
            if finding.custom_field_finding.all():

                for field_in_finding in finding.custom_field_finding.all():
                    html_custom_fields = f"<tr><td style=\"width: 15%\">**{bleach.clean(field_in_finding.title)}**</td><td>{bleach.clean(field_in_finding.description)}</td></tr>\n\n"

                    template_custom_fields += ''.join(html_custom_fields)


            # Appendix
            if finding.appendix_finding.all():

                template_appendix_in_finding = "<td style=\"width: 15%\">" + _('**Additional notes**') + "</td><td>\n"

                for appendix_in_finding in finding.appendix_finding.all():
                    html_appendix = render_to_string('tpl/html/md_appendix.md', {'appendix_in_finding': appendix_in_finding})

                    template_appendix += ''.join(html_appendix)
                    template_appendix_in_finding += ''.join(bleach.clean(appendix_in_finding.title) + "<br>")

                template_appendix_in_finding += ''.join("</td>\n")

            
            # attack flow
            if finding.attackflow_finding.all():

                template_attackflow_in_finding = "<td style=\"width: 15%\">" + _('**Attack Flow**') + "</td><td>\n"

                for attackflow_in_finding in finding.attackflow_finding.all():
                    html_attackflow = render_to_string('tpl/html/md_attackflow.md', {'attackflow_in_finding': attackflow_in_finding})

                    template_attackflow_in_finding += ''.join(html_attackflow + "<br>")
                    
                template_attackflow_in_finding += ''.join("</td>\n")


            # finding
            html_finding = render_to_string('tpl/html/html_finding.md', {'finding': finding, 'color_text_severity': color_text_severity, 'template_appendix_in_finding': template_appendix_in_finding, 'template_attackflow_in_finding': template_attackflow_in_finding, 'template_custom_fields': template_custom_fields})

            template_findings += ''.join(html_finding)

    # Summary table end
    finding_summary_table += render_to_string('tpl/html/html_finding_end_table.html')

    render_md = render_to_string('tpl/html/html_report.md', {'DB_report_query': DB_report_query, 'template_findings': mark_safe(template_findings), 'template_appendix': mark_safe(template_appendix), 'finding_summary': md_finding_summary, 'md_author': md_author, 'report_date': report_date, 'md_subject': md_subject, 'md_website': md_website, 'counter_finding_critical': counter_finding_critical, 'counter_finding_high': counter_finding_high, 'counter_finding_medium': counter_finding_medium, 'counter_finding_low': counter_finding_low, 'counter_finding_info': counter_finding_info, 'finding_summary_table': finding_summary_table})

    final_markdown = textwrap.dedent(render_md)
    final_markdown_output = mark_safe(final_markdown)

    html_template = os.path.join(TEMPLATES_ROOT, PETEREPORT_TEMPLATES['html_template'])    
    pathfile = f"html/{name_file}"

    html_file_output = os.path.join(REPORTS_MEDIA_ROOT, pathfile)

    output_pypandoc = pypandoc.convert_text(final_markdown_output, to='html', outputfile=html_file_output, format='md', extra_args=['--from', 'markdown+yaml_metadata_block+raw_html', '--template', html_template, '--toc', '--table-of-contents', '--toc-depth', '2', '--number-sections', '--top-level-division=chapter', '--self-contained'])

    if os.path.exists(html_file_output):
            with open(html_file_output, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/html; charset=utf-8")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(html_file_output)
                return response
    raise Http404




@login_required
def reportdownloadpdf(request,pk):

    # DB
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()

    # Datetime
    report_date = DB_report_query.report_date.strftime('%d-%m-%Y')

    # PDF filename
    name_file = PETEREPORT_TEMPLATES['report_pdf_name'] + '_' + DB_report_query.title + '_' +  str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M')) + '.pdf'

    # COLORS

    # INIT
    template_findings = template_appendix = pdf_finding_summary = ''
    md_author = PETEREPORT_MARKDOWN['author']
    md_subject = PETEREPORT_MARKDOWN['subject']
    md_website = PETEREPORT_MARKDOWN['website']
    counter_finding = counter_finding_critical = counter_finding_high = counter_finding_medium = counter_finding_low = counter_finding_info = 0
    title_background_image = f"preport/templates/tpl/pdf/{PETEREPORT_TEMPLATES['report_pdf_title_background']}"
    pages_background_image = f"preport/templates/tpl/pdf/{PETEREPORT_TEMPLATES['report_pdf_pages_background']}"

    # Appendix
    template_appendix = _('# Additional Notes') + "\n\n"

    # IMAGES
    if PETEREPORT_MARKDOWN['martor_upload_method'] == 'BASE64':
        report_executive_summary_image = DB_report_query.executive_summary_image
        report_executive_categories_image = DB_report_query.categories_summary_image
    elif PETEREPORT_MARKDOWN['martor_upload_method'] == 'MEDIA':
        report_executive_summary_image = f"{SERVER_CONF}{DB_report_query.executive_summary_image}"
        report_executive_categories_image = f"{SERVER_CONF}{DB_report_query.categories_summary_image}"

    for finding in DB_finding_query:
        # Custom fields
        template_custom_fields = ""

        # Only reporting Critical/High/Medium/Low/Info findings
        if finding.severity == 'None':
            pass
        else:
            counter_finding += 1
            template_appendix_in_finding = template_attackflow_in_finding = ''

            if finding.severity == 'Critical':
                counter_finding_critical += 1
                icon_finding = 'important'
                severity_color = 'criticalcolor'
                severity_box = 'criticalbox'
            elif finding.severity == 'High':
                counter_finding_high += 1
                icon_finding = 'highnote'
                severity_color = 'highcolor'
                severity_box = 'highbox'
            elif finding.severity == 'Medium':
                counter_finding_medium += 1
                icon_finding = 'mediumnote'
                severity_color = 'mediumcolor'
                severity_box = 'mediumbox'
            elif finding.severity == 'Low':
                counter_finding_low += 1
                icon_finding = 'lownote'
                severity_color = 'lowcolor'
                severity_box = 'lowbox'
            else:
                counter_finding_info += 1
                icon_finding = 'debugnote'
                severity_color = 'debugcolor'
                severity_box = 'infobox'

            # Summary table
            pdf_finding_summary += render_to_string('tpl/pdf/pdf_finding_summary.md', {'finding': finding, 'counter_finding': counter_finding, 'severity_box': severity_box})
            
            severity_color_finding = "\\textcolor{" + f"{severity_color}" +"}{" + f"{finding.severity}" + "}"

            # Custom fields
            if finding.custom_field_finding.all():

                for field_in_finding in finding.custom_field_finding.all():
                    md_custom_fields = f"**{bleach.clean(field_in_finding.title)}**\n\n{bleach.clean(field_in_finding.description)}\n\n"

                    template_custom_fields += ''.join(md_custom_fields)

            # appendix
            if finding.appendix_finding.all():

                template_appendix_in_finding = _('**Additional notes**') + "\n\n"

                for appendix_in_finding in finding.appendix_finding.all():

                    pdf_appendix = render_to_string('tpl/pdf/pdf_appendix.md', {'appendix_in_finding': appendix_in_finding})

                    template_appendix += ''.join(pdf_appendix)
                    template_appendix_in_finding += ''.join(bleach.clean(appendix_in_finding.title) + "\n")

                template_appendix_in_finding += ''.join("\\pagebreak")

            else:
                template_appendix_in_finding += ''.join("\\pagebreak")

            # attack flow
            if finding.attackflow_finding.all():

                template_attackflow_in_finding = _('**Attack Flow**') + "\n\n"

                for attackflow_in_finding in finding.attackflow_finding.all():

                    pdf_attackflow = render_to_string('tpl/pdf/pdf_attackflow.md', {'attackflow_in_finding': attackflow_in_finding})
            
                    template_attackflow_in_finding += ''.join(pdf_attackflow + "\n")

                template_attackflow_in_finding += ''.join("\\pagebreak")

            else:
                template_attackflow_in_finding += ''.join("\\pagebreak")



            # finding
            pdf_finding = render_to_string('tpl/pdf/pdf_finding.md', {'finding': finding, 'icon_finding': icon_finding, 'severity_color': severity_color, 'severity_color_finding': severity_color_finding, 'template_appendix_in_finding': template_appendix_in_finding, 'template_attackflow_in_finding': template_attackflow_in_finding, 'template_custom_fields': template_custom_fields})

            template_findings += ''.join(pdf_finding)


    pdf_markdown_report = render_to_string('tpl/pdf/pdf_header.yaml', {'DB_report_query': DB_report_query, 'md_author': md_author, 'report_date': report_date, 'md_subject': md_subject, 'md_website': md_website, 'report_pdf_language': PETEREPORT_TEMPLATES['report_pdf_language'], 'titlepagecolor': PETEREPORT_TEMPLATES['titlepage-color'], 'titlepagetextcolor': PETEREPORT_TEMPLATES['titlepage-text-color'], 'titlerulecolor': PETEREPORT_TEMPLATES['titlepage-rule-color'], 'titlepageruleheight': PETEREPORT_TEMPLATES['titlepage-rule-height'], 'title_background': title_background_image, 'pages_background': pages_background_image })

    pdf_markdown_report += render_to_string('tpl/pdf/pdf_report.md', {'DB_report_query': DB_report_query, 'report_executive_summary_image': report_executive_summary_image, 'report_executive_categories_image': report_executive_categories_image, 'pdf_finding_summary': pdf_finding_summary, 'template_findings': template_findings, 'template_appendix': template_appendix})

    final_markdown = textwrap.dedent(pdf_markdown_report)
    final_markdown_output = mark_safe(final_markdown)

    pathfile = f"pdf/{name_file}"
    pdf_file_output = os.path.join(REPORTS_MEDIA_ROOT, pathfile)

    header_file = "pdf/pdf_header.tex"
    PDF_HEADER_FILE = os.path.join(TEMPLATES_ROOT, header_file)

    PETEREPORT_LATEX_FILE = os.path.join(TEMPLATES_ROOT, PETEREPORT_TEMPLATES['pdf_latex_template'])

    output_pypandoc = pypandoc.convert_text(final_markdown_output, to='pdf', outputfile=pdf_file_output, format='md', extra_args=['-H', PDF_HEADER_FILE, '--from', 'markdown+yaml_metadata_block+raw_html', '--template', PETEREPORT_LATEX_FILE, '--table-of-contents', '--toc-depth', '4', '--number-sections', '--highlight-style', 'breezedark', '--filter', 'pandoc-latex-environment', '--listings'])
    #output_pypandoc = pypandoc.convert_text(final_markdown_output, to='pdf', outputfile=pdf_file_output, format='md', extra_args=['-H', PDF_HEADER_FILE, '--from', 'markdown+yaml_metadata_block+raw_html', '--template', PETEREPORT_LATEX_FILE, '--table-of-contents', '--toc-depth', '4', '--number-sections', '--highlight-style', 'breezedark', '--filter', 'pandoc-latex-environment', '--listings', '--pdf-engine', 'xelatex'])

    if os.path.exists(pdf_file_output):
            with open(pdf_file_output, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(pdf_file_output)
                return response

    raise Http404





@login_required
def reportdownloadjupyter(request,pk):

    # DB
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()

    # Datetime
    report_date = DB_report_query.report_date.strftime('%d-%m-%Y')

    # MD filename
    name_file = PETEREPORT_TEMPLATES['report_jupyter_name'] + '_' + DB_report_query.title + '_' +  str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M')) + '.ipynb'

    # INIT
    template_findings = template_appendix = ipynb_finding_summary = ipynb_finding = ""
    counter_finding = counter_finding_critical = counter_finding_high = counter_finding_medium = counter_finding_low = counter_finding_info = 0
    md_author = PETEREPORT_MARKDOWN['author']
    md_subject = PETEREPORT_MARKDOWN['subject']
    md_website = PETEREPORT_MARKDOWN['website']

    # Appendix
    template_appendix = render_to_string('tpl/jupyter/additional_notes.ipynb')

    # Attackflow init
    template_attackflow = render_to_string('tpl/jupyter/attackflows.ipynb')
    
    # IMAGES
    if PETEREPORT_MARKDOWN['martor_upload_method'] == 'BASE64':
        report_executive_summary_image = DB_report_query.executive_summary_image
        report_executive_categories_image = DB_report_query.categories_summary_image
    elif PETEREPORT_MARKDOWN['martor_upload_method'] == 'MEDIA':
        report_executive_summary_image = f"{SERVER_CONF}{DB_report_query.executive_summary_image}"
        report_executive_categories_image = f"{SERVER_CONF}{DB_report_query.categories_summary_image}"


    # FINDINGS
    for finding in DB_finding_query:
        # Only reporting Critical/High/Medium/Low/Info findings
        if finding.severity == 'None':
            pass
        else:
            counter_finding += 1

            if finding.severity == 'Critical':
                counter_finding_critical += 1 
            elif finding.severity == 'High':
                counter_finding_high += 1 
            elif finding.severity == 'Medium':
                counter_finding_medium += 1 
            elif finding.severity == 'Low':
                counter_finding_low += 1 
            else:
                counter_finding_info += 1 

            # Summary table
            ipynb_finding_summary += render_to_string('tpl/jupyter/finding_summary.ipynb', {'finding': finding, 'counter_finding': counter_finding})
            
            # finding
            ipynb_finding = render_to_string('tpl/jupyter/finding.ipynb', {'finding': finding})

            # appendix
            if finding.appendix_finding.all():

                for appendix_in_finding in finding.appendix_finding.all():
                    ipynb_finding += render_to_string('tpl/jupyter/appendix_in_finding.ipynb', {'appendix_in_finding': appendix_in_finding})

                    ipynb_appendix = render_to_string('tpl/jupyter/appendix.ipynb', {'appendix_in_finding': appendix_in_finding})

                    template_appendix += ''.join(ipynb_appendix)

            else:
                ipynb_finding += render_to_string('tpl/jupyter/NA.ipynb')


            # attack flow
            if finding.attackflow_finding.all():

                for attackflow_in_finding in finding.attackflow_finding.all():

                    ipynb_finding += render_to_string('tpl/jupyter/attackflow_in_finding.ipynb', {'attackflow_in_finding': attackflow_in_finding})

                    ipynb_attackflow = render_to_string('tpl/jupyter/attackflow.ipynb', {'attackflow_in_finding': attackflow_in_finding})

                    template_attackflow += ''.join(ipynb_attackflow)
                    
            
            template_findings += ''.join(ipynb_finding)

    render_jupyter = render_to_string('tpl/jupyter/report.ipynb', {'DB_report_query': DB_report_query, 'template_findings': template_findings, 'template_appendix': template_appendix, 'template_attackflow': template_attackflow, 'finding_summary': ipynb_finding_summary, 'md_author': md_author, 'report_date': report_date, 'md_subject': md_subject, 'md_website': md_website, 'counter_finding_critical': counter_finding_critical, 'counter_finding_high': counter_finding_high, 'counter_finding_medium': counter_finding_medium, 'counter_finding_low': counter_finding_low, 'counter_finding_info': counter_finding_info, 'report_executive_summary_image': report_executive_summary_image, 'report_executive_categories_image': report_executive_categories_image})

    final_markdown = textwrap.dedent(render_jupyter)
    final_markdown_output = mark_safe(final_markdown)

    # Create the HttpResponse object with the appropriate header.
    response = HttpResponse(final_markdown_output, content_type='application/x-ipynb+json')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(name_file)

    return response



# ----------------------------------------------------------------------
#                           Findings 
# ----------------------------------------------------------------------


@login_required
def reportfindings(request,pk):
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()
    count_finding_query = DB_finding_query.count()

    return render(request, 'findings/reportfindings.html', {'DB_report_query': DB_report_query, 'DB_finding_query': DB_finding_query, 'count_finding_query': count_finding_query})


@login_required
def openfindings(request):
    DB_finding_query = DB_Finding.objects.filter(status='Open').order_by('cvss_score').reverse()
    count_finding_query = DB_finding_query.count()

    return render(request, 'findings/findings_list.html', {'DB_finding_query': DB_finding_query, 'count_finding_query': count_finding_query})


@login_required
def closedfindings(request):
    DB_finding_query = DB_Finding.objects.filter(status='Closed').order_by('cvss_score').reverse()
    count_finding_query = DB_finding_query.count()

    return render(request, 'findings/findings_list.html', {'DB_finding_query': DB_finding_query, 'count_finding_query': count_finding_query})

@login_required
@allowed_users(allowed_roles=['administrator'])
def finding_add(request,pk):

    DB_report_query = get_object_or_404(DB_Report, pk=pk)

    if request.method == 'POST':
        form = NewFindingForm(request.POST)
        
        if form.is_valid():
            finding = form.save(commit=False)            
            finding.report = DB_report_query
            finding.finding_id = uuid.uuid4()
            finding.save()

            if '_finish' in request.POST:
                return redirect('reportfindings', pk=pk)
            elif '_next' in request.POST:
                return redirect('finding_add', pk=pk)

    else:
        form = NewFindingForm()
        form.fields['description'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['location'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['impact'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['recommendation'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['references'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['cwe'].initial = '1'

    return render(request, 'findings/finding_add.html', {
        'form': form, 'DB_report': DB_report_query})



@login_required
@allowed_users(allowed_roles=['administrator'])
def finding_edit(request,pk):

    finding = get_object_or_404(DB_Finding, pk=pk)
    report = finding.report
    DB_report_query = get_object_or_404(DB_Report, pk=report.pk)

    if request.method == 'POST':
        form = NewFindingForm(request.POST, instance=finding)
        if form.is_valid():
            finding = form.save(commit=False)
            finding.save()

            if '_finish' in request.POST:
                return redirect('reportfindings', pk=report.pk)
            elif '_next' in request.POST:
                return redirect('finding_add', pk=report.pk)

    else:
        form = NewFindingForm(instance=finding)
    return render(request, 'findings/finding_add.html', {
        'form': form, 'DB_report': DB_report_query
    })




@login_required
@allowed_users(allowed_roles=['administrator'])
def finding_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        DB_Finding.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')



@login_required
def finding_view(request,pk):
    finding = get_object_or_404(DB_Finding, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(pk=pk).order_by('cvss_score').reverse()
    DB_appendix = DB_Appendix.objects.filter(finding__in=DB_finding_query)
    DB_attackflow = DB_AttackFlow.objects.filter(finding__in=DB_finding_query)
    DB_field = DB_Custom_field.objects.filter(finding__in=DB_finding_query)

    return render(request, 'findings/finding_view.html', {'DB_report': finding.report, 'finding': finding, 'DB_appendix': DB_appendix, 'DB_attackflow': DB_attackflow, 'DB_field': DB_field})



@login_required
def downloadfindingscsv(request,pk):
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query)

    name_file = PETEREPORT_TEMPLATES['report_csv_name'] + '_' + DB_report_query.title + '_' +  str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M')) + '.csv'

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+name_file+'"'

    csv.register_dialect('MMDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    writer = csv.writer(response, dialect='MMDialect')
    writer.writerow(["ID", "Status", "Title", "Severity", "CVSS Base Score", "CVSS Score", "CWE", "CWE ID", "Description", "Location", "Impact", "Recommendation", "References", "Appendix", "Appendix Description"])

    for finding in DB_finding_query:
        cwe_title = f"{finding.cwe.cwe_id} - {finding.cwe.cwe_name}"
        cwe_id = finding.cwe.cwe_id

        if finding.appendix_finding.exists():
            for appendix in finding.appendix_finding.all():
                appendix_title = appendix.title
                appendix_description = appendix.description
        else:
            appendix_title = ""
            appendix_description = ""

        # Remove non ascii/unicode characters
        finding_title_encoded = finding.title.encode("ascii", "ignore").decode()
        finding_description_encoded = finding.description.encode("ascii", "ignore").decode()
        finding_location_encoded = finding.location.encode("ascii", "ignore").decode()
        finding_impact_encoded = finding.impact.encode("ascii", "ignore").decode()
        finding_recommendation_encoded = finding.recommendation.encode("ascii", "ignore").decode()
        finding_references_encoded = finding.references.encode("ascii", "ignore").decode()
        appendix_title_encoded = appendix_title.encode("ascii", "ignore").decode()
        appendix_description_encoded = appendix_description.encode("ascii", "ignore").decode()

        writer.writerow([finding.finding_id, finding.status, finding_title_encoded, finding.severity, finding.cvss_base_score, finding.cvss_score, cwe_title, cwe_id, finding_description_encoded, finding_location_encoded, finding_impact_encoded, finding_recommendation_encoded, finding_references_encoded, appendix_title_encoded, appendix_description_encoded])


    return response




@login_required
@allowed_users(allowed_roles=['administrator'])
def upload_csv_findings(request,pk):
    
    DB_report_query = get_object_or_404(DB_Report, pk=pk)

    if request.method == 'POST':
        csv_file = request.FILES['file'].file

        #csv_file_string = io.TextIOWrapper(csv_file, encoding='utf-8')
        csv_file_string = io.TextIOWrapper(csv_file, encoding='ISO-8859-1')

        csvReader = csv.reader(csv_file_string, dialect='excel')

        csv.field_size_limit(100000000)

        header = next(csvReader)
        f_id = header.index("ID")
        f_status = header.index("Status")
        f_title = header.index("Title")
        f_severity = header.index("Severity")
        f_cvss_score = header.index("CVSS Base Score")
        f_cvss = header.index("CVSS Score")
        f_cwe = header.index("CWE ID")
        f_description = header.index("Description")
        f_location = header.index("Location")
        f_impact = header.index("Impact")
        f_recommendation = header.index("Recommendation")
        f_references = header.index("References")
        f_appendix = header.index("Appendix")
        f_appendix_description = header.index("Appendix Description")
         
        List = []
         
        for row in csvReader:
            fid = row[f_id]
            ftitle = row[f_title]
            fstatus = row[f_status]
            fseverity = row[f_severity]
            fcvss_score = row[f_cvss_score]
            fcvss = row[f_cvss]
            fcwe = row[f_cwe]
            fdescription = row[f_description]
            flocation = row[f_location]
            fimpact = row[f_impact]
            frecommendation = row[f_recommendation]
            freferences = row[f_references]
            fappendix = row[f_appendix]
            fappendixdescription = row[f_appendix_description]
            
            List.append([fid,ftitle,fstatus,fseverity,fcvss_score,fcvss,fcwe,fdescription,flocation,fimpact,frecommendation,freferences,fappendix,fappendixdescription])

            DB_cwe = get_object_or_404(DB_CWE, cwe_id=fcwe)

            # Save finding
            finding_to_DB = DB_Finding(report=DB_report_query, finding_id=fid, title=ftitle, status=fstatus, severity=fseverity, cvss_base_score=fcvss_score, cvss_score=fcvss, description=fdescription, location=flocation, impact=fimpact, recommendation=frecommendation, references=freferences, cwe=DB_cwe)
            finding_to_DB.save()

            # Save appendix
            if fappendix:
                appendix_to_DB = DB_Appendix(title=fappendix, description=fappendixdescription)
                appendix_to_DB.save()
                appendix_to_DB.finding.add(finding_to_DB)

        return redirect('report_view', pk=pk)

    return render(request, 'findings/uploadfindings.html', {'DB_report_query': DB_report_query})



@login_required
@allowed_users(allowed_roles=['administrator'])
def defectdojo_products(request,pk):

    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DefectDojoURL = DEFECTDOJO_CONFIG['DefectDojoURL']
    DefectDojoURLProducts = f"{DefectDojoURL}/api/v2/products/"
    DefectDojoApiKey = DEFECTDOJO_CONFIG['apiKey']

    headersapi = {'Authorization': DefectDojoApiKey}
    params = {'limit': 10000}

    try:
        r = requests.get(DefectDojoURLProducts, params = params, headers = headersapi, verify=False)
    except requests.exceptions.HTTPError:
        return HttpResponseNotFound(f"Not found. Response error from DefectDojo {DefectDojoURL}")

    if not (r.status_code == 200 or r.status_code == 201):
        return HttpResponseNotFound(f"No data found. Response error from DefectDojo {DefectDojoURL}")

    jsondata = json.loads(r.text)

    DDproducts_count = jsondata['count']
    DDproducts = jsondata['results']

    return render(request, 'defectdojo/defectdojo_products.html', {'DB_report_query': DB_report_query, 'DDproducts_count': DDproducts_count, 'DDproducts': DDproducts, 'DefectDojoURL': DefectDojoURL})



@login_required
@allowed_users(allowed_roles=['administrator'])
def defectdojo_viewfindings(request,pk,ddpk):

    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DefectDojoURL = DEFECTDOJO_CONFIG['DefectDojoURL']
    DefectDojoURLProducts = f"{DefectDojoURL}/api/v2/products/{ddpk}"
    DefectDojoApiKey = DEFECTDOJO_CONFIG['apiKey']

    headersapi = {'Authorization': DefectDojoApiKey}

    try:
        r = requests.get(DefectDojoURLProducts, headers = headersapi, verify=False)
    except requests.exceptions.HTTPError:
        return HttpResponseNotFound(f"Not found. Response error from DefectDojo {DefectDojoURL}")

    if not (r.status_code == 200 or r.status_code == 201):
        return HttpResponseNotFound(f"No data found. Response error from DefectDojo {DefectDojoURL}")

    jsondata = json.loads(r.text)
    DDproduct_findings_count = jsondata['findings_count']
    DDproduct_name = jsondata['name']
    DDproduct_findings_ids = jsondata['findings_list']

    DDproduct_findings = {}

    for finding in DDproduct_findings_ids:
        DefectDojoURLFindings = f"{DefectDojoURL}/api/v2/findings/{finding}"
        r = requests.get(DefectDojoURLFindings, headers = headersapi, verify=False)

        jsondata = json.loads(r.text)

        DDproduct_findings[finding] = {}

        DDproduct_findings[finding]['id'] = jsondata['id']
        DDproduct_findings[finding]['title'] = jsondata['title'] or ""
        DDproduct_findings[finding]['cvssv3'] = jsondata['cvssv3'] or ""
        DDproduct_findings[finding]['cvssv3_score'] = jsondata['cvssv3_score'] or 0
        DDproduct_findings[finding]['cwe'] = jsondata['cwe'] or 0
        DDproduct_findings[finding]['severity'] = (jsondata['severity']).capitalize() or ""

    return render(request, 'defectdojo/defectdojo_findings_products.html', {'DDproduct_findings_count': DDproduct_findings_count, 'DDproduct_name': DDproduct_name, 'DDproduct_findings': DDproduct_findings, 'DB_report_query': DB_report_query, 'DefectDojoURL': DefectDojoURL})


@login_required
@allowed_users(allowed_roles=['administrator'])
def defectdojo_import(request,pk,ddpk):

    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DefectDojoURL = DEFECTDOJO_CONFIG['DefectDojoURL']
    DefectDojoURLProducts = f"{DefectDojoURL}/api/v2/products/{ddpk}"
    DefectDojoApiKey = DEFECTDOJO_CONFIG['apiKey']

    headersapi = {'Authorization': DefectDojoApiKey}

    r = requests.get(DefectDojoURLProducts, headers = headersapi, verify=False)

    if not (r.status_code == 200 or r.status_code == 201):
        return HttpResponseNotFound("Not found. Response error from DefectDojo")

    jsondata = json.loads(r.text)
    DDproduct_findings = jsondata['findings_list']

    for finding in DDproduct_findings:
        DefectDojoURLFindings = f"{DefectDojoURL}/api/v2/findings/{finding}"
        r = requests.get(DefectDojoURLFindings, headers = headersapi, verify=False)

        jsondata = json.loads(r.text)

        finding_title = jsondata['title'] or ""
        finding_cvssv3 = jsondata['cvssv3'] or ""
        finding_cvssv3_score = jsondata['cvssv3_score'] or 0
        finding_cwe = jsondata['cwe'] or 0
        finding_severity = (jsondata['severity']).capitalize() or ""
        finding_description = jsondata['description'] or ""
        finding_mitigation= jsondata['mitigation'] or ""
        finding_impact = jsondata['impact'] or ""
        finding_steps_to_reproduce = jsondata['steps_to_reproduce'] or ""
        finding_references = jsondata['references'] or ""
        finding_hash_code = jsondata['hash_code'] or uuid.uuid4()
        finding_file_path = jsondata['file_path'] or ""

        finding_final_description = (finding_description + "\n----------\n" + finding_steps_to_reproduce).replace("{", "\{\{").replace("}", "\}\}")

        cweDB = DB_CWE.objects.filter(cwe_id=finding_cwe).first() or DB_CWE.objects.filter(cwe_id=0).first()

        #Save Finding
        finding_to_DB = DB_Finding(report=DB_report_query, finding_id=finding_hash_code, status = 'Open', title=finding_title, severity=finding_severity, cvss_base_score=finding_cvssv3, cvss_score=finding_cvssv3_score, description=finding_final_description, location=finding_file_path, impact=finding_impact, recommendation=finding_mitigation, references=finding_references, cwe=cweDB)
        finding_to_DB.save()

    return redirect('report_view', pk=pk)



@login_required
@allowed_users(allowed_roles=['administrator'])
def defectdojo_import_finding(request,pk,ddpk):

    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DefectDojoURL = DEFECTDOJO_CONFIG['DefectDojoURL']
    DefectDojoURLFindings = f"{DefectDojoURL}/api/v2/findings/{ddpk}"
    DefectDojoApiKey = DEFECTDOJO_CONFIG['apiKey']

    headersapi = {'Authorization': DefectDojoApiKey}

    r = requests.get(DefectDojoURLFindings, headers = headersapi, verify=False)

    if not (r.status_code == 200 or r.status_code == 201):
        return HttpResponseNotFound("Not found. Response error from DefectDojo")

    jsondata = json.loads(r.text)

    jsondata['id']
    finding_title = jsondata['title'] or ""
    finding_cvssv3 = jsondata['cvssv3'] or ""
    finding_cvssv3_score = jsondata['cvssv3_score'] or 0
    finding_cwe = jsondata['cwe'] or 0
    finding_severity = (jsondata['severity']).capitalize() or ""
    finding_description = jsondata['description'] or ""
    finding_mitigation= jsondata['mitigation'] or ""
    finding_impact = jsondata['impact'] or ""
    finding_steps_to_reproduce = jsondata['steps_to_reproduce'] or ""
    finding_references = jsondata['references'] or ""
    finding_hash_code = jsondata['hash_code'] or uuid.uuid4()
    finding_file_path = jsondata['file_path'] or ""

    finding_final_description = (finding_description + "\n----------\n" + finding_steps_to_reproduce).replace("{", "\{\{").replace("}", "\}\}")


    cweDB = DB_CWE.objects.filter(cwe_id=finding_cwe).first() or DB_CWE.objects.filter(cwe_id=0).first()

    #Save Finding
    finding_to_DB = DB_Finding(report=DB_report_query, finding_id=finding_hash_code, status = 'Open', title=finding_title, severity=finding_severity, cvss_base_score=finding_cvssv3, cvss_score=finding_cvssv3_score, description=finding_final_description, location=finding_file_path, impact=finding_impact, recommendation=finding_mitigation, references=finding_references, cwe=cweDB)
    finding_to_DB.save()

    return redirect('report_view', pk=pk)

# ----------------------------------------------------------------------
#                           Appendix 
# ----------------------------------------------------------------------


@login_required
def reportappendix(request,pk):
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()
    DB_appendix_query = DB_Appendix.objects.filter(finding__in=DB_finding_query)

    count_appendix_query = DB_appendix_query.count()

    return render(request, 'appendix/reportappendix.html', {'DB_report_query': DB_report_query, 'DB_finding_query': DB_finding_query, 'DB_appendix_query': DB_appendix_query, 'count_appendix_query': count_appendix_query})



@login_required
@allowed_users(allowed_roles=['administrator'])
def appendix_add(request,pk):

    DB_report_query = get_object_or_404(DB_Report, pk=pk)

    if request.method == 'POST':
        form = NewAppendixForm(request.POST, reportpk=pk)
        if form.is_valid():
            appendix = form.save(commit=False)            
            finding_pk = form['finding'].value()
            DB_finding_m2m = get_object_or_404(DB_Finding, pk=finding_pk)
            appendix.save()
            appendix.finding.add(finding_pk)

            if '_finish' in request.POST:
                return redirect('reportappendix', pk=pk)
            elif '_next' in request.POST:
                return redirect('appendix_add', pk=pk)
    else:
        form = NewAppendixForm(reportpk=pk)
        form.fields['description'].initial = 'TBD'


    return render(request, 'appendix/appendix_add.html', {
        'form': form, 'DB_report_query': DB_report_query
    })



@login_required
@allowed_users(allowed_roles=['administrator'])
def appendix_edit(request,pk):

    appendix = get_object_or_404(DB_Appendix, pk=pk)
    finding_pk = appendix.finding.first().pk
    DB_finding_query = get_object_or_404(DB_Finding, pk=finding_pk)

    report = DB_finding_query.report
    DB_report_query = get_object_or_404(DB_Report, pk=report.pk)

    if request.method == 'POST':
        form = NewAppendixForm(request.POST, instance=appendix, reportpk=report.pk)
        if form.is_valid():
            appendix = form.save(commit=False)
            new_finding_pk = form['finding'].value()
            New_DB_finding = DB_Finding.objects.filter(pk=new_finding_pk)
            appendix.save()
            appendix.finding.set(New_DB_finding, clear=True)

            if '_finish' in request.POST:
                return redirect('reportappendix', pk=report.pk)
            elif '_next' in request.POST:
                return redirect('appendix_add', pk=report.pk)
    else:
        form = NewAppendixForm(reportpk=report.pk, instance=appendix, initial={'finding': finding_pk})

    return render(request, 'appendix/appendix_add.html', {
        'form': form, 'DB_report_query': DB_report_query
    })





@login_required
@allowed_users(allowed_roles=['administrator'])
def appendix_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        DB_Appendix.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')



@login_required
def appendix_view(request,pk):
    appendix = get_object_or_404(DB_Appendix, pk=pk)
    finding_pk = appendix.finding.first().pk
    DB_finding_query = get_object_or_404(DB_Finding, pk=finding_pk)

    return render(request, 'appendix/appendix_view.html', {'DB_finding_query': DB_finding_query, 'DB_appendix_query': appendix})





# ----------------------------------------------------------------------
#                           Custom Fields 
# ----------------------------------------------------------------------

@login_required
def fields(request,pk):

    DB_finding_query = get_object_or_404(DB_Finding, pk=pk)
    DB_custom_query = DB_Custom_field.objects.filter(finding_id=pk)

    count_custom_query = DB_custom_query.count()

    return render(request, 'findings/custom_fields.html', {'DB_custom_query': DB_custom_query, 'DB_finding_query': DB_finding_query, 'count_custom_query': count_custom_query})


@login_required
@allowed_users(allowed_roles=['administrator'])
def field_add(request,pk):

    DB_finding_query = get_object_or_404(DB_Finding, pk=pk)

    if request.method == 'POST':
        form = NewFieldForm(request.POST)
        if form.is_valid():
            custom_field = form.save(commit=False)
            custom_field.finding = DB_finding_query
            custom_field.save()

            if '_finish' in request.POST:
                return redirect('finding_view', pk=pk)
            elif '_next' in request.POST:
                return redirect('field_add', pk=pk)
    else:
        form = NewFieldForm()
        form.fields['description'].initial = 'TBD'


    return render(request, 'findings/custom_field_add.html', {
        'form': form, 'DB_finding_query': DB_finding_query
    })



@login_required
@allowed_users(allowed_roles=['administrator'])
def field_edit(request,pk):

    field = get_object_or_404(DB_Custom_field, pk=pk)
    finding_pk = field.finding.pk

    if request.method == 'POST':
        form = NewFieldForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
            return redirect('finding_view', pk=finding_pk)
    else:
        form = NewFieldForm(instance=field)
    return render(request, 'findings/custom_field_add.html', {
        'form': form, 'DB_finding_query': field.finding
    })


@login_required
@allowed_users(allowed_roles=['administrator'])
def field_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        DB_Custom_field.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')

# ----------------------------------------------------------------------
#                           Templates 
# ----------------------------------------------------------------------


@login_required
def template_list(request):
    DB_findings_query = DB_Finding_Template.objects.order_by('title').reverse()

    return render(request, 'findings/template_list.html', {'DB_findings_query': DB_findings_query})



@login_required
@allowed_users(allowed_roles=['administrator'])
def template_add(request):

    if request.method == 'POST':
        form = NewFindingTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.finding_id = uuid.uuid4()
            template.save()

            if '_finish' in request.POST:
                return redirect('template_list')
            elif '_next' in request.POST:
                return redirect('template_add')
    else:
        form = NewFindingTemplateForm()
        form.fields['description'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['location'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['impact'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['recommendation'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['references'].initial = PETEREPORT_TEMPLATES['initial_text']
        form.fields['cwe'].initial = '1'

    return render(request, 'findings/template_add.html', {
        'form': form
    })


@login_required
@allowed_users(allowed_roles=['administrator'])
def template_edit(request, pk):

    template = get_object_or_404(DB_Finding_Template, pk=pk)

    if request.method == 'POST':
        form = NewFindingTemplateForm(request.POST, instance=template)
        if form.is_valid():
            template = form.save(commit=False)
            template.save()

            if '_finish' in request.POST:
                return redirect('template_list')
            elif '_next' in request.POST:
                return redirect('template_add')
    else:
        form = NewFindingTemplateForm(instance=template)

    return render(request, 'findings/template_add.html', {
        'form': form
    })


@login_required
@allowed_users(allowed_roles=['administrator'])
def template_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        DB_Finding_Template.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')



@login_required
def template_view(request,pk):
    DB_Template = get_object_or_404(DB_Finding_Template, pk=pk)

    return render(request, 'findings/template_view.html', {'DB_Template': DB_Template})



@login_required
@allowed_users(allowed_roles=['administrator'])
def templateaddfinding(request,pk):

    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_findings_query = DB_Finding_Template.objects.order_by('title')

    return render(request, 'findings/templateaddfinding.html', {'DB_findings_query': DB_findings_query, 'DB_report_query': DB_report_query})


@login_required
@allowed_users(allowed_roles=['administrator'])
def templateaddreport(request,pk,reportpk):

    DB_report_query = get_object_or_404(DB_Report, pk=reportpk)
    DB_finding_template_query = get_object_or_404(DB_Finding_Template, pk=pk)

    # save template in DB
    finding_uuid = uuid.uuid4()
    finding_status = "Open"
    finding_to_DB = DB_Finding(report=DB_report_query, finding_id=finding_uuid, title=DB_finding_template_query.title, severity=DB_finding_template_query.severity, cvss_base_score=DB_finding_template_query.cvss_base_score, cvss_score=DB_finding_template_query.cvss_score, description=DB_finding_template_query.description, status=finding_status, location=DB_finding_template_query.location, impact=DB_finding_template_query.impact, recommendation=DB_finding_template_query.recommendation, references=DB_finding_template_query.references, cwe=DB_finding_template_query.cwe)

    finding_to_DB.save()

    return redirect('report_view', pk=reportpk)


# ----------------------------------------------------------------------
#                           CWE 
# ----------------------------------------------------------------------

@login_required
def cwe_list(request):

    DB_cwe_query = DB_CWE.objects.order_by('pk').all()

    return render(request, 'cwe/cwe_list.html', {'DB_cwe_query': DB_cwe_query})


@login_required
@allowed_users(allowed_roles=['administrator'])
def cwe_add(request):

    if request.method == 'POST':
        form = NewCWEForm(request.POST)
        if form.is_valid():
            cwe = form.save(commit=False)
            cwe.save()
            return redirect('cwe_list')
    else:
        form = NewCWEForm()
        latest_id = DB_CWE.objects.latest('cwe_id').cwe_id
        next_id = latest_id+1

    return render(request, 'cwe/cwe_add.html', {
        'form': form
    })


@login_required
@allowed_users(allowed_roles=['administrator'])
def cwe_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        DB_CWE.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')




@login_required
@allowed_users(allowed_roles=['administrator'])
def cwe_edit(request,pk):

    cwe = get_object_or_404(DB_CWE, pk=pk)

    if request.method == 'POST':
        form = NewCWEForm(request.POST, instance=cwe)
        if form.is_valid():
            form.save()
            return redirect('cwe_list')
    else:
        form = NewCWEForm(instance=cwe)
    return render(request, 'cwe/cwe_add.html', {
        'form': form
    })


# ----------------------------------------------------------------------
#                           Attack Flow 
# ----------------------------------------------------------------------


@login_required
def reportattackflow(request,pk):
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()
    DB_attackflow_query = DB_AttackFlow.objects.filter(finding__in=DB_finding_query)

    count_attackflowquery = DB_attackflow_query.count()

    return render(request, 'attackflow/reportattackflow.html', {'DB_report_query': DB_report_query, 'DB_attackflow_query': DB_attackflow_query, 'count_attackflowquery': count_attackflowquery})


@login_required
def attackflow_add(request,pk):
    DB_report_query = get_object_or_404(DB_Report, pk=pk)
    DB_finding_query = DB_Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()
    count_finding_query = DB_finding_query.count()

    return render(request, 'attackflow/reportfindings.html', {'DB_report_query': DB_report_query, 'DB_finding_query': DB_finding_query, 'count_finding_query': count_finding_query})


@login_required
@allowed_users(allowed_roles=['administrator'])
def attackflow_add_flow(request,pk,finding_pk):

    DB_report_query = get_object_or_404(DB_Report, pk=pk)

    return render(request, 'attackflow/attackflow_add.html', {
        'DB_report_query': DB_report_query, 'report_pk': pk, 'finding_pk': finding_pk
    })


@login_required
@allowed_users(allowed_roles=['administrator'])
def attackflow_edit_flow(request,pk):

    DB_attackflow_query = get_object_or_404(DB_AttackFlow, pk=pk)
    attackflow_afb = DB_attackflow_query.attackflow_afb

    finding_pk = DB_attackflow_query.finding.first().pk
    DB_finding_query = get_object_or_404(DB_Finding, pk=finding_pk)

    report = DB_finding_query.report

    return render(request, 'attackflow/attackflow_edit.html', {
        'report_pk': report.pk, 'attackflow_pk': pk, 'finding_pk': finding_pk, 'attackflow_afb': attackflow_afb
    })


@login_required
@allowed_users(allowed_roles=['administrator'])
def attackflow_add_afb(request,pk,finding_pk):

    if request.method == 'POST':

        # data received from mitre attack flow
        data = json.loads(request.body)
        title_file = data['title']
        afb_content = data['afb_content']
        afb_image = data['afb_image']

        # Save attack flow
        attackflow_to_DB = DB_AttackFlow(title=title_file, attackflow_afb=afb_content, attackflow_png=afb_image)
        
        attackflow_to_DB.save()
        attackflow_to_DB.finding.add(finding_pk)

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')


@login_required
@allowed_users(allowed_roles=['administrator'])
def attackflow_edit_afb(request,pk):
    
    DB_attackflow_query = get_object_or_404(DB_AttackFlow, pk=pk)

    if request.method == 'POST':

        # data received from mitre attack flow
        data = json.loads(request.body)
        title_file = data['title']
        data['extension']
        afb_content = data['afb_content']
        afb_image = data['afb_image']

        # Save attack flow
        DB_attackflow_query.title = title_file
        DB_attackflow_query.attackflow_afb = afb_content
        DB_attackflow_query.attackflow_png = afb_image
        DB_attackflow_query.save()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')


@login_required
@allowed_users(allowed_roles=['administrator'])
def attackflow_delete(request):

    if request.method == 'POST':
        delete_id = request.POST['delete_id']
        DB_AttackFlow.objects.filter(pk=delete_id).delete()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')
