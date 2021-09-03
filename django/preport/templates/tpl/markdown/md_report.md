---
title: "{{DB_report_query.title}}"
product: "{{DB_report_query.product.name}}"
author: ["{{md_author}}", "Report ID: {{DB_report_query.report_id}}"]
date: "{{report_date}}"
subject: "{{md_subject}}"
subtitle: "{{DB_report_query.report_id}}"
website: {{md_website}}
---

# Project Overview

## Description

{{DB_report_query.product.description}}

# Executive Summary

{{DB_report_query.executive_summary}}

## Summary of Findings Identified

![Breakdown by Severity]({{report_executive_summary_image}})

![Breakdown by Categories]({{report_executive_categories_image}})

{{finding_summary}}

## Scope

### In Scope

{{DB_report_query.scope}}

### Out of Scope

{{DB_report_query.outofscope}}

## Methodology

{{DB_report_query.methodology}}

## Recommendations

{{DB_report_query.recommendation}}

# Findings and Risk Analysis

{{template_findings}}

{{template_appendix}}

