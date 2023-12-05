{% load i18n %}

# {% translate "Identification du document" %}

|**Titre** | {{DB_report_query.title}}|
| - | - |
|**Classification** |{{DB_report_query.classification}} |
|**Version - Date** |{{DB_report_query.version}} – {{DB_report_query.report_date}} |
|**Statut** |{{DB_report_query.status}} |
|**Approbateur - Fonction** |{{DB_report_query.approver}} |
|**Rédacteur - Fonction** |{{DB_report_query.author}}|

\pagebreak

# {% translate "Points généraux sur l'évaluation" %}

{% if DB_report_query.audit_objectives %}
## {% translate "Objectifs de l'évaluation" %}

{{DB_report_query.audit_objectives | safe}}
{% endif %}

## {% translate "Avertissement sur ce document" %}

Le présent document, réalisé dans le cadre de l’évaluation de sécurité selon le schéma [CSPN](https://cyber.gouv.fr/documents-applicables-la-certification-de-securite-de-premier-niveau-cspn/) promu par l’ANSSI et adapté à notre contexte, est le rapport de l'évaluation :

* du produit **{{DB_report_query.product.name}}**,
* réalisée par **{{md_author}}**,
* du {{DB_report_query.audit_start|date:"Y-m-d" }} au {{DB_report_query.audit_end|date:"Y-m-d" }},
* depuis leurs locaux ({{md_address}}),
* à la demande de **{{DB_report_query.product.customer.name}}** à qui elle a été remise.


Toute communication, publication, divulgation, diffusion ou reproduction de ce rapport ou d'une partie de son contenu à des tiers sans l'accord écrit préalable de **{{md_author}}** et **{{DB_report_query.product.customer.name}}** n'est pas autorisé.

## {% translate "Classification des niveaux de risques" %}

Pour chaque vulnérabilité, une mitigation des risques est attendue (pour les points de faiblesse ne faisant pas l'objet d'une acceptation des risques) selon les délais indiqués dans le tableau ci-dessous.

\begin{center}
\begin{tabular}{cc}
    \hline
    \rowcolor{blue!30}
    Niveau de risque & Délais de mitigation des risques \\
    \hline\hline
    \rowcolor{criticalcolor}
    Critique & 1 jour \\
    \rowcolor{highcolor}
    Elevé & 3 jours \\
    \rowcolor{mediumcolor}
    Moyen & 14 jours \\
    \rowcolor{lowcolor}
    Bas & 30 jours \\
    \hline
\end{tabular}
\end{center} 
\pagebreak
# {% translate "Description du produit" %}

## {% translate "Présentation générale" %}

{{DB_report_query.product.description | safe}}

## {% translate "Récupération, installation et utilisation" %}

### {% translate "Récupération" %}

{% if DB_report_query.product.recovery %}
{{DB_report_query.product.recovery | safe}}
{% else %}
Sans objet.
{% endif %}

### {% translate "Installation" %}

{% if DB_report_query.product.installation %}
{{DB_report_query.product.installation | safe}}
{% else %}
Sans objet.
{% endif %}

### {% translate "Utilisation" %}
{% if DB_report_query.product.usage %}
{{DB_report_query.product.usage | safe}}
{% else %}
Sans objet.
{% endif %}

{% if DB_report_query.scope or DB_report_query.outofscope %}
## {% translate "Périmètre de l'évaluation" %}

{% if DB_report_query.scope %}
### {% translate "Dans le périmètre évalué" %}

{{DB_report_query.scope | safe}}
{% endif %}

{% if DB_report_query.outofscope %}
### {% translate "Hors du périmètre évalué" %}

{{DB_report_query.outofscope | safe}}
{% endif %}
\pagebreak
{% endif %}

# {% translate "Travaux d'évaluation" %}

## {% translate "Liste des évaluations" %}
{{pdf_cspn_eval_summary | safe}}
\pagebreak

{{template_cspn_evaluations | safe}}
\pagebreak

# {% translate "Analyse des vulnérabilités" %}

## {% translate "Liste des vulnérabilités identifiées" %}

{{pdf_finding_summary | safe}}

![Executive Summary]({{report_executive_summary_image}})

![Breakdown by OWASP Categories]({{report_owasp_categories_image}})
\pagebreak

{{template_findings | safe}}
\pagebreak

{% if counter_appendix > 0 %}
\pagebreak
{{template_appendix}}
{% endif %}
\pagebreak

# {% translate "Synthèse de l'évaluation" %}

{% if DB_report_query.executive_summary %}
## {% translate "Bilan" %}

{{DB_report_query.executive_summary | safe}}
{% endif %}

{% if DB_report_query.recommendation %}
## {% translate "Recommendations" %}

{{DB_report_query.recommendation | safe}}
{% endif %}



