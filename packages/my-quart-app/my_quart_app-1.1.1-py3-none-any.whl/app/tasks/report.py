"""
report.py
Usage: Generate Report
"""
import uuid
import xlsxwriter
import io
import json
import requests
import boto3
import base64
import csv
import shortuuid
import logging
import pathlib
import datetime
import os
from botocore import config as boto_config
from botocore.exceptions import ClientError
from app.utils import get_s3_client, validate_email

# from app.tasks.notice.notice_callback.commons import upload_file_to_s3
from celery import shared_task
from http import HTTPStatus
from ..settings import (
    AI_COMPLETION_REPORT_SENDGRID_ID,
    COMMUNICATION_SERVICE_BASE_URL,
    QUEUE_SERVICE_BASE_URL,
    RECOVERY_SERVICE_BASE_URL,
    SENDGRID_API_KEY,
    SENDGRID_TEMPLATE_ID,
    CAMPAIGN_SENDGRID_TEMPLATE_ID,
    BATCH_SENDGRID_TEMPLATE_ID,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_DEFAULT_REGION,
    S3_BUCKET_NAME,
    REPORT_SENDGRID_TEMPLATE_ID,
    COMPLETION_REPORT_SENDGRID_ID,
    UI_SERVICE_BASE_URL,
    EXPORTS_BUCKET_NAME,
    BCC_EMAILS,
    COUNTRY_WISE_MAPPING,
)
from ..choices import (
    REQUEST_COMPLETION_SMS_TEMP_ID,
    TypeOfTaskChoices,
    QueueTypeChoices,
    RequestTypeChoices,
    PROD_ENV,
    AI_RULE_EMAIL,
    CampaignTriggerTypeChoices,
    CampaignDeliveryTypeChoices,
    THRESHOLD_PERCENTAGE,
    COMPLETION_PERCENTAGE,
    PRINCIPAL_ENTITY_ID,
    MODULE,
    SOURCE,
    ColumnMapChoices,
    CAMPAIGN_STOPPED_ERROR_CODE,
)
from ..utils import format_email_dict, get_campaign_summary, get_users_details
from ..service import (
    create_dynamic_template,
    create_batch_dynamic_template,
    trigger_sms_communication,
    get_campaign_report_data,
    trigger_email_communication,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
s3_v4_config = boto_config.Config(signature_version="s3v4")

QUEUE_FAILURE = "QUEUE_FAILURE"


@shared_task(name="calculate_report_data", bind=True, ignore_result=False)
def calculate_report_data(self, *args, **kwargs):
    logger.info(f"calculate_report_data{kwargs}")
    type_of_task = kwargs["type_of_task"]
    url = f"{QUEUE_SERVICE_BASE_URL}/get_batch_number?batch_number=all&batch_id={kwargs['batch_id']}"
    try:
        batch_data = requests.request(
            method="GET",
            url=url,
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-Request-ID": kwargs["request_id"],
            },
        )
        logger.info(f"get_batch_number.status_code :: {batch_data.status_code}")
    except Exception as e:
        logger.info(f"get_batch_number.exception :: {str(e)}")
        return False

    if batch_data.status_code not in (200, 201):
        logger.info(f"get_batch_number.text :: {batch_data.text}")
        return False

    batch_data = json.loads(batch_data.text)

    data_list = batch_data["data"]
    report_string = "\n"
    failed_loan_data = []
    failed_loan_ids_list = []
    success_loan_data = []
    failed_data = []

    if data_list != []:
        time_data = data_list[0]
        time_data = json.loads(time_data["extras"])
        triggered_time = time_data["triggered_time"]

    for data in data_list:
        batch_status = json.loads(data["batch_status"])
        failed = batch_status["failed"]
        success = batch_status["success"]
        failed_loan_data.extend(failed)
        success_loan_data.extend(success)

    if type_of_task == TypeOfTaskChoices.scrape_indiapost.value:
        kwargs["company"] = "Credgenics"
        for fail_data in failed_loan_data:
            reason = fail_data["reason"]
            loan_id = fail_data["loan_id"]
            status_code = fail_data["status_code"]
            company_id = fail_data["company_id"]
            tracking_id = fail_data["tracking_id"]

            failed_loan_ids_list.append(loan_id)
            failed_data.append((loan_id, company_id, tracking_id, reason, status_code))
            report_string = report_string + f"<p>{loan_id} --company_id::{company_id} -- reason :: {reason}<p>"
    else:
        organisation_details_url = f"{RECOVERY_SERVICE_BASE_URL}/organisation/details?company_id={kwargs['company_id']}"
        try:
            organisation_data = requests.request(
                method="GET",
                url=organisation_details_url,
                headers={
                    "Content-Type": "application/json",
                    "X-CG-User": json.dumps(kwargs["user"]),
                    "X-Request-ID": kwargs["request_id"],
                },
            )
        except Exception as e:
            logger.info(f"organisation_data.exception :: {str(e)}")
            return False

        if organisation_data.status_code not in (200, 201):
            logger.info(f"organisation_data.text :: {organisation_data.text}")
            return False
        organisation_data = json.loads(organisation_data.text)
        for fail_data in failed_loan_data:
            reason = fail_data["reason"]
            loan_id = fail_data["loan_id"]
            status_code = fail_data["status_code"]

            failed_loan_ids_list.append(loan_id)
            failed_data.append((loan_id, reason, status_code))
            report_string = report_string + f"<p>{loan_id} -- reason :: {reason}<p>"
        kwargs["company"] = organisation_data["output"]["trademark"]

    kwargs["report_string"] = report_string
    kwargs["failed_loan_ids_list"] = failed_loan_ids_list
    kwargs["success_loan_ids_list"] = success_loan_data
    kwargs["failed_data"] = failed_data
    kwargs["triggered_time"] = triggered_time
    send_email_report.apply_async(queue=kwargs["queue"], kwargs=kwargs)
    return True


@shared_task(bind=True, name="queue_report_attach")
def queue_report_attach(self, *args, **kwargs):
    headers = {
        "authorization": f"Bearer {SENDGRID_API_KEY}",
        "content-type": "application/json",
        "Accept": "application/json",
    }
    mail_data = {
        "from": kwargs["from_data"],
        "reply_to": {"email": "reports@credgenics.com"},
        "personalizations": [
            {
                "to": [{"email": kwargs["to_email"]}],
                "cc": [{"email": "demo.agent@credgenics.com", "name": "Demo Agent"}],
                "dynamic_template_data": kwargs["dynamic_template_data"],
            }
        ],
        "template_id": kwargs["sendgrid_template_id"],
    }
    logger.info(f"mail_data:{mail_data}")
    file_path = None
    if kwargs["failed_loan_ids_list"] > 0:
        logger.info(f"failed_loan_ids: {kwargs['failed_loan_ids_list']}")
        unique_mail_id = shortuuid.ShortUUID().random(length=8)
        logger.info(f"unique_id: {unique_mail_id}")
        failed_data = kwargs["failed_data"]
        type_of_task = kwargs["type_of_task"]
        if type_of_task == TypeOfTaskChoices.scrape_indiapost.value:
            fields = ["Loan Id", "Company Id", "Tracking Id", "Reason", "Status code"]
        else:
            fields = ["Loan Id", "Reason", "Status code"]
        filename = f"bulk_{type_of_task}_report_{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.csv"

        with open(filename, "w") as csvfile:
            file_writer = csv.writer(csvfile)
            file_writer.writerow(fields)
            file_writer.writerows(failed_data)

        file_path = f"{pathlib.Path().absolute()}/{filename}"
        with open(file_path, "rb") as f:
            file_data = f.read()
            f.close()

        # Encode contents of file as Base 64
        encoded = base64.b64encode(file_data).decode()
        mail_data["attachments"] = [
            {
                "content": encoded,
                "content_id": unique_mail_id,
                "disposition": "inline",
                "filename": filename,
                "name": filename,
                "type": "csv",
            }
        ]
    response = requests.request(
        method="POST",
        url="https://api.sendgrid.com/v3/mail/send",
        data=json.dumps(mail_data),
        headers=headers,
    )
    logger.info(f"queue_report_attach :: {response.status_code}")
    if file_path:
        pathlib.Path(f"{file_path}").unlink()
    if response.status_code != HTTPStatus.ACCEPTED.value:
        logger.info(f"queue_report_attach :: {dir(response)}")
        logger.info(f"queue_report_attach :: {response.text}")
        return False
    return True


