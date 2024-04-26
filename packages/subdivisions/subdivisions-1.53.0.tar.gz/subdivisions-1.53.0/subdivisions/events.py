"""PubSub Events.

Declare here all PubSub topics which will be used.

These Topics will be created on AWS, when you send his first message.

"""
from enum import Enum


class UserEvents(Enum):
    USER_REGISTERED = "user_registered"
    USER_ACTIVATED = "user_activated"
    USER_LOGGED_IN = "user_logged_in"


class AccountEvents(Enum):
    BANK_ACCOUNT_REGISTERED = "bank_account_registered"
    AD_ACCOUNT_REGISTERED = "google_ad_account_registered"
    POLISHED_STATEMENT_TABLE = "polished_statement_table"
    STATEMENT_TABLE_UPDATED = "statement_table_updated"


class QiTechEscrowAccountEvents(Enum):
    QITECH_UPDATE_STATEMENT = "qitech_update_statement"
    QITECH_ACCOUNT_REGISTERED = "qitech_account_registered"


class ProposalEvents(Enum):
    PROPOSAL_SELECTED = "proposal_selected"
    PROPOSAL_APPROVED = "proposal_approved"
    PROPOSAL_ACCEPTED = "proposal_accepted"
    PROPOSAL_INDICATIVE = "proposal_indicative"
    PROPOSAL_REFUSED = "proposal_refused"
    PROPOSAL_EXPIRED = "proposal_expired"
    PROPOSAL_STATUS_UPDATED = "prpposal_status_updated"
    PROPOSAL_PENDING_APPROVAL = "proposal_pending_approval"
    PROPOSAL_ACCEPTED_START_FORMALIZATION = "proposal_accepted_start_formalization"


class CompanyEvents(Enum):
    COMPANY_REGISTERED = "company_registered"
    COMPANY_UPDATED = "company_updated"


class HubspotEvents(Enum):
    ORIGINATION_REGISTERED = "origination_registered"
    ORIGINATION = "origination"
    ADDITIONAL_DATA_SENT = "additional_data_sent"
    LEAD_SCORE = "lead_score"


class AdsEvents(Enum):
    ADS_ACCOUNT_CONNECTION = "ads_account_connection"


class CredentialEvents(Enum):
    NEW_TAX_ID_REGISTERED = "new_tax_id_registered"


class PartnerEvents(Enum):
    I_WANT_TO_BE_A_PARTNER = "i_want_to_be_a_partner"


class PartnershipEvents(Enum):
    ORDER_NEW = "order_new"
    ORDER_DENIED = "order_denied"
    ORDER_APPROVED = "order_approved"
    ORDER_INDICATIVE = "order_indicative"
    ORDER_USER_VERIFICATION = "order_user_verification"


class ClientManagerEvents(Enum):
    SHAREHOLDER_REGISTRATION = "shareholder_registration"
    GUARANTOR_REGISTRATION = "guarantor_registration"
    PROCURATOR_REGISTER = "procurator_register"
    EXECUTIVE_REGISTRATION = "executive_registration"
    PEP_FORM = "pep_form"


class DocumentationEvents(Enum):
    GENERATED_DOCUMENTATION = "generated_documentation"
    DOCUMENTATION_OK = "documentation_ok"
    DISBURSEMENT_MADE = "disbursement_made"
    CLIENT_PROCESS_APPROVED = "client_process_approved"
    CLIENT_PROCESS_WITH_PENDENCIES = "client_process_with_pendencies"
    UPLOAD_FIRST_DOCUMENT = "upload_first_document"
    MEMBERSHIP_DOCUMENT = "membership_document"
    START_ANALYSIS = "start_analysis"


class AssetEvents(Enum):
    CREATED_EXPECTED_CASHFLOW_ENTRY = "created_expected_cashflow_entry"
    CREATED_INSTRUMENT = "created_instrument"
    CREATED_RENEGOTIATION = "created_renegotiation"
    OVERDUE_INSTALLMENT = "overdue_installment"


class BankEvents(Enum):
    CREATED_BOLETO = "created_boleto"
    UPDATED_BOLETO = "updated_boleto"
    CREATED_BOLETO_PROCESSED = "created_boleto_processed"


class CercEvent(Enum):
    NEW_SCHEDULE = "new_schedule"
    UPDATE_SCHEDULE = "update_schedule"


class BillingEvents(Enum):
    PAYMENT_INSTALLMENT = "payment_installment"


class AlternativeCreditEvents(Enum):
    PRICING_REQUEST = "pricing_request"


class TermsEvents(Enum):
    TERMS_ACCEPTANCE = "terms_acceptance"


class ClientLifeCycleEvents(Enum):
    SUBSCRIBER = "subscriber"
    LIFECYCLE_LEAD = "lifecycle_lead"
    MARKETING_QUALIFIED_LEAD = "marketing_qualified_lead"
    SALES_QUALIFIED_LEAD = "sales_qualified_lead"


class QualifiedPolicyEvents(Enum):
    QUALIFIED_BY_POLICY = "qualified_by_policy"
    DISQUALIFIED = "disqualified"
    QUALIFIED_BY_POLICY_WITH_RESERVATIONS = "qualified_by_policy_with_reservations"
    DISQUALIFIED_FOR_ELIGIBILITY = "disqualified_for_eligibility"


class ClientValidatorEvents(Enum):
    LEAD_ANALYSIS_COMPLETED = "lead_analysis_completed"
    CLIENT_VALIDATION_REQUEST = "client_validation_request"
    CLIENT_VALIDATION_FINISHED = "client_validation_finished"


class MQLEvents(Enum):
    NEGATIVE_INTEREST = "negative_interest"
    CUSTOMER_CLICKED_CTA_INTEREST = "customer_clicked_cta_interest"


class SQLEvents(Enum):
    OPT_IN_TERMS = "opt_in_terms"
    ADDITIONAL_REGISTRATION_CLIENT = "additional_registration_client"
    WAITING_FINANCIAL_DATA = "waiting_financial_data"


class UpsellEvents(Enum):
    UPSELL_PRICING_REQUEST = "upsell_pricing_request"


class OfertaMakerEvents(Enum):
    OFFER_CALCULATION_REQUEST = "offer_calculation_request"
    OFFER_CALCULATION_FINISHED = "offer_calculation_finished"


class TransactionalRiskEvents(Enum):
    TRANSACTIONAL_RISK_REQUEST = "transactional_risk_request"
    TRANSACTIONAL_RISK_FINISHED = "transactional_risk_finished"


class PayhopReceivableScheduleEvent(Enum):
    NEW_SCHEDULE_AVAILABLE = "new_schedule_available"
    NEW_LOCKED_RECEIVABLES_AVAILABLE = "new_locked_receivables_available"


class ProductEvents(Enum):
    PRODUCT_SELECTED = "product_selected"


class DealQuestionsEvents(Enum):
    DEAL_QUESTIONS = "deal_questions"
