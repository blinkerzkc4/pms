from datetime import datetime

import nepali_datetime
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from budget_process.models import (
    BudgetAmmendment,
    BudgetTransfer,
    EstimateFinancialArrangements,
    ExpenseBudgetRangeDetermine,
    IncomeBudgetRangeDetermine,
)
from employee.models import (
    Department,
    Employee,
    EmployeeSector,
    EmployeeType,
    Position,
    PositionLevel,
    PublicRepresentativeDetail,
    PublicRepresentativePosition,
)
from formulate_plan.models import ProjectDocument, ProjectWorkType, WorkProject
from norm.models import Norm
from plan_execution.models import (
    BenefitedDetail,
    BudgetAllocationDetail,
    ProjectBidCollection,
    ProjectExecution,
    ProjectPhysicalDescription,
    ProjectUnitDetail,
)
from project.models import Rate
from project_planning.models import *
from project_planning.models import ExpanseType, ProjectType
from project_report.models import *
from utils.excel_generate import export_to_excel_old
from utils.generate_csv import export_to_csv
from utils.generate_pdf import render_to_pdf

from .models import Address, ContactDetail, ContactPerson, Gender
from .serializers import (
    AddressSerializer,
    ContactDetailSerializer,
    ContactPersonSerializer,
    GenderSerializer,
)

# from utils.nepali_date import today_nepali_date


# Create your views here.

common_table_heads = ["कोड़", "पुरा नाम", "Name"]
common_table_fields = ["code", "name", "name_eng"]
common_table_heads_parent = common_table_heads + ["माथिल्लो समुह "]
common_table_fields_parent = common_table_fields + ["parent"]
target_group_heads = common_table_heads + ["विवरण", "लक्षित समूहको प्रकार"]
target_group_fields = common_table_fields + ["detail", "target_group_category"]

project_type_display_head = ["कोड़", "पुरा नाम", "Name", "माथिल्लो समुह", "विवरण"]
project_type_head = ["code", "name", "name_eng", "parent", "detail"]

common_display_head = ["कोड़", "पुरा नाम", "Name", "विवरण"]
common_head = ["code", "name", "name_eng", "detail"]

strategic_sign_display_head = ["कोड़", "पुरा नाम", "Name", "विवरण"]
strategic_sign_head = ["code", "name", "name_eng", "detail"]

program_display_head = ["कोड़", "पुरा नाम", "Name", "विवरण"]
program_head = ["code", "name", "name_eng", "detail"]

extra_type_display_head = common_table_heads + ["क्रमागत", "विवरण"]
extra_type_head = common_table_fields + ["kramagat", "detail"]

contractor_type_display_head = common_table_heads + ["क्रमागत", "विवरण"]
contractor_type_head = common_table_fields + ["karmagat", "detail"]

standing_list_type_display_head = project_type_display_head
standing_list_type_head = project_type_head

standing_list_display_head = ["मिति", "प्रकार", "संस्था", "अा.ब", "स्थिति"]
standing_list_head = [
    "date",
    "standing_list_type",
    "organization",
    "financial_year",
    "status",
]

road_display_head = ["कोड़", "पुरा नाम", "Name", "विवरण"]
road_only_head = ["code", "name", "name_eng", "detail"]

### budget part

common_display_budget_head = ["कोड़", "पुरा नाम", "Name", "विवरण"]
common_budget_head = ["code", "name", "name_eng", "detail"]

atm_display_head = common_table_heads + [
    "माथिलो खाता कोड",
    "माथिलो खाता नाम",
    "मोड्युल",
    "आर्थिक वर्ष",
]
atm_head = common_table_fields + [
    "optional_code",
    "display_name",
    "module",
    "financial_year",
]

sbe_type_display_head = common_table_heads + ["क्रमागत", "विवरण"]
sbe_type_head = common_table_fields + ["karmagat", "detail"]

