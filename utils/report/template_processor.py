import re
from typing import List, Set


def extract_variables_from_template(template_text) -> List[str]:
    template_text = template_text or ""
    # Define the regular expression pattern for variable extraction
    variable_pattern = re.compile(r"{{\s*([\w.]+)\s*}}|{%\s*[\w]+\s*([\w.]+)\s*%}")

    # Find all matches in the template text
    matches = variable_pattern.findall(template_text)

    # Extract variable names from the matches
    variable_names = [match[0] or match[1] for match in matches]

    return variable_names


def get_main_variable_names_from_template(template_text: str) -> Set[str]:
    return set(
        [
            variable.split(".")[0]
            for variable in extract_variables_from_template(template_text)
        ]
    )


if __name__ == "__main__":
    # Example usage:
    template_text = """<p>पत्र संख्या : २०८०/२०८१</p>
    <p>चलानी नं. : {{ opening_contract_account.cha_no }}</p>
    <p>
        <strong>योजना कोड: {{ project_execution.code }}</strong>
    </p>
    <p style="text-align:right;">मिति :&nbsp;{{ today_date }}</p>
    <p>&nbsp;</p>
    <p>
        श्री <strong>{{ opening_contract_account.bank_name.full_name }}</strong>
    </p>
    <p>
        <strong>{{ opening_contract_account.bank_branch }}</strong>
    </p>
    <p>&nbsp;</p>
    <p style="text-align:center;">
        <strong><u>विषय: बैंक खाता खोलिदिने बारे सम्वन्धमा ।</u></strong>
    </p>
    <p style="text-align:justify;">&nbsp;</p>
    <p style="text-align:justify;">
        &nbsp; &nbsp; &nbsp; &nbsp; प्रस्तुत विषयमा यस लतितपुर महानगरपालिका वडा नं. {{ project_execution.ward }} स्थित {{ consumer_formulation.consumer_committee_name }} ललितपुरका तपशिलमा उल्लेख भएका पदाधिकारीहरुको संयुक्त&nbsp;दस्तखतबाट खाता संचालन हुने गरी सिफारिस उपलब्ध गराउनु हुन भनी &nbsp;ललितपुर महानगरपालिका {{ project_execution.ward }} नं वडा कार्यालयकाे सिफारिस बमाेजिम उक्त&nbsp;उपभोक्ता&nbsp;समितिको&nbsp;नाममा खाता खाेलि अध्यक्ष {{ consumer_formulation.chairman }} सचिव&nbsp;{{ opening_contract_account.user_committee_secretary }} <span style="background-color:rgba(220,220,220,0.5);">
        <img src="data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==" />
    </span> र&nbsp;कोषाध्यक्ष {{ opening_contract_account.bank_name.full_name }}को संयुक्त दस्तखतबाट खाता संचालन हुने व्यवस्था मिलाउनका लागी अनुरोध छ ।
    </p>
    <p style="text-align:justify;">&nbsp;</p>
    <p style="text-align:justify;">तपशिल</p>
    <p style="text-align:justify;">अध्यक्षः{{ consumer_formulation.chairman }}</p>
    <p style="text-align:justify;">सचिवः {{ opening_contract_account.user_committee_secretary }}&nbsp;</p>
    <p style="text-align:justify;">कोषाध्यक्ष:&nbsp;</p>
    """

    variables = get_main_variable_names_from_template(None)
    print(bool(variables))
