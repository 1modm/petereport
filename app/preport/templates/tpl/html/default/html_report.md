{% load martortags %}
{% load bleach_tags %}
{% load i18n %}
---
title: "{{DB_report_query.title| safe | bleach}}"
product: "{{DB_report_query.product.name| safe | bleach}}"
author: ["{{md_author}}", "Report ID: {{DB_report_query.report_id| safe | bleach}}"]
date: "{{report_date}}"
subject: "{{md_subject}}"
subtitle: "{{DB_report_query.report_id}}"
website: {{md_website}}
counter_finding_critical: "{{counter_finding_critical}}"
counter_finding_high: "{{counter_finding_high}}"
counter_finding_medium: "{{counter_finding_medium}}"
counter_finding_low: "{{counter_finding_low}}"
counter_finding_info: "{{counter_finding_info}}"
lang: "en"
colorlinks: true
---

# {% translate "Project Overview" %}

## {% translate "Description" %}

{{DB_report_query.product.description | safe_markdown | bleach}}

# {% translate "Executive Summary" %}

{{DB_report_query.executive_summary | safe_markdown | bleach}}

## {% translate "Summary of Findings Identified" %}

<div class="chart">
<center>
  <div id="SeveritybarChartEcharts" style="width:80%; height:450px;"></div>
</center>
</div>

{{finding_summary_table}}

## {% translate "Scope" %}

### {% translate "In Scope" %}

{{DB_report_query.scope | safe_markdown | bleach}}

### {% translate "Out of Scope" %}

{{DB_report_query.outofscope | safe_markdown | bleach}}

## {% translate "Methodology" %}

{{DB_report_query.methodology | safe_markdown | bleach}}

## {% translate "Recommendations" %}

{{DB_report_query.recommendation | safe_markdown | bleach}}

# {% translate "Findings and Risk Analysis" %}

{{template_findings}}

{{template_appendix}}
