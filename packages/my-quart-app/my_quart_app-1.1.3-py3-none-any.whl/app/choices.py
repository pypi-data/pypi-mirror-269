"""
Choices.py
Usage: Choices
"""

import enum


class RequestTypeChoices(enum.Enum):
    email = "email"
    sms = "sms"
    remark = "remark"
    voice = "voice"
    whatsapp = "whatsapp"
    whatsapp_bot = "whatsapp_bot"
    dtmf_ivr = "dtmf_ivr"
    communication = "communication"
    NA = "NA"


class QueueTypeChoices(enum.Enum):
    stag = "staging"
    prod = "production"
    celery = "celery"
    result = "result"
    reporting = "reporting"
    campaign_update = "campaign_update"


class AllocationApprovalStatuses(enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_APPROVAL = "under_approval"


class ReminderOffsetTypeChoices(enum.Enum):
    minutes = "minutes"
    hours = "hours"
    days = "days"


class CampaignProgressTypeChoices(enum.Enum):
    in_progress = "IN PROGRESS"
    in_queue = "IN QUEUE"
    completed = "COMPLETED"
    hold = "ON HOLD"
    partial_completed = "PARTIAL COMPLETED"


class CampaignTriggerTypeChoices(enum.Enum):
    in_process = "IN PROCESS"
    completed = "COMPLETED"
    hold = "ON HOLD"
    partial_completed = "PARTIAL COMPLETED"
    stopping = "STOPPING"
    stopped = "STOPPED"


class CampaignDeliveryTypeChoices(enum.Enum):
    updating = "UPDATING"
    completed = "COMPLETED"
    hold = "ON HOLD"
    partial_completed = "PARTIAL COMPLETED"


class CommServiceNameTypeChoices(enum.Enum):
    prod_recovery = "recovery"
    stag_recovery = "stagrecovery"


class TypeOfTaskChoices(enum.Enum):
    address_conversion_lat_long = "address_conversion_lat_long"
    scrape_indiapost = "indiapost_tracking"
    speedpost_upload = "speedpost_upload"
    upload_c2c_disposition = "upload_c2c_disposition"
    linked_loan_digital_notice = "linked_loan_digital_notice_generation"
    optin = "optin"
    notifications = "notifications"
    communication = "communication"
    notice = "notice"
    scrape = "scrape"
    indiapost_upload = "indiapost_upload"
    indiapost_tracking = "indiapost_tracking"
    linked_loan_digital = "linked_loan_digital"
    digital = "digital"
    physical = "physical"
    linked_loan_physical = "linked_loan_physical"
    lat_long_conversion = "lat_long_conversion"
    ecourt_tracking = "ecourt_tracking"
    add_ecourt_case = "add_ecourt_case"
    update_ecourt_case = "update_ecourt_case"
    fetch_ecourt_case_orders = "fetch_ecourt_case_orders"
    litigation_approval_request = "litigation_approval_request"


class NotificationTypeChoices(enum.Enum):
    notification = "notification"
    reminder = "reminder"


class ErrorCodeMessages(enum.Enum):
    internal_server_error = "Internal Server Error"
    request_timeout = "Request Timeout"
    bad_gateway = "Bad Gateway"
    gateway_timeout = "Gateway Timeout"


class HttpRequests(enum.Enum):
    HTTP_200_OK = 200
    HTTP_400_BAD_REQUEST = 400
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_204_NO_CONTENT = 204
    HTTP_424_FAILED_DEPENDENCY = 424
    HTTP_201_CREATED = 201


class ExportServiceCallType(enum.Enum):
    DELIVERY_REPORT_CONSUMER = "delivery_report_consumer"
    DEFAULT = "default"


CAMPAIGN_SUMMARY_CHOICES = {
    "sms": "delivered,clicked",
    "email": "delivered,opened,clicked",
    "voice": "delivered,answered",
    "dtmf_ivr": "delivered,answered,responded",
    "whatsapp": "sent,delivered,opened,clicked",
    "whatsapp_bot": "sent,delivered,opened",
}

COMPLETION_SUMMARY_CHOICES = {
    "sms": "delivered",
    "email": "delivered",
    "voice": "delivered,answered",
    "dtmf_ivr": "delivered,answered,responded",
    "whatsapp": "sent,delivered",
    "whatsapp_bot": "sent,delivered",
}


DB_SUCCESS = 1
CHANNELS = ["email", "sms", "voice", "whatsapp", "call", "whatsapp_bot", "dtmf_ivr"]
NOTIFICATION_SOURCE = ["web_client", "app"]
NOTIFY_TYPE = ["reminder", "notification"]
REMINDER_OFFSET_TYPE = ["minutes", "hours", "days"]
SEND_TO = ["applicant", "co_applicant", "both"]
COMMUNICATION_LEVEL = ["customer", "transaction"]
BATCH_TYPE = [
    "notice",
    "scrape",
    "notifications",
    "upload_c2c_disposition",
    "lat_long_conversion",
    "ecourt_tracking",
    "litigation_approval_request",
]
BATCH_CHANNELS = [
    "indiapost_upload",
    "indiapost_tracking",
    "digital",
    "linked_loan_digital",
    "add_ecourt_case",
    "update_ecourt_case",
    "physical",
    "linked_loan_physical",
    "fetch_ecourt_case_orders",
]
APPLICANT_TYPE = ["applicant", "co_applicant"]
RESULT_CODE = ["CONTC", "RNR", "INCNO", "INC"]
CAMPAIGN_SUBMODULE = [
    "sms_campaigns",
    "email_campaigns",
    "dtmf_ivr_campaigns",
    "obd_ivr_campaigns",
    "whatsapp_bot_campaigns",
    "whatsapp_campaigns",
    "master_campaigns",
]
HERO_DATA = {
    "SZUSERNAME": "",
    "SZPASSWORD": "",
    "SZACCOUNTNO": "",
    "SZEMAILID": "",
    "SZMOBILENO": "",
    "SZMOBILETYPE": "",
    "SZUSERID": "",
    "SZACTIONCODE": "PDMC",
    "SZRESULTCODE": "",
    "SZNEXTACTIONCODE": "",
    "DTNEXTACTION": "",
    "SZREMARKS": "",
    "DTPROMISEDATE1": "",
    "FPROMISEAMOUNT1": "",
    "DTPROMISEDATE2": "",
    "FPROMISEAMOUNT2": "",
    "DTPROMISEDATE3": "",
    "FPROMISEAMOUNT3": "",
    "DTPROMISEDATE4": "",
    "FPROMISEAMOUNT4": "",
    "DTPROMISEDATE5": "",
    "FPROMISEAMOUNT5": "",
    "SZTRAILSOURCE": "C2C",
    "SZCUSTCATEGORY": "",
    "SZEXECUTIVEID": "",
    "SZEXECUTIVENAME": "",
    "SZEXECUTIVEOFFICE": "",
    "SZEXECUTIVEQUALIFICATION": "",
    "SZEXECUTIVEVINTAGE": "",
    "SZEXECUTIVELANG": "",
    "SZCUSTMOBILENO": "",
    "SZCALLDURATION": "",
    "SZCALLSTARTTIME": "",
    "SZCALLENDTIME": "",
    "SZPAYMENTMODE": "",
    "SZPICKUPPARTNERCODE": "",
    "SZDIGIPARTNERCODE": "",
    "SZREFPARTNERCODE": "",
    "SZOTHERPARTNER": "",
    "SZCALLWRAPTIME": "",
    "SZCALLTYPE": "",
    "SZFIELD1": "",
    "SZFIELD2": "",
    "SZFIELD3": "",
    "SZFIELD4": "",
    "SZFIELD5": "",
    "SZFIELD6": "",
    "SZFIELD7": "",
    "SZFIELD8": "",
    "SZFIELD9": "",
    "SZFIELD10": "",
    "SZCAMPAIGNID": "",
}


class ColumnMapChoices(enum.Enum):
    email = {
        "loan_id": "dummy_column_map_choices_loan_id",
        "allocation_month": "",
        "type_of_communication": "",
        "digital_disposition": "",
        "applicant_type": "",
        "bulk_request_id": "",
        "bulk_request_name": "",
        "email_template_name": "",
        "email_subject": "",
        "email_delivery_time": "",
        "email_notice_clicked_time": "",
        "email_opened_time": "",
        "email_bounced_time": "",
        "email_notice_clicked_count": "",
        "email_notice_type(s)": "",
        "email_notice_link(s)": "",
        "email_reply_to": "",
        "email_address_cc": "",
        "email_address_bcc": "",
        "email_address_to": "",
        "email_address_from": "",
        "template_id": "",
        "author": "",
        "role": "",
        "triggered_time": "",
        "error_name": "",
        "error_group_name": "",
        "error_description": "",
    }
    voice = {
        "loan_id": "dummy_column_map_choices_loan_id",
        "allocation_month": "",
        "type_of_communication": "",
        "digital_disposition": "",
        "applicant_type": "",
        "bulk_request_id": "",
        "bulk_request_name": "",
        "ivr_template_name": "",
        "ivr_mobile_number": "",
        "ivr_start_time": "",
        "ivr_end_time": "",
        "ivr_answer_time": "",
        "ivr_call_duration_(in_seconds)": 0,
        "ivr_audio_time_span_(in_seconds)": 0,
        "ivr_language": "",
        "ivr_character_count": "",
        "ivr_pulse_count": 0,
        "voice_gender": "",
        "template_id": "",
        "author": "",
        "role": "",
        "triggered_time": "",
        "error_name": "",
        "error_group_name": "",
        "error_description": "",
    }
    whatsapp = {
        "loan_id": "dummy_column_map_choices_loan_id",
        "allocation_month": "",
        "type_of_communication": "",
        "digital_disposition": "",
        "applicant_type": "",
        "bulk_request_id": "",
        "bulk_request_name": "",
        "whatsapp_message_template_name": "",
        "client_template_id": "",
        "whatsapp_mobile_number": "",
        "whatsapp_message_delivery_time": "",
        "whatsapp_message_notice_clicked_time": "",
        "whatsapp_message_opened_time": "",
        "whatsapp_message_sent_time": "",
        "whatsapp_message_notice_clicked_count": "",
        "whatsapp_message_notice_type(s)": "",
        "whatsapp_message_notice_link(s)": "",
        "template_id": "",
        "author": "",
        "role": "",
        "triggered_time": "",
        "error_name": "",
        "error_group_name": "",
        "error_description": "",
    }
    whatsapp_bot = {
        "loan_id": "dummy_column_map_choices_loan_id",
        "allocation_month": "",
        "type_of_communication": "",
        "digital_disposition": "",
        "applicant_type": "",
        "bulk_request_id": "",
        "bulk_request_name": "",
        "whatsapp_bot_session_template_name": "",
        "whatsapp_bot_session_mobile_number": "",
        "whatsapp_bot_session_delivery_time": "",
        "whatsapp_bot_session_opened_time": "",
        "whatsapp_bot_session_sent_time": "",
        "template_id": "",
        "author": "",
        "role": "",
        "triggered_time": "",
        "error_name": "",
        "error_group_name": "",
        "error_description": "",
    }
    dtmf_ivr = {
        "loan_id": "dummy_column_map_choices_loan_id",
        "allocation_month": "",
        "type_of_communication": "",
        "digital_disposition": "",
        "applicant_type": "",
        "bulk_request_id": "",
        "bulk_request_name": "",
        "dtmf_ivr_template_name": "",
        "dtmf_ivr_mobile_number": "",
        "dtmf_ivr_start_time": "",
        "dtmf_ivr_end_time": "",
        "dtmf_ivr_answer_time": "",
        "dtmf_ivr_call_duration_(in_seconds)": 0,
        "dtmf_codes": "",
        "template_id": "",
        "collected_dtmfs": {"Pay_now": "", "Language": ""},
        "collected_mapped_dtmfs": {"Pay_now_Meaning": "", "Language_Meaning": ""},
        "author": "",
        "role": "",
        "triggered_time": "",
        "error_name": "",
        "error_group_name": "",
        "error_description": "",
    }
    sms = {
        "loan_id": "dummy_column_map_choices_loan_id",
        "allocation_month": "",
        "type_of_communication": "",
        "digital_disposition": "",
        "applicant_type": "",
        "bulk_request_id": "",
        "bulk_request_name": "",
        "sms_template_name": "",
        "sms_mobile_number": "",
        "sms_delivery_time": "",
        "sms_notice_clicked_time": "",
        "sms_bounced_time": "",
        "sms_notice_clicked_count": "",
        "sms_notice_type(s)": "",
        "sms_notice_link(s)": "",
        "sms_language": "en",
        "sms_message_count": 0,
        "sms_character_count": 0,
        "template_id": "",
        "sender_id": "",
        "author": "",
        "role": "admin",
        "triggered_time": "",
        "error_name": "",
        "error_group_name": "",
        "error_description": "",
    }


PROD_ENV = "production"

DEFAULT_EMPTY_RESPONSE = {"message": "success", "output": []}

DB_ERROR_RESPONSE = "database connection or query execution failure"
THRESHOLD_PERCENTAGE = 99.5
COMPLETION_PERCENTAGE = 100
AI_RULE_EMAIL = "ai.rule@credgenics.com"
SMS_KEY = "IBSMS_"
COLOR_CODING = ["#f44336", "#ef5350", "#e57373", "#ef9a9a", "#ffcdd2", "#ffebee"]
ERROR_FIELDS_COUNT = 5

ERROR_DICT_MAPPING = {"id": "error_name", "label": "error_name", "value": "count"}
REQUEST_COMPLETION_SMS_TEMP_ID = "1107166210293681407"
PRINCIPAL_ENTITY_ID = "1101360080000040019"

EXCEL_WORKSHEET_HYPERLINK_LIMIT = 65530
COMMA = ","
DELIMITER = "~"
PICKLE_EXTENSTION = ".pickle"
MAX_LIMIT_OF_ITERATION_REMINDERS = 10
NO_COMMUNICATION = "no_communication"
RESTRICTED_COMMUNICATION = "restricted_communication"
CAMPAIGNS_TABLE = "campaigns"
MODULE = "queue"
SOURCE = "queue_reporting"
CAMPAIGN_STOPPED_ERROR_CODE = "COM-104"
CALL_DURATION = 15


class ReattemptErrors(enum.Enum):
    SELECT_ALL_ATTEMPT = "select all"
    TRIGGERED_AND_DELIVERED_ATTEMPT = "successfully delivered"
    NOT_TRIGGERED_ATTEMPT = "failed to trigger"
    NOT_DELIVERED_ATTEMPT = "undelivered but successfully triggered"
    WEBHOOK_NOT_RECEIVED_ATTEMPT = "delivery status not updated"
    WHATSAPP_SENT_BUT_NOT_DELIVERED_ATTEMPT = "whatsApp sent but not delivered"
    LINK_CLICKED_ATTEMPT = "link clicked"
    ANSWERED_LESS_THAN_ATTEMPT = f"answered (less than & equal {CALL_DURATION} seconds)"
    ANSWERED_GREATER_THAN_ATTEMPT = f"answered (greater than {CALL_DURATION} seconds)"
    RESPONDED_ATTEMPT = "responded"
    OPENED_ATTEMPT = "opened"


class ReattemptGroups(enum.Enum):
    SELECT_ALL = "select_all"
    TRIGGERED_AND_DELIVERED = "triggered and delivered"
    WEBHOOK_NOT_RECEIVED = "webhook not received"
    QUEUE_FAILURES = "queue_failures"
    OPERATOR_FAILURES = "operator_failures"
    WHATSAPP_SENT_BUT_NOT_DELIVERED = "whatsapp_sent_but_not_delivered"
    IS_LINK_CLICKED = "is_link_clicked"
    FOR_LESS_THAN = "for_less_than"
    FOR_GREATER_THAN = "for_greater_than"
    RESPONDED_TIME = "responded_time"
    OPENED_TIME = "opened_time"
    TRIGGERED = "triggered"


MERGE_FILE_NAME_REPLACE_CHARACTER = "_"
LITIGATION_REPORT_DELIMITER = "~"
API_USER_DETAILS = {
    "assigned_companies": "All",
    "authentication_token": "aa53d8f4-31e6-400c-86aa-acfeb009364b",
    "author": "api@credgenics",
    "company_id": None,
    "email": "api@credgenics",
    "role": "api user",
    "user_id": "kvr7dtjueg5axc8l",
    "user_type": "api user",
}


class ReportStatus(enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    LOAN_BATCH_FAILED = "LOAN_BATCH_FAILED"
    COMPLETED = "COMPLETED"


HELICARRIER = "helicarrier"
DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_number = 1
MASTER_CAMPAIGN_CHANNEL = "master"
DATA_SCIENCE = "data_science"
