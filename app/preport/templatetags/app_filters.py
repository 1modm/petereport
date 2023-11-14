# ----------  Template filters ------------

from django import template
from django.utils.safestring import mark_safe, SafeData
from django.template.defaultfilters import stringfilter
from preport.models import DB_Finding, DB_CSPN_Evaluation

import json

register = template.Library()

@register.filter('findings_count')
def findings_count(reports):
    """
    usage example {{ value1|findings_count }}
    """
    count_findings = 0

    for r in reports:
        count_report_findings = DB_Finding.objects.filter(report=r.id).count()
        count_findings = count_findings + count_report_findings

    return count_findings


@register.filter('cspn_evaluations_count')
def cspn_evaluations_count(reports):
    """
    usage example {{ value1|cspn_evaluations_count }}
    """
    count_cspn_evaluations = 0

    for r in reports:
        count_report_cspn_evaluations = DB_CSPN_Evaluation.objects.filter(report=r.id).count()
        count_cspn_evaluations = count_cspn_evaluations + count_report_cspn_evaluations

    return count_cspn_evaluations

@register.filter('jupyter_format')
def jupyter_format(text):
    """
    usage example {{ string|jupyter_format}}
    """

    formated_text = "\\n".join(line.strip() for line in text.splitlines())

    return mark_safe(formated_text)
