from preport.models import DB_Deliverable, DB_Report, DB_Settings, DB_Finding
from preport.models import DB_Custom_field, DB_Customer, DB_Product
from preport.models import DB_Finding_Template, DB_CWE, DB_OWASP, DB_ShareConnection
from petereport.settings import MARTOR_UPLOAD_PATH, MARTOR_MEDIA_URL, PETEREPORT_MARKDOWN

import re, os, base64, mimetypes
from pathlib import Path

local_media_file_regex = re.compile(r'.*\]\((' + MARTOR_UPLOAD_PATH + '.+\.(?:png|gif|jpg|jpeg))\).*')
mimetypes.init()

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
    elif isinstance(item, DB_ShareConnection):
        return '/share/list/'
    else:
        return '/'

def replace_media_url_local_fs(markdown):
    return markdown.replace('](' + os.path.join(MARTOR_MEDIA_URL, 'uploads'), '](' + MARTOR_UPLOAD_PATH)

def replace_media_url_local_base64(markdown):
    return extract_local_media_files_to_base64(
            markdown.replace('](' + os.path.join(MARTOR_MEDIA_URL, 'uploads'), '](' + MARTOR_UPLOAD_PATH)
            )

def replace_media_url(markdown):
    if PETEREPORT_MARKDOWN['markdown_media_include'] == 'LOCAL_FS':
        return replace_media_url_local_fs(markdown)
    else:
        return replace_media_url_local_base64(markdown)

def extract_local_media_files_to_base64(markdown):
    mediafiles = re.findall(local_media_file_regex, markdown)
    if len(mediafiles) > 0:
        mediafiles = list(dict.fromkeys(mediafiles))
        for media in mediafiles:
            markdown = markdown.replace(media, local_file_to_base64(media))
    return markdown

def local_file_to_base64(mediafile):
    path = Path(mediafile)
    if path.is_file():
        with open(path, 'rb') as fh:
            mt = mimetypes.guess_type(path, strict=True)
            if mt:
                mt = mt[0]
            else:
                mt = 'application/octet-stream'
            return 'data:' + mt + ';base64,' + base64.b64encode(fh.read()).decode('utf-8')
    else:
        return mediafile
