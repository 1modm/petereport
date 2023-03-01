from preport.models import DB_Deliverable, DB_Report, DB_Settings, DB_Finding, DB_Custom_field, DB_Customer, DB_Product, DB_Finding_Template, DB_CWE, DB_OWASP


def get_object_url(item):
    if isinstance(item, DB_Deliverable):
        return '/deliverable/list/'
    elif isinstance(item, DB_Report):
        return '/report/view/' + str(item.pk)
    elif isinstance(item, DB_Settings):
        return 'configuration/settings/'
    elif isinstance(item, DB_Finding):
        return '/finding/view/' + str(item.pk)
    elif isinstance(item, DB_Custom_field):
        return '/finding/view/' + str(item.finding.pk)
    elif isinstance(item, DB_Customer):
        return '/customer/view/' + str(item.pk)
    elif isinstance(item, DB_Product):
        return '/product/view/' + str(item.pk)
    elif isinstance(item, DB_Finding_Template):
        return '/template/view/' + str(item.pk)
    elif isinstance(item, DB_CWE):
        return '/cwe/list/'
    elif isinstance(item, DB_OWASP):
        return '/owasp/list/'
    else:
        return '/'
