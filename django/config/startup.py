#!/usr/bin/env python3

import os
import sys
import csv
import json
import tempfile
import zipfile
import io

import requests
from requests import Response

from config.petereport_config import PETEREPORT_CONFIG


def createAdminUser():

    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'preport.settings')
    import django
    django.setup()
    from django.contrib.auth.models import User
    from django.db import Error as DjangoError
    try:
        user = User.objects.create_superuser(
            username = PETEREPORT_CONFIG['admin_username'],
            password = PETEREPORT_CONFIG['admin_password'],
            email = PETEREPORT_CONFIG['admin_email']
        )
        user.save()
    except DjangoError:
        pass