###
display_road_head = [
    "कोड़",
    "पुरा नाम",
    "Name",
    "जोडिएको_वार्डहरू",
    "बाटोको प्रकार",
    "बाटोको अवस्था",
    "अन्य अवस्थाहरु",
    "औसत चौडाई",
    "औसत चौडाई एकाई",
    "सडक शुरू हुने ठाउं",
    "सडक अन्त्य हुने ठाउं",
    "सडकको लम्बाई",
    "लम्बाईको एकाई",
    "जोडिएका सडकहरु",
    "जम्मा उपभोक्ताहरु",
    "जम्मा घरहरु",
    "निकासको स्थिति",
    "ढल निकासको प्रकार",
    "निकासको लम्बाई",
    "लम्बाईको एकाई",
    "निकासको चौडाई",
    "चौडाईको एकाई",
    " क्रमागत",
    "स्थिति",
]
road_head = [
    "code",
    "name",
    "name_eng",
    "connected_wards",
    "road_type",
    "road_status",
    "other_status",
    "average_width",
    "road_width_unit",
    "road_start_from",
    "road_end_to",
    "road_length",
    "road_length_unit",
    "connected_roads",
    "total_consumer",
    "total_house",
    "drainage_exit_status",
    "drainage_type",
    "drainage_length",
    "drainage_length_unit",
    "drainage_width",
    "drainage_width_unit",
    "karmagat",
    "status",
]

display_office_head = [
    "कोड़",
    "संगठन प्रकार",
    "पुरा नाम",
    "Name",
    "दर्ता नं.",
    "दर्ता मिति",
]
office_head = [
    "code",
    "organization_type",
    "name",
    "name_eng",
    "registration_no",
    "registration_date",
]

display_sbe_head = ["कोड़", "दाताको किसिम", "संस्थाकाे नाम", "विवरण"]
sbe_head = ["code", "bearer_type", "organization_name", "detail"]

display_budget_source_head = [
    "कोड़",
    "माथिल्लो स्रोत",
    "पुरा नाम",
    "Name",
    "देश",
    "फोन",
    "इमेल",
]
budget_source_head = [
    "code",
    "parent",
    "name",
    "name_eng",
    "country",
    "phone_number",
    "email",
]

display_newspaper_source_head = [
    "कोड़",
    "पुरा नाम",
    "Name",
    "पत्रिकाको ठेगाना",
    "छापाखाना गृह",
    "सम्पर्क व्यत्ति",
    "सम्पर्क नम्बर",
]
newspaper_source_head = [
    "code",
    "name",
    "name_eng",
    "news_paper_address",
    "printing_house",
    "contact_person",
    "contact_no",
]

display_organization_head = [
    "कोड़",
    "सस्थासंग सम्बन्धित प्रकार",
    "नाम/Name",
    "दर्ता नं.",
    "दर्ता मिति",
    "स्थाई ठेगाना",
    "सम्पर्क नम्बर",
    "FAX",
    "Email",
]
organization_head = [
    "code",
    "organization_type",
    "name_or_nepali_name",
    "register_no",
    "register_date_bs",
    "former_address",
    "contact",
    "fax",
    "email",
]

display_bank_account_head = [
    "खाता नम्बर",
    "पुरा नाम",
    "मुद्रा",
    "बैंकको नाम/Name",
    "सहायक मोड्युल",
]
bank_account_head = ["account_no", "name", "currency", "bank_name", "sub_module"]

display_bfi_head = [
    "कोड़",
    "बैंकको  प्रकार",
    "पुरा नाम",
    "ठेगाना बिवरण",
    "फोन",
    "FAX",
    "इमेल",
]
bfi_head = [
    "code",
    "bank_type",
    "name",
    "former_address",
    "phone_number",
    "fax",
    "email",
]

bank_type_display_head = ["कोड़", "नाम", "Name"]
bank_type_head = ["code", "name", "name_eng"]

consumer_committee_display_head = [
    "कोड",
    "उपभोक्ता वडा नं.",
    "नाम/Name",
    "दर्ता नं.",
    "दर्ता मिति",
    "स्थाई ठेगाना",
    "सम्पर्क नम्बर",
    "FAX",
    "Email",
]
consumer_committee_head = [
    "code",
    "ward_no",
    "name",
    "registration_no",
    "registration_date_bs",
    "former_address",
    "phone_number",
    "fax",
    "email",
]

expense_budget_ward_display_head = [
    "वडा",
    "आनुमानित सीमा",
    "आन्तरिक स्रोत",
    "जनसहभागिता",
    "स्वीकृत",
]
expense_budget_ward_head = [
    "ward",
    "estimated_amount",
    "internal_source",
    "public_participation",
    "is_approved",
]

