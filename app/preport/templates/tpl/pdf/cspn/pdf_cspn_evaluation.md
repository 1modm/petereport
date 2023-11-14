{% load i18n %}

## {{cspn_eval.stage.name|safe}}

::: {{icon_cspn}}
**{% translate "Statut" %}:** {% language "fr" %}{% translate cspn_eval.status%}{% endlanguage %}
:::

{% if cspn_eval.evaluation %}
### {% translate "Evaluation" %}

{{cspn_eval.evaluation|safe}}
{% endif %}

{% if cspn_eval.expert_notice %}
### {% translate "Avis d'expert" %}

{{cspn_eval.expert_notice|safe}}
{% endif %}