@shared_task(name="send_email_report", bind=True, ignore_result=False)
def send_email_report(self, *args, **kwargs):
    logger.info(f"send_email_report_kwargs:{kwargs}")
    author = kwargs["author"]
    company = kwargs["company"]
    batch_id = kwargs["batch_id"]
    total_number_of_loan_ids = kwargs["total_loans"]
    type_of_task = kwargs["type_of_task"].replace("_", " ")
    queue_env = self.app.conf.QUEUE_NAME.lower()

    success_loan_ids_list = kwargs["success_loan_ids_list"]
    failed_loan_ids_list = kwargs["failed_loan_ids_list"]
    failed_data = kwargs["failed_data"]
    triggered_time = kwargs["triggered_time"]
    linked_loan = kwargs.get("linked_loan", False)
    logger.info(f"queue name: {kwargs['queue']}")
    try:
        user_name = author.split("@")[0]
        if linked_loan == True:
            report_message = "Total linked loan Id's"
        else:
            report_message = "Total Loan accounts"
        sendgrid_template_id = f"{SENDGRID_TEMPLATE_ID}"
        dynamic_template_data = {
            "user_name": user_name,
            "type_of_task": type_of_task,
            "company": company,
            "total_number_of_loan_ids": total_number_of_loan_ids,
            "success_loan_ids_list": len(success_loan_ids_list),
            "failed_loan_ids_list": len(failed_loan_ids_list),
            "triggered_time": triggered_time,
            "batch_id": batch_id,
            "report_message": report_message,
            "env": queue_env if queue_env != PROD_ENV else None,
        }
        if kwargs.get("template_id", None):
            dynamic_template_data["template_id"] = kwargs.get("template_id")
        if kwargs.get("draft_id", None):
            dynamic_template_data["draft_id"] = kwargs.get("draft_id")
        if kwargs.get("template_name", None):
            dynamic_template_data["template_name"] = kwargs.get("template_name")
        if kwargs.get("rule_id", None) and kwargs.get("rule_name", None):
            dynamic_template_data["rule_id"] = kwargs.get("rule_id")
            dynamic_template_data["rule_name"] = kwargs.get("rule_name")
        if kwargs.get("applied_filter", None):
            filters = kwargs.get("applied_filter")
            filters = filters.replace("&", " ;&")
            filters = filters.split("&")
            dynamic_template_data["applied_filter"] = filters

        kwargs["failed_loan_ids_list"] = len(failed_loan_ids_list)
        kwargs["dynamic_template_data"] = dynamic_template_data
        kwargs["to_email"] = author
        kwargs["failed_data"] = failed_data
        kwargs["from_data"] = {
            "name": f"{type_of_task.capitalize()} Report",
            "email": "reports@credgenics.com",
        }
        kwargs["sendgrid_template_id"] = sendgrid_template_id
        queue_report_attach.apply_async(queue=kwargs["queue"], kwargs=kwargs)
    except Exception as e:
        logger.error(f"send_email_report.exception:{str(e)}")
        return False
    return True


################################################################################
######################## Queue Report ##############################################
################################################################################


@shared_task(bind=True, name="send_report")
def send_report(self, *args, **kwargs):
    logger.info("app.tasks.report.send_report")
    completion_report = kwargs.get("completion_report", False)
    queue_report = kwargs.get("queue_report", False)
    campaign_id = kwargs.get("campaign_id")
    cc_emails = [{"email": "demo.agent@credgenics.com", "name": "Demo Agent"}]
    trigger_stop_count = kwargs.get("trigger_stop_count")

    if kwargs.get("cc_emails"):
        cc_emails.extend(kwargs.get("cc_emails"))
    bcc_emails = kwargs.get("bcc_emails")
    dynamic_template_data = kwargs["dynamic_template_data"]
    if isinstance(kwargs["to_email"], list):
        email_to = []
        for email in kwargs["to_email"]:
            email_to.append({"email": email})
    else:
        email_to = [{"email": kwargs["to_email"]}]
    if dynamic_template_data.get("triggered_time"):
        dynamic_template_data["triggered_time"] = dynamic_template_data["triggered_time"].split(".")[0]
    mail_data = {
        "from": kwargs["from_data"],
        "reply_to": {"email": "reports@credgenics.com"},
        "personalizations": [
            {
                "to": email_to,
                "cc": cc_emails,
                "dynamic_template_data": dynamic_template_data,
            }
        ],
        "template_id": kwargs["sendgrid_template_id"],
    }
    if bcc_emails:
        mail_data["personalizations"][0]["bcc"] = bcc_emails
    filename = kwargs.get("filename", None)
    logger.debug(f"send_report.file_attachment: {filename}")
    if filename:
        unique_mail_id = shortuuid.ShortUUID().random(length=8)
        logger.info(f"send_report.unique_id: {unique_mail_id}")
        mail_data["attachments"] = [
            {
                "content": kwargs["encoded"],
                "content_id": unique_mail_id,
                "disposition": "inline",
                "filename": filename,
                "name": filename,
                "type": "csv",
            }
        ]
    logger.debug(f"send_report.mail_data:{mail_data}")
    mail_data["module"] = MODULE
    mail_data["source"] = SOURCE
    response_text, response_status_code = trigger_email_communication(mail_data)
    logger.debug(f"send_report.mail_data.response.status_code ::{response_status_code}")
    if filename:
        path = pathlib.Path(f"{pathlib.Path().absolute()}/{filename}")
        if path.exists():
            path.unlink()

    if response_status_code != HTTPStatus.OK.value:
        logger.error(f"send_report.mail_data.error ::{response_text}")
        return False
    if completion_report:
        total_loans = kwargs.get("total_loans")
        delivery_progress_count = kwargs.get("delivery_progress_count")
        delivery_status = kwargs.get("delivery_status")
        trigger_progress_count = f"{total_loans}/{total_loans}"
        trigger_status = CampaignTriggerTypeChoices.completed.value
        payload = {
            "table": "campaigns",
            "set_clause": {
                "email_report_sent": "email_report_sent",
                "delivery_status": "delivery_status",
                "delivery_progress_count": "delivery_progress_count",
                "trigger_status": "trigger_status",
                "trigger_progress_count": "trigger_progress_count",
                "trigger_stop_count": "trigger_stop_count",
            },
            "from_values": [
                f"('{campaign_id}', true, '{delivery_status}', '{delivery_progress_count}', '{trigger_status}', '{trigger_progress_count}', {trigger_stop_count})"
            ],
            "from_columns": [
                "campaign_id",
                "email_report_sent",
                "delivery_status",
                "delivery_progress_count",
                "trigger_status",
                "trigger_progress_count",
                "trigger_stop_count",
            ],
            "from_alias_name": "cd",
            "where": {"campaign_id": "campaign_id"},
        }
        update_data_kwargs = {
            "payload": payload,
            "user": kwargs["user"],
            "request_id": kwargs["request_id"],
        }
        update_data.apply_async(
            queue=f"{self.app.conf.QUEUE_NAME}_{QueueTypeChoices.campaign_update.value}",
            kwargs=update_data_kwargs,
        )
    elif queue_report and campaign_id:
        total_loans = dynamic_template_data.get("total_loans")
        trigger_progress_count = f"{total_loans}/{total_loans}"
        trigger_status = CampaignTriggerTypeChoices.completed.value
        payload = {
            "table": "campaigns",
            "set_clause": {
                "trigger_status": "trigger_status",
                "trigger_progress_count": "trigger_progress_count",
                "trigger_stop_count": "trigger_stop_count",
            },
            "from_values": [f"('{campaign_id}', '{trigger_status}', '{trigger_progress_count}', {trigger_stop_count})"],
            "from_columns": [
                "campaign_id",
                "trigger_status",
                "trigger_progress_count",
                "trigger_stop_count",
            ],
            "from_alias_name": "cd",
            "where": {"campaign_id": "campaign_id"},
        }
        update_data_kwargs = {
            "payload": payload,
            "user": kwargs["user"],
            "request_id": kwargs["request_id"],
        }
        update_data.apply_async(
            queue=f"{self.app.conf.QUEUE_NAME}_{QueueTypeChoices.campaign_update.value}",
            kwargs=update_data_kwargs,
        )

    return True


