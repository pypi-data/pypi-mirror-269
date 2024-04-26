import datetime
from typing import Optional, Union, Literal
from app.choices import (
    BATCH_CHANNELS,
    NOTIFICATION_SOURCE,
    NOTIFY_TYPE,
    REMINDER_OFFSET_TYPE,
    ReattemptErrors,
    TypeOfTaskChoices,
    DEFAULT_PAGE_number,
    DEFAULT_PAGE_SIZE,
)
from app.utils import is_valid_uuid
from pydantic import BaseModel, Field, root_validator, StrictInt, StrictStr, conlist
from enum import Enum
from typing import List


class ResultCode(Enum):
    CONTC = "CONTC"
    RNR = "RNR"
    INCNO = "INCNO"
    INC = "INC"


class SendTo(Enum):
    APPLICANT = "applicant"
    COAPPLICANT = "co_applicant"
    BOTH = "both"


class CommunicationLevel(Enum):
    CUSTOMER = "customer"
    TRANSACTION = "transaction"


class EmailContacts(Enum):
    CC = "cc"
    TO = "to"
    SEPARATE = "separate"


class Channel(Enum):
    EMAIL = "email"
    SMS = "sms"
    VOICE = "voice"
    WHATSAPP = "whatsapp"
    WHATSAPPBOT = "whatsapp_bot"
    DTMF = "dtmf_ivr"
    VOICE_BOT = "voice_bot"
    NA = "NA"


class BatchType(Enum):
    NOTICE = "notice"
    SCRAPE = "scrape"
    NOTIFICATION = "notifications"
    C2C_DISPOSITION = "upload_c2c_disposition"
    LAT_LONG_CONVERSION = "lat_long_conversion"
    OPTIN = "optin"
    ECOURT_TRACKING = "ecourt_tracking"
    LITIGATION_APPROVAL_REQUEST = "litigation_approval_request"


class LatLongConversionData(BaseModel):
    loan_id: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    applicant_index: StrictInt = Field(...)
    address_index: StrictInt = Field(...)


class IndiapostTrackingData(BaseModel):
    loan_id: str = Field(..., min_length=1)
    company_id: str = Field(..., min_length=1)
    tracking_id: str = Field(..., min_length=1)

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if other_errors:
            raise ValueError(other_errors)
        return values


class IndiapostUploadData(BaseModel):
    loan_id: str = Field(..., min_length=1)
    customer_name: Optional[str] = None
    customer_address1: Optional[str] = None
    customer_address2: Optional[str] = None
    customer_address3: Optional[str] = None
    customer_city: Optional[str] = None
    pin_code: Optional[str] = None
    customer_state: Optional[str] = None
    notice_id: Optional[str] = None
    tracking_no: Optional[str] = None


class UploadDispositionData(BaseModel):
    loan_id: str = Field(..., min_length=1)
    agent_id: str = Field(..., min_length=1)
    rec_url: str = Field(..., min_length=1)
    to_mobile: str = Field(..., min_length=1)
    call_duration: str = Field(..., min_length=1)
    result_code: ResultCode
    call_start_time: str = Field(..., min_length=1)
    call_end_time: str = Field(..., min_length=1)
    campaign_id: Optional[str] = None
    call_type: Optional[str] = None
    call_status: Optional[str] = None

    class Config:
        use_enum_values = True


class NotificationsData(BaseModel):
    message: str = Field(..., min_length=1)


