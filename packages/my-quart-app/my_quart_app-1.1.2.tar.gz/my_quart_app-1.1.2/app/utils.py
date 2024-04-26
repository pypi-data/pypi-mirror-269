"""
Utils.py
Usage: Serves Utility
"""
import boto3
import json
import requests
import logging
import shortuuid
import urllib
import re

from datetime import timedelta, datetime
from pathlib import Path
from functools import wraps
from quart import current_app as app, make_response, request
import uuid
from .choices import (
    ReminderOffsetTypeChoices,
    ErrorCodeMessages,
    CAMPAIGN_SUMMARY_CHOICES,
    COMPLETION_SUMMARY_CHOICES,
    COLOR_CODING,
    ERROR_FIELDS_COUNT,
    ERROR_DICT_MAPPING,
    PROD_ENV,
    ExportServiceCallType,
    MODULE,
    SOURCE,
)
from .settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_DEFAULT_REGION,
    COMMUNICATION_SERVICE_BASE_URL,
    LITIGATION_SERVICE_BASE_URL,
    SENDGRID_API_KEY,
    USER_SERVICE_BASE_URL,
    ENV,
    REPORT_SENDGRID_TEMPLATE_ID,
)
from http import HTTPStatus
from phonenumbers.phonenumberutil import region_code_for_country_code
from pytz import country_timezones, timezone
from cg_utils import mask_data


logger = logging.getLogger(__name__)


class BadEnvException(Exception):
    def __init__(self, message):
        self.errorCode = 501
        self.errorMessage = message
        return


class VerifyEnv:
    def __init__(self):
        self.used_configs = [
            "LOG_LEVEL",
            "POSTGRES",
            "APP_NAME",
            "REDIS",
            "USER_SERVICE_BASE_URL",
        ]

    def verify(self):
        unverified_envs = []
        success = True
        for i in self.used_configs:
            env_var = app.config.get(i, None)
            if env_var is None or "":
                unverified_envs.append(i)
                success = False

        return success, unverified_envs


def is_nullish(data_to_check: tuple) -> bool:
    nullish = ("", None, "null")
    for data in data_to_check:
        if data in nullish:
            return True
    return False


def _dict_key_filter(d, keys):
    return {k: v for k, v in d.items() if k not in keys}


def _make_batch(iterable, n=1):
    count = 1
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


def api_payload_validator(schema):
    """
    return response for request payload
    {
        "message": "success",
        "output": "Address conversion assigned to queue successfully",
        "data":
    }, 200
    """

    def innerfunc(func):
        @wraps(func)
        async def innerfunc1(*args, **kwargs):
            request_data = await request.get_data()
            request_data = json.loads(request_data)
            validation_errors = schema().validate(request_data)
            if validation_errors:
                return await make_response(
                    json.dumps(
                        {
                            "message": "failed",
                            "output": "payload is not valid",
                            "data": validation_errors,
                        }
                    ),
                    400,
                )
            return await func(*args, **kwargs)

        return innerfunc1

    return innerfunc


#############################################################################################
######################## Notifications methods ##############################################
#############################################################################################


def datetime_offset(trigger_time: str, reminder_offset_type: str, reminder_offset: list, now_time):
    offset_resolved_list = []
    for offset in reminder_offset:
        if reminder_offset_type == ReminderOffsetTypeChoices.minutes.value:
            offset_time = trigger_time - timedelta(minutes=offset)
        elif reminder_offset_type == ReminderOffsetTypeChoices.hours.value:
            offset_time = trigger_time - timedelta(hours=offset)
        elif reminder_offset_type == ReminderOffsetTypeChoices.days.value:
            offset_time = trigger_time - timedelta(days=offset)
        print(f"trigger_time - {offset_time} now_time - {now_time}")
        if not offset_time < now_time:
            offset_resolved_list.append((offset_time - now_time).seconds)

    print(f"utils.datetime_offset :: {offset_resolved_list}")
    return offset_resolved_list


def create_directory_if_not_exists(directory: str):
    return Path(directory).mkdir(parents=True, exist_ok=False)


