def build_report_file_name(template_name:str, type_name:str, report_name:str, report_date:str, report_extension:str) -> str:
    report_n =  ''.join(e if e.isalnum() or e.isspace() or e == '-' else '_' for e in report_name)
    type_n =  ''.join(e if e.isalnum() or e.isspace()  or e == '-' else '_' for e in type_name)
    name_file = template_name + '_' + type_n + '_' + report_n + '_' + \
            report_date + '.' + report_extension

    return name_file
