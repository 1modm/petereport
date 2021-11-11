## {{finding.title|safe}}

<table class="table table-bordered">

<tbody>

<tr>
<td style="width: 15%">**Severity**</td>
<td>**<span style="color:#{{color_text_severity}}">{{finding.severity}} </span>**</td>
</tr>

<tr>
<td style="width: 15%">**CVSS Score**</td>
<td>**<span style="color:#{{color_text_severity}}">{{finding.cvss_score}} </span>**</td>
</tr>

<tr>
<td style="width: 15%">**CWE**</td>
<td>{{finding.cwe.cwe_id}} - {{finding.cwe.cwe_name|safe}}</td>
</tr>

<tr>
<td style="width: 15%">**Description**</td>
<td>

{{finding.description|safe}}

</td>
</tr>

<tr>
<td style="width: 15%">**Location**</td>
<td>{{finding.location|safe}}</td>
</tr>

<tr>
<td style="width: 15%">**Impact**</td>
<td>{{finding.impact|safe}}</td>
</tr>

<tr>
<td style="width: 15%">**Recommendation**</td>
<td>{{finding.recommendation|safe}}</td>
</tr>

<tr>
<td style="width: 15%">**References**</td>
<td>{{finding.references|safe}}</td>
</tr>

{% if template_appendix_in_finding %}
<tr>
{{template_appendix_in_finding|safe}}
</tr> 
{% endif %}

{% if template_attacktree_in_finding %}
<tr>
{{template_attacktree_in_finding|safe}}
</tr> 
{% endif %}


</tbody> </table>