class BatchOperationSchema(BaseModel):
    type: str = Field(..., min_length=1)
    channel: Optional[str] = None
    loan_data: Union[
        List[str],
        List[IndiapostUploadData],
        List[LatLongConversionData],
        List[IndiapostTrackingData],
        List[UploadDispositionData],
    ] = Field(...)
    is_linked_loan: Optional[bool] = None
    company_id: Optional[str] = None
    applicant_type: Optional[Literal["applicant", "co_applicant"]] = None
    notice_type: Optional[str] = None
    allocation_month: Optional[str] = None
    source: Optional[str] = None
    notify_type: Optional[str] = None
    reminder_offset_type: Optional[str] = None
    trigger_time: Optional[str] = None
    reminder_offset: Optional[List[StrictStr]] = None

    @root_validator(pre=True)
    def validate_data(cls, values):
        other_errors = []
        type = values.get("type")
        channel = values.get("channel")
        company_id = values.get("company_id")
        if company_id and not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if channel and channel not in BATCH_CHANNELS:
            other_errors.append(f"provide valid channel; permitted: {BATCH_CHANNELS}")
        elif type == TypeOfTaskChoices.scrape.value and channel not in (
            TypeOfTaskChoices.indiapost_upload.value,
            TypeOfTaskChoices.indiapost_tracking.value,
        ):
            other_errors.append(
                f"provide valid channel; permitted: ({TypeOfTaskChoices.indiapost_upload.value}, {TypeOfTaskChoices.indiapost_tracking.value})"
            )
        elif type == TypeOfTaskChoices.notice.value and (
            channel
            not in (
                TypeOfTaskChoices.linked_loan_digital.value,
                TypeOfTaskChoices.digital.value,
                TypeOfTaskChoices.physical.value,
                TypeOfTaskChoices.linked_loan_physical.value,
            )
        ):
            other_errors.append(
                f"provide valid channel; permitted: ({TypeOfTaskChoices.linked_loan_digital.value, TypeOfTaskChoices.digital.value, TypeOfTaskChoices.physical.value, TypeOfTaskChoices.linked_loan_physical.value})"
            )
        elif (
            type
            not in (
                TypeOfTaskChoices.notice.value,
                TypeOfTaskChoices.scrape.value,
                TypeOfTaskChoices.ecourt_tracking.value,
            )
        ) and (channel or channel == ""):
            other_errors.append(f"channel is not required for type:{type}")

        if (
            (type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_upload.value)
            or type == TypeOfTaskChoices.upload_c2c_disposition.value
            or type == TypeOfTaskChoices.optin.value
            or type == TypeOfTaskChoices.notifications.value
        ) and not values.get("company_id"):
            other_errors.append(f"provide valid company id")
        if type == TypeOfTaskChoices.lat_long_conversion.value:
            if not values.get("company_id"):
                other_errors.append(f"provide valid company id")
            if not values.get("applicant_type"):
                other_errors.append(f"provide valid applicant type")
        if type == TypeOfTaskChoices.notifications.value:
            if not values.get("trigger_time"):
                other_errors.append(f"provide valid trigger time")
            if values.get("source") not in NOTIFICATION_SOURCE:
                other_errors.append(f"provide valid source; permitted: {NOTIFICATION_SOURCE}")
            if values.get("notify_type") not in NOTIFY_TYPE:
                other_errors.append(f"provide valid notify type; permitted: {NOTIFY_TYPE}")
            if values.get("reminder_offset_type") not in REMINDER_OFFSET_TYPE:
                other_errors.append(f"provide valid reminder offset type; permitted: {REMINDER_OFFSET_TYPE}")
            if values.get("notify_type") == "reminder" and (not values.get("reminder_offset")):
                other_errors.append(f"reminder offset is required for notify_type: reminder")
            if values.get("notify_type", "") == "reminder" and (not values.get("reminder_offset_type")):
                other_errors.append(f"reminder offset type is required for notify type: reminder")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignData(BaseModel):
    name: str = Field(..., min_length=1)
    channel: Channel
    type: str = Field(..., min_length=1)
    description: Optional[str] = None

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        channel = values.get("channel")
        if channel != Channel.DTMF.value:
            other_errors.append(f"{channel} campaign not allowed")
        if other_errors:
            raise ValueError(other_errors)
        return values


