{% load martortags %}
{% load bleach_tags %}
---
title: "{{DB_report_query.title|safe| bleach}}"
product: "{{DB_report_query.product.name|safe| bleach}}"
author: ["{{md_author}}", "Report ID: {{DB_report_query.report_id|safe| bleach}}"]
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

{{DB_report_query.product.description|safe| bleach}}

# Executive Summary

{{DB_report_query.executive_summary|safe| bleach}}

## Summary of Findings Identified

<div class="chart">
<center>
  <div id="SeveritybarChartEcharts" style="width:80%; height:450px;"></div>
</center>
</div>

{{finding_summary_table}}

## Scope

### In Scope

{{DB_report_query.scope|safe| bleach}}

### Out of Scope

{{DB_report_query.outofscope|safe| bleach}}

## Methodology

{{DB_report_query.methodology|safe| bleach}}

## Recommendations

{{DB_report_query.recommendation|safe| bleach}}

# Findings and Risk Analysis

{{template_findings}}

{{template_appendix}}

{{template_attacktree}}