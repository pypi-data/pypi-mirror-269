"""
service.py
Usage: All service methods
"""
import asyncio
import json
import requests
import logging
import datetime
from quart import current_app as app, g
from cg_utils import asynclient, get_profile_masked_variables
from urllib.parse import urlparse
import boto3
from botocore import config as boto_config
from .settings import (
    COMMUNICATION_SERVICE_BASE_URL,
    RECOVERY_SERVICE_BASE_URL,
    QUEUE_SERVICE_BASE_URL,
    UI_SERVICE_BASE_URL,
    MANHATTAN_SERVICE_BASE_URL,
    API_TOKEN,
    BASE_URL,
    EXPORT_BATCH_SIZE,
    EXPORT_SERVICE_BASE_URL,
    AWS_DEFAULT_REGION,
    AWS_S3_ACCESS_KEY,
    AWS_S3_SECRET_KEY,
    ATTEMPTED_DATE,
)
from .choices import (
    ReattemptErrors,
)
from app.utils import (
    execute_db_query,
    get_communication_masked_data,
)
from .choices import (
    ColumnMapChoices,
    PROD_ENV,
    RequestTypeChoices,
    TypeOfTaskChoices,
    CALL_DURATION,
    ReattemptGroups,
)
from app.utils import (
    format_api_response_text,
    encode_param,
    _dict_key_filter,
    get_export_mail_data_helper,
)


from http import HTTPStatus

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
QUEUE_FAILURE = "QUEUE_FAILURE"


def post(
    post_data,
    request_type,
    loan_id,
    company_id,
    user,
    request_id,
    company,
    channel: str,
):
    logger.info("app.service.post")
    status = ""
    success_status_code = HTTPStatus.OK.value
    if channel == RequestTypeChoices.whatsapp_bot.value:
        comm_endpoint = "/whatsapp_bot"
    elif channel == RequestTypeChoices.dtmf_ivr.value:
        comm_endpoint = "/ivr/create"
    else:
        comm_endpoint = "/create"

    if request_type == RequestTypeChoices.communication.value:
        url = f"{COMMUNICATION_SERVICE_BASE_URL}{comm_endpoint}"
        post_data["loan_id"] = loan_id
        post_data["company_id"] = company_id
    if request_type == RequestTypeChoices.remark.value:
        success_status_code = HTTPStatus.CREATED.value
        allocation_month = post_data.get("allocation_month", None)
        if channel == RequestTypeChoices.dtmf_ivr.value:
            template_name = post_data["template_name"]
        else:
            template_name = post_data["comm_dict"]["template_name"]

        url = f"{RECOVERY_SERVICE_BASE_URL}/create_remark/{encode_param(loan_id)}?company_id={company_id}&allocation_month={allocation_month}"
        if channel:
            post_data = {
                "remarks": f"({template_name}) {channel.title()} Sent",
                "source": f"queue_{channel}",
            }
    try:
        logger.debug(f"communication.post.{request_type}.url:: {url}")
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(post_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(user),
                "X-Request-ID": request_id,
                "X-CG-Company": json.dumps(company),
            },
        )
        logger.debug(f"communication.post.{request_type}.status_code:: {res.status_code}")

        res_text = json.loads(res.text)
        data = res_text.get("data", None)
        if res.status_code == success_status_code:
            status = "SUCCESS"
            res_text = str(res_text.get("output", ""))
        else:
            logger.error(f"communication.post.api.error :: {str(res.text)}")
            res_text = format_api_response_text(res)
            status = "FAIL"

        response = {
            "response": str(res_text),
            "status_code": str(res.status_code),
            "status": status,
            "loan_id": loan_id,
        }
    except Exception as e:
        logger.error(f"post.execution.communication.exception.{loan_id} -- {str(e)}")
        response = {
            "response": str({"message": "Internal server error"}),
            "status_code": "500",
            "status": "FAIL",
            "loan_id": loan_id,
        }
    logger.debug(f"post.execution.communication.response.{loan_id} -- {response}")
    return response


def create_dynamic_template(
    *args,
    payload: dict,
    failed: int,
    created: str,
    success: int,
    queue_env: str,
    campaign_name: str,
):
    logger.info(f"app.service.create_dynamic_template")
    author = payload["author"]
    channel = payload["channel"]
    company_details = payload["company"]
    campaign_id = payload["campaign_id"]
    company_id = company_details.get("company_id")
    campaign_link = f"{UI_SERVICE_BASE_URL}/app/bulk-management?company_id={company_id}&bulk_id={campaign_id}"
    total_loans = int(payload["total_loans"])
    data = json.loads(payload["data"])
    if not isinstance(data, dict):
        data = json.loads(data)
    comm_dict = data["comm_dict"]
    warning = False
    success_rate = round((success / total_loans) * 100)
    channel = channel.replace("_", " ").capitalize()
    if success_rate < 50:
        warning = True

    dynamic_template_data = {
        "user_name": " ".join(author.split("@")[0].split(".")).title(),
        "channel": channel,
        "total_loans": total_loans,
        "success": success,
        "failed": failed,
        "triggered_time": created,
        "campaign_id": campaign_id,
        "campaign_name": campaign_name,
        "report_message": "Total Loan accounts",
        "company": company_details["trademark"],
        "campaign_link": campaign_link,
        "env": queue_env if queue_env != PROD_ENV else None,
        "filters": data.get("filters"),
        "range": data.get("range"),
        "warning": warning,
    }
    if warning:
        dynamic_template_data[
            "subject"
        ] = f"[Warning] Bulk {channel} Request Triggered : Triggered rate is less than 50%"
    else:
        dynamic_template_data["subject"] = f"Bulk {channel} Request Triggered"

    if data.get("template_id", None):
        dynamic_template_data["template_id"] = data.get("template_id")

    if data.get("template_name"):
        dynamic_template_data["template_name"] = data.get("template_name")
    else:
        dynamic_template_data["template_name"] = comm_dict.get("template_name")

    if data.get("rule_id", None):
        dynamic_template_data["rule_id"] = data.get("rule_id")
    if data.get("rule_name", None):
        dynamic_template_data["rule_name"] = data.get("rule_name")
    if data.get("ai_author_ids", None):
        dynamic_template_data["ai_author_ids"] = data.get("ai_author_ids")
    logger.info(f"create_dynamic_template.close")
    return dynamic_template_data


def create_batch_dynamic_template(*args, payload: dict, failed: int, created: str, queue_env: str):
    logger.info(f"app.service.create_batch_dynamic_template")
    author = payload["author"]
    channel = payload["channel"]
    type = payload["type"]
    total_loans = payload["total_loans"]
    data = json.loads(payload["data"])
    company_details = payload["company"]

    if type == TypeOfTaskChoices.notice.value and channel == TypeOfTaskChoices.digital.value:
        data["applied_filter"] = payload.get("applied_filter", "")

    if payload.get("linked_loan", False) == True:
        trigger_message = "Total linked loan Id's"
    elif type == TypeOfTaskChoices.litigation_approval_request.value:
        trigger_message = "Total Case Id's"
    else:
        trigger_message = "Total Loan accounts"
    if channel == TypeOfTaskChoices.indiapost_tracking.value:
        type_of_task = channel.replace("_", " ")
        email_subject = f"Bulk {channel.replace('_', ' ')} report"
        report_message = f"Here is the bulk {channel.replace('_', ' ')} report that you've triggered."
    else:
        company = company_details["trademark"]
        type_of_task = ""
        if type == TypeOfTaskChoices.notice.value:
            type_of_task = f"{channel}_{type}"
        elif type == TypeOfTaskChoices.scrape.value:
            type_of_task = f"{channel}"
        else:
            type_of_task = f"{type}"
        type_of_task = type_of_task.replace("_", " ")
        email_subject = f"Bulk {type_of_task} report for {company}"
        report_message = f"Here is the bulk {type_of_task} report for {company} that you've triggered."
    dynamic_template_data = {
        "user_name": " ".join(author.split("@")[0].split(".")).title(),
        "total_loans": total_loans,
        "success": int(total_loans) - failed,
        "failed": failed,
        "triggered_time": created,
        "batch_id": payload["batch_id"],
        "trigger_message": trigger_message,
        "email_subject": email_subject,
        "report_message": report_message,
        "env": queue_env if queue_env != PROD_ENV else None,
    }

    if type == TypeOfTaskChoices.notice.value:
        dynamic_template_data["success"] = len(payload["success_data"])
        dynamic_template_data["failed"] = int(total_loans) - dynamic_template_data["success"]

    if data.get("template_id", None):
        dynamic_template_data["template_id"] = data.get("template_id")
    if data.get("template_name", None):
        dynamic_template_data["template_name"] = data.get("template_name")
    if data.get("rule_id", None):
        dynamic_template_data["rule_id"] = data.get("rule_id")
    if data.get("rule_name", None):
        dynamic_template_data["rule_name"] = data.get("rule_name")
    if data.get("draft_id", None):
        dynamic_template_data["draft_id"] = data.get("draft_id")
    if data.get("applied_filter", None):
        filters = data.get("applied_filter")
        filters = filters.replace("&", " ;&")
        filters = filters.split("&")
        dynamic_template_data["applied_filter"] = filters

    return dynamic_template_data


