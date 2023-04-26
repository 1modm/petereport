import re

simple_email_regex = '^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$'

def extract_valid_emails(emails_field:str) -> set:
    valid_emails = set()
    if isinstance(emails_field, str):
        tokens = re.split(',|;|:|\s', emails_field)
        for token in tokens:
            clean_token = str(token).strip().lower()
            if re.search(simple_email_regex, clean_token):
                valid_emails.add(clean_token)
    return valid_emails


emails_list_1 = 'andreea.alistar@thalesgroup.com - madalina.cozma.c@thalesdigital.io - radu.orleanu@thalesgroup.com'
print(extract_valid_emails(emails_list_1))

emails_list_2 = """andreea.alistar@thalesgroup.com -
madalina.cozma.c@thalesdigital.io ; toto
radu.orleanu@thalesgroup.com"""
print(extract_valid_emails(emails_list_2))

emails_list_3 = """andreea.alistar@thalesgroup.com : ;;;madalina.cozma.c@thalesdigital.io ;; ,, , : ;
    radu.orleanu@thalesgroup.com"""
print(extract_valid_emails(emails_list_3))

emails_list_4= """;andreea.alistar@thalesgroup.com,:;
 :;madalina.cozma.c@thalesdigital.io ,bob l'éponge;:
    radu.orleanu@thalesgroup.com;;"""
print(extract_valid_emails(emails_list_4))