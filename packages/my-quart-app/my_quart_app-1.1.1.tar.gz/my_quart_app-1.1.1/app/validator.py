from marshmallow import (
    Schema,
    fields,
    ValidationError,
    validates_schema,
    INCLUDE,
    validate,
)
from .choices import (
    CHANNELS,
    SEND_TO,
    COMMUNICATION_LEVEL,
    BATCH_TYPE,
    BATCH_CHANNELS,
    APPLICANT_TYPE,
    REMINDER_OFFSET_TYPE,
    NOTIFY_TYPE,
    RESULT_CODE,
    NOTIFICATION_SOURCE,
    TypeOfTaskChoices,
)


class CampaignDataInput(Schema):
    class Meta:
        unknown = INCLUDE

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="name should not be empty string"),
        error_messages={"required": "name data is required"},
    )
    channel = fields.Str(
        required=True,
        validate=validate.OneOf(CHANNELS),
        error_messages={"required": "channel is required"},
    )
    type = fields.Str(
        required=True,
        validate=validate.OneOf(["communication"]),
        error_messages={"required": "channel is required"},
    )
    description = fields.Str()


class CampaignInput(Schema):
    class Meta:
        unknown = INCLUDE

    campaign_data = fields.Nested(
        CampaignDataInput,
        required=True,
        error_messages={"required": "campaign data is required"},
    )
    loan_data = fields.List(
        fields.String(),
        required=True,
        validate=validate.Length(min=1, error="loan data should not be empty"),
        error_messages={"required": "loan data is required"},
    )
    comm_dict = fields.Dict()
    additional_loan_data = fields.Dict()
    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    template_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="template id should not be empty string"),
        error_messages={"required": "template id is required"},
    )
    # allocation_month = fields.DateTime(
    #     required=True,
    #     format='%Y-%m-%d',
    #     error_messages={"required": "Allocation month is required"}
    # )
    allocation_month = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="allocation month should not be empty"),
        error_messages={"required": "Allocation month is required"},
    )
    upto_index = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="upto index should not be empty string"),
        error_messages={"required": "upto index is required"},
    )
    send_to = fields.Str(
        required=True,
        validate=[
            validate.OneOf(SEND_TO),
            validate.Length(min=1, error="send to should not be empty string"),
        ],
        error_messages={"required": "send to is required"},
    )
    communication_level = fields.Str(
        required=True,
        validate=validate.OneOf(COMMUNICATION_LEVEL),
        error_messages={"required": "communication level is required"},
    )

    @validates_schema
    def validate_data(self, data, **kwargs):
        other_errors = []
        campaign_data = data.get("campaign_data", None)
        comm_dict = data.get("comm_dict", None)
        if comm_dict in (None, {}) and campaign_data["channel"] != "dtmf_ivr":
            other_errors.append("Comm dict is required")
        if other_errors:
            raise ValidationError({"message": other_errors})


class APIResponseInput(Schema):
    class Meta:
        unknown = INCLUDE

    status = fields.Str(required=True)
    response = fields.Str(required=True)
    loan_id = fields.Str(required=True)
    status_code = fields.Str(required=True)
    tracking_number = fields.Str()
    company_id = fields.UUID()
    campaign_id = fields.Str()


class GetBatchData(Schema):
    class Meta:
        unkown = INCLUDE

    batch_id = fields.List(
        fields.String(),
        validate=validate.Length(min=1, error="Please provide valid value"),
        required=True,
    )
    company_id = fields.UUID()


class UpdateRecordData(Schema):
    class Meta:
        unknown = INCLUDE

    table = fields.Str(required=True)
    set_clause = fields.Dict(required=True)
    from_values = fields.List(
        fields.String(),
        validate=validate.Length(min=1, error="Please provide valid value"),
        required=True,
    )
    from_columns = fields.List(
        fields.String(),
        validate=validate.Length(min=2, error="Please provide valid value for columns"),
        required=True,
    )
    from_alias_name = fields.Str(required=True)
    where = fields.Dict(required=True)


