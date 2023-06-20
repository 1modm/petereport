def build_report_file_name(template_name:str, type_name:str, report_name:str, report_date:str, report_extension:str) -> str:
    report_n =  ''.join(e if e.isalnum() else '_' for e in report_name)
    name_file = template_name + '_' + type_name + '_' + report_n + '_' + \
            report_date + '.' + report_extension

    return name_file