class Campaign(BaseModel):
    company_id: str = Field(..., min_length=1)
    template_id: str = Field(..., min_length=1)
    campaign_data: CampaignData
    loan_data: conlist(str, min_items=1)
    allocation_month: str = Field(..., min_length=1)
    upto_index: str = Field(..., min_length=1)
    send_to: SendTo
    communication_level: CommunicationLevel
    comm_dict: Optional[dict] = {}
    additional_loan_data: Optional[dict] = {}
    mention_email_cc: Optional[list] = None
    mention_email_bcc: Optional[list] = None
    email_contacts: Optional[EmailContacts] = "cc"
    rule_id: Optional[str] = None
    rule_name: Optional[str] = None
    ai_author_ids: Optional[str] = None
    template_name: Optional[str] = None
    filters: Union[str, dict] = None
    range: str = None

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        template_name = values.get("template_name")
        company_id = values.get("company_id")
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if other_errors:
            raise ValueError(other_errors)
        if not template_name:
            values.pop("template_name")
        return values


class APIResponseSchema(BaseModel):
    status: str = Field(..., min_length=1)
    response: str = Field(..., min_length=1)
    loan_id: str = Field(..., min_length=1)
    status_code: str = Field(..., min_length=1)
    campaign_id: Optional[str] = None
    error_code: Optional[str] = None
    error_name: Optional[str] = None
    error_description: Optional[str] = None

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        campaign_id = values.get("campaign_id")
        if company_id and not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if campaign_id and not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        if other_errors:
            raise ValueError(other_errors)
        if not campaign_id:
            values.pop("campaign_id")
        return values


class SaveResponse(BaseModel):
    payload: dict = Field(...)
    response: APIResponseSchema = Field(...)

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        payload = values.get("payload")
        if not payload:
            other_errors.append("provide valid payload")
        if other_errors:
            raise ValueError(other_errors)
        return values


class UpdateBatchRecord(BaseModel):
    table: str = Field(..., min_length=1)
    set_clause: dict = Field(...)
    from_values: conlist(str, min_items=1)
    from_columns: conlist(str, min_items=1)
    from_alias_name: str = Field(..., min_length=1)
    where: dict = Field(...)

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        where = values.get("where")
        set_clause = values.get("set_clause")
        if not set_clause:
            other_errors.append("provide valid set clause")
        if not where:
            other_errors.append("provide valid where clause")
        if other_errors:
            raise ValueError(other_errors)
        return values


class SaveBatchResponse(BaseModel):
    payload: dict = Field(...)
    insert_list: conlist(APIResponseSchema, min_items=1)

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        payload = values.get("payload")
        if not payload:
            other_errors.append("provide valid payload")
        if other_errors:
            raise ValueError(other_errors)
        return values


class ReportSchema(BaseModel):
    campaign_id: str = Field(..., min_length=1)
    channel: Channel
    company_id: str = Field(..., min_length=1)
    delivery_status: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    template_name: str = Field(..., min_length=1)
    email_subject: Optional[str]

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        campaign_id = values.get("campaign_id")
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        if other_errors:
            raise ValueError(other_errors)
        return values


class GetCampaignData(BaseModel):
    campaign_id: str = Field(..., min_length=1)
    channel: Channel
    updated_end_time_flag: Optional[bool] = False
    is_deleted: Optional[bool] = False
    company_id: Optional[str]
    trigger_report_flag: Optional[bool] = False
    masking: Optional[bool] = False
    profile_id: Optional[str] = None

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        campaign_id = values.get("campaign_id")
        if not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        if other_errors:
            raise ValueError(other_errors)
        return values


class GetBatchData(BaseModel):
    batch_id: str = Field(..., min_length=1)
    channel: Optional[str] = None
    type: BatchType

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        channel = values.get("channel")
        batch_id = values.get("batch_id")
        if channel and channel not in (BATCH_CHANNELS):
            other_errors.append(f"provide valid channel")
        if not is_valid_uuid(batch_id):
            other_errors.append(f"provide valid company id")
        if other_errors:
            raise ValueError(other_errors)
        return values


class FilterSchema(BaseModel):
    filter_author: List[str] = []
    filter_channel: List[str] = []
    filter_duration: dict = {}


