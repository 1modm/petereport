{% load i18n %}
# {% translate "Project Overview" %}

## {% translate "Description" %}

{{DB_report_query.product.description | safe}}

\pagebreak
# {% translate "Executive Summary" %}

{{DB_report_query.executive_summary | safe}}

## {% translate "Summary of Findings Identified" %}

![Executive Summary]({{report_executive_summary_image}})

![Breakdown by CWE Categories]({{report_cwe_categories_image}})

![Breakdown by OWASP Categories]({{report_owasp_categories_image}})

{{pdf_finding_summary}}

## {% translate "Scope" %}

### {% translate "In Scope" %}

{{DB_report_query.scope | safe}}

### {% translate "Out of Scope" %}

{{DB_report_query.outofscope | safe}}

\pagebreak
## {% translate "Methodology" %}

{{DB_report_query.methodology | safe}}

\pagebreak
## {% translate "Recommendations" %}

{{DB_report_query.recommendation | safe}}

\pagebreak
# {% translate "Findings and Risk Analysis" %}

{{template_findings}}

\pagebreak
{{template_appendix}}

\pagebreak
