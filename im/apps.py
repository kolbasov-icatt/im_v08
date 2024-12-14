from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver

class ImConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "im"



@receiver(connection_created)
def configure_sqlite(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        with connection.cursor() as cursor:
            # Increase SQLite variable limit
            cursor.execute("PRAGMA max_variable_number = 32766;")
