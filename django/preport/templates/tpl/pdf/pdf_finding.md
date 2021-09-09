
## {{finding.title|safe}}

::: {{icon_finding}}
**Severity:** {{severity_color_finding}}

**CVSS Score:** {{finding.cvss_base_score}}
:::

**CWE**

{{finding.cwe.cwe_id}} - {{finding.cwe.cwe_name|safe}}

**Description**

{{finding.description|safe}}

**Location**

{{finding.location|safe}}

**Impact**

{{finding.impact|safe}}

**Recommendation**

{{finding.recommendation|safe}}

**References**

{{finding.references|safe}}

{% if template_appendix_in_finding %}
{{template_appendix_in_finding|safe}}
{% endif %}

{% if template_attacktree_in_finding %}
{{template_attacktree_in_finding|safe}}
{% endif %}