class ResponseInput(Schema):
    class Meta:
        unknown = INCLUDE

    payload = fields.Dict(required=True, error_messages={"required": "payload is required"})
    response = fields.Nested(
        APIResponseInput,
        required=True,
        error_messages={"required": "response is required"},
    )

    @validates_schema
    def validate_data(self, data, **kwargs):
        other_errors = []
        payload = data.get("payload")
        response = data.get("response")
        if payload.get("type", "") == TypeOfTaskChoices.scrape.value and (not "tracking_number" in response):
            other_errors.append("Please provide valid tracking number")
        if payload.get("type", "") == TypeOfTaskChoices.scrape.value and (not "company_id" in response):
            other_errors.append("Please provide valid company id")
        if other_errors:
            raise ValidationError({"error": other_errors})


class ResponseBatchInput(Schema):
    class Meta:
        unknown = INCLUDE

    payload = fields.Dict(required=True, error_messages={"required": "payload is required"})
    insert_list = fields.List(
        fields.Nested(APIResponseInput),
        required=True,
        error_messages={"required": "insert list is required"},
    )


class ReportInput(Schema):
    class Meta:
        unknown = INCLUDE

    campaign_id = fields.UUID(required=True, error_messages={"required": "campaign id is required"})
    channel = fields.Str(
        required=True,
        validate=validate.OneOf(CHANNELS),
        error_messages={"required": "channel is required"},
    )
    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})


class GetCampaignInput(Schema):
    class Meta:
        unknown = INCLUDE

    campaign_id = fields.UUID(required=True, error_messages={"required": "campaign id is required"})
    channel = fields.Str(
        required=True,
        validate=[
            validate.OneOf(CHANNELS),
            validate.Length(min=1, error="channel should not be empty string"),
        ],
        error_messages={"required": "channel is required"},
    )

    @validates_schema
    def validate_data(self, data, **kwargs):
        other_errors = []
        if not data.get("channel", None) or data.get("channel", "") not in CHANNELS:
            other_errors.append("Please select valid channel")
        if other_errors:
            raise ValidationError({"message": other_errors})


class GetBatchInput(Schema):
    class Meta:
        unknown = INCLUDE

    batch_id = fields.UUID(required=True, error_messages={"required": "campaign id is required"})
    channel = fields.Str(required=True, error_messages={"required": "channel is required"})
    type = fields.Str(
        required=True,
        validate=[
            validate.OneOf(BATCH_TYPE),
            validate.Length(min=1, error="type should not be empty string"),
        ],
        error_messages={"required": "type is required"},
    )

    @validates_schema
    def validate_data(self, data, **kwargs):
        other_errors = []
        channel = data.get("channel", "")
        if channel and channel not in (BATCH_CHANNELS):
            other_errors.append(f"Please provide valid channel")