@shared_task(name="report_data", bind=True, ignore_result=False)
def report_data(self, *args, **kwargs):
    """
    Makes data for generating csv file and report template data
    """
    logger.info(f"app.tasks.report.report_data")
    payload = kwargs["payload"]
    channel = payload["channel"]
    failed_data = kwargs["failed_data"]
    dynamic_template_data = kwargs["dynamic_template_data"]
    campaign_id = dynamic_template_data.get("campaign_id", "")
    batch_id = dynamic_template_data.get("batch_id", "")
    logger.info(f"report_data.dynamic_template_data.campaign_id {campaign_id}")
    logger.info(f"report_data.dynamic_template_data.batch_id {batch_id}")
    try:
        if dynamic_template_data["failed"] > 0:
            if channel == TypeOfTaskChoices.indiapost_tracking.value:
                fields = [
                    "Loan Id",
                    "Company Id",
                    "Tracking Number",
                    "Reason",
                    "Status code",
                ]
            elif channel == TypeOfTaskChoices.indiapost_upload.value:
                fields = ["Loan Id", "Tracking Number", "Reason", "Status code"]
            else:
                fields = ["Loan Id", "Reason", "Status code"]
            if kwargs.get("type_of_task", ""):
                filename = (
                    f"{kwargs.get('type_of_task')}_report_{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.csv"
                )
            else:
                filename = f"{channel}_report_{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.csv"

            with open(filename, "w") as csvfile:
                file_writer = csv.writer(csvfile)
                file_writer.writerow(fields)
                file_writer.writerows(failed_data)
            file_path = f"{pathlib.Path().absolute()}/{filename}"
            with open(file_path, "rb") as f:
                file_data = f.read()
                f.close()

            if channel == TypeOfTaskChoices.digital.value:
                s3_failure_report_excel_path = f"digital_notice_reports/reports/{batch_id}.csv"

                s3 = get_s3_client()

                if os.path.exists(file_path):
                    upload_file_to_s3(s3, file_path, S3_BUCKET_NAME, s3_failure_report_excel_path)

                    try:
                        url = f"{QUEUE_SERVICE_BASE_URL}/update_batch_response"
                        data = {
                            "batch_id": batch_id,
                            "s3_error_report_excel_path": s3_failure_report_excel_path,
                        }
                        headers = {
                            "Content-Type": "application/json",
                            "X-CG-User": json.dumps(payload["user"]),
                            "X-Request-ID": payload["request_id"],
                            "X-CG-Company": json.dumps(payload["company"]),
                        }

                        update_response = requests.request(method="PATCH", url=url, json=data, headers=headers)

                        logger.debug(
                            "update_batch_response.status_code:: %s",
                            update_response.status_code,
                        )

                        if update_response.status_code != 200:
                            logger.debug(
                                "update_batch_response.response:: %s",
                                update_response.text,
                            )

                    except Exception as e:
                        logger.error("report.report_data Exception: %s", e)

            # Encode contents of file as Base 64
            encoded = base64.b64encode(file_data).decode()
            kwargs["encoded"] = encoded
            kwargs["filename"] = filename
        kwargs["campaign_id"] = campaign_id
        kwargs["user"] = payload.get("user")
        kwargs["request_id"] = payload.get("request_id")
        kwargs["queue_report"] = True

        send_report.apply_async(
            queue=f"{self.app.conf.QUEUE_NAME}_{QueueTypeChoices.result.value}",
            kwargs=kwargs,
        )
    except Exception as e:
        logger.error(f"report_data.exception.error :: {str(e)}")
        return False
    return True


@shared_task(name="campaign_comm_export", bind=True, ignore_result=False)
def campaign_comm_export(self, *args, **kwargs):
    """
    {
        "campaign_id": "3c2e8ea080ef4f32a81740950085ee34",
        "channel": "email"
    }
    """
    logger.info(f"app.tasks.report.campaign_comm_export")
    company_id = kwargs["company_id"]
    channel = kwargs["channel"]
    campaign_id = kwargs["campaign_id"]
    queue = kwargs["queue"]
    is_deleted = kwargs.get("is_deleted", False)

    url = f"{COMMUNICATION_SERVICE_BASE_URL}/export/{channel}?company_id={company_id}"
    logger.debug(f"campaign_comm_export.export.url: {url}")
    try:
        response_data = {
            "campaign_id": campaign_id,
            "response_type": "data",
            "source": "campaign_report",
            "is_deleted": is_deleted,
        }
        campaign_comm_export = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-Request-ID": kwargs["request_id"],
                "X-CG-Company": json.dumps(kwargs["company"]),
            },
        )
        logger.debug(f"campaign_comm_export.status_code :: {campaign_comm_export.status_code}")
    except Exception as e:
        logger.error(f"campaign_comm_export..exception :: {str(e)}")
        return False

    if campaign_comm_export.status_code != HTTPStatus.OK.value:
        logger.error(f"campaign_comm_export.error :: {campaign_comm_export.text}")
        return False

    #  0. create columns keys list

    #  1. export_comm keys none dict map with error source keys
    #  2. add error source keys to export comm ie. new_export_comm ### TODO list_1
    #  3. populate the export campaign_export data with 1 ### TODO list_2
    #  4. add list2 to list1

    campaign_comm_export = json.loads(campaign_comm_export.text)
    campaign_comm_export_output = campaign_comm_export.get("output", [])
    logger.info(f"campaign_comm_export_output :: {len(campaign_comm_export)}")
    if campaign_comm_export_output == []:
        campaign_comm_export_output = [ColumnMapChoices[channel].value.copy()]

    kwargs["export_comm"] = campaign_comm_export_output
    logger.info(f"campaign_comm_export.campaign_comm_export_output:{campaign_comm_export_output}")
    campaign_export.apply_async(queue=queue, kwargs=kwargs)
    return True


