#!/usr/bin/env python3

import os
import django
from config.petereport_config import PETEREPORT_CONFIG


def createAdminUser():

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'preport.settings')
    django.setup()

    from django.contrib.auth.models import User, Group
    from django.db import Error as DjangoError

    try:
        group_administrator, created_administrator = Group.objects.get_or_create(name='administrator')
        group_viewer, created_viewer = Group.objects.get_or_create(name='viewer')

    except DjangoError:
        pass

    try:
        user_administrator = User.objects.create_superuser(
            username = PETEREPORT_CONFIG['admin_username'],
            password = PETEREPORT_CONFIG['admin_password'],
            email = PETEREPORT_CONFIG['admin_email']
        )
        user_administrator.groups.add(group_administrator)
        user_administrator.save()

    except DjangoError:
        pass

    try:
        user_viewer = User.objects.create_user(
            username = PETEREPORT_CONFIG['viewer_username'],
            password = PETEREPORT_CONFIG['viewer_password'],
            email = PETEREPORT_CONFIG['viewer_email']
        )

        user_viewer.groups.add(group_viewer)
        user_viewer.save()

    except DjangoError:
        pass

