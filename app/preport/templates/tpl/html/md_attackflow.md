{% load martortags %}
{% load bleach_tags %}
{{attackflow_in_finding.title | safe | bleach}}

<center>
![{{attackflow_in_finding.title | safe | bleach}}]({{attackflow_in_finding.attackflow_png | safe | bleach}}){style="max-height:1000px;max-width:900px;height:auto;width:auto;"}
</center>