@shared_task(name="campaign_export", bind=True, ignore_result=False)
def campaign_export(self, *args, **kwargs):
    logger.info(f"app.tasks.report.campaign_export")
    logger.debug(f"campaign_export.kwargs {kwargs}")
    export_comm = kwargs["export_comm"]
    channel = kwargs["channel"]
    campaign_id = kwargs["campaign_id"]
    queue = kwargs["queue"]
    is_deleted = kwargs.get("is_deleted", False)
    company_id = kwargs["company_id"]
    url = f"{QUEUE_SERVICE_BASE_URL}/campaign_data"
    try:
        response_data = {
            "campaign_id": campaign_id,
            "channel": channel,
            "is_deleted": is_deleted,
            "profile_id": kwargs.get("profile_id")
            if kwargs.get("profile_id")
            else kwargs["user"].get("permission_group_id"),
            "masking": True,
        }
        campaign_export = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-CG-Company": json.dumps(kwargs["company"]),
                "X-Request-ID": kwargs["request_id"],
            },
        )
        logger.debug(f"campaign_export.status_code :: {campaign_export.status_code}")
    except Exception as e:
        logger.error(f"campaign_export.exception :: {str(e)}")
        return False

    if campaign_export.status_code != HTTPStatus.OK.value:
        logger.error(f"campaign_export.error :: {campaign_export.text}")
        return False
    #  0. columns keys list
    campaign_export = json.loads(campaign_export.text)
    campaign_export_output = campaign_export.get("output", None)
    campaign_output_data = campaign_export_output["campaign_data"]
    campaign_output_data = campaign_output_data[0]
    logger.debug(f"campaign_export.campaign_output_data: {campaign_output_data}")
    campaign_output_comm_data = json.loads(campaign_output_data["data"])
    if not isinstance(campaign_output_comm_data, dict):
        campaign_output_comm_data = json.loads(campaign_output_comm_data)
    comm_failed_count = campaign_export_output.get("comm_failed_count", 0)
    attempted_live = campaign_export_output.get("attempted_live", False)
    final_consolidated_comm_export_data = get_campaign_report_data(
        kwargs,
        communication_export_data=export_comm,
        campaign_data=campaign_export_output,
    )
    s3_kwargs = {}
    s3_kwargs["payload"] = kwargs
    s3_kwargs["final_consolidated_comm_export_data"] = final_consolidated_comm_export_data
    s3_kwargs["columns_key_mapping"] = list(final_consolidated_comm_export_data[0].keys())
    s3_kwargs["triggered_time"] = campaign_output_data.get("created")
    s3_kwargs["filters"] = campaign_output_comm_data.get("filters")
    s3_kwargs["range"] = campaign_output_comm_data.get("range")
    s3_kwargs["failed_count"] = comm_failed_count
    s3_kwargs["attempted_live"] = attempted_live
    campaign_s3_upload.apply_async(queue=queue, kwargs=s3_kwargs)
    return True


