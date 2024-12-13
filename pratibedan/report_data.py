"""
-- Created by Bikash Saud
-- Created on 2023-07-27
"""
import logging
from pprint import pprint

from base_model.models import Address
from plan_execution.models import (
    BenefitedDetail,
    BudgetAllocationDetail,
    ConsumerFormulation,
    DepositMandate,
    InstallmentDetail,
    OpeningContractAccount,
    ProjectAgreement,
    ProjectExecution,
    ProjectFinishedBailReturn,
)
from pratibedan.entities import (
    AddressData,
    DepositMandateData,
    DistrictData,
    InstallmentDetailData,
    MunicipalityData,
    OpenContractAccountData,
    ProjectAgreementData,
    ProjectBenefitedDetailData,
    ProjectBudgetAllocationData,
    ProjectDataResponse,
    ProjectFinishedBailReturnData,
    ProjectReport,
    ProjectReportByAgreement,
    ProjectReportByPaymentDetail,
    ProjectReportBySubjectArea,
    ProvinceData,
    UserCommitteeData,
    UserCommitteeFormData,
)
from project.models import District, Municipality, Province
from project_planning.models import ConsumerCommittee


class ReportData:
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("project execution")
        self.__project_data_response = ProjectDataResponse()

    def get_common_model_data(self, data):
        self.logger.info("Getting common fields data")
        if data is None:
            return {}
        return {
            "id": data.id if data.id else "",
            "code": data.code,
            "name": data.name,
            "name_eng": data.name_eng,
        }

    def get_fy_data(self, data):
        self.logger.info("Getting FY data")
        if data is None:
            return {}
        return {
            "id": data.id if data.id else "",
            "start_year": data.start_year,
            "end_year": data.end_year,
            "fy": data.fy,
        }

    def get_municipality_data(self, municipality):
        municipality_data = MunicipalityData()
        try:
            municipality = Municipality.objects.filter(id=municipality.id).first()
            if municipality:
                municipality_data.id = municipality.id
                municipality_data.name = municipality.name
                municipality_data.name_unicode = municipality.name_unicode
                municipality_data.name_eng = municipality.name_eng
                municipality_data.number_of_wards = municipality.number_of_wards
                municipality_data.remarks = municipality.remarks
                municipality_data.email = municipality.email
                municipality_data.phone = municipality.phone
            return municipality_data
        except Exception as e:
            self.logger.exception(f"Exception: {e}")
            return None

    def get_district_data(self, district):
        district_data = DistrictData()
        try:
            distrct = District.objects.filter(id=district.id).first()
            if district:
                district_data.id = district.id
                district_data.name = district.name
                district_data.name_unicode = district.name_unicode
                district_data.name_eng = district.name_eng
                district_data.municipalities = [
                    self.get_municipality_data(municipality)
                    for municipality in district.municipality_set.all()
                ]
            return district_data
        except Exception as e:
            self.logger.exception(f"Exception: {e}")
            return None

    def get_province_data(self, data):
        province_data = ProvinceData()
        try:
            self.logger.info("Get Province data")
            province = Province.objects.filter(id=data.id).first()
            if province:
                province_data.id = province.id
                province_data.name = province.name
                province_data.name_unicode = province.name_unicode
                province_data.province_number = province.province_number
                province_data.name_eng = province.name_eng
                province_data.districts = [
                    self.get_district_data(district)
                    for district in data.district_set.all()
                ]
            return province_data
        except Exception as e:
            self.logger.exception(f"Exception: {e}")
            return None

    def get_address_data(self, data):
        address_data = AddressData()
        if data is None:
            return address_data
        try:
            self.logger.info(f"Get Address: {data} ")
            address = Address.objects.filter(id=data.id).first()
            if address is None:
                return None
            address_data.id = address.id
            address_data.municipality = (
                self.get_municipality_data(address.municipality)
                if address.municipality
                else None
            )
            address_data.ward = address.ward
            address_data.ward_eng = address.ward_eng
            address_data.house_no = address.house_no
            address_data.tole = address.tole
            address_data.tole_eng = address.tole_eng
            address_data.road_name = address.road_name
            address_data.road_name_eng = address.road_name_eng
            return address_data
        except Exception as e:
            self.logger.exception(f"Exception to get address data: {e}")
            return None

    def get_project_data(self, data):
        try:
            self.logger.info("Get Project data")
            self.__project_data_response.id = data.id
            self.__project_data_response.code = data.code
            self.__project_data_response.name = data.name
            self.__project_data_response.name_eng = data.name_eng
            self.__project_data_response.financial_year = self.get_fy_data(
                data.financial_year
            )
            self.__project_data_response.ward = data.ward
            self.__project_data_response.address = (
                self.get_address_data(data.address) if data.address else None
            )
            self.__project_data_response.project_type = (
                self.get_common_model_data(data.project_type)
                if data.project_type
                else data.project_type
            )
            self.__project_data_response.project_nature = (
                self.get_common_model_data(data.project_nature)
                if data.project_nature
                else data.project_nature
            )
            self.__project_data_response.work_class = (
                self.get_common_model_data(data.work_class)
                if data.work_class
                else data.work_class
            )
            self.__project_data_response.subject_area = (
                self.get_common_model_data(data.subject_area)
                if data.subject_area
                else data.subject_area
            )
            self.__project_data_response.strategic_sign = (
                self.get_common_model_data(data.strategic_sign)
                if data.strategic_sign
                else data.strategic_sign
            )
            self.__project_data_response.work_proposer_type = data.work_proposer_type
            self.__project_data_response.program = (
                self.get_common_model_data(data.program) if data.program else None
            )
            self.__project_data_response.project_priority = (
                self.get_common_model_data(data.project_priority)
                if data.project_priority
                else None
            )
            self.__project_data_response.start_pms_process = (
                self.get_common_model_data(data.start_pms_process)
                if data.start_pms_process
                else None
            )
            self.__project_data_response.plan_start_decision = (
                self.get_common_model_data(data.plan_start_decision)
                if data.plan_start_decision
                else None
            )
            self.__project_data_response.project_level = (
                self.get_common_model_data(data.project_level)
                if data.project_level
                else None
            )
            self.__project_data_response.third_trimester = data.first_trimester
            self.__project_data_response.fourth_trimester = data.second_trimester
            self.__project_data_response.is_multi_year_plan = data.third_trimester
            self.__project_data_response.first_year = data.fourth_trimester
            self.__project_data_response.second_year = data.is_multi_year_plan
            self.__project_data_response.third_year = data.first_year
            self.__project_data_response.forth_year = data.second_year
            self.__project_data_response.fifth_year = data.third_year
            self.__project_data_response.other = data.forth_year
            self.__project_data_response.latitude = data.fifth_year
            self.__project_data_response.longitude = data.other
            self.__project_data_response.appropriated_amount = data.latitude
            self.__project_data_response.overhead = data.longitude
            self.__project_data_response.contingency = data.appropriated_amount
            self.__project_data_response.mu_aa_ka = data.overhead
            self.__project_data_response.public_charity = data.contingency
            self.__project_data_response.maintenance = data.mu_aa_ka
            self.__project_data_response.disaster_mgmt_fund = data.public_charity
            self.__project_data_response.total_estimate = data.maintenance
            self.__project_data_response.self_payment = data.disaster_mgmt_fund
            self.__project_data_response.is_executing = data.total_estimate
            return self.__project_data_response
        except Exception as e:
            self.logger.exception(f"Exception: {e}")
            self.__project_data_response.success = False
            self.__project_data_response.msg = "Error while gathering data."
            return self.__project_data_response

    def get_project_budget_data(self, data):
        budget_report = ProjectBudgetAllocationData()
        try:
            self.logger.info("Get project Budget data: ")
            project_id = data.id
            budget_data = BudgetAllocationDetail.objects.filter(project=data).first()
            if budget_data:
                budget_report.id = budget_data.id
                budget_report.budget_sub_title = (
                    budget_data.budget_sub_title.name
                    if budget_data.budget_sub_title
                    else None
                )
                budget_report.expense_title = (
                    budget_data.expense_title.display_name
                    if budget_data.expense_title
                    else None
                )
                budget_report.budget_source = (
                    budget_data.budget_source.name
                    if budget_data.budget_source
                    else None
                )
                budget_report.source_receipt = (
                    budget_data.source_receipt.name
                    if budget_data.source_receipt
                    else None
                )
                budget_report.expense_method = (
                    budget_data.expense_method.name
                    if budget_data.expense_method
                    else None
                )
                budget_report.first_quarter = budget_data.first_quarter
                budget_report.second_quarter = budget_data.second_quarter
                budget_report.third_quarter = budget_data.third_quarter
                budget_report.fourth_quarter = budget_data.fourth_quarter
                budget_report.total = budget_data.total
                budget_report.multi_year_budget = budget_data.multi_year_budget
                budget_report.is_revise_budget = budget_data.is_revise_budget
            return budget_report
        except Exception as e:
            self.logger.exception(f"Exception while getting project report: {e}")
            budget_report.success = False
            budget_report.msg = "Error while get data."
            return budget_report

    def get_project_agreement_data(self, data):
        project_agreement_data = ProjectAgreementData()
        try:
            project_agreement = ProjectAgreement.objects.filter(project=data).first()
            if project_agreement:
                project_agreement_data.id = project_agreement.id
                project_agreement_data.contractor_invoiced_date = (
                    project_agreement.contractor_invoiced_date
                )
                project_agreement_data.contractor_invoiced_date_eng = (
                    project_agreement.contractor_invoiced_date_eng
                )
                project_agreement_data.contractor_invoiced_no = (
                    project_agreement.contractor_invoiced_no
                )
                project_agreement_data.contractor_remarks_1 = (
                    project_agreement.contractor_remarks_1
                )
                project_agreement_data.contractor_remarks_2 = (
                    project_agreement.contractor_remarks_2
                )
                project_agreement_data.required_bail_amount = (
                    project_agreement.required_bail_amount
                )
                project_agreement_data.required_performance_bond_amount = (
                    project_agreement.required_performance_bond_amount
                )
                project_agreement_data.required_bail_date = (
                    project_agreement.required_bail_date
                )
                project_agreement_data.required_bail_date_eng = (
                    project_agreement.required_bail_date_eng
                )
                #
                project_agreement_data.contract_date = project_agreement.contract_date
                project_agreement_data.contract_date_eng = (
                    project_agreement.contract_date_eng
                )
                project_agreement_data.work_finished_date = (
                    project_agreement.work_finished_date
                )
                project_agreement_data.work_finished_date_eng = (
                    project_agreement.work_finished_date_eng
                )
                project_agreement_data.exist_bail_amount = (
                    project_agreement.exist_bail_amount
                )
                project_agreement_data.exist_performance_bond_amount = (
                    project_agreement.exist_performance_bond_amount
                )
                project_agreement_data.exist_bail_date = (
                    project_agreement.exist_bail_date
                )
                project_agreement_data.exist_bail_date_eng = (
                    project_agreement.exist_bail_date_eng
                )
                #
                # project_agreement_data.contractors_witness = project_agreement.contractors_witness
                # project_agreement_data.cw_position = project_agreement.cw_position
                # project_agreement_data.office_witness_1 = project_agreement.office_witness_1
                # project_agreement_data.office_witness_1_position = project_agreement.office_witness_1_position
                # project_agreement_data.office_witness_2 = project_agreement.office_witness_2
                # project_agreement_data.office_witness_2_position = project_agreement.office_witness_2_position
                # project_agreement_data.office_witness_3 = project_agreement.office_witness_3
                # project_agreement_data.office_witness_3_position = project_agreement.office_witness_3_position
                # project_agreement_data.office_witness_4 = project_agreement.office_witness_4
                # project_agreement_data.office_witness_4_position = project_agreement.office_witness_4_position
                project_agreement_data.mandate_invoice_date = (
                    project_agreement.mandate_invoice_date
                )
                project_agreement_data.mandate_invoice_date_eng = (
                    project_agreement.mandate_invoice_date_eng
                )
                project_agreement_data.mandate_invoice_no = (
                    project_agreement.mandate_invoice_no
                )
                project_agreement_data.pa_sa = project_agreement.pa_sa
                project_agreement_data.remark_1 = project_agreement.remark_1
                project_agreement_data.remark_2 = project_agreement.remark_2
                project_agreement_data.remark_3 = project_agreement.remark_3
                project_agreement_data.remark_4 = project_agreement.remark_4
                # project_agreement_data.officer_name = project_agreement.officer_name
                # project_agreement_data.officer_position = project_agreement.officer_position
            return project_agreement_data
        except Exception as e:
            print(f"Exception in get_project_agreement_data: {e}")
            project_agreement_data.success = False
            project_agreement_data.msg = "Error while getting data"
            return project_agreement_data

    def get_project_mandate_data(self, data):
        mandate_data = DepositMandateData()
        try:
            project_id = data.id
            project_mandate = DepositMandate.objects.filter(project=data).first()
            if project_mandate:
                mandate_data.id = project_mandate.id
                mandate_data.mandate_type = project_mandate.mandate_type
                # mandate_data.order_by = project_mandate.order_by
                # mandate_data.order_by_position = project_mandate.order_by_position
                mandate_data.order_date = project_mandate.order_date
                mandate_data.order_date_eng = project_mandate.order_date_eng
                # mandate_data.nominated_employee = project_mandate.nominated_employee
                # mandate_data.nominated_employee_position = project_mandate.nominated_employee_position
                mandate_data.invoice_date = project_mandate.invoice_date
                mandate_data.invoice_date_eng = project_mandate.invoice_date_eng
                mandate_data.invoice_no = project_mandate.invoice_no
                mandate_data.latter_no = project_mandate.latter_no
                mandate_data.work_complete_date = project_mandate.work_complete_date
                mandate_data.work_complete_date_eng = (
                    project_mandate.work_complete_date_eng
                )
                mandate_data.report_custom_print = project_mandate.report_custom_print
                mandate_data.opinion = project_mandate.opinion
            return mandate_data
        except Exception as e:
            print(f"Exception in get_project_mandate_data: {e}")
            mandate_data.success = False
            mandate_data.msg = "Error while getting data"
            return mandate_data

    def get_user_committee(self, data):
        user_committee_data = UserCommitteeData()
        try:
            if data is not None:
                user_committee = ConsumerCommittee.objects.filter(id=data.id).first()
                user_committee_data.id = user_committee.id
                user_committee_data.code = user_committee.code
                user_committee_data.status = user_committee.status
                user_committee_data.bank_address = user_committee.bank_address
                user_committee_data.ward_no = user_committee.ward_no
                user_committee_data.formation_date_bs = (
                    user_committee_data.formation_date_bs
                )
                user_committee_data.formation_date_eng = (
                    user_committee_data.formation_date_eng
                )
                user_committee_data.attended_no = user_committee.attended_no
                user_committee_data.witness_no = user_committee.witness_no
                user_committee_data.full_name = user_committee.full_name
                user_committee_data.full_name_eng = user_committee.full_name_eng
                user_committee_data.registration_no = (
                    user_committee_data.registration_no
                )
                user_committee_data.registration_date_bs = (
                    user_committee_data.registration_date_bs
                )
                user_committee_data.registration_date_eng = (
                    user_committee_data.registration_date_eng
                )
                user_committee_data.office = user_committee.office
                user_committee_data.other_detail = user_committee.other_detail
                # user_committee_data.bank = user_committee.bank
                # user_committee_data.bank_account_no = user_committee.bank_account_no
                # user_committee_data.member_type = user_committee.member_type
                # user_committee_data.current_address = user_committee.current_address
                # user_committee_data.former_address = user_committee.former_address
                # user_committee_data.contact_detail = user_committee.contact_detail
                # user_committee_data.contact_person = user_committee.contact_person
                user_committee_data.remarks = user_committee.remarks
                user_committee_data.display_order = user_committee.display_order
                return user_committee_data
            else:
                return None
        except Exception as e:
            print(f"Exception to get_user_committee: {e}")
            user_committee_data.success = False
            user_committee_data.msg = "Error while getting data"
            return user_committee_data

    def get_user_committee_form_data(self, data):
        committee_formulate_data = UserCommitteeFormData()
        try:
            project_user_committee = ConsumerFormulation.objects.filter(
                project=data
            ).first()
            if project_user_committee:
                committee_formulate_data.id = project_user_committee.id
                committee_formulate_data.first_time_publish = (
                    project_user_committee.first_time_publish
                )
                committee_formulate_data.first_time_publish_eng = (
                    project_user_committee.first_time_publish_eng
                )
                committee_formulate_data.form_amount = (
                    project_user_committee.form_amount
                )
                committee_formulate_data.consumer_committee = (
                    self.get_user_committee(project_user_committee.consumer_committee)
                    if project_user_committee.consumer_committee
                    else None
                )
                committee_formulate_data.code = project_user_committee.code
                committee_formulate_data.chairman = project_user_committee.chairman
                committee_formulate_data.address = project_user_committee.address
                committee_formulate_data.established_date = (
                    project_user_committee.established_date
                )
                committee_formulate_data.phone = project_user_committee.phone
                committee_formulate_data.report_date = (
                    project_user_committee.report_date
                )
                committee_formulate_data.report_date_eng = (
                    project_user_committee.report_date_eng
                )
                committee_formulate_data.invoice_no = project_user_committee.invoice_no
                committee_formulate_data.project_current_status = (
                    project_user_committee.project_current_status
                )
                committee_formulate_data.previous_work = (
                    project_user_committee.previous_work
                )
                committee_formulate_data.detail_from_office_date = (
                    project_user_committee.detail_from_office_date
                )
                committee_formulate_data.detail_from_office_date_eng = (
                    project_user_committee.detail_from_office_date_eng
                )
                committee_formulate_data.office_lecture = (
                    project_user_committee.office_lecture
                )
                # committee_formulate_data.emp_name = project_user_committee.emp_name
                # committee_formulate_data.position = project_user_committee.position
                committee_formulate_data.opinion = project_user_committee.opinion
                committee_formulate_data.positive_effect = (
                    project_user_committee.positive_effect
                )
                committee_formulate_data.other = project_user_committee.other
                committee_formulate_data.project_related_other = (
                    project_user_committee.project_related_other
                )
            return committee_formulate_data
        except Exception as e:
            print(f"Exception in get_user_committee_form_data: {e}")
            committee_formulate_data.success = False
            committee_formulate_data.msg = "Error while getting data"
            return committee_formulate_data

    def get_installment_detail(self, data):
        installment_data = InstallmentDetailData()
        installments = []
        try:
            installments_data = InstallmentDetail.objects.filter(
                open_account_installment=data
            )
            if installments_data is not None:
                for installment in installments_data:
                    installment_data.id = installment.id
                    installment_data.installment = self.get_common_model_data(
                        installment.installment
                    )
                    installment_data.date = installment.date
                    installment_data.date_eng = installment.date_eng
                    installment_data.amount = installment.amount
                    installment_data.percent = installment.percent
                    installment_data.remark = installment.remark
                    installments.append(installment_data)
                return installments
            else:
                return []
        except Exception as e:
            print(f"Exception in get_installment_detail: {e}")
            return []

    def get_open_contract_account_data(self, data):
        open_contract_account_data = OpenContractAccountData()
        try:
            project_oca = OpeningContractAccount.objects.filter(project=data).first()
            if project_oca:
                open_contract_account_data.id = project_oca.id
                open_contract_account_data.cha_no = project_oca.cha_no
                open_contract_account_data.pa_no = project_oca.pa_no
                open_contract_account_data.date = project_oca.date
                open_contract_account_data.date_eng = project_oca.date_eng
                open_contract_account_data.bank_name = ""  # FK
                open_contract_account_data.account_no = project_oca.account_no
                open_contract_account_data.bank_branch = project_oca.bank_branch
                open_contract_account_data.bodarth = project_oca.bodarth
                open_contract_account_data.contract_ch_no = project_oca.contract_ch_no
                open_contract_account_data.contract_date = project_oca.contract_date
                open_contract_account_data.contract_pa_no = project_oca.contract_pa_no
                open_contract_account_data.bodarth_1 = project_oca.bodarth_1
                open_contract_account_data.bodarth_2 = project_oca.bodarth_2
                open_contract_account_data.day = project_oca.day
                open_contract_account_data.contract_account_no = (
                    project_oca.contract_account_no
                )
                open_contract_account_data.print_custom_report = (
                    project_oca.print_custom_report
                )
                open_contract_account_data.project_contract_date = (
                    project_oca.project_contract_date
                )
                open_contract_account_data.project_contract_date_eng = (
                    project_oca.project_contract_date_eng
                )
                open_contract_account_data.project_contract_start_date = (
                    project_oca.project_contract_start_date
                )
                open_contract_account_data.project_contract_start_date_eng = (
                    project_oca.project_contract_start_date_eng
                )
                open_contract_account_data.project_completion_date = (
                    project_oca.project_completion_date
                )
                open_contract_account_data.project_completion_date_eng = (
                    project_oca.project_completion_date_eng
                )
                open_contract_account_data.contract_no = project_oca.contract_no
                open_contract_account_data.present_benefit = project_oca.present_benefit
                open_contract_account_data.absent_benefit = project_oca.absent_benefit
                open_contract_account_data.project_start_experience = (
                    project_oca.project_start_experience
                )
                open_contract_account_data.other_experience = (
                    project_oca.other_experience
                )
                open_contract_account_data.arrangements_for_taking_care_of_repairs = (
                    project_oca.arrangements_for_taking_care_of_repairs
                )
                open_contract_account_data.repairs_by_company = (
                    project_oca.repairs_by_company
                )
                open_contract_account_data.mandate_ch_no = project_oca.mandate_ch_no
                open_contract_account_data.mandate_date = project_oca.mandate_date
                open_contract_account_data.mandate_date_eng = (
                    project_oca.mandate_date_eng
                )
                open_contract_account_data.mandate_pa_no = project_oca.mandate_pa_no
                open_contract_account_data.mandate_bodarth = project_oca.mandate_bodarth
                open_contract_account_data.ward_no = project_oca.ward_no
                open_contract_account_data.installment_detail = (
                    self.get_installment_detail(project_oca)
                    if project_oca.installment_detail
                    else []
                )
                open_contract_account_data.building_material = ""  # FK
                open_contract_account_data.maintenance_arrangement = ""  # FK
            return open_contract_account_data
        except Exception as e:
            self.logger.exception(f"Exception while getting project report: {e}")
            open_contract_account_data.success = False
            open_contract_account_data.msg = (
                f"Exception while getting project report: {e}"
            )
            return open_contract_account_data

    def get_project_finish_data(self, data):
        project_finish_data = ProjectFinishedBailReturnData()
        try:
            project = ProjectFinishedBailReturn.objects.filter(project=data).first()
            if project:
                project_finish_data.id = project.id
                project_finish_data.comment_no = project.comment_no
                project_finish_data.date = project.date
                project_finish_data.date_eng = project.date_eng
                project_finish_data.executive_decision = project.executive_decision
                # project_finish_data.approved_by = project.approved_by.first_name
                # project_finish_data.print_custom_report = project.print_custom_report
            return project_finish_data
        except Exception as e:
            print(f"Exception in get_project_finish_data: {e}")
            project_finish_data.success = False
            project_finish_data.msg = "Error while getting data"
            return project_finish_data

    def get_project_benefited_data(self, data):
        project_benefit_data = ProjectBenefitedDetailData()
        try:
            project_benefit = BenefitedDetail.objects.filter(project=data).first()
            if project_benefit:
                project_benefit_data.id = project_benefit.id
                project_benefit_data.target_group = project_benefit.target_group
                project_benefit_data.total_house_number = (
                    project_benefit.total_house_number
                )
                project_benefit_data.total_man = project_benefit.total_man
                project_benefit_data.total_women = project_benefit.total_women
                project_benefit_data.total_other = project_benefit.total_other
                project_benefit_data.total_population = project_benefit.total_population
                project_benefit_data.remark = project_benefit.remark
            return project_benefit_data
        except Exception as e:
            print(f"Exception in get_project_benefited_data: {e}")
            project_benefit_data.success = False
            project_benefit_data.msg = "Error while getting data"
            return project_benefit_data

    # Report responses
    def get_project_new_report(self, data):
        report = ProjectReport()
        try:
            self.logger.info("getting report data: {data}")
            report.project_id = data.id
            report.project_detail = self.get_project_data(data)  # ProjectExecution
            report.project_budget = self.get_project_budget_data(data)  # Budget
            report.project_agreement = self.get_project_agreement_data(data)
            report.project_mandate = self.get_project_mandate_data(data)
            report.user_committee_form_data = self.get_user_committee_form_data(data)
            report.project_finish_data = self.get_project_finish_data(data)
            report.project_status = (
                "कार्य सम्पन्न भएको"
                if report.project_finish_data.id
                else "कार्य सम्पन्न नभएको"
            )
            # pprint(report.dict())
            return report
        except Exception as e:
            self.logger.exception(f"Exception while getting project report: {e}")
            return None

    def get_project_by_subject_area(self, data):
        report = ProjectReportBySubjectArea()
        try:
            self.logger.info("getting report data: {data}")
            report.project_id = data.id
            report.project_detail = self.get_project_data(data)
            report.project_agreement = self.get_project_agreement_data(data)
            report.project_finish_data = self.get_project_finish_data(data)
            report.project_benefited_data = self.get_project_benefited_data(data)
            report.project_status = (
                "कार्य सम्पन्न भएको"
                if report.project_finish_data.id
                else "कार्य सम्पन्न नभएको"
            )
            # pprint(report.dict())
            return report
        except Exception as e:
            self.logger.exception(f"Exception while getting project report: {e}")
            return None

    def get_project_by_agreement(self, data):
        report = ProjectReportByAgreement()
        try:
            self.logger.info("getting report data: {data}")
            report.project_id = data.id
            report.project_detail = self.get_project_data(data)
            report.project_agreement = self.get_project_agreement_data(data)
            report.project_finish_data = self.get_project_finish_data(data)
            report.user_committee_form_data = self.get_user_committee_form_data(data)
            report.project_status = (
                "कार्य सम्पन्न भएको"
                if report.project_finish_data.id
                else "कार्य सम्पन्न नभएको"
            )
            return report
        except Exception as e:
            self.logger.exception(f"Exception while getting project report: {e}")
            return None

    def get_project_by_payment_detail(self, data):
        report = ProjectReportByPaymentDetail()
        try:
            self.logger.info("getting report data: {data}")
            report.project_id = data.id
            report.project_detail = self.get_project_data(data)
            report.project_agreement = self.get_project_agreement_data(data)
            report.project_finish_data = self.get_project_finish_data(data)
            report.open_contract_account_data = self.get_open_contract_account_data(
                data
            )
            report.project_status = (
                "कार्य सम्पन्न भएको"
                if report.project_finish_data.id
                else "कार्य सम्पन्न नभएको"
            )
            return report
        except Exception as e:
            self.logger.exception(f"Exception while getting project report: {e}")
            return None

    def get_all_project_report_data(
        self, project, municipality, address, user_committee
    ):
        report_data = {
            "municipality_data": self.get_municipality_data(municipality),
            "district_data": self.get_district_data(municipality.district),
            "province_data": self.get_province_data(municipality.district.province),
            "address_data": self.get_address_data(address),
            "project_data_response": self.get_project_data(project.execution),
            # "report_by_project_type": ReportByProjectType,
            "project_budget_allocation_data": self.get_project_budget_data(
                project.execution
            ),
            "project_agreement_data": self.get_project_agreement_data(
                project.execution
            ),
            "deposit_mandate_data": self.get_project_mandate_data(project.execution),
            "user_committee_data": self.get_user_committee(user_committee),
            "user_committee_form_data": self.get_user_committee_form_data(
                project.execution
            ),
            "installment_detail_data": self.get_installment_detail(
                OpeningContractAccount.objects.filter(project=project.execution).first()
            ),
            "open_contract_account_data": self.get_open_contract_account_data(
                project.execution
            ),
            "project_finished_bail_return_data": self.get_project_finish_data(
                project.execution
            ),
            "project_benefited_detail_data": self.get_project_benefited_data(
                project.execution
            ),
            # "project_report": self.get_project_new_report(project),
            # "project_report_by_subject_area": self.get_project_by_subject_area(project),
            # "project_report_by_agreement": ProjectReportByAgreement,
            # "project_report_by_payment_detail": ProjectReportByPaymentDetail,
        }
        return report_data
