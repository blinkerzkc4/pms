from django.db.models import TextChoices


class FieldTypeChoices(TextChoices):
    DB_COLUMN = "db_col", "Database Column"
    LOOP = "table_loop", "Table Loop"