class CampaignDetails(BaseModel):
    company_id: str = Field(..., min_length=1)
    page_number: Optional[int] = DEFAULT_PAGE_number
    page_size: Optional[int] = DEFAULT_PAGE_SIZE
    search_type: Optional[str] = None
    query_arg: Optional[str] = None
    filter: Optional[FilterSchema] = None
    is_deleted: Optional[bool] = False
    parent_campaign_id: Optional[str] = None
    is_master_campaign_request: Optional[bool] = False

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if values["page_number"] <= 0:
            other_errors.append(f"provide valid page number")
        if values["page_size"] <= 0:
            other_errors.append(f"provide valid page size")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignSummary(BaseModel):
    campaign_id: str = Field(..., min_length=1)
    channel: Channel
    company_id: str = Field(..., min_length=1)
    is_deleted: Optional[bool] = False
    completion_summary: Optional[bool] = False
    created: str = Field(..., min_length=1)

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        campaign_id = values.get("campaign_id")
        created = values.get("created")
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        try:
            created = datetime.datetime.strptime(created, "%Y-%m-%d")
        except Exception as e:
            other_errors.append("provide valid campaign creation date")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignUpdate(BaseModel):
    company_id: str = Field(..., min_length=1)
    campaign_ids: str = Field(..., min_length=1)
    campaign_count_export: List[dict] = []

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignCount(BaseModel):
    table: str = Field(..., min_length=1)
    campaign_id: str = Field(..., min_length=1)
    is_deleted: Optional[bool] = False

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        campaign_id = values.get("campaign_id")
        if not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignFilter(BaseModel):
    company_id: Optional[str] = None
    is_deleted: Optional[bool] = False
    is_master_campaign_request = False

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        if not company_id or not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignErrors(BaseModel):
    company_id: Optional[str]
    campaign_id: Optional[str]
    channel: Optional[Channel]
    count: Optional[bool] = False

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        campaign_id = values.get("campaign_id")
        company_id = values.get("company_id")
        channel = values.get("channel")
        valid_channels = [channel.value for channel in Channel]
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        if not channel or channel not in valid_channels:
            other_errors.append(f"provide valid channel")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignErrorsV1(BaseModel):
    company_id: str = Field(..., min_length=1)
    campaign_id: str = Field(..., min_length=1)
    channel: Channel
    count: Optional[bool] = False
    errors: Optional[dict] = {}

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        campaign_id = values.get("campaign_id")
        company_id = values.get("company_id")
        channel = values.get("channel")
        valid_channels = [channel.value for channel in Channel]
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        if not channel or channel not in valid_channels:
            other_errors.append(f"provide valid channel")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignExport(BaseModel):
    company_id: str
    campaign_id: str
    channel: str
    template_name: str
    name: Optional[str] = None
    delivery_status: Optional[str] = None

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        campaign_id = values.get("campaign_id")
        company_id = values.get("company_id")
        channel = values.get("channel")
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        if not channel:
            other_errors.append(f"provide valid channel")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignReattempt(BaseModel):
    company_id: str = Field(..., min_length=1)
    campaign_id: str = Field(..., min_length=1)
    channel: Channel
    reattempt_on: Optional[dict] = {}

    class Config:
        use_enum_values = True

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        campaign_id = values.get("campaign_id")
        company_id = values.get("company_id")
        reattempt_on = values.get("reattempt_on", {})
        reattempt_on_keys = reattempt_on.keys()
        reattempt_errors = [error.value for error in ReattemptErrors]

        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if not is_valid_uuid(campaign_id):
            other_errors.append(f"provide valid campaign id")
        if reattempt_on and any(error not in reattempt_errors for error in reattempt_on_keys):
            other_errors.append(f"provide value reattempt_on value")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignCancel(BaseModel):
    company_id: str = Field(..., min_length=1)
    campaign_id: str = Field(..., min_length=1)

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        if not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if other_errors:
            raise ValueError(other_errors)
        return values


class CampaignStatus(BaseModel):
    company_id: Optional[str] = None
    campaign_id: Optional[str] = None

    @root_validator(pre=False)
    def validate_data(cls, values):
        other_errors = []
        company_id = values.get("company_id")
        if not company_id or not is_valid_uuid(company_id):
            other_errors.append(f"provide valid company id")
        if not values.get("campaign_id"):
            other_errors.append(f"provide valid campaign id")
        if other_errors:
            raise ValueError(other_errors)
        return values