expense_budget_display_head = [
    "व्यय शिर्षक नम्बर",
    "आनुमानित सीमा",
    "आन्तरिक स्रोतबाट",
    "जनसहभागिता",
    "स्वीकृत",
]
expense_budget_head = [
    "expense_title_no",
    "estimated_amount",
    "internal_source",
    "public_participation",
    "is_approved",
]

income_budget_display_head = [
    "आय शिर्षक नम्बर",
    "आनुमानित सीमा",
    "आन्तरिक श्रोतबाट",
    "जनसहभागिता",
    "स्वीकृत",
]
income_budget_head = [
    "income_title_no",
    "estimated_amount",
    "internal_source",
    "public_participation",
    "is_approved",
]

efa_display_head = ["आय शिर्षक नम्बर", "आनुमानित सीमा", "स्वीकृत"]
efa_head = ["income_title_no", "estimated_amount", "is_approved"]

unit_display_head = ["कोड़", "पुरा नाम", "Name"]
unit_head = ["code", "name", "name_eng"]

financial_year_display_head = ["मिति देखि", "मिति सम्म", "स्थिति"]
financial_year_head = ["start_year", "end_year", "status"]


employee_display_head = [
    "नाम",
    "संकेत",
    "लिङ्ग",
    "बिभाग/श्रेणी/तह",
    "सेवा समूह/कर्मचारीको प्रकार",
    "हालको पद सुरु मिति",
    "स्थिति",
]
employee_head = [
    "full_name",
    "code",
    "gender",
    "department",
    "service",
    "enroll_start_date",
    "status",
]

public_detail_display_head = [
    "हालको/भु.पू",
    "नाम/Name",
    "पदावधि सुरु मिति",
    "पदावधि समाप्ति मिति",
    "Email",
    "Mobile",
    "स्थिति",
]
public_detail_head = [
    "position_level",
    "full_name",
    "position_start_date",
    "position_end_date",
    "email",
    "mobile",
    "status",
]
project_physical_display_head = ["ईकाईको किसिम", "ईकाई"]
project_physical_head = ["name", "code"]

project_unit_display_head = ["ईकाईको किसिम", "ईकाई", "प्रति ईकाई दर", "जम्मा ईकाई"]
project_unit_head = ["name", "code", "unit_rate", "total_unit"]

budget_allocation_display_head = [
    "बजेट उपशीर्षक",
    "खर्च शीर्षक",
    "विषयगत क्षेत्र",
    "कार्यक्रम",
    "बजेट स्रोत",
    "प्राप्तिको स्रोत",
    "भुक्तानी विधि",
    "जम्मा",
]
budget_allocation_head = [
    "budget_sub_title",
    "expense_title",
    "subject_area",
    "program",
    "budget_source",
    "source_receipt",
    "expense_method",
    "total",
]

benefited_detail_display_head = [
    "लक्षित समूह ",
    "जम्मा घर संख्या",
    "पुरुषको जनसंख्या",
    "महिला जनसंख्या",
    "अन्य जनसंख्या",
    "जम्मा जनसंख्या",
]
benefited_detail_head = [
    "target_group",
    "total_house_number",
    "total_man",
    "total_women",
    "total_other",
    "total_population",
]

project_work_document_display_head = ["कागजातको नाम", "कागजातको किसिम"]
project_work_document_head = ["project", "document_type"]

local_display_head = [
    "कोड",
    "नाम/Name",
    "कामको वर्ग",
    "कामको प्रकार",
    "उपभोक्ता समिति",
    "वडा नं",
    "अनुमानित रकम",
    "आन्तरिक श्रोत",
    "नेपाल सरकार श्रोत",
    "नेपाल सरकार श्रोत",
    "स्थानीय तह श्रोत",
    "जनसहभागिता श्रोत",
    "ऋण श्रोत",
    "अनुमानित सुरु मिति(बि.स.)",
    "अनुमानित सकिने मिति(बि.स.)",
]
local_head = [
    "code",
    "name",
    "work_class",
    "work_type",
    "user_committee",
    "ward",
    "estimated_amount",
    "internal_source",
    "nepal_gov",
    "province_gov",
    "local_level_gov",
    "public_participation",
    "loan",
    "estimated_start_date",
    "estimated_end_date",
]

