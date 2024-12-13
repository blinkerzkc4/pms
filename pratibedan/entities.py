"""
-- Created by Bikash Saud
-- Created on 2023-07-27
"""
from typing import List

from pydantic import BaseModel


class MunicipalityData(BaseModel):
    id: str = ""
    name: str = ""
    name_unicode: str = ""
    name_eng: str = ""
    number_of_wards: str = ""
    remarks: str = ""
    email: str = ""
    phone: str = ""
    success: bool = False
    msg: str = ""


class DistrictData(BaseModel):
    id: str = ""
    name: str = ""
    name_eng: str = ""
    name_unicode: str = ""
    municipalities: list[MunicipalityData] = None
    success: bool = False
    msg: str = ""


class ProvinceData(BaseModel):
    districts: list[DistrictData] = None
    id: str = ""
    province_number: str = ""
    name: str = ""
    name_unicode: str = ""
    name_eng: str = ""
    remarks: str = ""
    success: bool = False
    msg: str = ""


class AddressData(BaseModel):
    id: str = ""
    municipality: MunicipalityData = None
    ward: str = ""
    ward_eng: str = ""
    house_no: str = ""
    tole: str = ""
    tole_eng: str = ""
    road_name: str = ""
    road_name_eng: str = ""
    success: bool = False
    msg: str = ""


class ProjectDataResponse(BaseModel):
    id: str = ""
    code: str = ""
    name: str = ""
    name_eng: str = ""
    financial_year: str = ""
    ward: str = ""
    address: AddressData = None
    project_type: str = None
    project_nature: str = None
    work_class: str = None
    subject_area: str = None
    strategic_sign: str = None
    work_proposer_type: str = None
    program: str = None
    project_priority: str = None
    start_pms_process: str = None
    plan_start_decision: str = None
    project_level: str = None
    first_trimester: str = ""
    second_trimester: str = ""
    third_trimester: str = ""
    fourth_trimester: str = ""
    is_multi_year_plan: str = False
    first_year: str = ""
    second_year: str = ""
    third_year: str = ""
    forth_year: str = ""
    fifth_year: str = ""
    other: str = None
    latitude: str = 0
    longitude: str = 0
    appropriated_amount: str = 0
    overhead: str = 0
    contingency: str = 0
    mu_aa_ka: str = 0
    public_charity: str = 0
    maintenance: str = 0
    disaster_mgmt_fund: str = 0
    total_estimate: str = 0
    self_payment: str = None
    is_executing: str = False
    success: bool = True
    msg: str = None


class ReportByProjectType(BaseModel):
    project_type: str = ""
    project_unit_name: str = ""
    completed_projects: int = 0
    not_completed_projects: int = 0
    success: bool = True
    msg: str = ""


class ProjectBudgetAllocationData(BaseModel):
    id: str = None
    budget_sub_title: str = ""  # common modes
    expense_title: str = ""  # AccountTitleManagement
    budget_source: str = ""
    source_receipt: str = ""
    expense_method: str = ""
    first_quarter: str = ""
    second_quarter: str = ""
    third_quarter: str = ""
    fourth_quarter: str = ""
    total: str = ""
    multi_year_budget: str = ""
    is_revise_budget: str = ""
    success: bool = True
    msg: str = ""


class ProjectAgreementData(BaseModel):
    id: str = None
    contractor_invoiced_date: str = ""
    contractor_invoiced_date_eng: str = ""
    contractor_invoiced_no: str = ""
    contractor_remarks_1: str = ""
    contractor_remarks_2: str = ""
    required_bail_amount: str = ""
    required_performance_bond_amount: str = ""
    required_bail_date: str = ""
    required_bail_date_eng: str = ""
    # firm_name: str = ""
    # firm_address: str = ""
    # firm_contact_no: str = ""
    # grand_father_name: str = ""
    # father_name: str = ""
    # contracting_party_name: str = ""
    # age: str = ""
    # address: str = ""
    contract_date: str = ""
    contract_date_eng: str = ""
    work_finished_date: str = ""
    work_finished_date_eng: str = ""
    exist_bail_amount: str = ""
    exist_performance_bond_amount: str = ""
    exist_bail_date: str = ""
    exist_bail_date_eng: str = ""
    # bank: str = ""
    # exist_bank_guarantee_no: str = ""
    # end_date: str = ""
    # end_date_eng: str = ""
    contractors_witness: str = ""
    cw_position: str = ""
    office_witness_1: str = ""
    office_witness_1_position: str = ""
    office_witness_2: str = ""
    office_witness_2_position: str = ""
    office_witness_3: str = ""
    office_witness_3_position: str = ""
    office_witness_4: str = ""
    office_witness_4_position: str = ""
    mandate_invoice_date: str = ""
    mandate_invoice_date_eng: str = ""
    mandate_invoice_no: str = ""
    pa_sa: str = ""
    remark_1: str = ""
    remark_2: str = ""
    remark_3: str = ""
    remark_4: str = ""
    officer_name: str = ""
    officer_position: str = ""
    success: bool = True
    msg: str = ""


class DepositMandateData(BaseModel):
    id: str = None
    mandate_type: str = ""
    order_by: str = ""
    order_by_position: str = ""
    order_date: str = ""  #
    order_date_eng: str = ""  #
    nominated_employee: str = ""
    nominated_employee_position: str = ""
    invoice_date: str = ""
    invoice_date_eng: str = ""
    invoice_no: str = ""
    latter_no: str = ""
    work_complete_date: str = ""
    work_complete_date_eng: str = ""
    report_custom_print: str = ""
    opinion: str = ""
    success: bool = True
    msg: str = ""


