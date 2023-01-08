#!/usr/bin/env python3

from petereport.settings import MEDIA_ROOT, REPORTS_MEDIA_ROOT
from preport.models import DB_Product, DB_Report, DB_Finding, DB_Finding_Template, DB_Appendix, DB_CWE

import os
import django
import shutil
from termcolor import colored #pip3 install termcolor

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petereport.settings")
django.setup()

def remove_folder(path):
    # check if folder exists
    if os.path.exists(path):
         # remove if exists
         shutil.rmtree(path)
    else:
        print(colored("[-] Error removing files", "red"))

def create_media_folders(path):

    pathimg = path + "/images"

    try:
        os.makedirs(pathimg)

    except OSError:
        print(colored(f"[-] Creation of the directory {path} failed", "red"))
    else:
        print(colored(f"[+] Successfully created the petereport directories {MEDIA_ROOT}", "green"))


def create_storage_reports_folders(path):

    pathhtml = path + "/html"
    pathpdf = path + "/pdf"
    pathimg = path + "/images"

    try:
        os.makedirs(pathhtml)
        os.makedirs(pathpdf)
        os.makedirs(pathimg)

    except OSError:
        print(colored(f"[-] Creation of the directory {path} failed", "red"))

    else:
        print(colored(f"[+] Successfully created the petereport directories {REPORTS_MEDIA_ROOT}", "green"))


#------------------------------------------------------------------------------
# Main of program
#------------------------------------------------------------------------------

def main():

    print(colored("[+] This will reset everything in the database and set up as fresh", "yellow"))
    print(colored("[+] Are you wanna do this?", "yellow"))

    answer = input("[No] | Yes?\n") or ""

    if "yes" == answer.lower():

        DB_Product.objects.all().delete()
        DB_Report.objects.all().delete()
        DB_Finding.objects.all().delete()
        DB_Appendix.objects.all().delete()
        DB_Finding_Template.objects.all().delete()
        DB_Appendix.objects.all().delete()
        DB_CWE.objects.all().delete()

        remove_folder(MEDIA_ROOT)
        create_media_folders(MEDIA_ROOT)

        remove_folder(REPORTS_MEDIA_ROOT)
        create_storage_reports_folders(REPORTS_MEDIA_ROOT)


#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
