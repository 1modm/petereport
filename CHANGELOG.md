Changelog
=========

## Version 1.4.1

### Enhancements and Bugfixes:

* Set martor to a fixed version 1.6.26 [#210](https://github.com/agusmakmun/django-markdown-editor/issues/210)
* POC section added to reports

## Version 1.4.0

### Enhancements and Bugfixes:

* Mayor upgrades and enhancement from bat_bast contributions
* Dashboard enhancement
* Customers management
* Deliverables management
* Reports and findings clone option
* Multiple output templates
* Findings OWASP top 10 categories [#5](https://github.com/1modm/petereport/issues/5)
* Settings section configuration added

## Version 1.3.3

### Enhancements and Bugfixes:
* lint the code and fix some code using ruff linter [#63](https://github.com/1modm/petereport/pull/63)
* Feature to select specific findings only from a product in DefectDojo [#64](https://github.com/1modm/petereport/issues/64)

## Version 1.3.2

### Enhancements and Bugfixes:
* Multilingual and Internationalization support
* Spanish and French lang files

## Version 1.3.1

### Enhancements and Bugfixes:
* CSV import enhancement
* Mitre [Attack Flow](https://github.com/center-for-threat-informed-defense/attack-flow) integration

## Version 1.3.0

### Enhancements and Bugfixes:
* Background logo image added to pdf reports
* Output templates improvements
* Custom fields

## Version 1.2.2

### Enhancements and Bugfixes:
* [#15](https://github.com/1modm/petereport/issues/15) Screenshots are not added to the appendix in reports

## Version 1.2.1

### Enhancements and Bugfixes:
* [#24](https://github.com/1modm/petereport/issues/24) Code is escaped in code box
* Minor changes in templates

## Version 1.2

### Enhancements and Bugfixes:
* [#28](https://github.com/1modm/petereport/issues/28) Add CWE directly in the web interface
* [#54](https://github.com/1modm/petereport/issues/54) Server error 500
* Error check in forms
* pluralize views
* Markdown, martor and image tags compatibility issues

## Version 1.1

### Enhancements and Bugfixes:
* [#51](https://github.com/1modm/petereport/issues/51) Error when importing from DefectDojo
* Minor changes

## Version 1.0

### Enhancements and Bugfixes:
* [#48](https://github.com/1modm/petereport/issues/48) 'bleach' causing Internal Error 500
* Upgraded bleach and django-bleach versions

## Version 0.9

### Enhancements and Bugfixes:
* Media images path support

## Version 0.8

### Enhancements and Bugfixes:
* [#39](https://github.com/1modm/petereport/issues/39) The newest version of bleach changed the parameters in the clean method (source: https://bleach.readthedocs.io/en/latest/changes.html#version-5-0-0-april-7th-2022). This causes the error: clean() got an unexpected keyword argument 'styles'. Workaround; to use bleach==4.1.0

Ubuntu 22.xx use python 3.10, in which was moved the library Collections Abstract Base Classes to the collections.abc module. For backwards compatibility, they continue to be visible through Python 3.9. Workaround; Ubuntu 20.04 is set to the correct docker image to pull.


## Version 0.7

### Enhancements and Bugfixes:
* [#36](https://github.com/1modm/petereport/issues/36) Security Issue - Stored XSS (Attack Tree)

## Version 0.6

### Enhancements and Bugfixes:
* [#34](https://github.com/1modm/petereport/issues/34) Security Issue - CSRF (Delete user,product,etc) [#35](https://github.com/1modm/petereport/issues/35) Security Issue -Stored XSS (markdown)


## Version 0.5

### Enhancements and Bugfixes:
* [#a92c7d3](https://github.com/1modm/petereport/commit/a92c7d3a88da43748799f01bdf9ea083b255a5f5) [#21](https://github.com/1modm/petereport/issues/21) None severity findings not shown


## Version 0.4

### Enhancements and Bugfixes:
* [#2076fd3](https://github.com/1modm/petereport/commit/2076fd3713e8b6d54b678ed2a10c2bd1158bb10a) [#22](https://github.com/1modm/petereport/issues/22) CVSS Calculator version 3.1
* [#2076fd3](https://github.com/1modm/petereport/commit/2076fd3713e8b6d54b678ed2a10c2bd1158bb10a) [#20](https://github.com/1modm/petereport/issues/20) Error 500 while exporting Report as Jupyter


## Version 0.3

### Enhancements and Bugfixes:
* [#b446175](https://github.com/1modm/petereport/commit/b446175a5d5fe240a57737fbc74f638cde0c83bd) Debug mode and Finding templates CWE search fix
* [#5caec18](https://github.com/1modm/petereport/commit/5caec18db8f7f77c79951b9672ecdd09108e7ec8) Add Finding CWE search searchbox


## Version 0.2

### Enhancements and Bugfixes:
* [#1647125](https://github.com/1modm/petereport/commit/1647125c61ae0ef79f74ea4e9de06cff1859129b) Documentation update and storage folder creation
* [#6461f72](https://github.com/1modm/petereport/commit/6461f7296f3801ca2efba73bd8857528a87a2518) app folder renaming


## Version 0.1

* [#64f78b2](https://github.com/1modm/petereport/commit/64f78b2edf504638ee619428dd4e2a54aeb9aaab) First commit
