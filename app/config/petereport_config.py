PETEREPORT_CONFIG = {
	'admin_username': 'admin',
	'admin_password': 'P3t3r3p0rt',
	'admin_email': 'admin@petereport.pentest',
	'viewer_username': 'viewer',
	'viewer_password': 'v13w3r',
	'viewer_email': 'viewer@petereport.pentest'
}

DEFECTDOJO_CONFIG = {
	'DefectDojoURL': 'https://demo.defectdojo.org',
	'apiKey': 'Token Key' # Format: Token <api_key>
}

DJANGO_CONFIG = {
	'secret_key': 'django-insecure-key-CHANGEMEPLEASE-pKj9bd9h7*RMCuU',
	'debug': False,
	'admin_module': False,
	'allowed_hosts': '[\'*\']',
	'server_host': 'http://127.0.0.1:8000'
}

PETEREPORT_TEMPLATES = {
	'templates_root': 'preport/templates/tpl',
	'storage_reports': 'storage_reports',
	'html_template': 'bootstrap-4-pandoc-template/template.html',
	'pdf_latex_template': 'petereport.latex',
	'report_id_format': 'PEN-DOC-',
	'report_csv_name': 'PEN-CSV',
	'report_markdown_name': 'PEN-MD',
	'report_html_name': 'PEN-HTML',
	'report_pdf_name': 'PEN-PDF',
	'report_jupyter_name': 'PEN-JUPYTER',
	'initial_text': 'TBC',
	'titlepage-color': "1E90FF",
	'titlepage-text-color': "FFFAFA",
	'titlepage-rule-color': "FFFAFA",
	'titlepage-rule-height': 2
}

PETEREPORT_MARKDOWN = {
	'author': 'Pentest company',
	'subject': 'Pentest Report',
	'website': 'https://github.com/1modm/petereport',
	'martor_upload_method': 'BASE64', # BASE64 (stored in DB) or MEDIA (path not protected, must be set 'debug': True. This is highly insecure and not encouraged for production use. Should be configured the web server (apache, nginx, etc) to serve the media content using a protected link) 
	'media_host': 'http://127.0.0.1:8000' # If docker deployment, set https://<HOST IP>, else for django deployment http://<HOST IP>:8000 
}