class UserCommitteeData(BaseModel):
    id: str = None
    code: str = ""
    status: str = ""
    bank_address: str = ""
    ward_no: str = ""
    formation_date_bs: str = ""
    formation_date_eng: str = ""
    attended_no: str = ""
    witness_no: str = ""
    full_name: str = ""
    full_name_eng: str = ""
    registration_no: str = ""
    registration_date_bs: str = ""
    registration_date_eng: str = ""
    office: str = ""
    other_detail: str = ""
    bank: str = ""
    bank_account_no: str = ""
    member_type: str = ""
    current_address: str = ""
    former_address: str = ""
    contact_detail: str = ""
    contact_person: str = ""
    remarks: str = ""
    display_order: str = ""
    success: bool = True
    msg: str = ""


class UserCommitteeFormData(BaseModel):
    id: str = None
    first_time_publish: str = ""
    first_time_publish_eng: str = ""
    form_amount: str = ""
    consumer_committee: UserCommitteeData = None
    code: str = ""
    chairman: str = ""
    address: str = ""
    established_date: str = ""
    phone: str = ""
    report_date: str = ""
    report_date_eng: str = ""
    invoice_no: str = ""
    project_current_status: str = ""
    previous_work: str = ""
    detail_from_office_date: str = ""
    detail_from_office_date_eng: str = ""
    office_lecture: str = ""
    emp_name: str = ""
    position: str = ""
    opinion: str = ""
    positive_effect: str = ""
    other: str = ""
    project_related_other: str = ""
    success: bool = True
    msg: str = ""


class InstallmentDetailData(BaseModel):
    id: str = ""
    installment: str = ""
    date: str = ""
    date_eng: str = ""
    amount: str = ""
    percent: str = ""
    remark: str = ""
    success: bool = False
    msg: str = ""


class OpenContractAccountData(BaseModel):
    id: str = ""
    project: str = ""
    cha_no: str = ""
    pa_no: str = ""
    date: str = ""
    date_eng: str = ""
    bank_name: str = ""  # FK
    account_no: str = ""
    bank_branch: str = ""
    bodarth: str = ""
    contract_ch_no: str = ""
    contract_date: str = ""
    contract_pa_no: str = ""
    bodarth_1: str = ""
    bodarth_2: str = ""
    day: str = ""
    contract_account_no: str = ""
    print_custom_report: str = ""
    project_contract_date: str = ""
    project_contract_date_eng: str = ""
    project_contract_start_date: str = ""
    project_contract_start_date_eng: str = ""
    project_completion_date: str = ""
    project_completion_date_eng: str = ""
    contract_no: str = ""
    present_benefit: str = ""
    absent_benefit: str = ""
    project_start_experience: str = ""
    other_experience: str = ""
    arrangements_for_taking_care_of_repairs: str = ""
    repairs_by_company: str = ""
    committee_witness: str = ""
    user_committee_secretary: str = ""
    office_side_1: str = ""
    office_side_1_position: str = ""
    office_side_2: str = ""
    office_side_2_position: str = ""
    office_side_3: str = ""
    office_side_3_position: str = ""
    office_side_4: str = ""
    office_side_4_position: str = ""
    mandate_ch_no: str = ""
    mandate_date: str = ""
    mandate_date_eng: str = ""
    mandate_pa_no: str = ""
    mandate_bodarth: str = ""
    mandate_employee: str = ""
    mandate_employee_position: str = ""
    ward_no: str = ""
    installment_detail: list[InstallmentDetailData] = None
    building_material: str = ""  # FK
    maintenance_arrangement: str = ""  # FK
    success: bool = False
    msg: str = ""


class ProjectFinishedBailReturnData(BaseModel):
    id: str = None
    comment_no: str = ""
    date: str = ""
    date_eng: str = ""
    executive_decision: str = ""
    approved_by: str = ""
    print_custom_report: str = ""
    success: bool = True
    msg: str = ""


class ProjectBenefitedDetailData(BaseModel):
    id: str = ""
    target_group: str = ""
    total_house_number: str = ""
    total_man: str = ""
    total_women: str = ""
    total_other: str = ""
    total_population: str = ""
    remark: str = ""
    success: bool = False
    msg: str = ""


class ProjectReport(BaseModel):
    project_id: str = ""
    project_detail: ProjectDataResponse = None
    project_budget: ProjectBudgetAllocationData = None
    project_agreement: ProjectAgreementData = None
    project_mandate: DepositMandateData = None
    user_committee_form_data: UserCommitteeFormData = None
    project_finish_data: ProjectFinishedBailReturnData = None
    project_status: str = ""
    success: bool = True
    msg: str = ""


class ProjectReportBySubjectArea(BaseModel):
    project_id: str = ""
    project_detail: ProjectDataResponse = None
    project_agreement: ProjectAgreementData = None
    project_finish_data: ProjectFinishedBailReturnData = None
    project_benefited_data: ProjectFinishedBailReturnData = None
    project_status: str = ""
    success: bool = True
    msg: str = ""


class ProjectReportByAgreement(BaseModel):
    project_id: str = ""
    project_detail: ProjectDataResponse = None
    project_agreement: ProjectAgreementData = None
    project_finish_data: ProjectFinishedBailReturnData = None
    user_committee_form_data: ProjectFinishedBailReturnData = None
    project_status: str = ""
    success: bool = True
    msg: str = ""


class ProjectReportByPaymentDetail(BaseModel):
    project_id: str = ""
    project_detail: ProjectDataResponse = None
    project_agreement: ProjectAgreementData = None
    project_finish_data: ProjectFinishedBailReturnData = None
    open_contract_account_data: OpenContractAccountData = None
    project_status: str = ""
    success: bool = True
    msg: str = ""