def delete_file_if_exists(file_path: str):
    return Path(file_path).unlink(missing_ok=True)


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
        endpoint_url="https://s3."+AWS_DEFAULT_REGION+".amazonaws.com",
    )


def send_mail_api(payload: dict, token: str, role: str, request_id):
    base_url = COMMUNICATION_SERVICE_BASE_URL
    url = f"{base_url}/mail"

    headers = {
        "authenticationtoken": token,
        "role": role,
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-Request-ID": str(request_id),
    }
    try:
        result = requests.request(
            method="POST",
            url=url,
            headers=headers,
            json=payload,
        )
        logger.info(f"send_mail_api.result.text: {result.text}")

        data = json.loads(result.text)
        status = data.get("status")
        logger.info(f"send_mail_api.result.status: {status}")
    except Exception as e:
        logger.info(f"send_mail_api.result.exception: {str(e)}")
        return False
    return True


def sendgrid_api(payload: dict):
    logger.info(f"sendgrid_api")
    unique_mail_id = shortuuid.ShortUUID().random(length=8)
    headers = {
        "authorization": f"Bearer {SENDGRID_API_KEY}",
        "content-type": "application/json",
        "Accept": "application/json",
    }
    try:
        mail_data = {
            "from": payload["from_data"],
            "subject": payload["subject"],
            "personalizations": [
                {
                    "to": [{"email": payload["to_email"]}],
                    "custom_args": {"unique_mail_id": unique_mail_id},
                }
            ],
            "content": [{"type": "text/html", "value": payload["email_body"]}],
            "reply_to": {"email": "reports@credgenics.com"},
        }
        response = requests.request(
            method="POST",
            url="https://api.sendgrid.com/v3/mail/send",
            data=json.dumps(mail_data),
            headers=headers,
        )
        logger.info(f"sendgrid_api.response {response}")
        if response.status_code != HTTPStatus.ACCEPTED.value:
            return False
    except Exception as e:
        logger.info(f"send_mail_api.result.exception: {str(e)}")
        return False
    return True


def format_api_response_text(response):
    logger.info(f"format_api_response")
    status_code = response.status_code
    res_text = response.text
    if res_text and status_code != 500:
        return str(res_text)
    elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value:
        return ErrorCodeMessages.internal_server_error.value
    elif status_code == HTTPStatus.REQUEST_TIMEOUT.value:
        return ErrorCodeMessages.request_timeout.value
    elif status_code == HTTPStatus.BAD_GATEWAY.value:
        return ErrorCodeMessages.bad_gateway.value
    elif status_code == HTTPStatus.GATEWAY_TIMEOUT.value:
        return ErrorCodeMessages.gateway_timeout.value


def get_campaign_summary(
    campaign_export_output: dict,
    channel: str,
    failed_count=0,
    attempted_live=False,
    trigger_errors=[],
    completion_summary: bool = False,
) -> dict:
    """_summary_

    Args:
        campaign_export_output (dict): webhook details of a campaign
        channel (str): type of communication
        completion_summary (bool): true if the summary is to be created for campaign completion report

    Returns:
        dict: returns summary of a campaign
    """
    campaign_summary = {}
    campaign_export_errors = []
    if campaign_export_output.get("error_counts") and isinstance(campaign_export_output.get("error_counts"), list):
        campaign_export_errors = campaign_export_output["error_counts"]
    if trigger_errors:
        campaign_export_errors.extend(trigger_errors)
    triggered_count = campaign_export_output.get("triggered_count", 0)
    if attempted_live:
        campaign_summary["attempted"] = failed_count + triggered_count
    campaign_summary["triggered"] = triggered_count
    if completion_summary:
        campaign_summary_keys = COMPLETION_SUMMARY_CHOICES.get(channel, None)
    else:
        campaign_summary_keys = CAMPAIGN_SUMMARY_CHOICES.get(channel, None)
    if campaign_summary_keys:
        campaign_summary_keys = campaign_summary_keys.split(",")
        for key in campaign_summary_keys:
            campaign_summary[key] = campaign_export_output.get(f"{key}_count", 0)
    if not completion_summary:
        campaign_summary["error_counts"] = []
        if campaign_export_errors:

            sorted_error_items = sorted(
                campaign_export_errors,
                key=lambda item: item["count"],
                reverse=True,
            )
            sorted_error_items_length = len(sorted_error_items)

            campaign_summary["error_counts"] = get_pie_chart_formatted_data(sorted_error_items[:ERROR_FIELDS_COUNT])
            if sorted_error_items_length > ERROR_FIELDS_COUNT:
                others = {}
                others["id"] = "others"
                others["label"] = "others"
                others["value"] = sum(
                    list(
                        map(
                            lambda x: x["count"],
                            sorted_error_items[ERROR_FIELDS_COUNT:],
                        )
                    )
                )
                campaign_summary["error_counts"].append(others)
            campaign_summary["colors"] = COLOR_CODING

    return campaign_summary


