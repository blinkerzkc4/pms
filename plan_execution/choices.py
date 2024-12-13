from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class CommentSentForChoices(TextChoices):
    PREPARATION = "P", _("Preparation")
    VERIFICATION = "V", _("Verification")
    AUTHORIZATION = "A", _("Authorization")


class CommentStatusChoices(TextChoices):
    PENDING = "P", _("Pending")
    APPROVED = "A", _("Approved")
    REJECTED = "R", _("Rejected")


class PaymentTypes(TextChoices):
    PESKI = "pes", _("Peski")
    BHUKTAANI = "bhk", _("Bhuktani")


class BOQTypeChoices(TextChoices):
    BOQ = "BOQ", _("BOQ")
    NON_BOQ = "NON_BOQ", _("Non BOQ")


class WorkProposerType(TextChoices):
    UPS = "ups", "उपभोक्ता समिति / टोल"
    WARD = "ward", "वडा"
    MUNICIPALITY = "muni", "न.पा./गा.पा."
    OTHER = "other", "अन्य"


class BankGuaranteeType(TextChoices):
    BID_BOND = "bid_bond", "बिड बन्ड"
    PERFORMANCE_BOND = "performance_bond", "पर्फरमेन्स बन्ड"


class BailType(TextChoices):
    CASH = "cash", "नगद"
    BANK_GUARANTEE = "bank_guarantee", "बैंक ग्यारेन्टी"


class ProcessNameChoices(TextChoices):
    # Common Choices
    EXTENSION = "म्याद थप", "म्याद थप"
    DISCHARGE = "निकासा", "निकासा"
    ESTIMATE = "इस्टिमेट पेश/स्वीकृत सम्बन्धि", "इस्टिमेट पेश/स्वीकृत सम्बन्धि"
    MOBILIZATION = "मोबिलैजेशन", "मोबिलैजेशन"
    PROJECT_REVISION = "योजना संशोधन", "योजना संशोधन"
    WORK_COMPLETION_DESCRIPTION = "कार्य सम्पन्न विवरण", "कार्य सम्पन्न विवरण"
    MEASURING_BOOK = "नापी किताब सम्बन्धि", "नापी किताब सम्बन्धि"
    # ठेक्कापट्टा
    TPPT_TENDER = "टेन्डर सम्बन्धि", "टेन्डर सम्बन्धि"
    TPPT_BOLPATRA = "बोलपत्र संकलन", "बोलपत्र संकलन"
    TPPT_RATE = "दरभाउ पत्र/बोलपत्र स्वीकृत", "दरभाउ पत्र/बोलपत्र स्वीकृत"
    TPPT_AGREEMENT = "सम्झौता सम्बन्धि", "सम्झौता सम्बन्धि"
    TPPT_DISCHARGE_BILL = "निकासा विल भुक्तानी सम्बन्धि", "निकासा विल भुक्तानी सम्बन्धि"
    # उपभोक्ता समिति
    UPS_CONSUMER_FORMULATION = "उपभोक्ता छनौट/गठन", "उपभोक्ता छनौट/गठन"
    UPS_PROBABILITY_STUDY = "सम्भाव्यता अध्ययन/स्वीकृत", "सम्भाव्यता अध्ययन/स्वीकृत"
    UPS_CONTRACT = "सम्झौता/खाता खोलिदिन सम्बन्धि", "सम्झौता/खाता खोलिदिन सम्बन्धि"
    UPS_MONITORING = "अनुगमन", "अनुगमन"
    UPS_COMMENT_AND_ORDER = "टिप्पणी र आदेश", "टिप्पणी र आदेश"
    # अमानत
    DP_DEPOSIT_MANDATE = "अमानत कार्यादेश", "अमानत कार्यादेश"
    DP_COMPLETION = "कार्य सम्पन्न तथा फरफारक", "कार्य सम्पन्न तथा फरफारक"
    # संस्थागत सहकार्य
    INST_NOMINATION = "मनोनित कर्मचारी", "मनोनित कर्मचारी"
    INST_MANDATE = "कार्यादेश", "कार्यादेश"