@shared_task(name="campaign_s3_upload", bind=True, ignore_result=False)
def campaign_s3_upload(self, *args, **kwargs):
    logger.info(f"app.tasks.report.campaign_s3_upload")
    warning = False
    payload = kwargs["payload"]
    author = payload["author"]
    channel = payload["channel"]
    queue = payload["queue"]
    campaign_id = payload["campaign_id"]
    status = payload["delivery_status"]
    campaign_name = payload["name"]
    template_name = payload["template_name"]
    column_names = kwargs["columns_key_mapping"]
    completion_report = payload.get("completion_report", False)
    company_id = payload.get("company_id")
    company_trademark = payload["company"].get("trademark")
    rule_name = payload.get("rule_name")
    data = kwargs["final_consolidated_comm_export_data"]
    queue_env = self.app.conf.QUEUE_NAME.lower()
    is_deleted = payload.get("is_deleted", False)
    dc_notification_channels = payload["company"].get("dc_notification_channel", [])
    try:
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        cell_format = workbook.add_format({"bold": True})

        worksheet.write_row(0, 0, column_names, cell_format)

        for row_idx, values in enumerate(data):
            worksheet.write_row(row_idx + 1, 0, list(values.values()))

        workbook.close()
        output.seek(0)

        bucket_credentials = {
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        }

        s3_link_uuid = str(uuid.uuid4().hex)
        file_name = f"campaigns-report/{s3_link_uuid}.xlsx"
        presigned_url = s3_upload_and_generate_presigned_url(
            bucket_credentials=bucket_credentials,
            bucket_name=EXPORTS_BUCKET_NAME,
            key=file_name,
            data_object=output,
        )
        logger.debug(f"campaign_s3_upload.presigned_url.{campaign_id} :: {presigned_url}")
        dynamic_template_data = {
            "channel": channel.replace("_", " ").capitalize(),
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "status": status,
            "template_name": template_name,
            "report_url": presigned_url,
            "env": queue_env if queue_env != PROD_ENV else None,
            "company": company_trademark,
            "triggered_time": kwargs.get("triggered_time"),
            "filters": kwargs.get("filters"),
            "range": kwargs.get("range"),
        }
        report_kwargs = {}
        if completion_report:
            report_kwargs["from_data"] = {
                "name": f"Bulk {channel.replace('_', ' ').capitalize()} Notification",
                "email": "reports@credgenics.com",
            }
            report_kwargs["delivery_progress_count"] = payload.get("delivery_progress_count")
            report_kwargs["delivery_status"] = payload.get("delivery_status")
            report_kwargs["total_loans"] = payload.get("total_loans")
            to_emails = author.split(",") if isinstance(author, str) else author
            dc_notification_email_ids = payload["company"].get("dc_notification_email_ids", [])
            valid_email_ids = []
            if dc_notification_email_ids:
                valid_email_ids = list(
                    filter(
                        lambda email: email not in to_emails and validate_email(email),
                        dc_notification_email_ids,
                    )
                )
                if valid_email_ids:
                    cc_emails = format_email_dict(valid_email_ids)
                    report_kwargs["cc_emails"] = cc_emails
                    logger.debug(f"cc_emails:- {cc_emails}")
            if BCC_EMAILS and isinstance(BCC_EMAILS, list):
                filtered_bcc_emails = list(
                    filter(lambda email: email not in to_emails and email not in valid_email_ids, BCC_EMAILS)
                )
                report_kwargs["bcc_emails"] = format_email_dict(filtered_bcc_emails)
                logger.debug(f"bcc_emails:- {report_kwargs['bcc_emails']}")
            dynamic_template_data[
                "campaign_link"
            ] = f"{UI_SERVICE_BASE_URL}/app/bulk-management?company_id={company_id}&bulk_id={campaign_id}"
            if rule_name:
                dynamic_template_data["rule_name"] = rule_name
                report_kwargs["sendgrid_template_id"] = str(AI_COMPLETION_REPORT_SENDGRID_ID)
            else:
                report_kwargs["sendgrid_template_id"] = str(COMPLETION_REPORT_SENDGRID_ID)
            try:
                export_comm_url = f"{COMMUNICATION_SERVICE_BASE_URL}/campaigns/count?company_id={company_id}&campaign_id={campaign_id}&channel={channel}&campaign_summary=True&is_deleted={is_deleted}"
                logger.debug(f"campaign_s3_upload.export_campaign_summary.url: {export_comm_url}")
                campaign_export = requests.request(
                    method="GET",
                    url=export_comm_url,
                    headers={
                        "Content-Type": "application/json",
                        "X-CG-User": json.dumps(payload["user"]),
                        "X-Request-ID": payload["request_id"],
                        "X-CG-Company": json.dumps(payload["company"]),
                    },
                )
                logger.debug(f"campaign_s3_upload.export_campaign_summary.status_code: {campaign_export.status_code}")

                if campaign_export.status_code != HTTPStatus.OK.value:
                    logger.error(f"campaign_summary.export_campaign_summary.error {campaign_export.text}")
                    return False
            except Exception as e:
                logger.error(f"campaign_summary.export_campaign_summary.exception: {str(e)}")
                return False
            campaign_export = json.loads(campaign_export.text)
            campaign_export_output = campaign_export.get("output", [])
            if not campaign_export_output:
                campaign_export_output = {}
            else:
                campaign_export_output = campaign_export_output[0]
            campaign_summary = get_campaign_summary(
                campaign_export_output,
                channel,
                failed_count=kwargs["failed_count"],
                attempted_live=kwargs["attempted_live"],
                completion_summary=True,
            )
            if campaign_summary and isinstance(campaign_summary, dict):
                camapign_summary_keys = []
                camapign_summary_values = campaign_summary.values()
                max_value = max(camapign_summary_values)
                camapign_summary_final_values = []
                camapign_summary_final_values_map = {}
                for key, value in campaign_summary.items():
                    camapign_summary_keys.append(key.capitalize())
                    if max_value == 0:
                        value_percentage = 0
                    else:
                        value_percentage = round((value / max_value) * 100)
                    if str(key).lower() == "delivered" and value_percentage < 50:
                        warning = True
                    camapign_summary_final_values.append(f"{value_percentage}% ({value})")
                    camapign_summary_final_values_map[key] = f"{value_percentage}% ({value})"
                dynamic_template_data["warning"] = warning
                if warning:
                    dynamic_template_data[
                        "subject"
                    ] = f"[Warning] Bulk {channel.replace('_', ' ').capitalize()} Request Completed : Delivery rate is less than 50%"
                else:
                    dynamic_template_data[
                        "subject"
                    ] = f"Bulk {channel.replace('_', ' ').capitalize()} Request Completed"
                dynamic_template_data["camapign_summary_keys"] = camapign_summary_keys
                dynamic_template_data["camapign_summary_values"] = camapign_summary_final_values
            if (
                payload["number"]
                and dc_notification_channels
                and (RequestTypeChoices.sms.value in dc_notification_channels)
            ):
                sms_report_kwargs = {}
                sms_report_kwargs["company_id"] = company_id
                sms_report_kwargs["campaign_name"] = campaign_name
                sms_report_kwargs["campaign_id"] = campaign_id
                sms_report_kwargs["campaign_summary"] = camapign_summary_final_values_map
                sms_report_kwargs["numbers"] = payload["number"]
                sms_report_kwargs["user"] = payload["user"]
                sms_report_kwargs["request_id"] = payload["request_id"]
                sms_report_kwargs["company"] = payload["company"]
                sms_report_kwargs["channel"] = channel.capitalize()
                sms_report_kwargs["delivery_progress_count"] = payload.get("delivery_progress_count")
                sms_report_kwargs["delivery_status"] = payload.get("delivery_status")
                sms_report_kwargs["total_loans"] = payload.get("total_loans")
                sms_report_kwargs["trigger_stop_count"] = payload.get("trigger_stop_count")
                send_sms_report.apply_async(queue=queue, kwargs=sms_report_kwargs)
        else:
            report_kwargs["sendgrid_template_id"] = str(REPORT_SENDGRID_TEMPLATE_ID)
            report_kwargs["from_data"] = {
                "name": f"Bulk {channel.replace('_', ' ').capitalize()} Report",
                "email": "reports@credgenics.com",
            }

        report_kwargs["dynamic_template_data"] = dynamic_template_data
        report_kwargs["to_email"] = author
        report_kwargs["campaign_id"] = campaign_id
        report_kwargs["completion_report"] = completion_report
        report_kwargs["user"] = payload["user"]
        report_kwargs["request_id"] = payload["request_id"]
        report_kwargs["trigger_stop_count"] = payload.get("trigger_stop_count")

        logger.debug(f"campaign_s3_upload.report_kwargs.{campaign_id} :: {report_kwargs}")
        if not completion_report:
            send_report.apply_async(queue=queue, kwargs=report_kwargs)
        elif (
            completion_report
            and dc_notification_channels
            and RequestTypeChoices.email.value in dc_notification_channels
        ):
            send_report.apply_async(queue=queue, kwargs=report_kwargs)
    except Exception as e:
        logger.error(f"campaign_s3_upload.exception.{campaign_id} :: {str(e)}")
        return False
    return True


@shared_task(name="save_report_url", bind=True, ignore_result=False)
def save_report_url(self, *args, **kwargs):
    pass


def s3_upload_and_generate_presigned_url(bucket_credentials, bucket_name, key, data_object):
    logger.info(f"app.tasks.report.s3_upload_and_generate_presigned_url")
    logger.info(
        "s3_upload_and_generate_presigned_url.bucket_name: %s, s3_upload_and_generate_presigned_url.key: %s",
        bucket_name,
        key,
    )

    aws_access_key_id = bucket_credentials.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = bucket_credentials.get("AWS_SECRET_ACCESS_KEY", "")

    try:
        s3_client_v4 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name="ap-south-1",
            config=s3_v4_config,
            endpoint_url="https://s3."+AWS_DEFAULT_REGION+".amazonaws.com",
        )
        s3_client_v4.put_object(Bucket=bucket_name, Body=data_object, Key=key)

        presigned_url = s3_client_v4.generate_presigned_url(
            "get_object", Params={"Bucket": bucket_name, "Key": key}, ExpiresIn=86400
        )
    except ClientError as error:
        raise error

    return presigned_url