ward_display_head = [
    "कोड",
    "नाम/Name",
    "कामको वर्ग",
    "कामको प्रकार",
    "उपभोक्ता समिति",
    "वडा नं",
    "अनुमानित रकम",
    "आन्तरिक श्रोत",
    "नेपाल सरकार श्रोत",
    "नेपाल सरकार श्रोत",
    "स्थानीय तह श्रोत",
    "जनसहभागिता श्रोत",
    "ऋण श्रोत",
    "अनुमानित सुरु मिति(बि.स.)",
    "अनुमानित सकिने मिति(बि.स.)",
]
ward_head = [
    "code",
    "name",
    "work_class",
    "work_type",
    "user_committee",
    "ward",
    "estimated_amount",
    "internal_source",
    "nepal_gov",
    "province_gov",
    "local_level_gov",
    "public_participation",
    "loan",
    "estimated_start_date",
    "estimated_end_date",
]

budget_ammend_display_head = [
    "खाताको नाम",
    "सब-मोड्यूल",
    "बजेट स्रोत",
    "आर्थिक वर्ष",
    "रकम",
    "क्रमागत",
    "विवरण",
    "स्थिति",
]
budget_ammend_head = [
    "account_title",
    "sub_module",
    "budget_source",
    "financial_year",
    "rakam",
    "kramagat",
    "description",
    "status",
]
budget_transfer_display_head = ["transfer_date", "स्थिति"]
budget_transfer_head = ["transfer_date", "status"]

project_execution_display_head = [
    "योजना कोड",
    "सन्चालन गर्ने वडा नं.",
    "योजना नाम",
    "सञ्चालन प्रकृया",
    "कार्यक्षेत्र",
    # "उपभोक्ता समिति/संध/सस्था नाम",
    # "सम्झौता अवस्था",
    "काम योजना/कार्यक्रम",
    "अनुमानित रकम",
    "खुद लगत ईस्टिमेट",
    "१५% ओभरहेड",
    "कन्टीनजेन्सी 0%",
    "१३% मू.अ. कर",
    "जम्मा लगत ईस्टिमेट",
    # "खुद भुक्तानीयोग्य रू.",
    "आर्थिक वर्ष ",
    # "प्रदेश",
]
project_execution_head = [
    "code",
    "ward",
    "name",
    "start_pms_process",
    "work_proposer_type",
    "program",
    "estimated_amount",
    "appropriated_amount",
    "overhead",
    "contingency",
    "mu_aa_ka",
    "total_estimate",
    "financial_year",
]

norm_display_head = [
    "क्रियाकलाप नम्बर",
    "विशिष्ट ग्राहक संख्या",
    "Description of Work",
    "कार्यको विवरण",
    "इकाई",
    "प्रकार",
    "दर",
    "परिमाण",
    "रकम",
    "साधन",
    "सामग्री",
    "उपकरण",
    "कार्य बल",
    "कैफियत",
]
norm_head = [
    "activity_no",
    "specification_no",
    "description_eng",
    "description",
    "unit",
    "resource",
    "work force",
    "type",
    "rate",
    "quantity",
    "amount",
    "material",
    "equipment",
    "remark",
]
rate_display_head = [
    "क्र.श.",
    "Description",
    "विवरण",
    "इकाई",
    "श्रोत",
    "क्षेत्रफल",
    "मु.अ.क. बाहेकको दर",
    "आर्थिक वर्ष",
]
rate_head = [
    "id",
    "title",
    "title_eng",
    "unit",
    "source",
    "area",
    "amount",
    "financial_year",
]

subject_area_display_head = common_table_heads + ["माथिल्लो समुह ", "विवरण"]
subject_area_head = common_table_fields + ["parent", "detail"]

template_field_mapping_display_head = common_table_heads + ["सञ्चालन प्रकृया"]
template_field_mapping_head = common_table_fields + ["pms_process_id"]

