# Generated by Django 4.2.1 on 2023-10-11 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0032_populate_chart_of_accounts_and_modules"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounttitlemanagement",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="bankaccount",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="banktype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="bfi",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="budgetsource",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="budgetsubtitle",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="chequeformat",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="collectpayment",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="constructionmaterialdescription",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="consumercommittee",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="contractortype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="currency",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="drainagetype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="executiveagency",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="expansetype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="membertype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="module",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="newspaper",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="office",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="organizationtype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="paymentmedium",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="paymentmethod",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="prioritytype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="program",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectactivity",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectlevel",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectnature",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectprocess",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectproposedtype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectstartdecision",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectstatus",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projecttype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="purchasetype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="purposeplan",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="road",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="roadstatus",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="roadtype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="selectionfeasibility",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="sourcebearerentity",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="sourcebearerentitytype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="sourcereceipt",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="standinglist",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="standinglisttype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="strategicsign",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="subjectarea",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="subledger",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="submodule",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="targetgroup",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="targetgroupcategory",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
