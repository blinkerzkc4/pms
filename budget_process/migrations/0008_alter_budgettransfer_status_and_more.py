# Generated by Django 4.2.1 on 2023-07-21 02:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_planning', '0025_projectproposedtype'),
        ('project', '0026_unit_code'),
        ('budget_process', '0007_budgettransfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgettransfer',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='budgettransfer',
            name='total_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budgettransfer',
            name='transfer_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='budgettransfer',
            name='transfer_date_eng',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='BudgetAmmendment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_year', models.CharField(blank=True, max_length=50, null=True)),
                ('from_year_eng', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('kramagat', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.BooleanField(blank=True, null=True)),
                ('allocation_type', models.CharField(blank=True, choices=[('1', 'Allocation'), ('2', 'Revision'), ('3', 'Transfer-in'), ('4', 'Transfer-out')], max_length=1, null=True)),
                ('account_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_planning.accounttitlemanagement')),
                ('budget_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_planning.budgetsource')),
                ('financial_year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.financialyear')),
                ('sub_module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_planning.submodule')),
            ],
        ),
    ]
