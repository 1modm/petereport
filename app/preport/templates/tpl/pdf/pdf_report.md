# Project Overview

## Description

{{DB_report_query.product.description | safe}}

\pagebreak
# Executive Summary

{{DB_report_query.executive_summary | safe}}

## Summary of Findings Identified

![Executive Summary]({{report_executive_summary_image}})

![Breakdown by Categories]({{report_executive_categories_image}})

{{pdf_finding_summary}}

## Scope

### In Scope

{{DB_report_query.scope | safe}}

### Out of Scope

{{DB_report_query.outofscope | safe}}

\pagebreak
## Methodology

{{DB_report_query.methodology | safe}}

\pagebreak
## Recommendations

{{DB_report_query.recommendation | safe}}

\pagebreak
# Findings and Risk Analysis

{{template_findings}}

\pagebreak
{{template_appendix}}

\pagebreak