class BatchOperationInput(Schema):
    class Meta:
        unknown = INCLUDE

    type = fields.Str(
        required=True,
        validate=validate.OneOf(BATCH_TYPE, error="Please provide valid type"),
        error_messages={"required": "type is required"},
    )
    channel = fields.Str(
        # validate=validate.OneOf(BATCH_CHANNELS, error = 'Please provide valid channel'),
        # error_messages={"required": "channel is required"}
    )

    @validates_schema
    def validate_data(self, data, **kwargs):
        other_errors = []
        type = data.get("type", "")
        channel = data.get("channel", "")
        is_linked_loan = data.get("is_linked_loan", False)
        if channel and channel not in (BATCH_CHANNELS):
            other_errors.append(f"Please provide valid channel")
        elif type == TypeOfTaskChoices.scrape.value and channel not in (
            TypeOfTaskChoices.indiapost_upload.value,
            TypeOfTaskChoices.indiapost_tracking.value,
        ):
            other_errors.append(f"Please provide valid channel")
        elif type == TypeOfTaskChoices.notice.value and (
            channel
            not in (
                TypeOfTaskChoices.linked_loan_digital.value,
                TypeOfTaskChoices.digital.value,
                TypeOfTaskChoices.physical.value,
                TypeOfTaskChoices.linked_loan_physical.value,
            )
        ):
            other_errors.append(f"Please provide valid channel")
        elif (
            type
            not in (
                TypeOfTaskChoices.notice.value,
                TypeOfTaskChoices.scrape.value,
                TypeOfTaskChoices.ecourt_tracking.value,
            )
        ) and (channel or data.get("channel", None) == ""):
            other_errors.append(f"channel is not required for type:{type}")
        if type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_upload.value:
            result = IndiapostUploadQueue().validate(data)
            if result != {}:
                other_errors.append(result)
        if type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_tracking.value:
            result = IndiapostTrackingQueue().validate(data)
            if result != {}:
                other_errors.append(result)
        if type == TypeOfTaskChoices.notice.value and channel == TypeOfTaskChoices.digital.value:
            if is_linked_loan:
                result = LinkedLoanQueue().validate(data)
            else:
                result = DigitalNoticeQueue().validate(data)
            if result != {}:
                other_errors.append(result)
        if type == TypeOfTaskChoices.lat_long_conversion.value:
            result = LatLongConversionQueue().validate(data)
            if result != {}:
                other_errors.append(result)
        if type == TypeOfTaskChoices.upload_c2c_disposition.value:
            result = UploadDispositionQueue().validate(data)
            if result != {}:
                other_errors.append(result)
        if type == TypeOfTaskChoices.optin.value:
            result = OptinQueue().validate(data)
            if result != {}:
                other_errors.append(result)
        if type == TypeOfTaskChoices.notifications.value:
            result = NotificationsQueue().validate(data)
            if result != {}:
                other_errors.append(result)
            if data.get("notify_type", "") == "reminder" and (not data.get("reminder_offset")):
                other_errors.append(f"reminder offset is required for notify_type: reminder")
            if data.get("notify_type", "") == "reminder" and (not data.get("reminder_offset_type")):
                other_errors.append(f"reminder offset type is required for notify type: reminder")
        if other_errors:
            raise ValidationError({"error": other_errors})


class NotificationsData(Schema):
    class Meta:
        unknown = INCLUDE

    message = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid message"),
        error_messages={"required": "message is required"},
    )


class NotificationsQueue(Schema):
    class Meta:
        unknown = INCLUDE

    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    source = fields.Str(
        required=True,
        validate=validate.OneOf(NOTIFICATION_SOURCE, error="Please provide valid source"),
        error_messages={"required": "source is required"},
    )
    notify_type = fields.Str(
        required=True,
        validate=validate.OneOf(NOTIFY_TYPE, error="Please provide valid notify type"),
        error_messages={"required": "notify type is required"},
    )
    reminder_offset_type = fields.Str(
        validate=validate.OneOf(REMINDER_OFFSET_TYPE, error="Please provide valid reminder offset type")
    )
    trigger_time = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid trigger time"),
        error_messages={"required": "trigger time is required"},
    )
    reminder_offset = fields.List(fields.Integer(strict=True))
    loan_data = fields.List(
        fields.Nested(NotificationsData),
        required=True,
        error_messages={"required": "Loan data is required"},
    )


class OptinQueue(Schema):
    class Meta:
        unknown = INCLUDE

    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    loan_data = fields.List(
        fields.String(),
        validate=validate.Length(min=1, error="No loan ids provided"),
        required=True,
        error_messages={"required": "loan data is required"},
    )


class UploadDispositionData(Schema):
    class Meta:
        unknown = INCLUDE

    loan_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid loan id"),
        error_messages={"required": "loan id is required"},
    )
    agent_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid agent id"),
        error_messages={"required": "agent id is required"},
    )
    rec_url = fields.Str(required=True, error_messages={"required": "rec_url is required"})
    to_mobile = fields.Str(required=True, error_messages={"required": "to_mobile key is required"})
    call_duration = fields.Str(required=True, error_messages={"required": "call duration is required"})
    call_type = fields.Str()
    call_status = fields.Str()
    call_start_time = fields.Str(required=True, error_messages={"required": "call start time is required"})
    call_end_time = fields.Str(required=True, error_messages={"required": "call end time is required"})
    campaign_id = fields.Str(
        required=True,
        allow_none=True,
        error_messages={"required": "campaign id is required"},
    )
    result_code = fields.Str(
        required=True,
        validate=validate.OneOf(RESULT_CODE, error="Please provide valid result code"),
        error_messages={"required": "result code is required"},
    )


