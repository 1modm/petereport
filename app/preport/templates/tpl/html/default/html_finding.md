{% load martortags %}
{% load bleach_tags %}
{% load i18n %}
## {{finding.title | safe | bleach}}

<table class="table table-bordered">

<tbody>

<tr>
<td style="width: 15%">**{% translate "Severity" %}**</td>
<td>**<span style="color:#{{color_text_severity}}">{{finding.severity | safe | bleach}} </span>**</td>
</tr>

<tr>
<td style="width: 15%">**{% translate "CVSS Score" %}**</td>
<td>**<span style="color:#{{color_text_severity}}">{{finding.cvss_score | safe | bleach}} </span>**</td>
</tr>

<tr>
<td style="width: 15%">**{% translate "CVSS Vector" %}**</td>
<td>**<span style="color:#{{color_text_severity}}">{{finding.cvss_vector | safe | bleach}} </span>**</td>
</tr>

<tr>
<td style="width: 15%">**CWE**</td>
<td>{{finding.cwe.cwe_id}} - {{finding.cwe.cwe_name | safe | bleach}}</td>
</tr>

<tr>
<td style="width: 15%">**OWASP**</td>
<td>{{finding.owasp.owasp_id|safe}} - {{finding.owasp.owasp_name|safe}}</td>
</tr>

{% if finding.description %}
<tr>
<td style="width: 15%">**{% translate "Description" %}**</td>
<td>

{{finding.description | safe_markdown | bleach}}

</td>
</tr>
{% endif %}

{% if finding.location %}
<tr>
<td style="width: 15%">**{% translate "Location" %}**</td>
<td>{{finding.location | safe_markdown | bleach}}</td>
</tr>
{% endif %}

{% if finding.impact %}
<tr>
<td style="width: 15%">**{% translate "Impact" %}**</td>
<td>{{finding.impact | safe_markdown | bleach}}</td>
</tr>
{% endif %}

{% if finding.poc %}
<tr>
<td style="width: 15%">**{% translate "Proof of Concept" %}**</td>
<td>{{finding.poc | safe_markdown | bleach}}</td>
</tr>
{% endif %}


{% if finding.recommendation %}
<tr>
<td style="width: 15%">**{% translate "Recommendation" %}**</td>
<td>{{finding.recommendation | safe_markdown | bleach}}</td>
</tr>
{% endif %}

{% if finding.references %}
<tr>
<td style="width: 15%">**{% translate "References" %}**</td>
<td>{{finding.references | safe_markdown | bleach}}</td>
</tr>
{% endif %}

{% if template_custom_fields %}
{{template_custom_fields | safe}}
{% endif %}

{% if template_attackflow_in_finding %}
<tr>
{{template_attackflow_in_finding | safe }}
</tr> 
{% endif %}

</tbody> </table>