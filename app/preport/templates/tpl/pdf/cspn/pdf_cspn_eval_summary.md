{% load i18n %}

::: {{evaluated_box}}
**# {{cspn_eval.stage.cspn_id}} - {{cspn_eval.stage.name|safe}}** ({% language "fr" %}{% translate cspn_eval.status%}{% endlanguage %})
:::
