"""
-- Created by Bikash Saud
--
-- Created on 2023-06-17
"""
from django.db import models

EXPENSE_DETERMINE_LEVEL = (
    ("ward", "Ward"),
    ("other", "Other"),
    ("municipality", "Municipality"),
)

PROJECT_LEVEL = (("ward", "ward"), ("local_level", "local_level"), ("other", "other"))

WORK_PROPOSER_TYPE = (
    ("ups", "उपभोक्ता समिति / टोल"),
    ("ward", "वडा"),
    ("muni", "न.पा./गा.पा."),
    ("other", "अन्य"),
)

BAIL_TYPES = (
    ("bank_guarantee", "बैंक ग्यारेन्टि"),
    ("cash", "नगद"),
)

BANK_GUARANTEE_TYPE = (
    ("bid_bond", "बिड बन्ड"),
    ("performance_bond", "पर्फरमेन्स बन्ड"),
)

TAX_PAYER_TYPE = (("हालको", "हालको"), ("भू.पू.", "भू.पू."))

MANDATE_TYPE = (
    ("from_a_specific_order", "तोक आदेशबाट"),
    ("from_allocated_budget", "विनियोजित बजेटबाट"),
)

ALLOCATION_TYPE = (
    ("Allocation", "Allocation"),
    ("Revision", "Revision"),
    ("Transfer-in", "Transfer-in"),
    ("Transfer-out", "Transfer-out"),
)

STATUS_CHOICES = (
    ("सुचारु नभएको", "सुचारु नभएको"),
    ("चालु अवस्था", "चालु अवस्था"),
    ("सम्पन्न भएको", "सम्पन्न भएको"),
)

ORIENTATION_CHOICES = (("Landscape", "Landscape"), ("Portrait", "Portrait"))

POSITION_CHOICES = (
    ("प्रशासनिक", "प्रशासनिक"),
    ("प्राविधिक", "प्राविधिक"),
    ("लागु नहुने", "लागु नहुने"),
)

PROJECT_PHASES = (
    ("created", "created"),
    ("initialized", "initialized"),
    ("agreement", "agreement"),
    ("partial-payment", "partial-payment"),
    ("completed", "completed"),
    ("issue", "issue"),
)

PROJECT_STATUSES = (
    "AGREEMENT_PENDING",
    "AGREEMENT_DONE",
    "WORK_ONGOING",
    "WORK_COMPLETED",
)


class RequestSend(models.TextChoices):
    PREPARATION = "P", "Preparation"
    VERIFICATION = "V", "Verification"
    APPROVAL = "A", "Approval"


class ProcessStatus(models.TextChoices):
    ACCEPT = "A", "Accept"
    REJECT = "R", "Reject"
    PENDING = "P", "Pending"


BASE_FRONTEND_URL = "lgerp.org"
APP_NAME = "Yojana"

TEMPLATE_LOAD_TAGS = """{% load custom_filters %}
{% load static %}"""

TEMPLATE_STARTING_BLOCK = (
    TEMPLATE_LOAD_TAGS
    + """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="{% static "custom_report_templates/css/main.css" %}" />
        <style>
            body {
                font-family: "Kalimati";
                width: 100vw;
            }
            
            figure.table {
                width: 100% !important;
                margin: 10px 0 !important;
            }

            table {
                width: 100%;
                margin: 10px 0 !important;
                border-spacing: 0;
            }

            table,
            table tr th,
            table tr td {
                border: 1px solid black;
            }

            table tr th,
            table tr td {
                padding: 2px 5px;
            }
        </style>
    </head>
    <body>"""
)

TEMPLATE_ENDING_BLOCK = """</body></html>"""