def generate_campaign_search_query_string(search_type, query_term):
    logger.info(f"app.service.generate_campaign_search_query_string")
    query_term = query_term.lower()
    if search_type == "campaign_name":
        query_string = f"and lower(name) LIKE '%{query_term}%' "
    elif search_type == "campaign_id":
        query_string = f"and campaign_id LIKE '%{query_term}%'"
    else:
        query_string = ""
    return query_string


async def generate_filter_dict(filter):
    logger.info(f"app.service.generate_filter_dict")
    common_filter_string = ""
    filter_author = filter.get("filter_author", [])
    filter_channel = filter.get("filter_channel", [])
    filter_duration = filter.get("filter_duration", {})
    if not filter_author:
        filter_author_string = ""
    else:
        filter_author_list = [f"author='{author}'" for author in filter_author]
        filter_author_string = f"({str(' or '.join(filter_author_list))})"
        common_filter_string = filter_author_string

    if not filter_channel:
        filter_channel_string = ""
    else:
        filter_channel_list = [f"channel='{channel}'" for channel in filter_channel]
        filter_channel_string = f"({str(' or '.join(filter_channel_list))})"
        common_filter_string = filter_channel_string

    if (filter_duration) and (not filter_duration.get("to", None) or not filter_duration.get("from", None)):
        duration_query = ""
    else:
        to_ = filter_duration.get("to", None)
        from_ = filter_duration.get("from", None)
        if to_:
            datetime_object = datetime.datetime.strptime(to_, "%Y-%m-%d")
            datetime_object += datetime.timedelta(days=1)
            to_ = str(datetime_object).split(" ")[0]
        duration_query = f""" and created < '{to_}' and created >= '{from_}' """

    if filter_author and filter_channel:
        common_filter_string = " and ".join((filter_author_string, filter_channel_string))

    if filter_duration or filter_duration.get("to") and filter_duration.get("from"):
        if not common_filter_string and duration_query:
            common_filter_string = duration_query.split("and", 1)[1]
        else:
            common_filter_string = common_filter_string + duration_query

    return common_filter_string


def get_dtmf_report_variables(company_id, template_id, user, request_id, company):
    logger.info(f"app.service.generate_filter_dict")

    url = f"{COMMUNICATION_SERVICE_BASE_URL}/dtmf/templates?company_id={company_id}&is_deleted=False&template_id={template_id}"
    logger.debug(f"get_dtmf_report_variables.url: {url}")
    try:
        dtmf_template_response = requests.request(
            method="GET",
            url=url,
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(user),
                "X-Request-ID": request_id,
                "X-CG-Company": json.dumps(company),
            },
        )
        logger.debug(f"get_dtmf_report_variables.status_code :: {dtmf_template_response.status_code}")
    except Exception as e:
        logger.error(f"campaign_comm_export..exception :: {str(e)}")
        return False

    if dtmf_template_response and dtmf_template_response.status_code == HTTPStatus.OK.value:
        dtmf_template_data = json.loads(dtmf_template_response.text).get("output", [])
        if dtmf_template_data:
            report_variables = dtmf_template_data[0].get("fields", {}).get("report_variables")
            report_variables = report_variables.split(",") if report_variables else []
            return report_variables
        else:
            return False
    else:
        logger.error(f"campaign_comm_export.error :: {dtmf_template_response.text}")
        return False


def save_dtmf_response(dtmf_response, loan_ids, payload):
    logger.info(f"app.service.save_dtmf_response")
    status_code = dtmf_response["status_code"]
    error_code = dtmf_response["error_code"]
    error_name = dtmf_response["error_name"]
    error_description = dtmf_response["error_description"]
    res_data = dtmf_response["res_data"]
    res_message = dtmf_response["res_message"]
    company_id = payload["company_id"]
    campaign_id = payload["campaign_id"]
    user = payload["user"]
    request_id = payload["request_id"]
    company = payload["company"]
    channel = payload["channel"]
    post_data = json.loads(payload["data"])
    insert_list = []
    if status_code == HTTPStatus.MULTI_STATUS.value:
        for loan_id in loan_ids:
            loan_response = res_data.get(loan_id, [])
            if loan_response:
                success = False
                for response in loan_response:
                    if not response.get("error"):
                        success = True
                        error_code = response.get("error_code")
                        error_name = response.get("error_name")
                        error_description = response.get("error_description")
                success = any([True if not response.get("error") else False for response in loan_response])
                if success:
                    status_code = HTTPStatus.OK.value
                    status = "SUCCESS"
                    response_message = f"Successfully created DTMF communication.{loan_response}"
                else:
                    status_codes = []
                    error_codes = []
                    error_names = []
                    error_desc = []
                    for response in loan_response:
                        status_codes.append(response.get("status_code", HTTPStatus.BAD_REQUEST.value))
                        error_codes.append(response.get("error_code"))
                        error_names.append(response.get("error_name"))
                        error_desc.append(response.get("error_description"))
                    status_code = max(status_codes, key=status_codes.count)
                    error_code = max(error_codes, key=error_codes.count)
                    error_name = max(error_names, key=error_names.count)
                    error_description = max(error_desc, key=error_desc.count)
                    status = "FAIL"
                    error = f"Error details: {loan_response}" if loan_response else ""
                    response_message = f"Failed to create dtmf communication. {error}"
            else:
                status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
                status = "FAIL"
                response_message = f"Failed to create dtmf communication."
                error_code = "COM-501"
                error_name = HTTPStatus.INTERNAL_SERVER_ERROR.name
                error_desc = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
            response = {
                "response": response_message,
                "status_code": str(status_code),
                "loan_id": loan_id,
                "status": status,
                "campaign_id": campaign_id,
                "error_code": error_code,
                "error_name": error_name,
                "error_description": error_description,
            }
            insert_list.append(response)
        return communication_save_response(payload, insert_list)
    else:
        insert_list = []
        for loan_id in loan_ids:
            response = {
                "response": res_message,
                "status_code": str(status_code),
                "loan_id": loan_id,
                "status": "FAIL",
                "campaign_id": campaign_id,
                "error_code": error_code,
                "error_name": error_name,
                "error_description": error_description,
            }
            insert_list.append(response)
        return communication_save_response(payload, insert_list)


def communication_save_response(payload, insert_list):
    logger.info("app.service.communication_save_response")
    save_campaign_payload = {"payload": payload, "insert_list": insert_list}
    campaign_id = payload["campaign_id"]
    url = f"{QUEUE_SERVICE_BASE_URL}/save_campaign_batch_response"
    try:
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(save_campaign_payload),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"communication_save_response.save_response.status_code.{campaign_id} :: {res.status_code}")
    except Exception as e:
        logger.error(f"communication_save_response.exception.{campaign_id} :: {str(e)}")
        return False
    if res.status_code != HTTPStatus.CREATED.value:
        logger.error(f"communication_save_response.error.{campaign_id} :: {res.text}")
        return False
    return True


async def policy_control_check(company_id, channel):
    try:
        policy_control_details_url = (
            f"{MANHATTAN_SERVICE_BASE_URL}/policy/control/check?company_id={company_id}&channels={channel}"
        )
        policy_control_response = await asynclient.get(
            url=policy_control_details_url, headers={"Content-Type": "application/json"}
        )
        app.logger.debug(f"campaign.policy_control_check.status_code: {policy_control_response.status_code}")
        if policy_control_response.status_code != HTTPStatus.OK.value:
            app.logger.error(f"campaign.get_policy_control_details.error {policy_control_response.text}")
            if policy_control_response.status_code == HTTPStatus.BAD_REQUEST.value:
                status_code = HTTPStatus.BAD_REQUEST.value
            elif policy_control_response.status_code == HTTPStatus.UNAUTHORIZED.value:
                status_code = HTTPStatus.UNAUTHORIZED.value
            else:
                status_code = HTTPStatus.FAILED_DEPENDENCY.value
            return {
                "message": "failed",
                "output": f"Failed to fetch policy control details: {policy_control_response.text}",
                "status_code": status_code,
            }
        policy_control_details = (json.loads(policy_control_response.text))["data"]
        app.logger.debug(f"campaign.policy_control_check.data: {policy_control_details}")
        if not policy_control_details:
            return {
                "message": "failed",
                "output": "Policy control details not found",
                "status_code": HTTPStatus.BAD_REQUEST.value,
            }
        communication_validation_details = policy_control_details["validation_details"][channel]
        if not communication_validation_details["is_valid"]:
            return {
                "message": "failed",
                "output": communication_validation_details["error_message"],
                "status_code": HTTPStatus.BAD_REQUEST.value,
            }
        return {
            "message": "success",
            "output": f"Successfully Fetched policy control details",
            "status_code": HTTPStatus.OK.value,
        }
    except Exception as e:
        app.logger.error(f"campaign.policy_control_check.exception: {str(e)}")
        return {
            "message": "failed",
            "output": f"Failed to fetch policy control details",
            "status_code": HTTPStatus.INTERNAL_SERVER_ERROR.value,
        }