@shared_task(name="campaign_update", bind=True, ignore_result=False)
def campaign_update(self, *args, **kwargs):
    logger.info(f"app.tasks.report.campaign_update")
    company_id = kwargs["company_id"]
    campaign_data = kwargs["campaign_data"]
    campaign_export_output_map = kwargs["campaign_export_output_map"]
    update_list = []
    queue = kwargs["queue"]
    dc_notification_channels = kwargs["company"].get("dc_notification_channel", [])
    try:
        for data in campaign_data:
            campaign_id = data["campaign_id"]
            logger.debug(f"campaign_update.campaign_id: {campaign_id}")
            name = data["name"]
            channel = data["channel"]
            created = datetime.datetime.strptime(data["created"], "%Y-%m-%dT%H:%M:%S.%f")
            latest_triggered_time = data["latest_triggered_time"]
            author_id = data.get("author_id")
            campaign_author = data.get("author")
            old_trigger_status = data.get("trigger_status")
            old_trigger_progress_count = data.get("trigger_progress_count")
            old_delivery_status = data.get("delivery_status")
            old_delivery_progress_count = data.get("delivery_progress_count")
            old_trigger_stop_count = data.get("trigger_stop_count", 0)
            old_delivery_count = old_delivery_progress_count.split("/")[0]
            email_report_sent = data.get("email_report_sent")
            sms_report_sent = data.get("sms_report_sent")
            total_loans = int(data["total_loans"])
            table = f"campaign_{channel}"
            comm_data = json.loads(data["comm_data"])
            queue_processed = 0
            queue_fails = 0
            campaign_stopped_count = 0

            if channel != RequestTypeChoices.dtmf_ivr.value:
                if not isinstance(comm_data, dict):
                    comm_data = json.loads(comm_data)
                if comm_data.get("template_name"):
                    template_name = comm_data["template_name"]
                elif comm_data.get("comm_dict", {}).get("template_name"):
                    template_name = comm_data["comm_dict"]["template_name"]
                else:
                    template_name = ""
            else:
                template_name = comm_data.get("template_name", "")
            url = f"{QUEUE_SERVICE_BASE_URL}/campaign/count"
            payload = {"table": table, "campaign_id": campaign_id}
            logger.debug(f"campaign_update.get_campaign_count.url: {url}")
            campaign_res = requests.request(
                method="POST",
                url=url,
                data=json.dumps(payload),
                headers={
                    "Content-Type": "application/json",
                    "X-CG-User": json.dumps(kwargs["user"]),
                    "X-Request-ID": kwargs["request_id"],
                },
            )
            logger.debug(f"campaign_update.get_campaign_count.status_code :: {campaign_res.status_code}")
            logger.debug(f"campaign_update.get_campaign_count.response :: {campaign_res.text}")
            res_text = json.loads(campaign_res.text)
            if campaign_res.status_code == HTTPStatus.OK.value:
                campaign_count = res_text.get("output", [])
                if not (isinstance(campaign_count, list)):
                    continue
            else:
                continue

            logger.debug(f"campaign_update.campaigns_count_result: {campaign_count}")
            for campaigns_data_item in campaign_count:
                queue_processed += campaigns_data_item.get("count", 0)
                queue_fails += campaigns_data_item.get("count", 0) if campaigns_data_item.get("status") == "FAIL" else 0
                campaign_stopped_count += (
                    campaigns_data_item.get("count", 0)
                    if campaigns_data_item.get("error_code") == CAMPAIGN_STOPPED_ERROR_CODE
                    else 0
                )
            trigger_stop_count = queue_processed - campaign_stopped_count
            trigger_progress_count = f"{queue_processed}/{total_loans}"
            trigger_percentage = (queue_processed / total_loans) * 100
            if queue_processed != total_loans:
                if THRESHOLD_PERCENTAGE <= trigger_percentage < COMPLETION_PERCENTAGE:
                    trigger_status = CampaignTriggerTypeChoices.partial_completed.value
                elif trigger_percentage >= COMPLETION_PERCENTAGE:
                    trigger_status = CampaignTriggerTypeChoices.completed.value
                elif datetime.datetime.now() - created > datetime.timedelta(hours=24):
                    trigger_status = CampaignTriggerTypeChoices.hold.value
                else:
                    trigger_status = CampaignTriggerTypeChoices.in_process.value
            else:
                trigger_status = CampaignTriggerTypeChoices.completed.value
            campaign_export_output_data = campaign_export_output_map.get(campaign_id, None)
            webhook_success_comm = 0
            if campaign_export_output_data is not None:
                webhook_success_comm = campaign_export_output_data.get("webhook_success_count", 0)
            total_process_success_count = queue_fails + webhook_success_comm
            delivery_progress_count = f"{total_process_success_count}/{total_loans}"
            delivery_percentage = (total_process_success_count / total_loans) * 100
            if total_process_success_count != total_loans:
                if THRESHOLD_PERCENTAGE <= delivery_percentage < COMPLETION_PERCENTAGE:
                    delivery_status = CampaignDeliveryTypeChoices.partial_completed.value
                elif delivery_percentage >= COMPLETION_PERCENTAGE:
                    delivery_status = CampaignDeliveryTypeChoices.completed.value
                elif datetime.datetime.now() - created > datetime.timedelta(hours=48):
                    delivery_status = CampaignDeliveryTypeChoices.hold.value
                else:
                    delivery_status = CampaignDeliveryTypeChoices.updating.value
            else:
                delivery_status = CampaignDeliveryTypeChoices.completed.value
            if (
                old_trigger_status != CampaignTriggerTypeChoices.completed.value
                and trigger_progress_count != old_trigger_progress_count
            ):
                latest_triggered_time = datetime.datetime.now()
            if (
                delivery_status
                in (
                    CampaignDeliveryTypeChoices.completed.value,
                    CampaignDeliveryTypeChoices.partial_completed.value,
                )
                and not (email_report_sent or sms_report_sent)
                and dc_notification_channels
                and (
                    (RequestTypeChoices.sms.value in dc_notification_channels and not sms_report_sent)
                    or (RequestTypeChoices.email.value in dc_notification_channels and not email_report_sent)
                )
            ):
                author = None
                number = None
                rule_name = comm_data.get("rule_name", "")
                rule_id = comm_data.get("rule_id", "")
                if rule_name:
                    author_id = comm_data.get("ai_author_ids", "")
                logger.info(f"campaign_update.author_ids {author_id}")
                if author_id:
                    user_details = get_users_details(
                        company_id,
                        author_id,
                        kwargs["user"],
                        kwargs["request_id"],
                        kwargs["company"],
                    )
                    author = user_details.get("user_emails")
                    number = user_details.get("user_numbers")
                    profile_id = user_details.get("author_profile_id")
                if not author:
                    if rule_name:
                        author = AI_RULE_EMAIL
                    else:
                        author = campaign_author
                report_data = {
                    "campaign_id": campaign_id,
                    "channel": channel,
                    "author": author,
                    "number": number,
                    "company_id": company_id,
                    "name": name,
                    "delivery_status": delivery_status,
                    "delivery_progress_count": delivery_progress_count,
                    "total_loans": total_loans,
                    "template_name": template_name,
                    "user": kwargs["user"],
                    "request_id": kwargs["request_id"],
                    "completion_report": True,
                    "queue": queue,
                    "company": kwargs["company"],
                    "rule_name": rule_name,
                    "rule_id": rule_id,
                    "trigger_stop_count": trigger_stop_count,
                    "profile_id": profile_id,
                }
                campaign_comm_export.apply_async(queue=queue, kwargs=report_data)
            elif (
                trigger_status != old_trigger_status
                or trigger_progress_count != old_trigger_progress_count
                or delivery_status != old_delivery_status
                or delivery_progress_count != old_delivery_progress_count
                or trigger_stop_count != old_trigger_stop_count
            ) and total_process_success_count >= int(old_delivery_count):
                if latest_triggered_time:
                    update_value = f"""('{campaign_id}', '{trigger_status}', '{trigger_progress_count}', '{delivery_status}', '{delivery_progress_count}', {trigger_stop_count}, '{latest_triggered_time}'::timestamp)"""
                else:
                    update_value = f"""('{campaign_id}', '{trigger_status}', '{trigger_progress_count}', '{delivery_status}', '{delivery_progress_count}', {trigger_stop_count}, null::timestamp)"""
                update_list.append(update_value)
        if update_list:
            payload = {
                "table": "campaigns",
                "set_clause": {
                    "trigger_status": "trigger_status",
                    "trigger_progress_count": "trigger_progress_count",
                    "delivery_status": "delivery_status",
                    "delivery_progress_count": "delivery_progress_count",
                    "trigger_stop_count": "trigger_stop_count",
                    "latest_triggered_time": "latest_triggered_time",
                },
                "from_values": update_list,
                "from_columns": [
                    "campaign_id",
                    "trigger_status",
                    "trigger_progress_count",
                    "delivery_status",
                    "delivery_progress_count",
                    "trigger_stop_count",
                    "latest_triggered_time",
                ],
                "from_alias_name": "cd",
                "where": {"campaign_id": "campaign_id"},
            }
            update_data_kwargs = {
                "payload": payload,
                "user": kwargs["user"],
                "request_id": kwargs["request_id"],
            }
            update_data.apply_async(queue=queue, kwargs=update_data_kwargs)
    except Exception as e:
        logger.error(f"campaign_update.exception {str(e)}")
        return False
    return True


