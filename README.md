# PeTeReport 

PeTeReport (**Pe**n**Te**st **Report**) is an open-source application vulnerability reporting tool designed to assist pentesting/redteaming efforts, by simplifying the task of writting and generation of reports.

Focused in product security, the tool help security researchers and pentesters to provide detailed findings, appendix, attack paths and manage a finding template database to avoid wasting time spent in the reporting phase.

PeTeReport (**Pe**n**Te**st **Report**) is written in Django and Python 3 with the aim to help pentesters and security researchers to manage a finding repository, write reports (in Markdown) and generate reports in different formats (HTML, CSV, PDF, Jupyter and Markdown).

<h4 align="center">Pentesting content management and reporting tool</h4>

<h1 align="center">
  <br>
  <a href="https://github.com/1modm/petereport"><img src="https://github.com/1modm/petereport/raw/main/images/dashboard.png" alt="petereport" width="80%" height="80%"></a>
  <br>
</h1>

## Documentation

[Documentation](https://1modm.github.io/petereport/)

[Installation and deployment](https://1modm.github.io/petereport/docker/)

## Features

- [x] Customizable reports output
- [x] Customizable reports templates thanks to [Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template)
- [x] Findings template database
- [x] Possibility to add appendix to findings
- [x] Possibility to add [Attack Flow](https://github.com/center-for-threat-informed-defense/attack-flow) to findings. This project is created and maintained by the MITRE Engenuity Center for Threat-Informed Defense
- [x] HTML Output format
- [x] CSV Output format
- [x] PDF Output format
- [x] Jupyter Notebook Output format
- [x] Markdown Output format
- [x] CVSS 4 Score
- [x] Docker installation
- [x] DefectDojo integration
- [x] User management
- [x] Custom fields
- [x] CWE custom list
- [x] Multilingual UI Lang files

## TODO

- [ ] More Output formats
- [ ] API
- [ ] Multilingual Report templates

## Demo

[Demo](https://petereport.mpsec.eu/) **admin/P3t3r3p0rt**


## Sample Reports

- [PDF Sample](https://github.com/1modm/petereport/raw/main/sample_reports/PEN-PDF_Offensive_Security_network.pdf "PDF Sample")
- [HTML Sample](https://github.com/1modm/petereport/raw/main/sample_reports/PEN-HTML_Offensive_Security_network.html "HTML Sample")
- [MD Sample](https://github.com/1modm/petereport/raw/main/sample_reports/PEN-MD_Offensive_Security_network.md "MD Sample")
- [CSV Sample](https://github.com/1modm/petereport/raw/main/sample_reports/PEN-CSV_Offensive_Security_network.csv "CSV Sample")
- [Jupyter Sample](https://github.com/1modm/petereport/raw/main/sample_reports/PEN-JUPYTER_Offensive_Security_network.ipynb "Jupyter Sample")


### Infrastructure model
![Infrastructure main model](.infragenie/infrastructure_main_model.svg)
- [petereport_django component model](.infragenie/petereport_django_component_model.svg)

---
