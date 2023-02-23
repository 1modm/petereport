#!/usr/bin/env python3

import os
import django

from config.petereport_config import PETEREPORT_CONFIG

def initApplication():

    os.environ["DJANGO_SETTINGS_MODULE"] = 'petereport.settings'
    django.setup()

    createAdminUser()
    createSettings()


def createSettings():

    from preport.models import DB_Settings
    from django.db import Error as DjangoError

    try:
        if not DB_Settings.objects.count():
            company_settings = DB_Settings(
                company_name = PETEREPORT_CONFIG['company_name'],
                company_website = PETEREPORT_CONFIG['company_website'],
                company_address = PETEREPORT_CONFIG['company_address'],
                company_picture = PETEREPORT_CONFIG['company_picture']
            )
            company_settings.save()

    except DjangoError:
        pass

def createAdminUser():

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