def get_pie_chart_formatted_data(data):
    result = []
    for error in data:
        sub_data = {}
        for k1, k2 in ERROR_DICT_MAPPING.items():
            if k2 == "error_name":
                error[k2] = " ".join(list(error[k2].split("_")))
            sub_data[k1] = error[k2]
        result.append(sub_data)
    return result


def encode_param(data):
    encoded_data = urllib.parse.quote(data, safe=" ")
    return encoded_data


def list_chunker(data, chunk_size):
    """splits a list into chunks of size chunk_size

    Args:
        data(list): list to split
        chunk_size (int): chunk size
    Returns:
        data(list): list of chunks
    """
    return list(data[index : index + chunk_size] for index in range(0, len(data), chunk_size))


def create_query(
    table,
    set_clause,
    from_values_list,
    from_columns_list,
    from_alias_name,
    where,
    operation,
):
    """creates a single update query

    Args:
        table(string): name of table,
        set_clause(dict): columns to be updated,
        from_values_list(list): list of values to be updated,
        from_columns_list(list): columns to be used in update query
        from_alias_name(string): alias name for values to be updated,
        where(dict) : columns to be used in where condition,
        operation(string): operation to be performed
    Returns:
        query(string): update query

    Sample query:
        update table_name
        set column = nv.column
        from
            ( values
                (12, 'EURO'),
                (18, 'DOLLAR'),
                (13, 'Pound')
            ) as nv (id, column)
        where account.id = nv.id ;
    """
    query = ""
    set_clause_list = []
    where_list = []
    if operation.lower() == "update":
        for key, value in set_clause.items():
            set_clause_list.append(f"{key} = {from_alias_name}.{value}")
        for key, value in where.items():
            where_list.append(f"{table}.{key} = {from_alias_name}.{value}")
        if set_clause_list:
            set_clause = ",".join(set_clause_list)
            from_values = ",".join(from_values_list)
            where_clause = " and ".join(where_list)
            from_columns = ",".join(from_columns_list)
            query = f""" update {table} set {set_clause} from (values {from_values}) as {from_alias_name} ({from_columns}) where {where_clause};
            """
    return query


def get_users_details(company_id, user_ids, user, request_id, company_details):
    user_details = {"user_emails": [], "user_numbers": [], "profile_id": None}
    user_id_list = user_ids.split(",")
    user_emails = []
    user_numbers = []
    url = f"{USER_SERVICE_BASE_URL}/internal/company/users"
    payload = {
        "company_id": company_id,
        "user_ids": user_id_list,
        "include_chief_admin": True,
    }
    users = requests.request(
        method="POST",
        url=url,
        data=json.dumps(payload),
        headers={
            "Content-Type": "application/json",
            "X-CG-User": json.dumps(user),
            "X-Request-ID": request_id,
            "X-CG-Company": json.dumps(company_details),
        },
    )
    if users.status_code != HTTPStatus.OK.value:
        user_list = []
    else:
        try:
            user_list = json.loads(users.text)["data"]["users"]
        except Exception as e:
            user_list = []
    sms_mobile_data = {}
    if user_list:
        for user in user_list:
            if user["user_id"] == user_id_list[0]:
                user_details["author_profile_id"] = user["profile_id"]
            if user.get("email"):
                user_emails.append(user.get("email"))

            if user.get("country_isd_code") not in sms_mobile_data and user.get("mobile"):
                sms_mobile_data[user.get("country_isd_code")] = []

            if user.get("mobile"):
                sms_mobile_data[user.get("country_isd_code")].append(user.get("mobile"))

    user_details["user_emails"] = user_emails
    user_details["user_numbers"] = sms_mobile_data
    return user_details


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))

        return True
    except ValueError:
        return False