def trigger_sms_communication(payload):
    try:
        logger.info(f"app.service.trigger_sms_communication")
        url = f"{BASE_URL}/communication/sms"
        payload = json.dumps(payload)
        headers = {"authenticationtoken": API_TOKEN, "Content-Type": "application/json"}
        logger.info(f"app.service.trigger_sms_communication :: url:{url} payload: {payload} headers : {headers}")
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text), response.status_code
    except Exception as e:
        return (
            {"message": f"Exception.trigger_sms_communication: {e}"},
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


async def get_communication_details(payload):
    logger.info(f"app.tasks.report.campaign_comm_export")
    company_id = payload.get("company_id")
    channel = payload["channel"]
    campaign_id = payload["campaign_id"]
    is_deleted = payload.get("is_deleted", False)
    campaign_comm_export_output = {"error": None, "status_code": HTTPStatus.OK.value, "data": []}
    url = f"{COMMUNICATION_SERVICE_BASE_URL}/export/{channel}?company_id={company_id}"
    logger.info(f"campaign_comm_export.export.url: {url}")
    try:
        response_data = {
            "campaign_id": campaign_id,
            "response_type": "data",
            "selected_loan_ids": payload.get("selected_loan_ids", []),
            "is_deleted": is_deleted,
            "source": "campaign_report",
        }
        logger.info(f"communication_export_payload:{response_data}")
        campaign_comm_export = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload.get("request_id"),
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"campaign_comm_export.status_code :: {campaign_comm_export.status_code}")
    except Exception as e:
        logger.error(f"campaign_comm_export..exception :: {str(e)}")
        campaign_comm_export_output["error"] = f"Failed to fetch communication details.Error Details:{str(e)}"
        campaign_comm_export_output["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        return campaign_comm_export_output

    if campaign_comm_export.status_code != HTTPStatus.OK.value:
        logger.error(f"campaign_comm_export.error :: {campaign_comm_export.text}")
        campaign_comm_export_output[
            "error"
        ] = f"Failed to fetch communication details.Error Details:{campaign_comm_export.text}"
        campaign_comm_export_output["status_code"] = HTTPStatus.FAILED_DEPENDENCY.value
        return campaign_comm_export_output

    campaign_comm_export = json.loads(campaign_comm_export.text)
    campaign_comm_export_output["data"] = campaign_comm_export.get("output", [])
    logger.info(f"campaign_comm_export_output :: {len(campaign_comm_export)}")
    if campaign_comm_export_output["data"] == []:
        campaign_comm_export_output["data"] = [ColumnMapChoices[channel].value.copy()]

    return campaign_comm_export_output


async def get_full_campaign_data(data, channel_campaigns_columns=[], get_channel_data=False):
    result = {"campaign_data": [], "channel_campaign_data": []}
    channel = data["channel"]
    campaign_id = data["campaign_id"]
    is_deleted = data.get("is_deleted", False)
    loan_ids = data.get("selected_loan_ids", [])
    channel_campaign_data, campaign_data = [], []
    attempted_live = False
    try:
        campaign_data = await get_campaigns_details(campaign_id=campaign_id, channel=channel, is_deleted=is_deleted)
        logger.debug(f"get_full_campaign_data.campaign_data.length:{len(campaign_data)}")
        if campaign_data and channel != "NA":
            created = campaign_data[0].get("created")
            created = created.split(" ")[0]
            created = datetime.datetime.strptime(created, "%Y-%m-%d").date()
            if created > ATTEMPTED_DATE and get_channel_data:
                channel_campaigns_columns = [
                    "'FAIL' as status",
                    "error as response",
                    "status_code",
                    "loan_id",
                    "created::VARCHAR",
                    "error_code",
                    "applicant_type",
                    "contact_to",
                ]
                attempted_live = True
            if channel_campaigns_columns:
                channel_campaign_data = await get_campaign_channel_details(
                    campaign_id=campaign_id,
                    channel=channel,
                    columns=channel_campaigns_columns,
                    is_deleted=is_deleted,
                    loan_ids=loan_ids,
                    attempted_live=attempted_live,
                    company_id=data.get("company_id"),
                )
            logger.debug(f"get_full_campaign_data.channel_campaign_data.length:{len(channel_campaign_data)}")
    except Exception as e:
        logger.error(f"campaign_data.exception {str(e)}")
    result["campaign_data"] = campaign_data
    result["channel_campaign_data"] = channel_campaign_data
    return result


def get_campaign_report_data(data, communication_export_data, campaign_data):
    #  0. columns keys list
    company_id = data["company_id"]
    channel = data["channel"]
    export_comm_keys = communication_export_data[0].keys()

    # list of export keys
    columns_key_mapping = []
    list_export_comm_keys = list(export_comm_keys)
    for key in export_comm_keys:
        char = " ".join([i.capitalize() for i in key.split("_")])
        columns_key_mapping.append(char)

    if channel == RequestTypeChoices.dtmf_ivr.value:
        columns_key_mapping.remove("Collected Dtmfs")
        columns_key_mapping.remove("Collected Mapped Dtmfs")
        list_export_comm_keys.remove("collected_dtmfs")
        list_export_comm_keys.remove("collected_mapped_dtmfs")

        dtmf_template_id = communication_export_data[0].get("template_id", None)

        dtmf_report_variables = None
        if dtmf_template_id:
            dtmf_report_variables = get_dtmf_report_variables(
                company_id, dtmf_template_id, data["user"], data.get("request_id"), data["company"]
            )

        if dtmf_report_variables:
            for var in dtmf_report_variables:
                report_variable = " ".join([i.capitalize() for i in var.split("_")])
                columns_key_mapping.append(report_variable)
                columns_key_mapping.append(f"{report_variable} Meaning")
                list_export_comm_keys.append(report_variable)
                list_export_comm_keys.append(f"{report_variable}_Meaning")

    columns_key_mapping = columns_key_mapping + [
        "Error Source",
        "Error Reason",
        "Error Status",
    ]

    #  1. export_comm keys none dict map with error source keys
    list_export_comm_keys = list_export_comm_keys + [
        "error_source",
        "error_reason",
        "error_status",
    ]

    #  2. add error source keys to export comm ie. new_export_comm ### TODO list_1
    new_export_comm = []
    for comm in communication_export_data:
        new_comm = comm

        if channel == RequestTypeChoices.dtmf_ivr.value:

            collected_dtmfs = new_comm.pop("collected_dtmfs", {})
            collected_mapped_dtmfs = new_comm.pop("collected_mapped_dtmfs", {})
            if not isinstance(collected_dtmfs, dict):
                collected_dtmfs = {}
            if not isinstance(collected_mapped_dtmfs, dict):
                collected_mapped_dtmfs = {}

            if dtmf_report_variables:
                for var in dtmf_report_variables:
                    var_meaning = f"{var}_Meaning"
                    new_comm[var] = collected_dtmfs.get(var, "")
                    new_comm[var_meaning] = collected_mapped_dtmfs.get(var_meaning, "")

        new_comm["error_source"] = ""
        new_comm["error_reason"] = ""

        if new_comm.get("error_name"):
            new_comm["error_status"] = "FAIL"
        elif (
            (channel == RequestTypeChoices.voice.value and new_comm["ivr_call_duration_(in_seconds)"] == "")
            or (
                channel == RequestTypeChoices.whatsapp.value
                and new_comm["whatsapp_message_delivery_time"] == ""
                and new_comm["whatsapp_message_sent_time"] == ""
            )
            or (
                channel == RequestTypeChoices.whatsapp_bot.value
                and new_comm["whatsapp_bot_session_delivery_time"] == ""
                and new_comm["whatsapp_bot_session_sent_time"] == ""
            )
            or (channel == RequestTypeChoices.email.value and new_comm["email_delivery_time"] == "")
            or (channel == RequestTypeChoices.sms.value and new_comm["sms_delivery_time"] == "")
            or (channel == RequestTypeChoices.dtmf_ivr.value and new_comm["dtmf_ivr_call_duration_(in_seconds)"] == "")
        ):
            new_comm["error_status"] = "PENDING"
        else:
            new_comm["error_status"] = "SUCCESS"
        new_export_comm.append(new_comm)

    logger.info(f"get_campaign_report_data.new_export_comm:{new_export_comm}")

    #  3. populate the export campaign_export data with 1 ### TODO list_2
    if not campaign_data:
        logger.error(f"campaign_data not found")
        return []
    channel_campaign_output_data = campaign_data["channel_campaign_data"]
    campaign_output_data = campaign_data["campaign_data"]

    campaign_output_data = campaign_output_data[0]
    campaign_output_comm_data = json.loads(campaign_output_data["data"])
    if not isinstance(campaign_output_comm_data, dict):
        campaign_output_comm_data = json.loads(campaign_output_comm_data)
    channel_campaign_output_data_list = []

    for channel_campaign_output_item in channel_campaign_output_data:
        if channel_campaign_output_item["status"] == "SUCCESS":
            continue
        default_export_comm_dict_map = {}
        for list_export_comm_key in list_export_comm_keys:
            default_export_comm_dict_map[list_export_comm_key] = ""

        channel_campaign_output_data_list.append(default_export_comm_dict_map)
        default_export_comm_dict_map["loan_id"] = f"'{channel_campaign_output_item['loan_id']}"
        default_export_comm_dict_map["triggered_time"] = channel_campaign_output_item["created"]

        default_export_comm_dict_map["type_of_communication"] = campaign_output_data["channel"]
        default_export_comm_dict_map["digital_disposition"] = QUEUE_FAILURE
        default_export_comm_dict_map["bulk_request_id"] = campaign_output_data["campaign_id"]
        default_export_comm_dict_map["bulk_request_name"] = campaign_output_data.get("name")
        default_export_comm_dict_map["author"] = campaign_output_data["author"]
        default_export_comm_dict_map["role"] = campaign_output_data["role"]

        default_export_comm_dict_map["applicant_type"] = (
            channel_campaign_output_item["applicant_type"]
            if channel_campaign_output_item.get("applicant_type")
            else campaign_output_comm_data["send_to"]
        )
        default_export_comm_dict_map["template_id"] = campaign_output_comm_data["template_id"]
        default_export_comm_dict_map["allocation_month"] = campaign_output_comm_data["allocation_month"]
        if channel == RequestTypeChoices.whatsapp.value:
            if campaign_output_comm_data.get("template_name"):
                default_export_comm_dict_map[f"whatsapp_message_template_name"] = campaign_output_comm_data.get(
                    "template_name", ""
                )
            else:
                default_export_comm_dict_map[f"whatsapp_message_template_name"] = campaign_output_comm_data.get(
                    "comm_dict", {}
                ).get("template_name")
            default_export_comm_dict_map["whatsapp_mobile_number"] = channel_campaign_output_item.get("contact_to", "")

        elif channel == RequestTypeChoices.whatsapp_bot.value:
            if campaign_output_comm_data.get("template_name"):
                default_export_comm_dict_map[f"whatsapp_bot_session_template_name"] = campaign_output_comm_data.get(
                    "template_name", ""
                )
            else:
                default_export_comm_dict_map[f"whatsapp_bot_session_template_name"] = campaign_output_comm_data.get(
                    "comm_dict", {}
                ).get("template_name")
            default_export_comm_dict_map["whatsapp_bot_session_mobile_number"] = channel_campaign_output_item.get(
                "contact_to", ""
            )
        elif channel == RequestTypeChoices.voice.value:
            if campaign_output_comm_data.get("template_name"):
                default_export_comm_dict_map[f"ivr_template_name"] = campaign_output_comm_data.get("template_name", "")
            else:
                default_export_comm_dict_map[f"ivr_template_name"] = campaign_output_comm_data.get("comm_dict", {}).get(
                    "template_name"
                )
            default_export_comm_dict_map["ivr_mobile_number"] = channel_campaign_output_item.get("contact_to", "")
        else:
            if campaign_output_comm_data.get("template_name"):
                default_export_comm_dict_map[f"{channel}_template_name"] = campaign_output_comm_data.get(
                    "template_name", ""
                )
            else:
                default_export_comm_dict_map[f"{channel}_template_name"] = campaign_output_comm_data.get(
                    "comm_dict", {}
                ).get("template_name")
            if channel != RequestTypeChoices.email.value:
                default_export_comm_dict_map[f"{channel}_mobile_number"] = channel_campaign_output_item.get(
                    "contact_to", ""
                )
        if channel == RequestTypeChoices.email.value:
            if campaign_output_comm_data.get("comm_dict", {}).get("email_subject"):
                default_export_comm_dict_map[f"{channel}_subject"] = campaign_output_comm_data["comm_dict"][
                    "email_subject"
                ]
            else:
                default_export_comm_dict_map[f"{channel}_subject"] = campaign_output_comm_data.get("email_subject")
            default_export_comm_dict_map["email_address_to"] = channel_campaign_output_item.get("contact_to", "")
        default_export_comm_dict_map["error_source"] = "queue"
        default_export_comm_dict_map["error_reason"] = channel_campaign_output_item["response"]
        default_export_comm_dict_map["error_status"] = channel_campaign_output_item["status"]

    #  4. add list2 to list1
    logger.info(f"get_campaign_report_data.channel_campaign_output_data_list:{len(channel_campaign_output_data_list)}")
    final_consolidated_comm_export_data = new_export_comm + channel_campaign_output_data_list
    if len(new_export_comm) == 1 and new_export_comm[0]["loan_id"] == "dummy_column_map_choices_loan_id":
        final_consolidated_comm_export_data = channel_campaign_output_data_list
    if channel_campaign_output_data_list == []:
        final_consolidated_comm_export_data = new_export_comm
    logger.info(
        f"get_campaign_report_data.final_consolidated_comm_export_data:{len(final_consolidated_comm_export_data)}"
    )
    return final_consolidated_comm_export_data


async def trigger_campaign_export(
    company_id: str,
    campaign_id: str,
    loan_ids: list,
    total_count: int,
    payload: dict,
    user_details: dict,
    request_headers: dict,
    file_type: str = "xlsx",
):
    try:
        logger.info("service.trigger_campaign_export")
        allocation_month = payload.get("allocation_month")
        result = {"error": None, "success": False, "status_code": None}
        # if allocation month is not provided, export for current allocation month
        if not allocation_month:
            allocation_month = str(datetime.now().year) + "-" + str(datetime.now().month) + "-01"

        channel = payload["channel"]
        export_data = _dict_key_filter(payload, ["company_id"])
        logger.info(f"user_details:{user_details}")
        logger.info("export_data_payload=>")
        export_id = await app.comm_db.insert_with_returning(
            table="export",
            values={
                "company_id": company_id,
                "data": json.dumps(export_data, default=str),
                "record_count": int(total_count),
                "export_category": f"{channel}_campaign_report",
                "author_id": user_details["user_id"],
                "author_name": f"{user_details.get('first_name','')} {user_details.get('last_name','')}".strip(),
                "author_email": user_details["email"],
            },
            returning="id",
        )
        logger.debug("trigger_campaign_export.export_id: %s", export_id)
        logger.info("trigger_campaign_export.export_id: %s", export_id)
        campaign_export_data = "campaign_export_data"
        campaign_export_data_api_payload = {
            "company_id": company_id,
            "allocation_month": allocation_month,
            "response_type": "data",
            "source": "comm_export",
            "selected_loan_ids": loan_ids,
            "campaign_id": campaign_id,
            "channel": payload["channel"],
            "archive": payload.get("archive", False),
        }
        campaign_export_activity_api = "campaign_report_activity"
        payload = {
            "cg_service": "QUEUE",
            "report_name": "campaign-export",
            "company_id": company_id,
            "metadata": {
                "start_date": str(datetime.datetime.now()),
                "end_date": str(datetime.datetime.now()),
                "file_type": file_type,
                "batch_size": EXPORT_BATCH_SIZE,
                "chunk_key": "selected_loan_ids",
                "total_records": total_count,
                "api": {
                    "path": campaign_export_data,
                    "parameters": {"company_id": company_id},
                    "body": campaign_export_data_api_payload,
                    "method": "POST",
                    "headers": request_headers,
                },
                "callback_url": f"{QUEUE_SERVICE_BASE_URL.rstrip('/')}/{campaign_export_activity_api}?export_id={export_id}&company_id={company_id}",
                "callback_header": request_headers,
            },
        }

        create_export_url = f"{EXPORT_SERVICE_BASE_URL.rstrip('/')}/create"
        response = await asynclient.post(create_export_url, json=payload)
        logger.debug(f"trigger_communication_export_task.export_service.status_code: {response.status_code}")
        logger.info(f"export_api:{create_export_url},export_api_payload:{payload}:payload_end")
        if response.status_code == HTTPStatus.ACCEPTED.value:
            reference_export_id = response.json()["data"]
            logger.debug("trigger_communication_export_task.reference_export_id: %s", reference_export_id)
            logger.info("trigger_communication_export_task.reference_export_id: %s", reference_export_id)

            await app.comm_db.update(
                table="export",
                values={"reference_export_id": reference_export_id},
                where={"id = %s": export_id, "company_id = '%s'": company_id},
            )
            result["status_code"] = HTTPStatus.OK.value
            result["success"] = True
            result["message"] = f"Report will be shared on your email :: {user_details['email']}"
        else:
            error_message = ""
            try:
                export_response = json.loads(response.text)
                if isinstance(export_response, dict) and export_response.get("error", {}).get("message"):
                    error_message = export_response["error"]["message"]
                else:
                    error_message = response.text
            except Exception as e:
                logger.info(f"export_api.json_loads.exception :{e}")
                error_message = response.text
            result["message"] = f"Failed to send export request: {error_message}"
            result["status_code"] = HTTPStatus.FAILED_DEPENDENCY.value
            await app.comm_db.update(
                table="export",
                values={"status": "FAILED", "response": response.text},
                where={"id = %s": export_id, "company_id = '%s'": company_id},
            )
    except Exception as e:
        logger.error(f"trigger_communication_export_task.exception: {str(e)}")
        result["message"] = f"Failed to process export request"
        result["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
    return result


async def send_campaign_export_report(
    export_id, company_id, download_link, company_trademark, failure_message, service_flag=None
):
    logger.info("queue.service.send_campaign_export_report")
    output = {"message": None, "status_code": HTTPStatus.OK.value, "success": True}
    email_sent = False
    if not export_id:
        output["success"] = False
        output["message"] = "export_id not provided"
        output["status_code"] = HTTPStatus.BAD_REQUEST.value
        return output
    try:
        export_task = await app.comm_db.select(
            table="export",
            columns=[
                "company_id",
                "record_count",
                "data",
                "export_category",
                "author_email",
                "is_email_sent",
                "created",
                "reference_export_id",
            ],
            where={"id = %s": export_id, "company_id = '%s'": company_id},
            limit=1,
        )
        if not export_task:
            output["success"] = False
            output["message"] = "invalid export_id not provided"
            output["status_code"] = HTTPStatus.BAD_REQUEST.value
            return output

        export_task = export_task[0]
        email_flag = export_task["is_email_sent"]
        logger.info(f"export_task:{export_task}")
        if email_flag:
            output["message"] = "download link has already been shared."
            return output

        update_values = {"status": "FAILED", "updated": datetime.datetime.now()}
        send_mail_api = f"{COMMUNICATION_SERVICE_BASE_URL}/mail/send"
        if download_link:
            update_values["download_link"] = download_link
            presigned_url_res = get_presigned_url(download_link)
            logger.info(f"presigned_url_res:{presigned_url_res}")
            if not presigned_url_res["presigned_url"]:
                output["message"] = presigned_url_res.get("error", "Failed to generate presigned url")
            else:
                presigned_url = presigned_url_res["presigned_url"]
            status = "FAILED"
            mail_data = get_export_mail_data_helper(
                export_task=export_task,
                presigned_url=presigned_url,
                company_trademark=company_trademark,
                service=service_flag,
            )
            logger.info(f"send_campaign_export_report.email_payload:{mail_data}")
            response = await asynclient.post(send_mail_api, json=mail_data)
            logger.info(f"send_campaign_export_report.mail_sent_response:{response.status_code}")
            if response.status_code == HTTPStatus.OK.value:
                email_sent = True
                output["success"] = True
                output["message"] = "Download link sent successfully"
                status = "COMPLETED"
            else:
                logger.error(f"Failed to send download link:{response.text}")
                output["success"] = False
                output["message"] = f"Failed to send download link:: {response.text}"
            update_values.update({"status": status, "is_email_sent": email_sent})
        else:
            output["message"] = failure_message if failure_message else "download link not found."
        update_values["response"] = output["message"]
        await app.comm_db.update(
            table="export", values=update_values, where={"id = %s": export_id, "company_id = '%s'": company_id}
        )
    except Exception as e:
        logger.error(f"send_campaign_export_report.error:{str(e)}")
        output["success"] = False
        output["message"] = "Failed to process export."
        output["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
    return output


def get_presigned_url(export_link):
    logger.info("app.service.get_presigned_url")
    output = {"error": None, "status_code": None, "success": False, "presigned_url": None}
    try:
        # parse link and extract bucket name and file path
        parsed_url_object = urlparse(export_link)
        bucket_name = parsed_url_object.netloc.split(".")[0]
        file_path = parsed_url_object.path
        s3_client_v4 = boto3.client(
            "s3",
            aws_access_key_id=AWS_S3_ACCESS_KEY,
            aws_secret_access_key=AWS_S3_SECRET_KEY,
            region_name=AWS_DEFAULT_REGION,
            config=boto_config.Config(s3={"addressing_style": "virtual"}, signature_version="s3v4"),
            endpoint_url="https://s3." + AWS_DEFAULT_REGION + ".amazonaws.com",
        )
        presigned_url = s3_client_v4.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": file_path.lstrip("/")},
            ExpiresIn=86400,
        )
        output["success"] = True
        output["presigned_url"] = presigned_url
        return output
    except Exception as e:
        logger.error(f"get_presigned_url.exception:{str(e)}")
        output["error"] = "Failed to generate presigned url"
        output["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        return output


async def get_campaigns_details(campaign_id, channel, is_deleted=False):
    result = []
    CAMPAIGNS_TABLE = "campaigns"
    campaign_report_redis_key = f"campaign_report_{campaign_id}"
    columns = [
        "campaign_id",
        "name",
        "channel",
        "created::VARCHAR",
        "data",
        "type",
        "author",
        "role",
        "company_id",
        "total_loans",
        "description",
        "loan_data",
    ]
    try:
        result = await app.redis.get(key=campaign_report_redis_key)
        if not result:
            result = await app.campaign_db.select(
                table=CAMPAIGNS_TABLE,
                columns=columns,
                where={"campaign_id='%s'": campaign_id, "channel='%s'": channel, "is_deleted = %s": is_deleted},
            )
            await app.redis.set(key=campaign_report_redis_key, value=result, expiry_time=6 * 60 * 60)
    except Exception as e:
        logger.error(f"Error in get_campaigns_details:{str(e)}")
    return result


async def get_campaign_channel_details(
    campaign_id, columns, channel, loan_ids=[], is_deleted=False, attempted_live=False, company_id=None
):
    result = []
    CHANNEL_CAMPAIGNS_TABLE = f"campaign_{channel}"
    column_string = ",".join(columns)
    loan_ids_string = tuple(loan_ids)
    if len(loan_ids) == 1:
        loan_ids_string = "('" + str(loan_ids[0]) + "')"
    is_deleted = "true" if is_deleted else "false"
    if not company_id:
        company_id = g.company["company_id"]
    try:
        if attempted_live:
            query = f"select {column_string} from {channel}_failure where company_id= '{company_id}' and campaign_id='{campaign_id}' and is_deleted={is_deleted} and loan_id in {loan_ids_string}"
            app.logger.info(f"get_campaign_channel_details.query {query}")
            result = await app.comm_db.execute_raw_select_query(query)
            masked_variables = await get_profile_masked_variables(
                company_id=company_id, permission_group_id=g.user["permission_group_id"]
            )
            if masked_variables and result:
                for idx, channel_data in enumerate(result):
                    result[idx] = await get_communication_masked_data(
                        channel_data, masked_variables, channel, channel_data["applicant_type"]
                    )
        else:
            query = f"select {column_string} from {CHANNEL_CAMPAIGNS_TABLE} where campaign_id='{campaign_id}' and is_deleted={is_deleted} and loan_id in {loan_ids_string}"
            app.logger.info(f"get_campaign_channel_details.query {query}")
            result = await app.campaign_db.execute_raw_select_query(query)
    except Exception as e:
        logger.error(f"Error while fetching channel campaign data:{str(e)}")
    return result


async def get_mc_failure_details(payload):
    logger.info(f"app.tasks.report.get_mc_failure_details")
    response = {"message": "success", "output": None, "data": [], "status_code": HTTPStatus.OK.value}
    table = "mc_failure"
    company_id = payload.get("company_id")
    campaign_id = payload["campaign_id"]
    is_deleted = payload.get("is_deleted", False)
    columns = [
        "campaign_id",
        "campaign_name",
        "loan_id",
        "allocation_month",
        "applicant_type",
        "created_by",
        "created::VARCHAR",
        "error_name",
        "error_description",
    ]
    try:
        result = await app.comm_db.select(
            table=table,
            columns=columns,
            where={"campaign_id='%s'": campaign_id, "company_id='%s'": company_id, "is_deleted = %s": is_deleted},
        )
        if not result and isinstance(result, list):
            response["message"] = "success"
            response["output"] = "Master campaign failure campaigns not found"
        elif not isinstance(result, list):
            response["message"] = "failed"
            response["output"] = "Failed to fetch master campaign failure campaigns"
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        else:
            response["data"] = result
    except Exception as e:
        logger.error(f"Error in get_campaigns_details:{str(e)}")
        response["message"] = "failed"
        response["output"] = "Failed to fetch master campaign failure campaigns"
        response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
    return response


async def get_mc_failure_campaign_report(mc_failure_data, campaign_output_data):
    logger.info(f"app.tasks.report.get_mc_failure_campaign_report")
    campaign_data = campaign_output_data["campaign_data"]
    campaign_data = campaign_data[0]
    result = []
    for failed_data in mc_failure_data:
        result.append(
            {
                "bulk_request_id": failed_data["campaign_id"],
                "bulk_request_name": failed_data.get("campaign_name"),
                "loan_id": failed_data["loan_id"],
                "allocation_month": failed_data["allocation_month"],
                "digital_disposition": QUEUE_FAILURE,
                "applicant_type": failed_data["applicant_type"],
                "author": campaign_data["author"],
                "triggered_time": failed_data["created"],
                "error_name": failed_data["error_name"],
                "error_description": failed_data["error_description"],
            }
        )
    return result


async def get_campaigns_data(company_id, campaign_id, is_deleted=False):
    campaign_metadata = {}
    try:
        logger.info(f"app.service.get_campaigns_data")
        redis_key = f"{campaign_id}_campaign_metadata"
        campaign_metadata = await app.redis.get(redis_key)
        if not campaign_metadata:
            query = f"select data as campaign_metadata from campaigns where company_id='{company_id}' and campaign_id='{campaign_id}' and is_deleted = {is_deleted}"
            campaign_data = await app.campaign_db.execute_raw_select_query(query)
            if campaign_data:
                campaign_data = campaign_data[0]
                campaign_metadata = campaign_data.get("campaign_metadata", {})
                if campaign_metadata:
                    campaign_metadata = json.loads(campaign_metadata)
                    if campaign_metadata and not isinstance(campaign_metadata, dict):
                        campaign_metadata = json.loads(campaign_metadata)
                    await app.redis.set(redis_key, campaign_metadata)
    except Exception as e:
        logger.error(f"failed to fetch campaign data:{e}")
    return campaign_metadata


def trigger_email_communication(payload):
    try:
        url = f"{BASE_URL}/communication/mail/send"
        payload = json.dumps(payload)
        headers = {"authenticationtoken": API_TOKEN, "role": "admin", "Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text), response.status_code
    except Exception as e:
        return {
            "message": f"Exception.trigger_email_communication: {e}",
        }, HTTPStatus.INTERNAL_SERVER_ERROR.value


async def get_campaign_errors(
    campaign_id: str, company_id: str, channel: str, campaign_data: dict, count: bool = False, campaign_errors={}
):
    app.logger.info(f"app.service.get_campaign_errors")
    task_name_list = []
    task_list = []
    select_all = []
    triggered_and_delivered = []
    webhook_not_received = []
    whatsapp_sent_but_not_delivered = []
    queue_failures = []
    operator_failures = []
    link_clicked = []
    answered_greater_than = []
    answered_less_than = []
    opened = []
    responded = []
    total_loan_count = 0
    response = {
        "message": "All Campaign Errors fetched successfully",
        "success": True,
        "status_code": HTTPStatus.OK.value,
    }
    total_loan_count = int(campaign_data["total_loans"])
    total_loan_ids = json.loads(campaign_data["loan_data"])
    helicarrier_trigger = campaign_data["helicarrier_trigger"]
    select_all.append(
        {
            "error": "all",
            "loan_count": total_loan_count,
            "percent_count": 100,
        }
    )
    if not count:
        select_all[0]["loan_ids"] = total_loan_ids
    webhook_not_received_loans = []
    whatsapp_sent_but_not_delivered_loans = []
    link_clicked_loans = []
    answered_loans = []
    dtmf_responded_loans = []
    opened_loans = []
    triggered_delivered_loans = []
    triggered_loans = []
    company_id_condition = ""
    queue_failure_loans = []
    operator_failure_loans = []
    answered_greater_than_loans = []

    db_instance = app.comm_db
    table = channel if channel != RequestTypeChoices.NA.value else "mc_failure"
    company_id_condition = f"and company_id = '{company_id}'"

    try:
        # fetching records whose webhook is not received from communication
        if channel != RequestTypeChoices.NA.value:
            query = f"select array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and is_webhook_received is false;"
            task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=db_instance)))
            task_name_list.append(ReattemptGroups.WEBHOOK_NOT_RECEIVED.value)

            # fetching channel specific data from campaign_channel table
            if helicarrier_trigger:
                query = f"select error_name, array_agg(loan_id) as loan_ids from {channel}_failure where campaign_id= '{campaign_id}' {company_id_condition}  group by error_name;"
                task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=app.comm_db)))
                task_name_list.append("queue_failures")

                # fetching triggered records from communication
                query = f"select array_agg(loan_id) as loan_ids from {channel} where campaign_id= '{campaign_id}' {company_id_condition};"
                task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=app.comm_db)))
                task_name_list.append(ReattemptGroups.TRIGGERED.value)

            else:
                table_name = f"campaign_{channel}"
                query = f"select error_name, array_agg(loan_id) as loan_ids from {table_name} where campaign_id= '{campaign_id}' and status= 'FAIL' group by error_name;"
                task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=app.campaign_db)))
                task_name_list.append(ReattemptGroups.QUEUE_FAILURES.value)

            # fetching records whose delivered status is not null from communication channel table
            query_for_fetching_delivered_communication = f"select array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and delivered_time is not null;"
            task_list.append(
                asyncio.create_task(
                    execute_db_query(query=query_for_fetching_delivered_communication, db_instance=db_instance)
                )
            )
            task_name_list.append(ReattemptGroups.TRIGGERED_AND_DELIVERED.value)

            # query for fetching operator error communication
            query = f"select error_name, array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and error_name is not null group by error_name;"
            task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=db_instance)))
            task_name_list.append(ReattemptGroups.OPERATOR_FAILURES.value)

        else:
            query = f"select error_name, array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition}  group by error_name;"
            task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=app.comm_db)))
            task_name_list.append(ReattemptGroups.QUEUE_FAILURES.value)

        # query for fetching whatsapp sent communication
        if channel == RequestTypeChoices.whatsapp.value:
            query = f"select array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and sent_time is not null;"
            task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=db_instance)))
            task_name_list.append(ReattemptGroups.WHATSAPP_SENT_BUT_NOT_DELIVERED.value)

        # query for fetching link_clicked
        if channel not in (
            RequestTypeChoices.dtmf_ivr.value,
            RequestTypeChoices.voice.value,
            RequestTypeChoices.NA.value,
        ):
            query = f"select array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and is_link_clicked is true;"
            task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=db_instance)))
            task_name_list.append(ReattemptGroups.IS_LINK_CLICKED.value)

        # query for fetching answered communication
        if channel in (RequestTypeChoices.dtmf_ivr.value, RequestTypeChoices.voice.value):
            query_for_less_than = f"select array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and answer_time is not null and call_duration <= {CALL_DURATION};"
            task_list.append(asyncio.create_task(execute_db_query(query=query_for_less_than, db_instance=db_instance)))
            task_name_list.append(ReattemptGroups.FOR_LESS_THAN.value)

            query_for_greater_than = f"select array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and answer_time is not null and call_duration > {CALL_DURATION};"
            task_list.append(
                asyncio.create_task(execute_db_query(query=query_for_greater_than, db_instance=db_instance))
            )
            task_name_list.append(ReattemptGroups.FOR_GREATER_THAN.value)

        # query for fetching responded communication
        if channel == RequestTypeChoices.dtmf_ivr.value:
            query = f"select array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and responded_time is not null;"
            task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=db_instance)))
            task_name_list.append(ReattemptGroups.RESPONDED_TIME.value)

        # query for fetching opened communication
        if channel in (RequestTypeChoices.email.value, RequestTypeChoices.whatsapp.value):
            query = f"select array_agg(loan_id) as loan_ids from {table} where campaign_id= '{campaign_id}' {company_id_condition} and opened_time is not null;"
            task_list.append(asyncio.create_task(execute_db_query(query=query, db_instance=db_instance)))
            task_name_list.append(ReattemptGroups.OPENED_TIME.value)

        task_results = await asyncio.gather(*task_list, return_exceptions=True)
        for task_result, task_name in zip(task_results, task_name_list):
            if task_result:
                status_code = task_result[0]
                db_response_message = task_result[1]
                if status_code == HTTPStatus.OK.value:
                    if task_name == ReattemptGroups.TRIGGERED_AND_DELIVERED.value:
                        comm_data = task_result[2]
                        if comm_data:
                            if comm_data[0].get("loan_ids"):
                                app.logger.debug(f"get_campaign_errors.comm_data: {comm_data}")
                                triggered_delivered_loans = comm_data[0].get("loan_ids", [])
                                triggered_delivered_loans = list(set(triggered_delivered_loans))
                                triggered_and_delivered.append(
                                    {
                                        "error": ReattemptGroups.TRIGGERED_AND_DELIVERED.value,
                                        "loan_ids": triggered_delivered_loans,
                                    }
                                )

                    elif task_name == ReattemptGroups.WEBHOOK_NOT_RECEIVED.value:
                        comm_data = task_result[2]
                        if comm_data:
                            if comm_data[0].get("loan_ids"):
                                app.logger.debug(f"get_campaign_errors.comm_data: {comm_data}")
                                webhook_not_received_loans = comm_data[0].get("loan_ids", [])
                                webhook_not_received_loans = list(set(webhook_not_received_loans))
                                webhook_not_received.append(
                                    {
                                        "error": ReattemptGroups.WEBHOOK_NOT_RECEIVED.value,
                                        "loan_ids": webhook_not_received_loans,
                                    }
                                )

                    elif task_name == ReattemptGroups.WHATSAPP_SENT_BUT_NOT_DELIVERED.value:
                        comm_data = task_result[2]
                        if comm_data:
                            if comm_data[0].get("loan_ids"):
                                app.logger.debug(f"get_campaign_errors.comm_data: {comm_data}")
                                whatsapp_sent_but_not_delivered_loans = comm_data[0].get("loan_ids", [])
                                whatsapp_sent_but_not_delivered_loans = list(set(whatsapp_sent_but_not_delivered_loans))
                                whatsapp_sent_but_not_delivered.append(
                                    {
                                        "error": ReattemptErrors.WHATSAPP_SENT_BUT_NOT_DELIVERED_ATTEMPT.value,
                                        "loan_ids": whatsapp_sent_but_not_delivered_loans,
                                    }
                                )

                    elif task_name == ReattemptGroups.QUEUE_FAILURES.value:
                        campaign_channel_data = task_result[2]
                        if campaign_channel_data:
                            app.logger.debug(f"get_campaign_errors.campaign_channel_data: {campaign_channel_data}")
                            for data in campaign_channel_data:
                                loan_ids = list(set(data.get("loan_ids")))
                                queue_failures.append(
                                    {
                                        "error": data["error_name"].replace("_", " ").lower()
                                        if data.get("error_name")
                                        else "",
                                        "loan_ids": loan_ids,
                                    }
                                )

                    elif task_name == ReattemptGroups.OPERATOR_FAILURES.value:
                        comm_error_data = task_result[2]
                        if comm_error_data:
                            app.logger.debug(f"get_campaign_errors.comm_error_data: {comm_error_data}")
                            for data in comm_error_data:
                                loan_ids = list(set(data.get("loan_ids")))
                                operator_failures.append(
                                    {
                                        "error": data["error_name"].replace("_", " ").lower()
                                        if data.get("error_name")
                                        else "",
                                        "loan_ids": loan_ids,
                                    }
                                )

                    elif task_name == ReattemptGroups.IS_LINK_CLICKED.value:
                        link_clicked_data = task_result[2]
                        if (
                            link_clicked_data
                            and isinstance(link_clicked_data, list)
                            and link_clicked_data[0].get("loan_ids")
                        ):
                            app.logger.debug(f"get_campaign_errors.link_clicked_data: {link_clicked_data}")
                            link_clicked_loans = list(set(link_clicked_data[0]["loan_ids"]))
                            link_clicked_loan_count = len(link_clicked_loans)
                            link_clicked.append(
                                {
                                    "error": ReattemptErrors.LINK_CLICKED_ATTEMPT.value,
                                    "loan_count": link_clicked_loan_count,
                                    "percent_count": round(100 * link_clicked_loan_count / total_loan_count),
                                }
                            )
                            if not count:
                                link_clicked[0]["loan_ids"] = link_clicked_loans

                    elif task_name == ReattemptGroups.FOR_LESS_THAN.value:
                        for_less_than_data = task_result[2]
                        if (
                            for_less_than_data
                            and isinstance(for_less_than_data, list)
                            and for_less_than_data[0].get("loan_ids")
                        ):
                            app.logger.debug(f"get_campaign_errors.for_less_than_data: {for_less_than_data}")
                            answered_less_than_loans = list(set(for_less_than_data[0]["loan_ids"]))
                            answered_loans.extend(answered_less_than_loans)
                            answered_less_than.append(
                                {
                                    "error": ReattemptErrors.ANSWERED_LESS_THAN_ATTEMPT.value,
                                    "loan_ids": answered_less_than_loans,
                                }
                            )

                    elif task_name == ReattemptGroups.FOR_GREATER_THAN.value:
                        for_greater_than_data = task_result[2]
                        if (
                            for_greater_than_data
                            and isinstance(for_greater_than_data, list)
                            and for_greater_than_data[0].get("loan_ids")
                        ):
                            app.logger.debug(f"get_campaign_errors.for_greater_than_data: {for_greater_than_data}")
                            answered_greater_than_loans = list(set(for_greater_than_data[0]["loan_ids"]))
                            answered_loans.extend(answered_greater_than_loans)
                            answered_greater_than.append(
                                {
                                    "error": ReattemptErrors.ANSWERED_GREATER_THAN_ATTEMPT.value,
                                    "loan_ids": answered_greater_than_loans,
                                }
                            )

                    elif task_name == ReattemptGroups.RESPONDED_TIME.value:
                        responded_data = task_result[2]
                        if responded_data and isinstance(responded_data, list) and responded_data[0].get("loan_ids"):
                            app.logger.debug(f"get_campaign_errors.responded_data: {responded_data}")
                            dtmf_responded_loans = list(set(responded_data[0]["loan_ids"]))
                            responded_loan_count = len(dtmf_responded_loans)
                            responded.append(
                                {
                                    "error": ReattemptErrors.RESPONDED_ATTEMPT.value,
                                    "loan_count": responded_loan_count,
                                    "percent_count": round(100 * responded_loan_count / total_loan_count),
                                }
                            )
                            if not count:
                                responded[0]["loan_ids"] = dtmf_responded_loans

                    elif task_name == ReattemptGroups.OPENED_TIME.value:
                        opened_data = task_result[2]
                        if opened_data and isinstance(opened_data, list) and opened_data[0].get("loan_ids"):
                            app.logger.debug(f"get_campaign_errors.opened_data: {opened_data}")
                            opened_loans = list(set(opened_data[0]["loan_ids"]))
                            opened.append(
                                {
                                    "error": ReattemptErrors.OPENED_ATTEMPT.value,
                                    "loan_ids": opened_loans,
                                }
                            )
                    elif task_name == ReattemptGroups.TRIGGERED.value:
                        triggered_data = task_result[2]
                        if triggered_data and isinstance(triggered_data, list) and triggered_data[0].get("loan_ids"):
                            app.logger.debug(f"get_campaign_errors.triggered_data: {triggered_data}")
                            triggered_loans = list(set(triggered_data[0]["loan_ids"]))

                else:
                    response["message"] = db_response_message
                    response["status_code"] = status_code
                    response["success"] = False
                    return response

        reattempt_failures = {}
        if select_all:
            reattempt_failures[ReattemptErrors.SELECT_ALL_ATTEMPT.value] = select_all
        if link_clicked:
            reattempt_failures[ReattemptErrors.LINK_CLICKED_ATTEMPT.value] = link_clicked
        if responded:
            reattempt_failures[ReattemptErrors.RESPONDED_ATTEMPT.value] = responded
        if queue_failures:
            queue_failure_data = []
            for queue_failure in queue_failures:
                loan_ids = queue_failure.pop("loan_ids", [])
                if helicarrier_trigger and channel != RequestTypeChoices.NA.value:
                    loan_ids = list(set(loan_ids) - set(triggered_loans) - set(queue_failure_loans))
                if loan_ids:
                    queue_failure_loans.extend(loan_ids)
                    loan_ids_count = len(loan_ids)
                    queue_failure["loan_count"] = loan_ids_count
                    queue_failure["percent_count"] = round(100 * loan_ids_count / total_loan_count)
                    if not count:
                        queue_failure["loan_ids"] = loan_ids
                    queue_failure_data.append(queue_failure)
            if queue_failure_data:
                reattempt_failures[ReattemptErrors.NOT_TRIGGERED_ATTEMPT.value] = queue_failure_data
        if operator_failures:
            operator_failure_data = []
            for operator_failure in operator_failures:
                loan_ids = operator_failure.pop("loan_ids", [])
                loan_ids = list(
                    set(loan_ids)
                    - set(link_clicked_loans)
                    - set(opened_loans)
                    - set(dtmf_responded_loans)
                    - set(answered_loans)
                    - set(triggered_delivered_loans)
                    - set(whatsapp_sent_but_not_delivered_loans)
                    - set(operator_failure_loans)
                )
                if loan_ids:
                    operator_failure_loans.extend(loan_ids)
                    loan_ids_count = len(loan_ids)
                    operator_failure["loan_count"] = loan_ids_count
                    operator_failure["percent_count"] = round(100 * loan_ids_count / total_loan_count)
                    if not count:
                        operator_failure["loan_ids"] = loan_ids
                    operator_failure_data.append(operator_failure)
            if operator_failure_data:
                reattempt_failures[ReattemptErrors.NOT_DELIVERED_ATTEMPT.value] = operator_failure_data
        if triggered_and_delivered:
            data = triggered_and_delivered.pop(0)
            loan_ids = data.pop("loan_ids", [])
            loan_ids = list(
                set(loan_ids)
                - set(link_clicked_loans)
                - set(opened_loans)
                - set(dtmf_responded_loans)
                - set(answered_loans)
            )
            if loan_ids:
                loan_ids_count = len(loan_ids)
                data["loan_count"] = loan_ids_count
                data["percent_count"] = round(100 * loan_ids_count / total_loan_count)
                if not count:
                    data["loan_ids"] = loan_ids
                reattempt_failures[ReattemptErrors.TRIGGERED_AND_DELIVERED_ATTEMPT.value] = [data]
        if webhook_not_received:
            data = webhook_not_received.pop(0)
            loan_ids = data.pop("loan_ids", [])
            loan_ids = list(
                set(loan_ids)
                - set(link_clicked_loans)
                - set(opened_loans)
                - set(dtmf_responded_loans)
                - set(answered_loans)
                - set(triggered_delivered_loans)
                - set(whatsapp_sent_but_not_delivered_loans)
            )
            if loan_ids:
                loan_ids_count = len(loan_ids)
                data["loan_count"] = loan_ids_count
                data["percent_count"] = round(100 * loan_ids_count / total_loan_count)
                if not count:
                    data["loan_ids"] = loan_ids
                reattempt_failures[ReattemptErrors.WEBHOOK_NOT_RECEIVED_ATTEMPT.value] = [data]
        if whatsapp_sent_but_not_delivered:
            data = whatsapp_sent_but_not_delivered.pop(0)
            loan_ids = data.pop("loan_ids", [])
            loan_ids = list(
                set(loan_ids)
                - set(link_clicked_loans)
                - set(opened_loans)
                - set(dtmf_responded_loans)
                - set(answered_loans)
                - set(triggered_delivered_loans)
            )
            if loan_ids:
                loan_ids_count = len(loan_ids)
                data["loan_count"] = loan_ids_count
                data["percent_count"] = round(100 * loan_ids_count / total_loan_count)
                if not count:
                    data["loan_ids"] = loan_ids
                reattempt_failures[ReattemptErrors.WHATSAPP_SENT_BUT_NOT_DELIVERED_ATTEMPT.value] = [data]
        if answered_less_than:
            data = answered_less_than.pop(0)
            loan_ids = data.pop("loan_ids", [])
            loan_ids = list(set(loan_ids) - set(answered_greater_than_loans) - set(dtmf_responded_loans))
            if loan_ids:
                loan_ids_count = len(loan_ids)
                data["loan_count"] = loan_ids_count
                data["percent_count"] = round(100 * loan_ids_count / total_loan_count)
                if not count:
                    data["loan_ids"] = loan_ids
                reattempt_failures[ReattemptErrors.ANSWERED_LESS_THAN_ATTEMPT.value] = [data]
        if answered_greater_than:
            data = answered_greater_than.pop(0)
            loan_ids = data.pop("loan_ids", [])
            loan_ids = list(set(loan_ids) - set(dtmf_responded_loans))
            if loan_ids:
                loan_ids_count = len(loan_ids)
                data["loan_count"] = loan_ids_count
                data["percent_count"] = round(100 * loan_ids_count / total_loan_count)
                if not count:
                    data["loan_ids"] = loan_ids
                reattempt_failures[ReattemptErrors.ANSWERED_GREATER_THAN_ATTEMPT.value] = [data]
        if opened:
            data = opened.pop(0)
            loan_ids = data.pop("loan_ids", [])
            loan_ids = list(set(loan_ids) - set(link_clicked_loans))
            if loan_ids:
                loan_ids_count = len(loan_ids)
                data["loan_count"] = loan_ids_count
                data["percent_count"] = round(100 * loan_ids_count / total_loan_count)
                if not count:
                    data["loan_ids"] = loan_ids
                reattempt_failures[ReattemptErrors.OPENED_ATTEMPT.value] = [data]

        response["data"] = reattempt_failures

        if campaign_errors:
            reattempt_failures_filtered = {}
            for error_heading, error_object in reattempt_failures.items():
                if error_heading in campaign_errors.keys():
                    error_list = campaign_errors[error_heading]
                    for error_loan_data in error_object:
                        error_name = error_loan_data["error"]
                        if error_name in error_list:
                            if reattempt_failures_filtered.get(error_heading):
                                reattempt_failures_filtered[error_heading].append(error_loan_data)
                            else:
                                reattempt_failures_filtered[error_heading] = []
                                reattempt_failures_filtered[error_heading].append(error_loan_data)
            response["data"] = reattempt_failures_filtered

    except Exception as e:
        app.logger.error(f"app.routes.get_campaign_errors.exception :: {str(e)}")
        response["message"] = f"Failed to fetch campaign error records:: {str(e)}"
        response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        response["success"] = False

    return response


