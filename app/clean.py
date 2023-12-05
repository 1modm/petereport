#!/usr/bin/env python3

import os
import django
import shutil

from termcolor import colored  # pip3 install termcolor

os.environ['DJANGO_SETTINGS_MODULE'] = 'petereport.settings'
django.setup()

from petereport.settings import MEDIA_ROOT, REPORTS_MEDIA_ROOT, BASE_DIR
from preport.models import (DB_Customer,
                            DB_Product,
                            DB_Report,
                            DB_Finding,
                            DB_Finding_Template,
                            DB_Appendix,
                            DB_CWE,
                            DB_OWASP,
                            DB_CSPN_Evaluation,
                            DB_CSPN_Evaluation_Stage,
                            DB_Settings,
                            DB_Deliverable,
                            DB_FTSModel,
                            DB_ShareConnection,
                            DB_Custom_field,
                            DB_AttackFlow,
                            DB_AttackTree
                            )

import logging

logger = logging.getLogger(__name__)


def remove_folder(path):
    # check if folder exists
    if os.path.exists(path):
        # remove if exists
        shutil.rmtree(path)
    else:
        logger.error(colored("[-] Error removing files", "red"))


def create_media_folders(path):

    pathimg = path + "/images"

    try:
        os.makedirs(pathimg)
        try:
            shutil.copyfile(os.path.join(BASE_DIR, '..', 'images', 'company_picture.png'), os.path.join(pathimg, 'company_picture.png'))
        except OSError as ose:
            logger.error(colored(f"[-] Copy default Company logo failed", "red"))
        else:
            logger.info(colored(f"[+] Successfully copy default Company logo", "green"))
    except OSError:
        logger.error(colored(f"[-] Creation of the directory {path} failed", "red"))
    else:
        logger.error(colored(f"[+] Successfully created the petereport directories {MEDIA_ROOT}", "green"))




def create_storage_reports_folders(path):

    pathhtml = path + "/html"
    pathpdf = path + "/pdf"
    pathjupyter = path + "/jupyter"
    pathmarkdown = path + "/markdown"
    pathpandoc = path + "/pandoc"
    pathimg = path + "/images"

    try:
        os.makedirs(pathhtml)
        os.makedirs(pathpdf)
        os.makedirs(pathjupyter)
        os.makedirs(pathmarkdown)
        os.makedirs(pathpandoc)
        os.makedirs(pathimg)

    except OSError:
        logger.error(colored(f"[-] Creation of the directory {path} failed", "red"))

    else:
        logger.info(colored(f"[+] Successfully created the petereport directories {REPORTS_MEDIA_ROOT}", "green"))


#------------------------------------------------------------------------------
# Main of program
#------------------------------------------------------------------------------

def main():

    logger.warning(colored("[+] This will reset everything in the database and set up as fresh", "yellow"))
    logger.warning(colored("[+] Are you wanna do this?", "yellow"))

    answer = input("[No] | Yes?\n") or ""

    if "yes" == answer.lower():

        DB_Customer.objects.all().delete()
        DB_Product.objects.all().delete()
        DB_Report.objects.all().delete()
        DB_Finding.objects.all().delete()
        DB_Finding_Template.objects.all().delete()
        DB_Appendix.objects.all().delete()
        DB_CWE.objects.all().delete()
        DB_OWASP.objects.all().delete()
        DB_CSPN_Evaluation.objects.all().delete()
        DB_CSPN_Evaluation_Stage.objects.all().delete()
        DB_Settings.objects.all().delete()
        DB_Deliverable.objects.all().delete()
        DB_FTSModel.objects.all().delete()
        DB_ShareConnection.objects.all().delete()
        DB_AttackFlow.objects.all().delete()
        DB_AttackTree.objects.all().delete()
        DB_Custom_field.objects.all().delete()

        remove_folder(MEDIA_ROOT)
        create_media_folders(MEDIA_ROOT)

        remove_folder(REPORTS_MEDIA_ROOT)
        create_storage_reports_folders(REPORTS_MEDIA_ROOT)


#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
