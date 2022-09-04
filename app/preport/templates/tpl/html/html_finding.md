{% load martortags %}
{% load bleach_tags %}
## {{finding.title | safe | bleach}}

<table class="table table-bordered">

<tbody>

<tr>
<td style="width: 15%">**Severity**</td>
<td>**<span style="color:#{{color_text_severity}}">{{finding.severity | safe | bleach}} </span>**</td>
</tr>

<tr>
<td style="width: 15%">**CVSS Score**</td>
<td>**<span style="color:#{{color_text_severity}}">{{finding.cvss_score | safe | bleach}} </span>**</td>
</tr>

<tr>
<td style="width: 15%">**CWE**</td>
<td>{{finding.cwe.cwe_id}} - {{finding.cwe.cwe_name | safe | bleach}}</td>
</tr>

<tr>
<td style="width: 15%">**Description**</td>
<td>

{{finding.description | safe_markdown | bleach}}

</td>
</tr>

<tr>
<td style="width: 15%">**Location**</td>
<td>{{finding.location | safe_markdown | bleach}}</td>
</tr>

<tr>
<td style="width: 15%">**Impact**</td>
<td>{{finding.impact | safe_markdown | bleach}}</td>
</tr>

<tr>
<td style="width: 15%">**Recommendation**</td>
<td>{{finding.recommendation | safe_markdown | bleach}}</td>
</tr>

<tr>
<td style="width: 15%">**References**</td>
<td>{{finding.references | safe_markdown | bleach}}</td>
</tr>

{% if template_appendix_in_finding %}
<tr>
{{template_appendix_in_finding | safe }}
</tr> 
{% endif %}

{% if template_attacktree_in_finding %}
<tr>
{{template_attacktree_in_finding | safe }}
</tr> 
{% endif %}


</tbody> </table>