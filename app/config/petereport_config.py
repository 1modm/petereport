# Review Django settings (https://djangostars.com/blog/configuring-django-settings-best-practices/)

# Read variables only from OS environment, not from file
import environ


env = environ.Env()

PETEREPORT_CONFIG = {
    'admin_username': env.str('PETEREPORT_ADMIN_USERNAME', default='admin'),
    'admin_password': env.str('PETEREPORT_ADMIN_PASSWORD', default='P3t3r3p0rt'),
    'admin_email': env.str('PETEREPORT_ADMIN_EMAIL', default='admin@petereport.pentest'),
    'viewer_username': env.str('PETEREPORT_VIEWER_USERNAME', default='viewer'),
    'viewer_password': env.str('PETEREPORT_VIEWER_PASSWORD', default='v13w3r'),
    'viewer_email': env.str('PETEREPORT_VIEWER_EMAIL', default='viewer@petereport.pentest'),
    'company_name': env.str('PETEREPORT_COMPANY_NAME', default='Pentest company'),
    'company_website': env.str('PETEREPORT_COMPANY_WEBSITE', default='https://github.com/1modm/petereport'),
    'company_picture': env.str('PETEREPORT_COMPANY_PICTURE', default='images/company_picture.png'),
    'company_address': env.str('PETEREPORT_COMPANY_ADDRESS', default='Spain'),
    'application_name': env.str('PETEREPORT_APPLICATION_NAME', default='PeTeReport'),
    'application_license': env.str('PETEREPORT_APPLICATION_LICENSE', default='BSD 3-Clause Copyright ©')
}

DEFECTDOJO_CONFIG = {
    'DefectDojoURL': env.str('PETEREPORT_DEFECTDOJO_URL', default='https://demo.defectdojo.org'),
    'apiKey': env.str('PETEREPORT_DEJECTDOJO_APIKEY', default='Token <Key>')
}

DJANGO_CONFIG = {
    'secret_key': env.str('PETEREPORT_DJANGO_SECRET_KEY', default='django-insecure-key-CHANGEMEPLEASE-pKj9bd9h7*RMCuU'),
    'debug': env.bool('PETEREPORT_DJANGO_DEBUG', default=False),
    'admin_module': env.bool('PETEREPORT_DJANGO_AMIN_MODULE', default=False),
    'allowed_hosts': env.list('PETEREPORT_DJANGO_ALLOWED_HOSTS', default=['*','localhost']),
    'csrf_trusted_origins': env.list('PETEREPORT_DJANGO_CSRF_TRUSTED_ORIGINS', default=['https://localhost']),
    'server_host': env.str('PETEREPORT_DJANGO_SERVER_HOST', default='http://127.0.0.1:8000'),
    'time_zone': env.str('PETEREPORT_DJANGO_TIME_ZONE', default='UTC'),
    'upload_memory_size': env.int('PETEREPORT_DJANGO_UPLOAD_MEMORY_SIZE', default=10485760) # 10MB

}

PETEREPORT_TEMPLATES = {
    'templates_root': 'preport/templates',
    'tpl_default_directory': 'default',
    'storage_reports': 'storage_reports',
    'html_template': 'bootstrap-4-pandoc-template/template.html',
    'report_csv_name': env.str('PETEREPORT_REPORT_CSV_NAME', default='PEN-CSV'),
    'report_markdown_name': env.str('PETEREPORT_REPORT_MARKDOWN_NAME', default='PEN-MD'),
    'report_html_name': env.str('PETEREPORT_REPORT_HTML_NAME', default='PEN-HTML'),
    'report_pdf_name': env.str('PETEREPORT_REPORT_PDF_NAME', default='PEN-PDF'),
    'report_jupyter_name': env.str('PETEREPORT_REPORT_JUPYTER_NAME', default='PEN-JUPYTER'),
    'report_custom_name': env.str('PETEREPORT_REPORT_CUSTOMR_NAME', default='PEN-CUSTOM'),
    'report_pdf_language': "en",
    'report_pdf_title_background': "title.png", # Location: app/preport/templates/tpl/pdf/default
    'report_pdf_pages_background': "pages.png", # Location: app/preport/templates/tpl/pdf/default
    'initial_text': 'TBC',
    'titlepage-color': "e6e2e2",
    'titlepage-text-color': "000000",
    'titlepage-rule-color': "cc0000",
    'titlepage-rule-height': 2
}

PETEREPORT_MARKDOWN = {
    'subject': env.str('PETEREPORT_SUBJECT', default='Pentest Report'),
    'martor_upload_method': env.str('PETEREPORT_MARTOR_UPLOAD_METHOD', default='BASE64'), # BASE64 (stored in DB) or MEDIA (path not protected, must be set 'debug': True. This is highly insecure and not encouraged for production use. Should be configured the web server (apache, nginx, etc) to serve the media content using a protected link)
    'media_host': env.str('PETEREPORT_MEDIA_HOST', default='http://127.0.0.1:8000') # If docker deployment, set https://<HOST IP>, else for django deployment http://<HOST IP>:8000
}