class UploadDispositionQueue(Schema):
    class Meta:
        unknown = INCLUDE

    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    loan_data = fields.List(
        fields.Nested(UploadDispositionData),
        required=True,
        error_messages={"required": "Loan data is required"},
    )


class LatLongConversionData(Schema):
    class Meta:
        unknown = INCLUDE

    loan_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid loan id"),
        error_messages={"required": "loan id is required"},
    )
    address = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid address"),
        error_messages={"required": "address is required"},
    )
    applicant_index = fields.Integer(
        strict=True,
        required=True,
        allow_none=True,
        error_messages={"required": "applicant_index is required"},
    )
    address_index = fields.Integer(
        strict=True,
        required=True,
        error_messages={"required": "address_index is required"},
    )


class LatLongConversionQueue(Schema):
    class Meta:
        unknown = INCLUDE

    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    applicant_type = fields.Str(
        required=True,
        validate=validate.OneOf(APPLICANT_TYPE, error="Please provide valid applicant_type"),
        error_messages={"required": "applicant_type is required"},
    )
    loan_data = fields.List(
        fields.Nested(LatLongConversionData),
        required=True,
        error_messages={"required": "Loan data is required"},
    )


class LinkedLoanDataInput(Schema):
    class Meta:
        unknown = INCLUDE

    linked_loan_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid linked_loan_id"),
        error_messages={"required": "linked_loan_id is required"},
    )
    loan_ids = fields.List(
        fields.String(),
        validate=validate.Length(min=1, error="No loan ids provided"),
        required=True,
        error_messages={"required": "loan ids is required"},
    )


class LinkedLoanQueue(Schema):
    class Meta:
        unknown = INCLUDE

    draft_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid draft id"),
        error_messages={"required": "Please provide Draft id"},
    )
    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    creditline = fields.Str()
    delivery_partner = fields.Str()
    allocation_month = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid allocation month"),
        error_messages={"required": "Allocation month is required"},
    )
    all_applicants = fields.Str()
    co_applicant = fields.Str()
    loan_data = fields.List(
        fields.Nested(LinkedLoanDataInput),
        required=True,
        error_messages={"required": "Loan data is required"},
    )


class DigitalNoticeQueue(Schema):
    class Meta:
        unknown = INCLUDE

    draft_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid draft id"),
        error_messages={"required": "Please provide Draft id"},
    )
    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    creditline = fields.Str()
    delivery_partner = fields.Str()
    allocation_month = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid allocation month"),
        error_messages={"required": "Allocation month is required"},
    )
    all_applicants = fields.Str()
    co_applicant = fields.Str()
    loan_data = fields.List(
        fields.String(),
        validate=validate.Length(min=1, error="No loan ids provided"),
        required=True,
        error_messages={"required": "loan data is required"},
    )


class IndiapostUploadData(Schema):
    class Meta:
        unknown = INCLUDE

    loan_id = fields.Str(validate=validate.Length(min=1, error="Please provide valid loan id"))
    customer_name = fields.Str()
    customer_address1 = fields.Str()
    customer_address2 = fields.Str()
    customer_address3 = fields.Str()
    customer_city = fields.Str()
    pin_code = fields.Str()
    customer_state = fields.Str()
    notice_id = fields.Str()
    tracking_no = fields.Str()


class IndiapostUploadQueue(Schema):
    class Meta:
        unknown = INCLUDE

    notice_type = fields.Str()
    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    allocation_month = fields.Str()
    loan_data = fields.List(fields.Nested(IndiapostUploadData))


class IndiapostTrackingData(Schema):
    class Meta:
        unknown = INCLUDE

    loan_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid loan id"),
        error_messages={"required": "loan id is required"},
    )
    company_id = fields.UUID(required=True, error_messages={"required": "company id is required"})
    tracking_id = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Please provide valid tracking id"),
        error_messages={"required": "tracking id is required"},
    )


class IndiapostTrackingQueue(Schema):
    class Meta:
        unknown = INCLUDE

    loan_data = fields.List(fields.Nested(IndiapostTrackingData))