async def retrigger_campaign(campaign_id, company_id, channel, reattempt_on={}):
    app.logger.info(f"app.service.retrigger_campaign")

    response = {"message": "Campaign Data Fetched Successfully", "success": True, "status_code": HTTPStatus.OK.value}
    try:
        query = f"select name as campaign_name, data, type, description from campaigns where campaign_id= '{campaign_id}' and channel= '{channel}' and company_id= '{company_id}';"
        status_code, message, campaign_data = await execute_db_query(query=query, db_instance=app.campaign_db)
        if status_code == HTTPStatus.OK.value:
            if campaign_data:
                campaign_data = campaign_data[0]
                campaign_name = campaign_data.get("campaign_name")
                campaign_meta_data = json.loads(campaign_data.get("data", "{}"))
                campaign_type = campaign_data.get("type")
                campaign_description = campaign_data.get("description")
                allocation_month = campaign_meta_data.get("allocation_month")

                bulk_comm_payload = {
                    "company_id": company_id,
                    "allocation_month": allocation_month,
                    "params": f"company_id={company_id}",
                    "module": "communication",
                    "loan_key": "loan_data",
                    "module_method": "POST",
                    "linked": campaign_meta_data.get("linked", False),
                    "payload": {
                        "allocation_month": allocation_month,
                        "campaign_data": {
                            "channel": channel,
                            "description": campaign_description,
                            "name": f"Retriggered({campaign_name})",
                            "type": campaign_type,
                        },
                        "template_id": campaign_meta_data.get("template_id"),
                        "template_name": campaign_meta_data.get("template_name"),
                        "send_to": campaign_meta_data.get("send_to"),
                        "upto_index": campaign_meta_data.get("upto_index"),
                        "communication_level": campaign_meta_data.get("communication_level"),
                        "amount_type": campaign_meta_data.get("amount_type"),
                        "link_expiry_info": campaign_meta_data.get("link_expiry_info", {}),
                        "use_generated_payment_link": campaign_meta_data.get("use_generated_payment_link", False),
                        "filters": {
                            "campaign_filter": [f"Retriggered Bulk Request ({campaign_name})"],
                        },
                    },
                }
                if channel == RequestTypeChoices.email.value:
                    bulk_comm_payload["payload"]["mention_email_cc"] = campaign_meta_data.get("mention_email_cc", [])
                    bulk_comm_payload["payload"]["mention_email_bcc"] = campaign_meta_data.get("mention_email_bcc", [])
                    bulk_comm_payload["payload"]["email_contacts"] = campaign_meta_data.get("email_contacts", "")

                if reattempt_on:
                    reattempt_filters = []
                    selected_loan_ids = []
                    for error_heading, error_object in reattempt_on.items():
                        for error_name, reattempt_loan_ids in error_object.items():
                            if reattempt_loan_ids:
                                selected_loan_ids.extend(reattempt_loan_ids)
                                reattempt_filters.append(error_name)

                    logger.debug(f"retrigger_campaign.loan_ids :: {selected_loan_ids}")
                    selected_loan_ids = list(set(selected_loan_ids))
                    bulk_comm_payload["selected"] = selected_loan_ids
                    bulk_comm_payload["total_loan_ids"] = len(selected_loan_ids)
                    bulk_comm_payload["payload"]["filters"]["reattempt_filters"] = reattempt_filters
                response["data"] = bulk_comm_payload

            else:
                response["message"] = "No Campaign record found"
                response["status_code"] = HTTPStatus.BAD_REQUEST.value
                response["success"] = False
        else:
            response["message"] = message
            response["success"] = False
            response["status_code"] = status_code
            return response

    except Exception as e:
        app.logger.error(f"app.routes.campaign_reattempt.exception :: {str(e)}")
        response["message"] = f"Failed to fetch campaign records."
        response["success"] = False
        response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value

    return response


