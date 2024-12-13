from django.conf import settings
from django.db import migrations, models

from plan_execution.models import ProjectComment as ProjectCommentModel


def update_users_allowed_to_comment(apps, schema_editor):
    ProjectComment: ProjectCommentModel = apps.get_model(
        "plan_execution", "ProjectComment"
    )
    db_alias = schema_editor.connection.alias
    for project_comment in ProjectComment.objects.using(db_alias).all():
        if not project_comment.send_to:
            continue
        project_comment.users_allowed_to_comment.add(project_comment.send_to)
        project_comment.save()


class Migration(migrations.Migration):
    dependencies = [
        (
            "plan_execution",
            "0042_rename_allowed_to_comment_projectcomment_users_allowed_to_comment",
        ),
    ]

    operations = [
        migrations.RunPython(update_users_allowed_to_comment),
    ]
