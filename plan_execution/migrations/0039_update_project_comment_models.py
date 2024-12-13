from django.conf import settings
from django.db import migrations, models

from plan_execution.models import (
    IndividualProjectComment as IndividualProjectCommentModel,
)
from plan_execution.models import ProjectComment as ProjectCommentModel


def update_project_execution_according_to_project(apps, schema_editor):
    ProjectComment: ProjectCommentModel = apps.get_model(
        "plan_execution", "ProjectComment"
    )
    db_alias = schema_editor.connection.alias
    for project_comment in ProjectComment.objects.using(db_alias).all():
        if not project_comment.project_execution:
            continue
        project_comment.project_execution = project_comment.project.projectexecution
        project_comment.save()


def create_individual_project_comments(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    ProjectComment: ProjectCommentModel = apps.get_model(
        "plan_execution", "ProjectComment"
    )
    IndividualProjectComment: IndividualProjectCommentModel = apps.get_model(
        "plan_execution", "IndividualProjectComment"
    )
    for project_comment in ProjectComment.objects.using(db_alias).all():
        individual_project_comment = IndividualProjectComment.objects.using(
            db_alias
        ).create(
            project_comment=project_comment,
            commented_by=project_comment.request_by,
            comment=project_comment.remarks,
        )
        for remark_file in project_comment.remark_files.all():
            remark_file.individual_comment = individual_project_comment
            remark_file.save()


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0038_projectcomment_last_status_update_and_more"),
    ]

    operations = [
        migrations.RunPython(update_project_execution_according_to_project),
        migrations.RunPython(create_individual_project_comments),
    ]