async def get_master_campaign_channel_count(company_id, campaign_data):
    app.logger.info(f"app.service.get_master_campaign_channel_count")
    response = {"message": None, "success": False, "status_code": None, "data": {}}
    try:
        master_campaign_ids = [campaign["campaign_id"] for campaign in campaign_data]
        master_campaign_ids = (
            f"('{master_campaign_ids[0]}')" if len(master_campaign_ids) == 1 else tuple(master_campaign_ids)
        )
        query = f"SELECT parent_campaign_id, COUNT(*) as channel_count FROM campaigns WHERE company_id = '{company_id}' AND is_deleted = False AND parent_campaign_id in {master_campaign_ids} group by parent_campaign_id;"
        campaign_data = await app.campaign_db.execute_raw_select_query(query)
        if not isinstance(campaign_data, list):
            response["message"] = f"Failed to fetch master campaign channel count"
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        elif not campaign_data:
            response["success"] = True
            response["message"] = f"Master campaign channel count not found"
            response["status_code"] = HTTPStatus.OK.value
        else:
            response["success"] = True
            response["data"] = {campaign["parent_campaign_id"]: campaign["channel_count"] for campaign in campaign_data}
    except Exception as e:
        app.logger.error(f"app.routes.get_master_campaign_channel_count.exception :: {str(e)}")
        response["message"] = f"Failed to fetch master campaign channel count"
        response["success"] = False
        response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
    return response


async def get_master_campaign_details(columns, where):
    app.logger.info(f"app.service.get_master_campaign_details")
    response = {"message": None, "success": True, "status_code": HTTPStatus.OK.value, "data": []}
    try:
        campaign_data = await app.campaign_db.select(table="campaigns", columns=columns, where=where)
        if not isinstance(campaign_data, list):
            response["success"] = False
            response["message"] = f"Failed to fetch master campaign details"
            response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        elif not campaign_data:
            response["message"] = f"Master campaign details not found"
        else:
            response["data"] = campaign_data
            response["message"] = f"Successfully fetched Master campaign details"
    except Exception as e:
        app.logger.error(f"app.routes.get_master_campaign_details.exception :: {str(e)}")
        response["message"] = f"Failed to fetch master campaign details"
        response["success"] = False
        response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
    return response
