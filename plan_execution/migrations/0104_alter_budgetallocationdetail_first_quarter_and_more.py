# Generated by Django 4.2.1 on 2024-01-04 01:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0103_projectcommentremarkfile_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budgetallocationdetail",
            name="first_quarter",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="budgetallocationdetail",
            name="fourth_quarter",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="budgetallocationdetail",
            name="second_quarter",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="budgetallocationdetail",
            name="third_quarter",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="budgetallocationdetail",
            name="total",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="expensetypedetail",
            name="amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="measuringbook",
            name="previous_measuring_book_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="measuringbook",
            name="result_obtained_so_far",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="measuringbook",
            name="this_measuring_book_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentdetail",
            name="amount",
            field=models.BigIntegerField(
                blank=True, help_text="रकम", null=True, verbose_name="Amount"
            ),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="advance_income_tex",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="check_pass_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="contentment_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="disbursement_assessment_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="env_disaster_fund_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="marmat_sambhar_fund_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="mu_aa_ka",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="nikasha_total_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="peski_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="plan_mst_total_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="public_participation_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="public_participation_percent",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="reinstatement_tex",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="total_remaining_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="u_sa_maag_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymentexitbill",
            name="withdrawal_eligible_amount",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="fifth_year",
            field=models.BigIntegerField(
                blank=True, help_text="पाँचौ वर्ष", null=True, verbose_name="Fifth Year"
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="first_trimester",
            field=models.BigIntegerField(
                blank=True,
                help_text="प्रथम त्रैमासिक",
                null=True,
                verbose_name="First Trimester",
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="first_year",
            field=models.BigIntegerField(
                blank=True, help_text="प्रथम वर्ष", null=True, verbose_name="First Year"
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="forth_year",
            field=models.BigIntegerField(
                blank=True, help_text="चौथो वर्ष", null=True, verbose_name="Fourth Year"
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="fourth_trimester",
            field=models.BigIntegerField(
                blank=True,
                help_text="चौथो त्रैमासिक",
                null=True,
                verbose_name="Fourth Trimester",
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="other",
            field=models.BigIntegerField(
                blank=True, help_text="अन्य", null=True, verbose_name="Other"
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="second_trimester",
            field=models.BigIntegerField(
                blank=True,
                help_text="दोस्रो त्रैमासिक",
                null=True,
                verbose_name="Second Trimester",
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="second_year",
            field=models.BigIntegerField(
                blank=True,
                help_text="दोस्रो वर्ष",
                null=True,
                verbose_name="Second Year",
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="third_trimester",
            field=models.BigIntegerField(
                blank=True,
                help_text="तेस्रो त्रैमासिक",
                null=True,
                verbose_name="Third Trimester",
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="third_year",
            field=models.BigIntegerField(
                blank=True,
                help_text="तेस्रो वर्ष",
                null=True,
                verbose_name="Third Year",
            ),
        ),
        migrations.AlterField(
            model_name="projectmobilization",
            name="mobilization_amount",
            field=models.BigIntegerField(
                blank=True,
                help_text="योजना संचालन रकम",
                null=True,
                verbose_name="Mobilization Amount",
            ),
        ),
        migrations.AlterField(
            model_name="projectmobilization",
            name="project_amount",
            field=models.BigIntegerField(
                blank=True,
                help_text="योजना रकम",
                null=True,
                verbose_name="Project Amount",
            ),
        ),
        migrations.AlterField(
            model_name="projectmobilizationdetail",
            name="amount",
            field=models.BigIntegerField(
                blank=True, help_text="रकम", null=True, verbose_name="Amount"
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="fifth_year",
            field=models.BigIntegerField(
                blank=True, help_text="पाँचौ वर्ष", null=True, verbose_name="Fifth Year"
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="first_trimester",
            field=models.BigIntegerField(
                blank=True,
                help_text="प्रथम त्रैमासिक",
                null=True,
                verbose_name="First Trimester",
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="first_year",
            field=models.BigIntegerField(
                blank=True, help_text="पहिलो वर्ष", null=True, verbose_name="First Year"
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="forth_year",
            field=models.BigIntegerField(
                blank=True, help_text="चौथो वर्ष", null=True, verbose_name="Forth Year"
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="fourth_trimester",
            field=models.BigIntegerField(
                blank=True,
                help_text="चौथो त्रैमासिक",
                null=True,
                verbose_name="Fourth Trimester",
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="other",
            field=models.BigIntegerField(
                blank=True, help_text="अन्य", null=True, verbose_name="Other"
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="second_trimester",
            field=models.BigIntegerField(
                blank=True,
                help_text="दोस्रो त्रैमासिक",
                null=True,
                verbose_name="Second Trimester",
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="second_year",
            field=models.BigIntegerField(
                blank=True,
                help_text="दोस्रो वर्ष",
                null=True,
                verbose_name="Second Year",
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="third_trimester",
            field=models.BigIntegerField(
                blank=True,
                help_text="तेस्रो त्रैमासिक",
                null=True,
                verbose_name="Third Trimester",
            ),
        ),
        migrations.AlterField(
            model_name="projectrevision",
            name="third_year",
            field=models.BigIntegerField(
                blank=True,
                help_text="तेस्रो वर्ष",
                null=True,
                verbose_name="Third Year",
            ),
        ),
        migrations.AlterField(
            model_name="usercommitteemonitoring",
            name="amount_payable_as_per_assessment",
            field=models.BigIntegerField(
                blank=True,
                help_text="मूल्यांकन अनुसार भुक्तानी गर्नु पर्ने रकम",
                null=True,
                verbose_name="Amount Payable As Per Assessment",
            ),
        ),
        migrations.AlterField(
            model_name="usercommitteemonitoring",
            name="assessment_amount",
            field=models.BigIntegerField(
                blank=True,
                help_text="मूल्यांकन रकम",
                null=True,
                verbose_name="Assessment Amount",
            ),
        ),
        migrations.AlterField(
            model_name="usercommitteemonitoring",
            name="project_amount",
            field=models.BigIntegerField(
                blank=True,
                help_text="योजना रकम",
                null=True,
                verbose_name="Project Amount",
            ),
        ),
    ]
