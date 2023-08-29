{% load i18n %}
---
title: "{{DB_report_query.title}}"
product: "{{DB_report_query.product.name}}"
author: ["{{md_author}}", "Report ID: {{DB_report_query.report_id}}"]
date: "{{report_date}}"
subject: "{{md_subject}}"
subtitle: "{{DB_report_query.report_id}}"
website: {{md_website}}
---

# {% translate "Project Overview" %}

## {% translate "Description" %}

{{DB_report_query.product.description | safe}}

# {% translate "Executive Summary" %}

{{DB_report_query.executive_summary | safe}}

## {% translate "Summary of Findings Identified" %}

![Breakdown by Severity]({{report_executive_summary_image}})

![Breakdown by CWE Categories]({{report_cwe_categories_image}})

![Breakdown by OWASP Categories]({{report_owasp_categories_image}})

{{finding_summary}}

## {% translate "Scope" %}

### {% translate "In Scope" %}

{{DB_report_query.scope | safe}}

### {% translate "Out of Scope" %}

{{DB_report_query.outofscope | safe}}

## {% translate "Methodology" %}

{{DB_report_query.methodology | safe}}

## {% translate "Recommendations" %}

{{DB_report_query.recommendation | safe}}

# {% translate "Findings and Risk Analysis" %}

{{template_findings}}

{{template_appendix}}