project_bid_collection_display_head = [
    "निर्माण व्यवसायीको नाम",
    "Builder Pan No",
    "नियमपुर्बक",
    "धरौटीको रकम",
    "धरौटीको किसिम",
    "बैंकको नाम",
    "बैंक ग्यारेन्टीको न.",
    "बैंक ग्यारेन्टीको प्रकार",
    "जम्मा कबुल रकम",
    "मु. अ. कर",
    "जम्मा",
    "स्वीकृत",
]

project_bid_collection_head = [
    "builder_name",
    "builder_pan_no",
    "is_legal",
    "bail_amount",
    "bid_type",
    "bail_type",
    "bank_guarantee_no",
    "bank_guarantee_type",
    "total_amount",
    "mu_aa_ka",
    "total",
    "is_approved",
]

export_models = {
    "norms": [
        Norm,
        norm_display_head,
        norm_head,
        "नोर्म",
    ],
    "district-rate": [
        Rate,
        rate_display_head,
        rate_head,
        "जिल्ला दर",
    ],
    "expense-type": [
        ExpanseType,
        common_display_head,
        common_head,
        "खर्चको फाटवारी विवरण",
    ],
    "project-type": [
        ProjectType,
        project_type_display_head,
        project_type_head,
        "योजनाको किसिम",
    ],
    "purpose-plan": [
        PurposePlan,
        common_display_head,
        common_head,
        "योजनाको उदेश्य",
    ],
    "project-process": [
        ProjectProcess,
        common_display_head,
        common_head,
        "योजना संचालन प्रक्रिया",
    ],
    "project-nature": [
        ProjectNature,
        common_display_head,
        common_head,
        "योजनाको प्रकृति",
    ],
    "project-level": [
        ProjectLevel,
        common_display_head,
        common_head,
        "योजनाको स्तर",
    ],
    "project-proposed-type": [
        ProjectProposedType,
        common_table_heads,
        common_table_fields,
        "परियोजना प्रस्तावित प्रकार",
    ],
    "project-activity": [
        ProjectActivity,
        common_display_head,
        common_head,
        "योजना किर्यकलाप",
    ],
    "purchase-type": [
        PurchaseType,
        common_display_head,
        common_head,
        "खरिद प्रकार",
    ],
    "priority-type": [
        PriorityType,
        common_display_head,
        common_head,
        "प्राथमिकताको प्रकार",
    ],
    "selection-feasibility": [
        SelectionFeasibility,
        common_display_head,
        common_head,
        "योजना छनौट आधार",
    ],
    "strategic-sign": [
        StrategicSign,
        strategic_sign_display_head,
        strategic_sign_head,
        "रणनैतिक संकेत",
    ],
    "program": [
        Program,
        program_display_head,
        program_head,
        "कार्यक्रम",
    ],
    "units": [Unit, unit_display_head, unit_head, "इकाईको प्रकार"],
    "target-group": [
        TargetGroup,
        target_group_heads,
        target_group_fields,
        "लक्षित समूह",
    ],
    "project-status": [
        ProjectStatus,
        common_display_head,
        common_head,
        "योजनाको अवस्था",
    ],
    "contract-type": [
        ContractorType,
        contractor_type_display_head,
        contractor_type_head,
        "ठेकदारको प्रकार",
    ],
    "subject-area": [
        SubjectArea,
        subject_area_display_head,
        subject_area_head,
        "विषयगत कार्यक्षेत्र",
    ],
    "organization-type": [
        OrganizationType,
        common_display_head,
        common_head,
        "सस्था प्रकार",
    ],
    "office": [Office, display_office_head, office_head, "कार्यालय"],  # TODO:
    "organization": [
        Organization,
        display_organization_head,
        organization_head,
        "फर्म / संस्था",
    ],  # TODO:
    "currency": [Currency, common_table_heads, common_table_fields, "मुद्राको नाम "],
    # "module": [Module, common_table_heads, common_table_fields, ""],
    "sub-module": [
        SubModule,
        common_table_heads_parent,
        common_table_fields_parent,
        "सहायक मोड्युल",
    ],
    "news-paper": [
        NewsPaper,
        display_newspaper_source_head,
        newspaper_source_head,
        "पत्र-पत्रिका विवरण",
    ],  # TODO
    "project-start-decision": [
        ProjectStartDecision,
        common_display_head,
        common_head,
        "योजना संचालन निर्णय",
    ],
    "construction-material-description": [
        ConstructionMaterialDescription,
        common_table_heads,
        common_table_fields,
        "निर्माण सामग्रीको विवरण",
    ],
    "budget-sub-title": [
        BudgetSubTitle,
        common_display_budget_head,
        common_budget_head,
        "बजेट उपशीर्षक",
    ],
    "payment-method": [
        PaymentMethod,
        common_display_budget_head,
        common_budget_head,
        "भुक्तानी विधि",
    ],
    "source-receipt": [
        SourceReceipt,
        common_display_budget_head,
        common_budget_head,
        "प्राप्तिको स्रोत",
    ],
    "collect-payment": [
        CollectPayment,
        common_display_budget_head,
        common_budget_head,
        "भुक्तानी माध्यम",
    ],
    "sub-ledger": [
        SubLedger,
        common_display_budget_head,
        common_budget_head,
        "सहायक लेजर",
    ],
    "atm": [
        AccountTitleManagement,
        atm_display_head,
        atm_head,
        "लेखा शीर्षक व्यवस्थापन",
    ],  # TODO
    "budget-source": [
        BudgetSource,
        display_budget_source_head,
        budget_source_head,
        "बजेट स्रोत",
    ],  # TODO
    "sbe-type": [
        SourceBearerEntityType,
        sbe_type_display_head,
        sbe_type_head,
        "स्रोत व्यहोर्ने निकायको प्रकार",
    ],
    # "payment-medium": [PaymentMedium, common_table_heads, common_table_fields, ""],
    "bank-type": [
        BankType,
        bank_type_display_head,
        bank_type_head,
        "बैंक तथा वित्तिय संस्थाको प्रकार",
    ],
    # "cheque-format": [ChequeFormat, common_table_heads, common_table_fields, ""],
    "bfi": [
        BFI,
        display_bfi_head,
        bfi_head,
        "बैंक तथा वित्तिय संस्थाको नामावली",
    ],  # TODO
    "bank-account": [
        BankAccount,
        display_bank_account_head,
        bank_account_head,
        "बैंक तथा वित्तिय संस्थाको खाता",
    ],  # TODO
    "member-type": [
        MemberType,
        common_display_head,
        common_head,
        "सदस्यताको प्रकार",
    ],
    "consumer-committee": [
        ConsumerCommittee,
        consumer_committee_display_head,
        consumer_committee_head,
        "उपभोक्ता समितिको नामावली ",
    ],
    "executive-agency": [
        ExecutiveAgency,
        common_table_heads,
        common_table_fields,
        "कार्यान्वयन गर्ने निकाय विवरण",
    ],
    "standing-list-type": [
        StandingListType,
        standing_list_type_display_head,
        standing_list_type_head,
        "सुचिकृतको प्रकार",
    ],
    "standing-list": [
        StandingList,
        standing_list_display_head,
        standing_list_head,
        "सुचिकृतको विवरण",
    ],
    "road-status": [RoadStatus, road_display_head, road_only_head, "सडकको स्थिति"],
    "road-type": [RoadType, road_display_head, road_only_head, "सडकको प्रकार"],
    "drainage_type": [
        DrainageType,
        road_display_head,
        road_only_head,
        "ढल निकासको किसिम",
    ],
    "road": [
        Road,
        display_road_head,
        road_head,
        "सडकको नामावली बिबरण",
    ],  # TODO
    "sbe": [
        SourceBearerEntity,
        display_sbe_head,
        sbe_head,
        "स्रोत व्यहोर्ने निकाय",
    ],  # TODO
    "project-work-type": [
        ProjectWorkType,
        extra_type_display_head,
        extra_type_head,
        "काम/योजनाको प्रकार",
    ],
    "project-work": [
        WorkProject,
        common_table_heads,
        common_table_fields,
        "काम योजना/कार्यक्रम ",
    ],
    "project-work-local-level": [
        WorkProject,
        local_display_head,
        local_head,
        "काम योजना/कार्यक्रम (न.पा./गा.पा.)",
    ],
    "project-work-ward": [
        WorkProject,
        ward_display_head,
        ward_head,
        "काम योजना/कार्यक्रम (वडा स्तरिय)",
    ],
    "project-work-priority": [
        WorkProject,
        ward_display_head,
        ward_head,
        "काम योजना/कार्यक्रम (प्राथमिकीकरण)",
    ],
    "project-work-shortlist": [
        WorkProject,
        ward_display_head,
        ward_head,
        "काम/योजना/कार्यक्रम (सुचिकृत/ShortList)",
    ],
    "project-work-approved": [
        WorkProject,
        ward_display_head,
        ward_head,
        "काम/योजना/कार्यक्रम (स्वीकृत गर्ने)",
    ],
    # "project-document": [
    #     ProjectDocument,
    #     common_table_heads,
    #     common_table_fields,
    #     "काम/योजनाको प्रकार",
    # ],
    "expense-budget-ward-range-determine": [
        ExpenseBudgetRangeDetermine,
        expense_budget_ward_display_head,
        expense_budget_ward_head,
        "व्यय बजेट सिमा निर्धारण (वडा)",
    ],
    "expense-budget-range-determine": [
        ExpenseBudgetRangeDetermine,
        expense_budget_display_head,
        expense_budget_head,
        "व्यय बजेट सिमा निर्धारण",
    ],
    "income-budget-range-determine": [
        IncomeBudgetRangeDetermine,
        income_budget_display_head,
        income_budget_head,
        "आय बजेट सिमा निर्धारण",
    ],
    "efa": [
        EstimateFinancialArrangements,
        efa_display_head,
        efa_head,
        "वित्तीय व्यवस्था अनुमान",
    ],
    "financial-years": [
        FinancialYear,
        financial_year_display_head,
        financial_year_head,
        "आर्थिक वर्ष",
    ],
    "employee-detail": [
        Employee,
        employee_display_head,
        employee_head,
        "कर्मचारी विवरण",
    ],
    "department": [
        Department,
        common_table_heads,
        common_table_fields,
        "शाखा/विभाग",
    ],
    "position": [
        Position,
        common_display_head,
        common_head,
        "पदको प्रकार",
    ],
    "position-level": [
        PositionLevel,
        common_table_heads,
        common_table_fields,
        "पद श्रेणी विवरण",
    ],
    "employee-sector": [
        EmployeeSector,
        common_table_heads,
        common_table_fields,
        "पद",
    ],
    "employee-type": [
        EmployeeType,
        common_table_heads,
        common_table_fields,
        "कर्मचारीको किसिम विवरण",
    ],
    "public-representative-position": [
        PublicRepresentativePosition,
        extra_type_display_head,
        extra_type_head,
        "जनप्रतिनिधीको पद",
    ],
    "public-representative-detail": [
        PublicRepresentativeDetail,
        public_detail_display_head,
        public_detail_head,
        "जनप्रतिनिधिको विवरण",
    ],
    "project-physical-description": [
        ProjectPhysicalDescription,
        project_physical_display_head,
        project_physical_head,
        "योजनाको संक्ष्क्षिप्त भौतिक विवरण",
    ],
    "project-unit-detail": [
        ProjectUnitDetail,
        project_unit_display_head,
        project_unit_head,
        "योजनाको ईकाई विवरण",
    ],
    "budget-allocation": [
        BudgetAllocationDetail,
        budget_allocation_display_head,
        budget_allocation_head,
        "स्रोत ब्यहोर्ने निकायहरु",
    ],
    "benefited-detail": [
        BenefitedDetail,
        benefited_detail_display_head,
        benefited_detail_head,
        "लाभान्वितको विवरण",
    ],
    "project-work-document": [
        ProjectDocument,
        project_work_document_display_head,
        project_work_document_head,
        "योजना कामको कागजात",
    ],
    "budget-ammend": [
        BudgetAmmendment,
        budget_ammend_display_head,
        budget_ammend_head,
        "बजेट संसोधनको विवरण",
    ],
    "budget-transfer": [
        BudgetTransfer,
        budget_transfer_display_head,
        budget_transfer_head,
        "बजेट रकमान्तर",
    ],
    "project-execution": [
        ProjectExecution,
        project_execution_display_head,
        project_execution_head,
        "योजनाको विवरण प्रविष्टी",
    ],
    "template-field-mapping": [
        TemplateFieldMapping,
        template_field_mapping_display_head,
        template_field_mapping_head,
        "Custom Report Fields Mapping",
    ],
    "project-bid-collection": [
        ProjectBidCollection,
        project_bid_collection_display_head,
        project_bid_collection_head,
        "बोलपत्र सङ्कलन",
    ],
}


