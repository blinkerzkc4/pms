# Generated by Django 4.2.1 on 2024-04-27 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("norm", "0025_alter_activitytype_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="normcomponent",
            name="norm",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="norm.norm",
            ),
        ),
    ]
