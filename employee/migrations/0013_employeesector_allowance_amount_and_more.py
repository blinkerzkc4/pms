# Generated by Django 4.2.1 on 2023-08-13 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0012_alter_country_detail_alter_department_detail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeesector',
            name='allowance_amount',
            field=models.FloatField(blank=True, help_text='भत्ता रकम', null=True),
        ),
        migrations.AddField(
            model_name='employeesector',
            name='insurance_amount',
            field=models.FloatField(blank=True, help_text='बिमा रकम', null=True),
        ),
        migrations.AddField(
            model_name='employeesector',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.position'),
        ),
        migrations.AddField(
            model_name='employeesector',
            name='position_level',
            field=models.ForeignKey(blank=True, help_text='श्रेणी/तह', null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.positionlevel'),
        ),
        migrations.AddField(
            model_name='employeesector',
            name='remarks',
            field=models.TextField(blank=True, help_text='कैफियत', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='positionlevel',
            name='adjustment_grade_rate',
            field=models.FloatField(blank=True, help_text='ग्रेडको दर', null=True),
        ),
        migrations.AddField(
            model_name='positionlevel',
            name='basic_salary',
            field=models.FloatField(blank=True, help_text='तलब स्केल', null=True),
        ),
        migrations.AddField(
            model_name='positionlevel',
            name='maximum_grade_rate',
            field=models.FloatField(blank=True, help_text='अधिकतम ग्रेड रकम', null=True),
        ),
        migrations.AddField(
            model_name='positionlevel',
            name='position_type',
            field=models.CharField(blank=True, choices=[('प्रशासनिक', 'प्रशासनिक'), ('प्राविधिक', 'प्राविधिक'), ('लागु नहुने', 'लागु नहुने')], help_text='प्राविधिक/प्रशासन', max_length=10, null=True),
        ),
    ]
