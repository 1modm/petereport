{% load i18n %}
## {{finding.title|safe}}

**{% translate "Severity" %}:** {{finding.severity|safe}}

{% if finding.cvss_vector != "0" %}
**{% translate "CVSS Vector" %}:** {{finding.cvss_vector|safe}}
{% endif %}

{% if finding.cvss_score != "0" %}
**{% translate "CVSS Score" %}:** {{finding.cvss_score|safe}}
{% endif %}

**{% translate "CWE" %}:** {{finding.cwe.cwe_id|safe}} - {{finding.cwe.cwe_name|safe}}

**{% translate "OWASP" %}:** {{finding.owasp.owasp_id|safe}} - {{finding.owasp.owasp_name|safe}}


{% if finding.description %}
**{% translate "Description" %}**

{{finding.description|safe}}
{% endif %}

{% if finding.location %}
**{% translate "Location" %}**

{{finding.location|safe}}
{% endif %}

{% if finding.impact %}
**{% translate "Impact" %}**

{{finding.impact|safe}}
{% endif %}

{% if finding.poc %}
**{% translate "Proof of Concept" %}**

{{finding.poc|safe}}
{% endif %}

{% if finding.recommendation %}
**{% translate "Recommendation" %}**

{{finding.recommendation|safe}}
{% endif %}

{% if finding.references %}
**{% translate "References" %}**

{{finding.references|safe}}
{% endif %}

{% if template_custom_fields %}
{{template_custom_fields | safe}}
{% endif %}

{% if template_appendix_in_finding %}
{{template_appendix_in_finding|safe}}
{% endif %}


{% if template_attackflow_in_finding %}
{{template_attackflow_in_finding|safe}}
{% endif %}