def get_export_model(request_model):
    return export_models.get(request_model, None)


class GenderViewSet(ModelViewSet):
    serializer_class = GenderSerializer
    queryset = Gender.objects.all()


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class ContactDetailViewSet(ModelViewSet):
    serializer_class = ContactDetailSerializer
    queryset = ContactDetail.objects.all()


class ContactPersonViewSet(ModelViewSet):
    serializer_class = ContactPersonSerializer
    queryset = ContactPerson.objects.all()


class PdfView(APIView):
    template_name = "pdf.html"

    def get(self, request, *args, **kwargs):
        company_name = self.request.user
        try:
            request_type = self.request.query_params.get("request_type")
            if not request_type:
                return Response(
                    {"error": "Request type is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            model_name = get_export_model(request_type)
            if model_name is not None:
                data = model_name[0].objects.all()
                # print(model_name[0].__dict__)
                context = {
                    "headers": model_name[1],
                    "actual_heads": model_name[2],
                    "title": model_name[3],
                    "date": nepali_datetime.date.today().strftime("%K-%n-%D"),
                    "data": data,
                    "company_name": request.user.assigned_municipality.office_name,
                    "company_sub_name": request.user.assigned_municipality.sub_name,
                    "company_address": request.user.assigned_municipality.office_address,
                    "email": request.user.assigned_municipality.email,
                    "phone": request.user.assigned_municipality.phone,
                }
                print(len(model_name[1]) > 10)
                return render_to_pdf(
                    request=request,
                    template=self.template_name,
                    context=context,
                    landscape=len(model_name[1]) > 10,
                )
            else:
                return Response(
                    {
                        "error": "Request type is not found, please provide available type"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            raise e


class ExcelViewOld(APIView):
    def get(self, request, *args, **kwargs):
        try:
            request_type = self.request.query_params.get("request_type")
            print(request_type)
            if not request_type:
                return Response(
                    {"error": "Request type is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            model_name = get_export_model(request_type)
            print(model_name)
            if model_name is not None:
                data = model_name[0].objects.all()
                print(data, 8989)
                context = {
                    "headers": model_name[1],
                    "actual_heads": model_name[2],
                    "title": model_name[3],
                    "date": datetime.now().date(),
                    "data": data,
                    "company_name": request.user.assigned_municipality.office_name,
                    "company_sub_name": request.user.assigned_municipality.sub_name,
                    "company_address": request.user.assigned_municipality.office_address,
                    "email": request.user.assigned_municipality.email,
                    "phone": request.user.assigned_municipality.phone,
                    "column_widths": [15, 40, 40, 40],
                }
                response = export_to_excel_old(context)
                return response
        except Exception as e:
            print(f"Error exporting excel data: {e}")
            return Response(
                {"error": "Error to generate document"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ExcelView(APIView):
    def get(self, request: HttpRequest, *args, **kwargs):
        pass


class CsvView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            request_type = self.request.query_params.get("request_type")
            print(request_type)
            if not request_type:
                return Response(
                    {"error": "Request type is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            model_name = get_export_model(request_type)
            if model_name is not None:
                data = model_name[0].objects.all()
                context = {
                    "headers": model_name[1],
                    "actual_heads": model_name[2],
                    "title": model_name[3],
                    "date": datetime.now().date(),
                    "data": data,
                    "company_name": request.user.assigned_municipality.office_name,
                    "company_sub_name": request.user.assigned_municipality.sub_name,
                    "company_address": request.user.assigned_municipality.office_address,
                    "email": request.user.assigned_municipality.email,
                    "phone": request.user.assigned_municipality.phone,
                    # "column_widths": [15, 40, 40, 40],
                }
                response = export_to_csv(context)
                return response
                # file_path, file_url, file_name = export_to_csv(context)
                # context_data = {"path": file_url}
                # return Response(context_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error exporting excel data: {e}")
            return Response(
                {"error": "Error to generate document"},
                status=status.HTTP_400_BAD_REQUEST,
            )