async def get_current_datetime(country_isd_code):
    country_isd_code = int(country_isd_code.replace("+", ""))
    country_code = region_code_for_country_code(country_isd_code)
    time_zone = country_timezones[country_code][0]
    current_datetime = datetime.now().astimezone(timezone(time_zone))
    return current_datetime


def validate_email(email: str):
    """
    verify belows list of emails
    mynam.dewe.ew@google.co.in
    tarun.kumar.1234@gmail.com
    tarun.kumar@credgenics.com
    dantala.satish@stfc.co.in
    anand.andy.139@gmail.com
    """
    pattern = "^[a-zA-Z0-9._-]+[@]\w+[-]?\w+([.]\w{2,20}){1,}$"
    if re.search(pattern, email):
        return True
    else:
        return False


def format_email_dict(email_list):
    return list(map(lambda email: {"email": email}, email_list))


def get_export_mail_data_helper(export_task, presigned_url, company_trademark, service=None):
    logger.info(f"get_export_mail_data_helper.export_task:{export_task}")
    export_metadata = export_task.get("data")
    if export_metadata and not isinstance(export_metadata, dict):
        export_metadata = json.loads(export_metadata)
    to = [{"email": export_task.get("author_email")}]
    cc = [{"email": "demo.agent@credgenics.com", "name": "Demo Agent"}]
    bcc = []
    logger.info(f"get_export_mail_data_helper.service:{service}")
    template_id = REPORT_SENDGRID_TEMPLATE_ID
    if service and service == ExportServiceCallType.DELIVERY_REPORT_CONSUMER.value:
        campaign_author_emails = export_metadata.get("campaign_author_emails", [])
        to = format_email_dict(campaign_author_emails)
        cc.extend(format_email_dict(export_metadata.get("cc_emails", [])))
        bcc = format_email_dict(export_metadata.get("bcc_emails", []))
        template_id = export_metadata.get("template_id")
    logger.debug(
        f"get_export_mail_data_helper.cc:{cc},get_export_mail_data_helper.bcc:{bcc},get_export_mail_data_helper.to:{to},get_export_mail_data_helper.template_id:{template_id}"
    )
    return get_mail_data(
        export_task=export_task,
        presigned_url=presigned_url,
        company_trademark=company_trademark,
        export_metadata=export_metadata,
        template_id=template_id,
        to=to,
        cc=cc,
        bcc=bcc,
    )


def get_mail_data(export_task, presigned_url, company_trademark, export_metadata, template_id, to, cc=None, bcc=None):
    mail_data = {
        "from": {
            "name": f"{export_task['export_category'].replace('_',' ').capitalize()}",
            "email": "reports@credgenics.com",
        },
        "personalizations": [
            {
                "to": to,
                "dynamic_template_data": {
                    "report_url": presigned_url,
                    "company": company_trademark,
                    "campaign_id": export_metadata.get("campaign_id"),
                    "channel": export_metadata.get("channel").replace("_", " ").capitalize(),
                    "status": export_metadata.get("delivery_status"),
                    "template_name": export_metadata.get("template_name"),
                    "campaign_name": export_metadata.get("name"),
                    "rule_name": export_metadata.get("rule_name"),
                    "filters": export_metadata.get("filters"),
                    "range": export_metadata.get("range"),
                    "campaign_link": export_metadata.get("campaign_link"),
                    "camapign_summary_keys": export_metadata.get("camapign_summary_keys"),
                    "camapign_summary_values": export_metadata.get("camapign_summary_values"),
                    "subject": export_metadata.get("subject"),
                    "warning": export_metadata.get("warning"),
                    "triggered_time": export_metadata.get("triggered_time").split(".")[0]
                    if export_metadata.get("triggered_time")
                    else "",
                    "env": ENV if str(ENV).lower() != PROD_ENV else None,
                },
            }
        ],
        "template_id": template_id,
        "source": SOURCE,
        "module": MODULE,
    }
    if cc:
        mail_data["personalizations"][0]["cc"] = cc
    if bcc:
        mail_data["personalizations"][0]["bcc"] = bcc
    return mail_data


