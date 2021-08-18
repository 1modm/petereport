# ----------  Template filters ------------

from django import template
from django.utils.safestring import mark_safe, SafeData
from django.template.defaultfilters import stringfilter
from preport.models import DB_Report, DB_Finding

import json

register = template.Library()

@register.filter('findings_count')
def findings_count(reports):
    """
    usage example {{ value1|findings_count:value2 }}
    """
    count_findings = 0

    for r in reports:
        count_report_findings = DB_Finding.objects.filter(report=r.id).count()
        count_findings = count_findings + count_report_findings

    return count_findings

