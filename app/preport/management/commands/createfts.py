
from django.core.management.base import BaseCommand
import preport.utils.fts as ufts
from preport.models import DB_FTSModel

import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Rebuilds the database fts tables."

    def handle(self, *args, **options):
        """Runs the management command."""

        models = ufts.get_fts_models()

        DB_FTSModel.objects.all().delete()

        for model_name, model_fields in models.items():
            model = DB_FTSModel(model_name=model_name, fts_fields=', '.join(model_fields))
            model.save()

            logger.info("-- FTS " + model_name + " -----------------------")
            #logger.info("-- DELETE " + model_name)
            #logger.info(ufts.sql_delete_table_fts(model_name))
            ufts.execute_script_sql(ufts.sql_delete_table_fts(model_name))

            #logger.info("-- CREATE " + model_name)
            #logger.info(ufts.sql_create_table_fts(model_name, model_fields))
            ufts.execute_script_sql(ufts.sql_create_table_fts(model_name, model_fields))
