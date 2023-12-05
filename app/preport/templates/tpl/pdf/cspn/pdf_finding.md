{% load i18n %}

## {{finding.title|safe}}

::: {{icon_finding}}
**Sévérité:** {{severity_color_finding}}

{% if finding.cvss_base_score != "0" %}
**Score CVSS** [{{finding.cvss_base_score|safe}}](https://www.first.org/cvss/calculator/3.1#{{finding.get_cvss_score_anchor|safe}})
{% endif %}

**Statut** {{finding.status}}
:::

**{% translate "OWASP" %}**

[OWASP-{{finding.owasp.owasp_full_id}} - {{finding.owasp.owasp_name|safe}}]({{finding.owasp.owasp_url}})

{% if finding.description %}
**{% translate "Description" %}**

{{finding.description|safe}}
{% endif %}

{% if finding.poc %}
**Preuve de concept**

{{finding.poc|safe}}
{% endif %}

{% if finding.location %}
**Localisation**

{{finding.location|safe}}
{% endif %}

{% if finding.impact %}
**{% translate "Impact" %}**

{{finding.impact|safe}}
{% endif %}

{% if finding.recommendation %}
**Recommandation**

{{finding.recommendation|safe}}
{% endif %}

{% if finding.ref %}
**Références**

{{finding.ref|safe}}
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
