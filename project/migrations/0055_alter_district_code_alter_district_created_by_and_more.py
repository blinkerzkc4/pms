# Generated by Django 4.2.1 on 2023-11-23 18:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0054_alter_project_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="district",
            name="code",
            field=models.CharField(
                help_text="कोड",
                max_length=10,
                null=True,
                unique=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="name",
            field=models.CharField(
                blank=True, help_text="नाम", max_length=120, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=120,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="name_unicode",
            field=models.CharField(
                blank=True,
                help_text="नाम (युनिकोड)",
                max_length=120,
                verbose_name="Name (Unicode)",
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="province",
            field=models.ForeignKey(
                blank=True,
                help_text="प्रदेश",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.province",
                verbose_name="Province",
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="remarks",
            field=models.TextField(
                blank=True, help_text="कैफियत", verbose_name="Remarks"
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="districtratefiles",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="districtratefiles",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="districtratefiles",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="estimate",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="estimate",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="estimate",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="end_year",
            field=models.IntegerField(
                help_text="समाप्त वर्ष (बि.सं.)", verbose_name="End Year"
            ),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="fy",
            field=models.CharField(
                blank=True,
                help_text="आर्थिक बर्ष",
                max_length=100,
                null=True,
                verbose_name="Financial Year",
            ),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="start_year",
            field=models.IntegerField(
                help_text="आरम्भ वर्ष (बि.सं.)", verbose_name="Start Year"
            ),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="jdcomment",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="jdcomment",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="jdcomment",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="jobdescription",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="jobdescription",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="jobdescription",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="jobdescriptionfile",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="jobdescriptionfile",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="jobdescriptionfile",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="code",
            field=models.CharField(
                help_text="कोड",
                max_length=10,
                null=True,
                unique=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="district",
            field=models.ForeignKey(
                blank=True,
                help_text="जिल्ला",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.district",
                verbose_name="District",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="email",
            field=models.EmailField(
                blank=True,
                help_text="ईमेल",
                max_length=100,
                null=True,
                verbose_name="Email",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="name",
            field=models.CharField(
                blank=True, help_text="नाम", max_length=120, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=120,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="name_unicode",
            field=models.CharField(
                blank=True,
                help_text="नाम (युनिकोड)",
                max_length=120,
                verbose_name="Name (Unicode)",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="number_of_wards",
            field=models.PositiveSmallIntegerField(
                default=1, help_text="वडा संख्या", verbose_name="Number of Wards"
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="office_address",
            field=models.CharField(
                blank=True,
                default="",
                help_text="कार्यालयको ठेगाना",
                max_length=255,
                verbose_name="Office Address",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="office_name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="कार्यालयको नाम",
                max_length=255,
                verbose_name="Office Name",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="phone",
            field=models.CharField(
                blank=True,
                default="",
                help_text="फोन",
                max_length=15,
                null=True,
                verbose_name="Phone",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="remarks",
            field=models.TextField(
                blank=True, help_text="कैफियत", verbose_name="Remarks"
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="sub_name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="उपनाम",
                max_length=255,
                verbose_name="Sub Name",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="category",
            field=models.ForeignKey(
                blank=True,
                help_text="श्रेणी",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.projectcategory",
                verbose_name="Category",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="financial_year",
            field=models.ForeignKey(
                blank=True,
                help_text="आर्थिक बर्ष",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.financialyear",
                verbose_name="Financial Year",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                help_text="नगरपालिका",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
                verbose_name="Municipality",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="name",
            field=models.CharField(
                blank=True, help_text="नाम", max_length=500, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="ward",
            field=models.ManyToManyField(
                blank=True, help_text="वडा", to="project.ward", verbose_name="Ward"
            ),
        ),
        migrations.AlterField(
            model_name="projectcategory",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="projectcategory",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="projectcategory",
            name="name",
            field=models.CharField(
                blank=True, help_text="नाम", max_length=120, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="projectcategory",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=120,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="projectcategory",
            name="name_unicode",
            field=models.CharField(
                blank=True,
                help_text="नाम (युनिकोड)",
                max_length=120,
                verbose_name="Name (Unicode)",
            ),
        ),
        migrations.AlterField(
            model_name="projectcategory",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="projectcategory",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="code",
            field=models.CharField(
                help_text="कोड",
                max_length=10,
                null=True,
                unique=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="name",
            field=models.CharField(
                blank=True, help_text="नाम", max_length=120, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=120,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="name_unicode",
            field=models.CharField(
                blank=True,
                help_text="नाम (युनिकोड)",
                max_length=120,
                verbose_name="Name (Unicode)",
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="province_number",
            field=models.PositiveIntegerField(
                help_text="प्रदेश नम्बर", verbose_name="Province Number"
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="remarks",
            field=models.TextField(
                blank=True, help_text="कैफियत", verbose_name="Remarks"
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="quantity",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="quantity",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="quantity",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="rate",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="rate",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="rate",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="ratearea",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="ratearea",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="ratearea",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="ratecategory",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="ratecategory",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="ratecategory",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="ratesource",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="ratesource",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="ratesource",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="summaryextra",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="summaryextra",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="summaryextra",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=50,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                help_text="नगरपालिका",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
                verbose_name="Municipality",
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="name",
            field=models.CharField(
                blank=True, help_text="नाम", max_length=120, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=120,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="name_unicode",
            field=models.CharField(
                blank=True,
                help_text="नाम (युनिकोड)",
                max_length=120,
                verbose_name="Name (Unicode)",
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="remarks",
            field=models.TextField(
                blank=True, help_text="कैफियत", verbose_name="Remarks"
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="ward",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="ward",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="ward",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
    ]