@shared_task(name="update_data", bind=True, ignore_result=False)
def update_data(self, *args, **kwargs):
    """
    Update the records of a table
    """
    logger.info(f"app.tasks.report.update_data")
    payload = kwargs["payload"]
    logger.debug(f"app.tasks.report.update_data.payload: {payload}")
    try:
        url = f"{QUEUE_SERVICE_BASE_URL}/update/data"
        logger.debug(f"update_data.url: {url}")
        update_res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-Request-ID": kwargs["request_id"],
            },
        )
        logger.debug(f"update_data.status_code :: {update_res.status_code}")
        if update_res.status_code != HTTPStatus.OK.value:
            logger.debug(f"update_data.error :: {update_res.text}")
            return False
    except Exception as e:
        logger.error(f"update_data.exception :: {str(e)}")
        return False
    return True


@shared_task(name="campaign_result", bind=True, ignore_result=False)
def campaign_result(self, *args, **kwargs):
    """
    Aggregates the campaign data from database
    """
    logger.info(f"app.tasks.report.campaign_result")
    payload = kwargs["payload"]
    logger.info(f"campaign_result.campaign_id {payload['campaign_id']}")
    company_details = payload["company"]
    request_id = payload["request_id"]
    user = payload["user"]
    failed_data = []
    success_data = []
    updated_end_time_flag = kwargs["updated_end_time_flag"]
    queue_env = self.app.conf.QUEUE_NAME.lower()
    try:
        url = f"{QUEUE_SERVICE_BASE_URL}/campaign_data"
        data = requests.request(
            method="POST",
            url=url,
            data=json.dumps(
                {
                    "campaign_id": payload["campaign_id"],
                    "channel": payload["channel"],
                    "updated_end_time_flag": updated_end_time_flag,
                    "trigger_report_flag": True,
                }
            ),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(user),
                "X-Request-ID": request_id,
                "X-CG-Company": json.dumps(company_details),
            },
        )
        logger.debug(f"campaign_result.campaign_data.status_code :: {data.status_code}")
    except Exception as e:
        logger.error(f"campaign_result.campaign_data.exception :: {str(e)}")
        return False

    if data.status_code != HTTPStatus.OK.value:
        logger.error(f"campaign_result.campaign_data.error :: {data.text}")
        return False

    try:
        data = json.loads(data.text)
        output = data["output"]
        if (not output["channel_campaign_data"]) or (not output["campaign_data"]):
            return False
        campaign_data = output["campaign_data"][0]
        channel_campaign_data = output["channel_campaign_data"]
        trigger_stop_count = 0
        for data in channel_campaign_data:
            response = data["response"]
            status_code = data["status_code"]
            error_code = data["error_code"]
            loan_id = data["loan_id"]
            if data["status"] == "FAIL":
                failed_data.append((loan_id, response, status_code))
            if data["status"] == "SUCCESS":
                success_data.append((loan_id, response, status_code))
            if error_code != CAMPAIGN_STOPPED_ERROR_CODE:
                trigger_stop_count += 1

        dynamic_template_data = create_dynamic_template(
            payload=payload,
            failed=len(failed_data),
            created=campaign_data["created"],
            success=len(success_data),
            queue_env=queue_env,
            campaign_name=campaign_data["name"],
        )
        logger.debug(f"dynamic_template_data: {dynamic_template_data}")
        if isinstance(dynamic_template_data, dict):
            kwargs["dynamic_template_data"] = dynamic_template_data
            kwargs["to_email"] = payload["author"]
            kwargs["failed_data"] = failed_data
            kwargs["trigger_stop_count"] = trigger_stop_count
            kwargs["from_data"] = {
                "name": f"Bulk {payload['channel'].replace('_', ' ').capitalize()} Notification",
                "email": "reports@credgenics.com",
            }
            kwargs["sendgrid_template_id"] = str(CAMPAIGN_SENDGRID_TEMPLATE_ID)
            kwargs["role"] = payload["role"]
            rule_name = dynamic_template_data.get("rule_name")
            author = None
            if rule_name:
                author_id = dynamic_template_data.pop("ai_author_ids", None)
                if author_id:
                    user_details = get_users_details(
                        company_details.get("company_id"), author_id, user, request_id, company_details
                    )
                    author = user_details.get("user_emails")

            if not author:
                if rule_name:
                    author = AI_RULE_EMAIL
                else:
                    author = kwargs["to_email"]
            to_emails = author.split(",") if isinstance(author, str) else author
            kwargs["to_email"] = to_emails
            dc_notification_email_ids = payload["company"].get("dc_notification_email_ids", [])
            valid_email_ids = []
            if dc_notification_email_ids:
                valid_email_ids = list(
                    filter(
                        lambda email: email not in to_emails and validate_email(email),
                        dc_notification_email_ids,
                    )
                )
                if valid_email_ids:
                    kwargs["cc_emails"] = format_email_dict(valid_email_ids)
                    logger.debug(f"cc_emails:- {kwargs['cc_emails']}")
            if BCC_EMAILS and isinstance(BCC_EMAILS, list):
                filtered_bcc_emails = list(
                    filter(lambda email: email not in to_emails and email not in valid_email_ids, BCC_EMAILS)
                )
                kwargs["bcc_emails"] = format_email_dict(filtered_bcc_emails)
                logger.debug(f"bcc_emails:- {kwargs['bcc_emails']}")
            report_data.apply_async(
                queue=f"{self.app.conf.QUEUE_NAME}_{QueueTypeChoices.result.value}",
                kwargs=kwargs,
            )
    except Exception as e:
        logger.error(f"campaign_result.exception :: {str(e)}")
        return False
    logger.info("campaign_result.close")
    return True


