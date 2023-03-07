from django.apps import apps
from django.db import OperationalError, connection

def get_fts_models():
    models = {model.__name__: model for model in apps.get_models()}

    models_fields = {}
    for model_name, model_class in models.items():
        fields = [field.name for field in model_class._meta.fields]
        try:
            if  model_class.fts_enabled:
                try:
                    fts_excluded_fields = model_class.fts_excluded_fields
                    fts_excluded_fields.append('id')
                except AttributeError:
                    fts_excluded_fields = ['id']
                try:
                    fts_included_fields = model_class.fts_included_fields
                except AttributeError:
                    fts_included_fields = fields
                fts_fields = list(set(fts_included_fields).symmetric_difference(set(fts_excluded_fields)))
                models_fields[model_name] = fts_fields
        except AttributeError:
            pass

    return models_fields

def sql_delete_table_fts(model_name):
        table_name = 'preport_' + model_name.lower()

        fts_sql = 'DROP TABLE IF EXISTS fts_' + table_name + ';\n'
        for ext in ['config', 'data', 'docsize', 'idx']:
             fts_sql += 'DROP TABLE IF EXISTS fts_' + table_name + '_' + ext + ';\n'

        sql_events = ['INSERT', 'DELETE', 'UPDATE']
        for event in sql_events:
            fts_sql += 'DROP TRIGGER IF EXISTS fts_a' + event[0].lower() + '_' + table_name + ';\n'

        return fts_sql

def sql_create_table_fts(model_name, fts_fields):
        table_name = 'preport_' + model_name.lower()

        fts_sql = 'CREATE VIRTUAL TABLE fts_' + table_name + \
                        ' USING fts5(' + ', '.join(fts_fields) + ', content="' + table_name + '",' + \
                            ' content_rowid="id", prefix=2, prefix=3, prefix=4,' + \
                            ' tokenize="porter unicode61 remove_diacritics 1");\n'
        
        # Rebuild index to avoid error: Content in the virtual table is corrupt
        # https://www.sqlite.org/fts5.html#the_integrity_check_command
        fts_sql += 'INSERT INTO fts_' + table_name + '(fts_' + table_name + ') VALUES("rebuild");\n';

        fts_sql += 'CREATE TRIGGER fts_ai_' + table_name + ' AFTER INSERT ON ' + table_name + ' BEGIN\n' + \
                        'INSERT INTO fts_' + table_name + ' (rowid, ' + ', '.join(fts_fields) + ') ' + \
                            'VALUES (new.id, new.' + ', new.'.join(fts_fields) + ');\n' + \
                    'END;\n'

        fts_sql += 'CREATE TRIGGER fts_ad_' + table_name + ' AFTER DELETE ON ' + table_name + ' BEGIN\n' + \
                        'INSERT INTO fts_' + table_name + ' (fts_' + table_name + ', rowid, ' + ', '.join(fts_fields) + ') ' + \
                            'VALUES ("delete", old.id, old.' + ', old.'.join(fts_fields) + ');\n' + \
                    'END;\n'

        fts_sql += 'CREATE TRIGGER fts_au_' + table_name + ' AFTER UPDATE ON ' + table_name + ' BEGIN\n' + \
                        'INSERT INTO fts_' + table_name + ' (fts_' + table_name + ', rowid, ' + ', '.join(fts_fields) + ') ' + \
                            'VALUES ("delete", old.id, old.' + ', old.'.join(fts_fields) + ');\n' + \
                        'INSERT INTO fts_' + table_name + ' (rowid, ' + ', '.join(fts_fields) + ') ' + \
                            'VALUES (new.id, new.' + ', new.'.join(fts_fields) + ');\n' + \
                    'END;\n'

        return fts_sql

def search_into_model(table_model_name, query):
     with connection.cursor() as cursor:
        fts_table_model_name = 'fts_' + table_model_name
        sql_fts_query = "SELECT rowid, snippet({}, -1, '<mark>', '</mark>', '', 5) FROM {}(%s) ORDER BY rank".format(fts_table_model_name, fts_table_model_name)
        try:
            cursor.execute(sql_fts_query, (query, ))
            return cursor.fetchall()
        except OperationalError:
             pass



def execute_script_sql(sql_query):
     with connection.cursor() as cursor:
          return cursor.executescript(sql_query)