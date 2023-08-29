from petereport.settings import MARTOR_UPLOAD_PATH, MARTOR_MEDIA_URL

import re, os, base64, mimetypes
from pathlib import Path

local_media_file_regex = re.compile(r'.*\((' + MARTOR_UPLOAD_PATH + '.+\.(?:png|gif|jpg|jpeg))\).*')
mimetypes.init()

def replace_media_url_local_base64(markdown):
    return extract_local_media_files(
            markdown.replace('(' + os.path.join(MARTOR_MEDIA_URL, 'uploads'), '(' + MARTOR_UPLOAD_PATH)
            )

def extract_local_media_files(markdown):
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