@shared_task(name="batch_result", bind=True, ignore_result=False)
def batch_result(self, *args, **kwargs):
    """
    Aggregates the campaign data from database
    """
    logger.info(f"app.tasks.report.batch_result")
    payload = kwargs["payload"]
    failed_data = []
    success_data = []
    logger.info(f"batch_result.batch_id: {payload['batch_id']}")
    queue_env = self.app.conf.QUEUE_NAME.lower()

    try:
        url = f"{QUEUE_SERVICE_BASE_URL}/batch_data"
        data = requests.request(
            method="POST",
            url=url,
            data=json.dumps(
                {
                    "batch_id": payload["batch_id"],
                    "channel": payload["channel"],
                    "type": payload["type"],
                }
            ),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"batch_result.batch_data.status_code :: {data.status_code}")
    except Exception as e:
        logger.error(f"batch_result.batch_data.exception :: {str(e)}")
        return False

    if data.status_code != HTTPStatus.OK.value:
        logger.error(f"batch_result.batch_data.error :: {data.text}")
        return False

    try:
        data = json.loads(data.text)
        output = data["output"]
        if not output["batch_data"]:
            return False
        batch_data = output["batch_data"][0]
        type = batch_data.get("type", "")
        channel = batch_data.get("channel", "")
        batch_loans_data = output["batch_loans_data"]
        if type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_upload.value:
            for data in batch_loans_data:
                response = data["response"]
                status_code = data["status_code"]
                loan_id = data["loan_id"]
                tracking_number = data.get("tracking_number", "")
                failed_data.append((loan_id, tracking_number, response, status_code))
        elif type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_tracking.value:
            for data in batch_loans_data:
                response = data["response"]
                status_code = data["status_code"]
                loan_id = data["loan_id"]
                company_id = data.get("company_id", "")
                tracking_number = data.get("tracking_number", "")
                failed_data.append((loan_id, company_id, tracking_number, response, status_code))
        elif type == TypeOfTaskChoices.notice.value:
            for data in batch_loans_data:
                status = data["status"]
                response = data["response"]
                status_code = data["status_code"]
                loan_id = data["loan_id"] if type != TypeOfTaskChoices.notice.value else "'" + str(data["loan_id"])
                if status == "SUCCESS":
                    success_data.append((loan_id, response, status_code))
                else:
                    failed_data.append((loan_id, response, status_code))

            payload["success_data"] = success_data
        else:
            for data in batch_loans_data:
                response = data["response"]
                status_code = data["status_code"]
                loan_id = data["loan_id"] if type != TypeOfTaskChoices.notice.value else "'" + str(data["loan_id"])
                failed_data.append((loan_id, response, status_code))

        dynamic_template_data = create_batch_dynamic_template(
            payload=payload,
            failed=len(failed_data),
            created=batch_data["created"],
            queue_env=queue_env,
        )
        type_of_task = ""
        if type == TypeOfTaskChoices.notice.value:
            type_of_task = f"{channel}_{type}"
        elif type == TypeOfTaskChoices.scrape.value:
            type_of_task = f"{channel}"
        else:
            type_of_task = f"{type}"
        kwargs["type_of_task"] = type_of_task
        type_of_task = type_of_task.replace("_", " ")
        if isinstance(dynamic_template_data, dict):
            kwargs["dynamic_template_data"] = dynamic_template_data
            kwargs["to_email"] = payload["author"]
            kwargs["failed_data"] = failed_data
            kwargs["from_data"] = {
                "name": f"{type_of_task.capitalize()} Report",
                "email": "reports@credgenics.com",
            }
            kwargs["sendgrid_template_id"] = str(BATCH_SENDGRID_TEMPLATE_ID)

            report_data.apply_async(
                queue=f"{self.app.conf.QUEUE_NAME}_{QueueTypeChoices.result.value}",
                kwargs=kwargs,
            )
    except Exception as e:
        logger.error(f"batch_result.exception :: {str(e)}")
        return False
    return True


@shared_task(bind=True, name="send_sms_report")
def send_sms_report(self, *args, **kwargs):
    logger.info("app.tasks.report.send_sms_report")
    logger.debug(f"send_sms_report.kwargs: {kwargs}")
    company_id = kwargs.get("company_id")
    campaign_name = kwargs.get("campaign_name")
    channel = kwargs.get("channel")
    campaign_id = kwargs.get("campaign_id")
    campaign_summary = kwargs.get("campaign_summary")
    triggered = campaign_summary.get("triggered", 0)
    delivered = campaign_summary.get("delivered", 0)
    sms_mobile_data = kwargs.get("numbers")
    delivery_progress_count = kwargs.get("delivery_progress_count")
    delivery_status = kwargs.get("delivery_status")
    total_loans = kwargs.get("total_loans")
    company_details = kwargs["company"]
    trigger_progress_count = f"{total_loans}/{total_loans}"
    trigger_status = CampaignTriggerTypeChoices.completed.value
    trigger_stop_count = kwargs.get("trigger_stop_count")

    country_isd_code = None
    trademark = None
    try:
        trademark = company_details.get("trademark", "").capitalize()
        sms_body = (
            f"{trademark} bulk {channel.lower()} request {campaign_name} completed on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Triggered: {triggered}, Delivered: {delivered}\n- Credgenics",
        )
        for country_code, value in sms_mobile_data.items():
            if not len(value):
                logger.error(f"send_sms_report.exception :: No mobile number found")
                continue
            country_mapping_data = COUNTRY_WISE_MAPPING.get(str(country_code.split("+")[-1]))
            if country_mapping_data:
                if country_mapping_data["dlt_check_applicable"]:
                    data = {
                        "sms_mobile": ",".join(value),
                        "sms_body": str(sms_body),
                        "company_id": company_id,
                        "content_template_id": REQUEST_COMPLETION_SMS_TEMP_ID,
                        "principal_entity_id": PRINCIPAL_ENTITY_ID,
                        "country_isd_code": str(country_code.split("+")[-1]),
                    }
                else:
                    data = {
                        "sms_mobile": ",".join(value),
                        "sms_body": str(sms_body),
                        "company_id": company_id,
                        "country_isd_code": str(country_code.split("+")[-1]),
                    }
            data["module"] = MODULE
            data["source"] = SOURCE
            response_text, response_status_code = trigger_sms_communication(data)
            logger.debug(f"trigger_sms_communication.response.status_code ::{response_status_code}")
            if response_status_code != HTTPStatus.OK.value:
                logger.error(f"trigger_sms_communication.response.status_code ::{response_text}")
                continue

        update_payload = {
            "table": "campaigns",
            "set_clause": {
                "sms_report_sent": "sms_report_sent",
                "delivery_status": "delivery_status",
                "delivery_progress_count": "delivery_progress_count",
                "trigger_status": "trigger_status",
                "trigger_progress_count": "trigger_progress_count",
                "trigger_stop_count": "trigger_stop_count",
            },
            "from_values": [
                f"('{campaign_id}', true, '{delivery_status}', '{delivery_progress_count}', '{trigger_status}', '{trigger_progress_count}', {trigger_stop_count})"
            ],
            "from_columns": [
                "campaign_id",
                "sms_report_sent",
                "delivery_status",
                "delivery_progress_count",
                "trigger_status",
                "trigger_progress_count",
                "trigger_stop_count",
            ],
            "from_alias_name": "cd",
            "where": {"campaign_id": "campaign_id"},
        }
        update_data_kwargs = {
            "payload": update_payload,
            "user": kwargs["user"],
            "request_id": kwargs["request_id"],
        }
        update_data.apply_async(
            queue=f"{self.app.conf.QUEUE_NAME}_{QueueTypeChoices.campaign_update.value}",
            kwargs=update_data_kwargs,
        )
        return True
    except Exception as e:
        logger.error(f"send_sms_report.exception :: {str(e)}")
        return False
