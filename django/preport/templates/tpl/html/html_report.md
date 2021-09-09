---
title: "{{DB_report_query.title}}"
product: "{{DB_report_query.product.name}}"
author: ["{{md_author}}", "Report ID: {{DB_report_query.report_id}}"]
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

# Project Overview

## Description

{{DB_report_query.product.description|safe}}

# Executive Summary

{{DB_report_query.executive_summary|safe}}

## Summary of Findings Identified

<div class="chart">
<center>
  <div id="SeveritybarChartEcharts" style="width:80%; height:450px;"></div>
</center>
</div>

{{finding_summary_table}}

## Scope

### In Scope

{{DB_report_query.scope|safe}}

### Out of Scope

{{DB_report_query.outofscope|safe}}

## Methodology

{{DB_report_query.methodology|safe}}

## Recommendations

{{DB_report_query.recommendation|safe}}

# Findings and Risk Analysis

{{template_findings}}

{{template_appendix}}

{{template_attacktree}}