async def execute_db_query(query, db_instance):
    app.logger.info(f"app.utils.execute_db_query")
    status_code = HTTPStatus.OK.value
    message = "Records fetched successfully"
    data = []
    try:
        app.logger.debug(f"app.utils.execute_db_query.query:: {query}")
        data = await db_instance.execute_raw_select_query(query)
        app.logger.debug(f"app.utils.execute_db_query.data :: {data}")

    except Exception as e:
        app.logger.error(f"app.utils.execute_db_query.exception {str(e)}")
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        message = f"Failed to fetch campaign error records. {str(e)}"
        data = []

    if not isinstance(data, list) or isinstance(data, str):
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        message = "Failed to fetch campaign error records"
        data = []

    return status_code, message, data


async def get_communication_masked_data(data, masked_variables, channel, applicant_type):
    app.logger.info(f"app.utils.get_communication_masked_data")
    if channel != "email":
        masking_variable = "contact_to"
        if applicant_type == "co_applicant":
            keys_alias = {"co_applicant_contact_number": masking_variable}
        elif applicant_type == "applicant":
            keys_alias = {
                "applicant_contact_number": masking_variable,
            }
        else:
            keys_alias = {
                "applicant_contact_number": masking_variable,
                "co_applicant_contact_number": masking_variable,
            }
    else:
        if applicant_type == "co_applicant":
            keys_alias = [
                {"co_applicant_email": "contact_to"},
            ]
        elif applicant_type == "applicant":
            keys_alias = [
                {"applicant_email": "contact_to"},
            ]
        else:
            keys_alias = [{"applicant_email": "contact_to", "co_applicant_email": "contact_to"}]

    if channel != "email":
        masked_variables_copy = masked_variables.copy()
        for key in keys_alias:
            if masked_variables_copy.get(key):
                masked_variables_copy[keys_alias[key]] = masked_variables_copy.pop(key)
        data = await mask_data(data, keys_to_be_masked=masked_variables_copy)
    else:
        for alias in keys_alias:
            masked_variables_copy = masked_variables.copy()
            for key in alias:
                if masked_variables_copy.get(key):
                    masked_variables_copy[alias[key]] = masked_variables_copy.pop(key)
            data = await mask_data(data, keys_to_be_masked=masked_variables_copy)
    return data


def get_excluded_columns(columns):
    excluded_columns = ""
    for column in columns:
        if excluded_columns:
            excluded_columns += ","
        excluded_columns += f"{column}=EXCLUDED.{column}"
    return excluded_columns


def generate_billing_report(user: dict, company: dict, batch_id: str, case_type: str):
    logger.info(f"utils.generate_billing_report.company_id : {company['company_id']}")
    headers = {
        "authenticationtoken": user["authentication_token"],
        "Content-type": "application/json",
        "X-CG-User": json.dumps(user),
    }
    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/billing-email"
    logger.info(f"utils.generate_billing_report.url : {url}")
    payload = {"company_id": company["company_id"], "batch_id": batch_id, "case_type": case_type}
    try:
        resp = requests.post(
            url=url,
            data=json.dumps({**payload, "triggered_from": "approval_request"}),
            headers=headers,
        )
        logger.info(f"utils.generate_billing_report.status_code : {resp.status_code}")
        if resp.status_code != HTTPStatus.OK.value:
            raise Exception(resp.text)
    except Exception as e:
        logger.error(f"utils.generate_billing_report.exception : {str(e)}")
