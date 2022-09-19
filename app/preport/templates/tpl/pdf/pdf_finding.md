
## {{finding.title|safe}}

::: {{icon_finding}}
**Severity:** {{severity_color_finding}}

{% if finding.cvss_base_score != "0" %}
**CVSS Score:** {{finding.cvss_base_score|safe}}
{% endif %}
:::

**CWE**

{{finding.cwe.cwe_id}} - {{finding.cwe.cwe_name|safe}}

{% if finding.description %}
**Description**

{{finding.description|safe}}
{% endif %}

{% if finding.location %}
**Location**

{{finding.location|safe}}
{% endif %}

{% if finding.impact %}
**Impact**

{{finding.impact|safe}}
{% endif %}

{% if finding.recommendation %}
**Recommendation**

{{finding.recommendation|safe}}
{% endif %}

{% if finding.references %}
**References**

{{finding.references|safe}}
{% endif %}

{% if template_custom_fields %}
{{template_custom_fields | safe}}
{% endif %}

{% if template_appendix_in_finding %}
{{template_appendix_in_finding|safe}}
{% endif %}

{% if template_attacktree_in_finding %}
{{template_attacktree_in_finding|safe}}
{% endif %}

