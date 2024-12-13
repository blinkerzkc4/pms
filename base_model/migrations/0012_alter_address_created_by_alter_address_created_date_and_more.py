# Generated by Django 4.2.1 on 2023-11-23 18:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0055_alter_district_code_alter_district_created_by_and_more"),
        ("base_model", "0011_documenttype_code_documenttype_detail_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
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
            model_name="address",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="house_no",
            field=models.CharField(
                blank=True,
                help_text="घर नं",
                max_length=55,
                null=True,
                verbose_name="House No",
            ),
        ),
        migrations.AlterField(
            model_name="address",
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
            model_name="address",
            name="road_name",
            field=models.CharField(
                blank=True,
                help_text="सडकको नाम",
                max_length=55,
                null=True,
                verbose_name="Road Name",
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="road_name_eng",
            field=models.CharField(
                blank=True,
                help_text="सडकको नाम (अंग्रेजी)",
                max_length=55,
                null=True,
                verbose_name="Road Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="tole",
            field=models.CharField(
                blank=True,
                help_text="टोल",
                max_length=55,
                null=True,
                verbose_name="Tole",
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="tole_eng",
            field=models.CharField(
                blank=True,
                help_text="टोल (अंग्रेजी)",
                max_length=55,
                null=True,
                verbose_name="Tole (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="ward",
            field=models.CharField(
                blank=True,
                help_text="वडा",
                max_length=55,
                null=True,
                verbose_name="Ward",
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="ward_eng",
            field=models.CharField(
                blank=True,
                help_text="वडा (अंग्रेजी)",
                max_length=55,
                null=True,
                verbose_name="Ward (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="contactdetail",
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
            model_name="contactdetail",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="contactdetail",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
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
            model_name="contactperson",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="email",
            field=models.CharField(
                blank=True,
                help_text="ईमेल",
                max_length=100,
                null=True,
                verbose_name="Email",
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="kramagat",
            field=models.CharField(
                blank=True,
                help_text="क्रमागत",
                max_length=255,
                null=True,
                verbose_name="Kramagat",
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="mobile_number",
            field=models.CharField(
                blank=True,
                help_text="मोबाइल नं",
                max_length=15,
                null=True,
                verbose_name="Mobile Number",
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="नाम",
                max_length=255,
                null=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=255,
                null=True,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="phone_number",
            field=models.CharField(
                blank=True,
                help_text="फोन नं",
                max_length=15,
                null=True,
                verbose_name="Phone Number",
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="position",
            field=models.CharField(
                blank=True,
                help_text="पद",
                max_length=255,
                null=True,
                verbose_name="Position",
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="remark",
            field=models.CharField(
                blank=True,
                help_text="कैफियत",
                max_length=255,
                null=True,
                verbose_name="Remark",
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="contactperson",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="documenttype",
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
            model_name="documenttype",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="documenttype",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="documenttype",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="gender",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="gender",
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
            model_name="gender",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="gender",
            name="detail",
            field=models.CharField(
                blank=True,
                help_text="विवरण",
                max_length=500,
                null=True,
                verbose_name="Detail",
            ),
        ),
        migrations.AlterField(
            model_name="gender",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="नाम",
                max_length=100,
                null=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="gender",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="gender",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="gender",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
    ]
