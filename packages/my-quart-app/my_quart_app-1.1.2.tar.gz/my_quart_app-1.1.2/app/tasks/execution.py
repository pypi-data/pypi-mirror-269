"""
execution.py
Usage: All execution tasks
"""
from celery import chord, group
import redis
import json
import os
import shutil
import requests
import logging
import xlsxwriter
import time
import copy
import traceback

import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

from app.tasks.helpers import ChunkClass, LitigationReportRedisKeys, get_required_headers_per_level
from ..services.user_service import get_users

# TODO import this from celery_app
from ..settings import (
    AWS_ACCESS_KEY_ID,
    AWS_DEFAULT_REGION,
    AWS_SECRET_ACCESS_KEY,
    AWS_DEFAULT_REGION,
    COMMUNICATION_SERVICE_BASE_URL,
    QUEUE_SERVICE_BASE_URL,
    LITIGATION_SERVICE_BASE_URL,
    VOLUME_MOUNT_DIRECTORY,
    RECOVERY_SERVICE_BASE_URL,
    SCRAPE_SERVICE_BASE_URL,
    HEROUSER,
    HEROPASS,
    HEROFINCORP_URL,
    S3_BUCKET_NAME,
    S3_LITIGATION_REPORTS_DIRECTORY,
    S3_LITIGATION_ORDERS_DIRECTORY,
    DOMAIN_NAME,
    LITIGATION_REPORT_BATCH_SIZE,
    S3_CLOUDFRONT_BUCKET_ENDPOINT,
    UI_SERVICE_BASE_URL,
    REDIS,
    LITIGATION_REPORT_DIRECTORY,
)


from celery import shared_task
from ..choices import (
    RequestTypeChoices,
    HERO_DATA,
    AllocationApprovalStatuses,
    COMMA,
    DELIMITER,
    PICKLE_EXTENSTION,
    MAX_LIMIT_OF_ITERATION_REMINDERS,
    LITIGATION_REPORT_DELIMITER,
    ReportStatus,
)
from ..utils import encode_param, format_api_response_text
from ..service import post, save_dtmf_response

import logging
from http import HTTPStatus

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# cred = credentials.Certificate("./notificationstesting-firebase.json")
# firebase_admin.initialize_app(cred)
# firebase_db = firestore.client()
# logger.info(f"credentials.firebase_admin")


@shared_task(bind=True, name="send_communications")
def send_communications(self, *args, **kwargs):
    comm_type = kwargs["comm_type"]
    payload = kwargs["payload"]
    loan_id = kwargs["loan_id"]

    def post(post_data, request_type, loan_id):
        url = None
        remark_endpoint = "create_remark"
        company_id = post_data["company_id"]
        comm_type = post_data["type_of_comm"]
        if comm_type == "whatsapp_bot":
            comm_endpoint = "/whatsapp_bot"
        elif comm_type == "dtmf_ivr":
            comm_endpoint = "/ivr/create"
        else:
            comm_endpoint = "/create"
        comm_dict = post_data["comm_dict"]

        if request_type in (
            RequestTypeChoices.email.value,
            RequestTypeChoices.sms.value,
            RequestTypeChoices.voice.value,
            RequestTypeChoices.whatsapp.value,
            RequestTypeChoices.whatsapp_bot.value,
            RequestTypeChoices.dtmf_ivr.value,
        ):
            url = f"{COMMUNICATION_SERVICE_BASE_URL}{comm_endpoint}"
            post_data["loan_id"] = loan_id
            post_data["company_id"] = company_id
        if request_type == RequestTypeChoices.remark.value and comm_type is not None:
            allocation_month = post_data.get("allocation_month", None)
            if allocation_month in (""):
                allocation_month = None
            template_name = comm_dict.get("template_name", None)
            url = f"{RECOVERY_SERVICE_BASE_URL}/{remark_endpoint}/{encode_param(loan_id)}?company_id={company_id}&allocation_month={allocation_month}"
            if comm_type == RequestTypeChoices.email.value:
                post_data = {
                    "remarks": "(" + template_name + " ) Email Sent",
                    "source": "queue_email",
                }
            if comm_type == RequestTypeChoices.sms.value:
                post_data = {
                    "remarks": "(" + template_name + " ) SMS Sent",
                    "source": "queue_sms",
                }
            if comm_type == RequestTypeChoices.voice.value:
                post_data = {
                    "remarks": "(" + template_name + " ) Voice Message Sent",
                    "source": "queue_voice",
                }
            if comm_type == RequestTypeChoices.whatsapp.value:
                post_data = {
                    "remarks": "(" + template_name + " ) Whatsapp Message Sent",
                    "source": "queue_whatsapp",
                }
            if comm_type == RequestTypeChoices.dtmf_ivr.value:
                template_name = post_data.get("template_name")
                post_data = {
                    "remarks": "(" + template_name + " ) DTMF IVR Sent",
                    "source": "queue_dtmf_ivr",
                }
        try:
            logger.info(f"communication - {comm_type} url - {url} post_data - {json.dumps(post_data)}")
            res = requests.request(
                method="POST",
                url=url,
                data=json.dumps(post_data),
                headers={
                    "Content-Type": "application/json",
                    "X-CG-User": json.dumps(kwargs["user"]),
                    "X-Request-ID": kwargs["request_id"],
                },
            )
            logger.info(f"tasks.send_communications: {res.text}")
            logger.info(f"execution.send_communications: {res.text}")
            if res.status_code in (200, 201):
                res_text = json.loads(res.text)
                data = res_text.get("data", {})
                if len(data.get("failed_communication", [])) > 0:
                    status = "FAIL"
                    res_text = str(data)
                else:
                    status = "SUCCESS"
                    res_text = str(res.text)
            elif res.status_code in (504, 408, 502):
                logger.info(f"queue-service.execution.send_communications, Error message: Internal server error")
                res_text = str({"message": "Internal server error"})
                status = "FAIL"
            else:
                res_text = res.text
                status = "FAIL"
            response = {
                "response": res_text,
                "status_code": res.status_code,
                "kwargs": kwargs,
                "status": status,
            }
        except Exception as e:
            logger.info(
                f"queue-service.execution.send_communications, Error message: Internal server error, Exception: {str(e)}"
            )
            response = {
                "response": str({"message": "Internal server error"}),
                "status_code": 500,
                "kwargs": kwargs,
                "status": "FAIL",
            }

        return response

    if comm_type == RequestTypeChoices.email.value:
        response = post(
            request_type=RequestTypeChoices.email.value,
            post_data=payload,
            loan_id=loan_id,
        )
        if response["status_code"] in (201, 200):
            post(
                request_type=RequestTypeChoices.remark.value,
                post_data=payload,
                loan_id=loan_id,
            )
    if comm_type == RequestTypeChoices.sms.value:
        response = post(
            request_type=RequestTypeChoices.sms.value,
            post_data=payload,
            loan_id=loan_id,
        )
        if response["status_code"] in (201, 200):
            post(
                request_type=RequestTypeChoices.remark.value,
                post_data=payload,
                loan_id=loan_id,
            )
    if comm_type == RequestTypeChoices.voice.value:
        response = post(
            request_type=RequestTypeChoices.voice.value,
            post_data=payload,
            loan_id=loan_id,
        )
        if response["status_code"] in (201, 200):
            post(
                request_type=RequestTypeChoices.remark.value,
                post_data=payload,
                loan_id=loan_id,
            )
    if comm_type == RequestTypeChoices.whatsapp.value:
        response = post(
            request_type=RequestTypeChoices.whatsapp.value,
            post_data=payload,
            loan_id=loan_id,
        )
        if response["status_code"] in (201, 200):
            post(
                request_type=RequestTypeChoices.remark.value,
                post_data=payload,
                loan_id=loan_id,
            )
    if comm_type == RequestTypeChoices.dtmf_ivr.value:
        response = post(
            request_type=RequestTypeChoices.dtmf_ivr.value,
            post_data=payload,
            loan_id=loan_id,
        )
        if response["status_code"] in (201, 200):
            post(
                request_type=RequestTypeChoices.remark.value,
                post_data=payload,
                loan_id=loan_id,
            )
    if comm_type == RequestTypeChoices.whatsapp_bot.value:
        response = post(
            request_type=RequestTypeChoices.whatsapp_bot.value,
            post_data=payload,
            loan_id=loan_id,
        )
        # if response['status_code'] in (201, 200):
        #     post(
        #         request_type=RequestTypeChoices.remark.value,
        #         post_data=payload, loan_id=loan_id
        #     )

    url = f"{QUEUE_SERVICE_BASE_URL}/execution_response"
    # print(response)
    try:
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-Request-ID": kwargs["request_id"],
            },
        )
        logger.info(f"send_communications.execution_response_update.status_code :: {res.status_code}")
    except Exception as e:
        logger.info(f"send_communications.execution_response_update.exception :: {str(e)}")
        self.retry(kwargs=kwargs, countdown=240, max_retries=2)

    if res.status_code not in (200, 201):
        logger.info(f"send_communications.execution_response_update.text :: {res.text}")
        self.retry(kwargs=kwargs, countdown=240, max_retries=2)
    return True


@shared_task(bind=True, name="optin", ignore_result=False)
def optin(self, *args, **kwargs):

    loan_id = kwargs["loan_id"]
    url = f"{COMMUNICATION_SERVICE_BASE_URL}/whatsapp/optin"
    try:
        request_payload = {"loan_id": loan_id, "company_id": kwargs["company_id"]}

        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(request_payload),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-Request-ID": kwargs["request_id"],
            },
        )
        logger.info(f"execution.optin: {res.text}")

        if res.status_code in (200, 201):
            res_text = json.loads(res.text)
            if res_text.get("output", "") != "success":
                status = "FAIL"
                res_text = f"{res_text.get('message', '')} - {res_text.get('result','')}"
            else:
                for _result in res_text.get("result", []):
                    details = _result.get("details")
                    response_messages = details["response_messages"]
                    for response_message in response_messages:
                        if response_message["status"] == "error":
                            status = "FAIL"
                            res_text = f"{response_message.get('details', '')} - {response_message.get('phone','')}"
                        else:
                            status = "SUCCESS"
                            res_text = str(res_text)
        elif res.status_code in (504, 408, 502):
            logger.info(f"queue-service.execution.optin, Error message: Internal server error")
            res_text = str({"message": "Internal server error"})
            status = "FAIL"
        else:
            res_text = str(res.text)
            status = "FAIL"
        response = {
            "response": res_text,
            "status_code": res.status_code,
            "kwargs": kwargs,
            "status": status,
        }
    except Exception as e:
        # TODO change the response type handle it more efficiently
        logger.info(f"queue-service.execution.optin exception {str(e)}")
        response = {
            "response": str(e),
            "status_code": 400,
            "kwargs": kwargs,
            "status": "FAIL",
        }

    url = f"{QUEUE_SERVICE_BASE_URL}/execution_response"
    # print(response)
    try:
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-Request-ID": kwargs["request_id"],
            },
        )
        logger.info(f"optin.execution_response_update.status_code :: {res.status_code}")
    except Exception as e:
        logger.info(f"optin.execution_response_update.exception :: {str(e)}")
        return False

    if res.status_code not in (200, 201):
        logger.info(f"optin.execution_response_update.text :: {res.text}")
        return False
    return True


@shared_task(bind=True, name="address_conversion", ignore_result=False)
def address_conversion(self, *args, **kwargs):
    """
    Address conversion API call to recovery service
    {
        "applicant_index": null,
        "address_index": 0,
        "address": "#12/13/1 Layout 560008",
        "loan_id": "v8"
    }
    """
    payload = kwargs["payload"]
    message = kwargs["message"]
    company_id = payload["company_id"]
    applicant_type = payload["applicant_type"]

    url = f"{RECOVERY_SERVICE_BASE_URL}/address_to_coordinates?company_id={company_id}&source=recovery&applicant_type={applicant_type}"

    try:
        logger.info(
            f"Address conversion url - {url} request_payload - {json.dumps(message)} \
            author - {payload['author']}"
        )
        linked_loan_res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(message),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.info(f"execution.address_conversion: {linked_loan_res.text}")

        if linked_loan_res.status_code in (200, 201):
            status = "SUCCESS"
            linked_loan_response = linked_loan_res.text
        elif linked_loan_res.status_code in (504, 408, 502):
            linked_loan_response = str({"message": "Internal server error"})
            status = "FAIL"
        else:
            linked_loan_response = linked_loan_res.text
            status = "FAIL"

        response = {
            "response": linked_loan_response,
            "status_code": linked_loan_res.status_code,
            "kwargs": {**payload, **message},
            "status": status,
        }
    except Exception as e:
        response = {
            "response": str({"message": f"Internal server error - {str(e)}"}),
            "status_code": 500,
            "kwargs": {**payload, **message},
            "status": "FAIL",
        }
    url = f"{QUEUE_SERVICE_BASE_URL}/execution_response"
    try:
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.info(f"address_conversion.execution_response_update.status_code :: {res.status_code}")
    except Exception as e:
        logger.info(f"address_conversion.execution_response_update.exception :: {str(e)}")
        return False
    if res.status_code not in (200, 201):
        logger.info(f"address_conversion.execution_response_update.status :: str({res.text})")
        return False
    return True


@shared_task(bind=True, name="add_ecourt_case", ignore_result=False)
def add_ecourt_case(self, *args, **kwargs):
    logger.info(f"execution.add_ecourt_case")
    payload = kwargs["payload"]
    message = kwargs["message"]

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/ecourt/add-case"

    try:
        logger.debug(f"ecourt add case url - {url} post_data - {json.dumps(message)}")

        result = requests.request(
            method="POST",
            url=url,
            json=message,
            headers={
                "X-CG-User": json.dumps(payload.get("user")),
                "X-CG-Company": json.dumps(payload.get("company")),
            },
        )

        logger.debug(f"add_ecourt_case.result: {result.text}")

        if result.status_code == 200:
            status = "SUCCESS"
            message["status"] = status
        else:
            status = "FAIL"
            message["status"] = status

        response = {
            "response": result.text,
            "status_code": str(result.status_code),
            "loan_id": message["loan_id"],
            "status": status,
        }

    except Exception as e:
        logger.error(f"queue-service.execution.add_ecourt_case exception {str(e)}")
        message["status"] = "FAIL"
        response = {
            "response": str(e),
            "status_code": "400",
            "status": "FAIL",
            "loan_id": message["loan_id"],
        }

    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        logger.debug(f"add_ecourt_case.save_batch_response.url: {url}")
        response_data = {"payload": payload, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.debug(f"add_ecourt_case.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.error(f"add_ecourt_case.save_response.exception :: {str(e)}")
        return False

    if res.status_code not in (200, 201):
        logger.error(f"add_ecourt_case.save_response.text :: {res.text}")
        return False
    return True


@shared_task(bind=True, name="update_ecourt_case")
def update_ecourt_case(self, *args, **kwargs):
    logger.info("execution.update_ecourt_case")
    payload = kwargs["payload"]
    message = kwargs["message"]

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/ecourt/update-ecourt-case"

    try:
        logger.debug(f"ecourt update case url  - {url} post_data - {json.dumps(message)}")

        result = requests.request(
            method="PATCH",
            url=url,
            json=message,
            headers={
                "X-CG-User": json.dumps(payload.get("user")),
                "X-CG-Company": json.dumps(payload.get("company")),
            },
        )

        logger.debug(f"update_ecourt_case.result: {result.text}")

        if result.status_code == 200:
            status = "SUCCESS"
            message["status"] = status

        else:
            status = "FAIL"
            message["status"] = status

        response = {
            "response": result.text,
            "status_code": str(result.status_code),
            "loan_id": "",
            "status": status,
        }

    except Exception as e:
        logger.error(f"queue-service.execution.update_ecourt_case exception {str(e)}")
        response = {
            "response": str(e),
            "status_code": "400",
            "status": "FAIL",
            "loan_id": "",
        }

    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        logger.debug(f"update_ecourt_case.save_batch_response.url: {url}")
        response_data = {"payload": payload, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.debug(f"update_ecourt_case.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.error(f"update_ecourt_case.save_response.exception :: {str(e)}")
        return False

    if res.status_code not in (200, 201):
        logger.error(f"update_ecourt_case.save_response.text :: {res.text}")
        return False
    return True


@shared_task(bind=True, name="fetch_ecourt_case_orders")
def fetch_ecourt_case_orders(self, *args, **kwargs):
    logger.info("execution.fetch_ecourt_case_orders.kwargs :: %s", kwargs)
    payload = kwargs["payload"]
    message = kwargs["message"]

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/ecourt/fetch-ecourt-case-orders"

    try:
        logger.info(f"ecourt update case url  - {url} post_data - {json.dumps(message)}")

        result = requests.request(
            method="PATCH",
            url=url,
            json=message,
            headers={
                "X-CG-User": json.dumps(payload.get("user")),
                "X-CG-Company": json.dumps(payload.get("company")),
            },
        )

        if result.status_code == 200:
            status = "SUCCESS"
            message["status"] = status

        else:
            status = "FAIL"
            message["status"] = status
            logger.error(f"fetch_ecourt_case_orders response :: {result.text}")

        response = {
            "status_code": str(result.status_code),
            "loan_id": "",
            "status": status,
        }

        result_text = json.loads(result.text)

        order_data = result_text.get("data")

        if order_data:
            download_result = download_order_file(order_data, **kwargs)
            response["response"] = str(download_result)

            if not download_result:
                response["status_code"] = str(400)
                response["status"] = "FAIL"
        else:
            response["response"] = "No Orders"

    except Exception as e:
        logger.info(f"queue-service.execution.fetch_ecourt_case_orders exception {str(e)}")
        response = {
            "response": str(e),
            "status_code": "400",
            "status": "FAIL",
            "loan_id": "",
        }

    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        response_data = {"payload": payload, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.info(f"fetch_ecourt_case_orders.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.info(f"fetch_ecourt_case_orders.save_response.exception :: {str(e)}")
        return False

    if res.status_code not in (200, 201):
        logger.info(f"fetch_ecourt_case_orders.save_response.text :: {res.text}")
        return False
    return True


@shared_task(bind=True, name="update_approval_request")
def update_approval_request(self, *args, **kwargs):
    logger.info("execution.update_approval_request")
    payload = kwargs["payload"]
    message = kwargs["message"]

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/approval-requests"

    # message = {**message, "batch_id": payload["batch_id"], "is_created_in_bulk": True}
    approval_request_payload = {
        "row_id": message["row_id"],
        "company_id": message["company_id"],
        "action": message["action"],
        "next_approver_email": message["next_approver_email"],
        "rejection_reason": message["rejection_reason"],
        "batch_id": payload["batch_id"],
        "is_created_in_bulk": True,
    }

    headers = {
        "X-CG-User": json.dumps(payload.get("user")),
        "X-CG-Company": json.dumps(payload.get("company")),
    }

    try:
        logger.debug(f"update_approval_request url  - {url} post_data - {json.dumps(message)}")

        result = requests.request(
            method="PATCH",
            url=url,
            json=approval_request_payload,
            headers=headers,
        )

        logger.debug(f"update_approval_request.result: {result.text}")

        if result.status_code == 200:
            status = "SUCCESS"
            message["status"] = status

        else:
            status = "FAIL"
            message["status"] = status

        response = {
            "response": json.dumps({"case_id": message["case_id"], "response": result.text}),
            "status_code": str(result.status_code),
            "status": status,
            "loan_id": "",
        }

    except Exception as e:
        logger.error(f"queue-service.execution.update_approval_request exception {str(e)}")
        response = {
            "response": json.dumps({"case_id": message["case_id"], "response": str(e)}),
            "status_code": "400",
            "status": "FAIL",
            "loan_id": "",
        }

    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        logger.debug(f"update_approval_request.save_batch_response.url: {url}")
        response_data = {"payload": payload, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.debug(f"update_approval_request.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.error(f"update_approval_request.save_response.exception :: {str(e)}")
        return False

    if res.status_code not in (200, 201):
        logger.error(f"update_approval_request.save_response.text :: {res.text}")
        return False
    return True


@shared_task(bind=True, name="upload_data")
def upload_data(self, *args, **kwargs):
    payload = kwargs["payload"]
    message = kwargs["message"]
    message["company_id"] = payload["company_id"]
    message["notice_type"] = payload["notice_type"]
    message["allocation_month"] = payload["allocation_month"]
    url = f"{SCRAPE_SERVICE_BASE_URL}/speedpost_data_insert"
    try:
        logger.info(f"upload data url - {url} post_data - {json.dumps(message)}")
        api_res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(message),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.info(f"tasks.upload_data: {api_res.text}")
        if api_res.status_code == 200:
            status = "SUCCESS"
            upload_data_response = api_res.text
            logger.info(f"tasks.upload_data.status :: {str(api_res.text)}")
        elif api_res.status_code in (504, 408, 502):
            upload_data_response = str({"message": "Internal server error"})
            status = "FAIL"
        else:
            upload_data_response = api_res.text
            status = "FAIL"

        response = {
            "response": upload_data_response,
            "status_code": api_res.status_code,
            "kwargs": {**payload, **message},
            "status": status,
        }
    except Exception as e:
        logger.info(f"queue-service.tasks.upload_data exception {str(e)}")
        response = {
            "response": str({"message": f"Internal server error - {str(e)}"}),
            "status_code": 500,
            "kwargs": {**payload, **message},
            "status": "FAIL",
        }
    url = f"{QUEUE_SERVICE_BASE_URL}/execution_response"
    try:
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.info(f"upload_data.execution_response_update.status_code :: {res.status_code}")
    except Exception as e:
        logger.info(f"upload_data.execution_response_update.exception :: {str(e)}")
        return False
    if res.status_code not in (200, 201):
        logger.info(f"upload_data.execution_response_update.status :: {str(res.text)}")
        return False
    return True


@shared_task(bind=True, name="upload_disposition", ignore_result=False)
def upload_disposition(self, *args, **kwargs):
    payload = kwargs["payload"]
    message = kwargs["message"]
    logger.info(f"kwargs_upload_disposition:::{kwargs}")

    url = f"{HEROFINCORP_URL}"
    data = {
        "SZUSERNAME": HEROUSER,
        "SZPASSWORD": HEROPASS,
        "SZACCOUNTNO": message["loan_id"],
        "SZEMAILID": "",
        "SZMOBILENO": "",
        "SZMOBILETYPE": "",
        "SZUSERID": message["agent_id"],
        "SZACTIONCODE": "OC",
        "SZRESULTCODE": message["result_code"],
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
        "SZCUSTMOBILENO": message["to_mobile"],
        "SZCALLDURATION": message["call_duration"],
        "SZCALLSTARTTIME": message["call_start_time"][11:16],
        "SZCALLENDTIME": message["call_end_time"][11:16],
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
        "SZFIELD5": message["rec_url"],
        "SZFIELD6": "",
        "SZFIELD7": "",
        "SZFIELD8": "",
        "SZFIELD9": "",
        "SZFIELD10": "",
        "SZCAMPAIGNID": message["campaign_id"],
    }

    try:
        logger.info(f"Herofincorp url - {url}, data::{data}")
        api_res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(data),
            headers={"X-Request-ID": payload["request_id"]},
        )
        logger.info(f"execution.upload_disposition: {api_res.text}")

        if api_res.status_code in (200, 201) and json.loads(api_res.text)["ISTATUSCODE"] == "1":
            status = "SUCCESS"
            upload_disposition_response = api_res.text
            logger.info(f"upload_disposition.execution_response_update.status :: {str(api_res.text)}")
        elif api_res.status_code in (504, 408, 502):
            upload_disposition_response = str({"message": "Internal server error"})
            status = "FAIL"
        else:
            upload_disposition_response = api_res.text
            status = "FAIL"

        response = {
            "response": upload_disposition_response,
            "status_code": api_res.status_code,
            "kwargs": {**payload, **message},
            "status": status,
        }
    except Exception as e:
        logger.info(f"execution.upload_disposition_exception: {str(e)}")
        response = {
            "response": str({"message": f"Internal server error - {str(e)}"}),
            "status_code": 500,
            "kwargs": {**payload, **message},
            "status": "FAIL",
        }
    url = f"{QUEUE_SERVICE_BASE_URL}/execution_response"
    try:
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.info(f"upload_disposition.execution_response_update.status_code :: {res.status_code}")
    except Exception as e:
        logger.info(f"upload_disposition.execution_response_update.exception :: {str(e)}")
        return False
    if res.status_code not in (200, 201):
        logger.info(f"upload_disposition.execution_response_update.status :: {str(res.text)}")
        return False
    return True


# @shared_task(bind=True, name='notifications', ignore_result=False)
# def notifications(self, *args, **kwargs):
#     """
#     Push notifications
#     Pushes data to firestore to trigger notifications
#     Message :
#         {
#             "type": "notifications",
#             "company_id": "ad8b5a88-637f-49a3-b8af-f341dd9db5fd",
#             "loan_data": [
#                     {
#                         "message": "1235 allocated! Schedule your first visit now this is a new message"
#                     }
#                 ],
#             "source": "web_client/app",
#             "notify_type": "reminder/notification",
#             "reminder_offset": [
#                 3
#             ],
#             "reminder_offset_type": "minutes or days or hours",
#             "trigger_time": "2021-11-25 17:30:00"
#     """
#     logger.info("app.tasks.execution.notifications")
#     logger.debug(f"notifications.kwargs: {kwargs}")
#     payload = kwargs['payload']
#     message = kwargs['message']
#     data = payload['data']
#     data = json.loads(data)
#     notify_type = data.get("notify_type", None)
#     trigger_time = data.get('trigger_time', None)
#     now_time = datetime.now()

#     if not notify_type and not trigger_time:
#         logger.error(
#             f"notifications.notify_type :: {notify_type} {trigger_time} not  valid"
#         )
#         return False

#     trigger_time = datetime.strptime(
#         trigger_time, '%Y-%m-%d %H:%M:%S'
#     )
#     if notify_type == NotificationTypeChoices.reminder.value:
#         reminder_offset = data.get("reminder_offset", None)
#         reminder_offset_type = data.get("reminder_offset_type", None)
#         logger.debug(
#             f"notifications.reminder_offset_type :: {reminder_offset_type} - {reminder_offset}"
#         )
#         if isinstance(reminder_offset, list) and isinstance(reminder_offset_type, str):
#             offset_resolved_list = datetime_offset(
#                 trigger_time=trigger_time,
#                 reminder_offset_type=reminder_offset_type,
#                 reminder_offset=reminder_offset,
#                 now_time=now_time
#             )
#             if not offset_resolved_list:
#                 logger.error(
#                     f"notifications.offset_resolved_list :: {offset_resolved_list}"
#                 )
#                 return False
#             for offset_resolved in offset_resolved_list:
#                 logger.debug(
#                     f"notifications.firestore_push :: {offset_resolved} pushing to firstore"
#                 )
#                 firestore_push.s(**kwargs).apply_async(
#                     queue=payload['queue'],
#                     countdown=offset_resolved
#                 )

#     elif notify_type == NotificationTypeChoices.notification.value:
#         if trigger_time < now_time:
#             logger.error(
#                 f"notifications.trigger_time - {trigger_time} now_time - {now_time} trigger time is not valid"
#             )
#             return False
#         notification_countdown = (trigger_time - now_time).seconds
#         print(f"notifications.countdown :: {notification_countdown}")
#         print(f"notifications.firestore_push :: {kwargs}")
#         firestore_push.s(**kwargs).apply_async(
#             queue=payload['queue'],
#             countdown=notification_countdown
#         )

#     return True


# @shared_task(bind=True, name='firestore_push', ignore_result=False)
# def firestore_push(self, *args, **kwargs):
#     """
#     Firestore push
#     """
#     logger.info("app.tasks.execution.firestore_push")
#     logger.debug(f"firestore_push.kwargs :: {kwargs}")

#     payload = kwargs['payload']
#     message = kwargs['message']
#     try:
#         user_id_url = f"{USER_SERVICE_BASE_URL}/public/user-id?username={payload['author']}"
#         logger.debug(
#             f"firestore_push.get_user_id.url :: {user_id_url}"
#         )
#         user_id_data = requests.request(
#             method='GET',
#             url=user_id_url,
#             headers={"Content-Type": "application/json"}
#         )
#         logger.debug(
#                 f"firestore_push.user_id.status_code :: {str(user_id_data.status_code)}"
#             )
#         if user_id_data.status_code != 200:
#             logger.error(
#                 f"firestore_push.user_id.error :: {str(user_id_data.text)}"
#             )
#             return False

#         user_id = json.loads(user_id_data.text)['user_id']
#         ((firebase_db.collection("notifications").document(payload['company_id'])).collection(
#             "user_ids").document(user_id)).collection("notify").add(message)
#     except Exception as e:
#         logger.error(
#             f"firestore_push.exception :: {str(e)}"
#         )
#         return False
#     return True


@shared_task(bind=True, name="upload_c2c_disposition", ignore_result=False)
def upload_c2c_disposition(self, *args, **kwargs):
    logger.info("app.tasks.execution.upload_c2c_disposition")
    payload = kwargs["payload"]
    message = kwargs["message"]
    logger.debug(f"upload_c2c_disposition.kwargs:{kwargs}")

    url = f"{HEROFINCORP_URL}"
    data = HERO_DATA
    data["SZUSERNAME"] = HEROUSER
    data["SZPASSWORD"] = HEROPASS
    data["SZACCOUNTNO"] = message["loan_id"]
    data["SZUSERID"] = message["agent_id"]
    data["SZRESULTCODE"] = message["result_code"]
    data["SZCUSTMOBILENO"] = message["to_mobile"]
    data["SZCALLDURATION"] = message["call_duration"]
    data["SZCALLSTARTTIME"] = message["call_start_time"][11:16]
    data["SZCALLENDTIME"] = message["call_end_time"][11:16]
    data["SZFIELD5"] = message["rec_url"]
    data["SZCAMPAIGNID"] = message["campaign_id"]
    try:
        logger.debug(f"upload_c2c_disposition.url: {url}")
        api_res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(data),
            headers={"X-Request-ID": payload["request_id"]},
        )
        logger.info(f"upload_c2c_disposition.api.status_code: {api_res.status_code}")

        if api_res.status_code == HTTPStatus.OK.value:
            res_text = json.loads(api_res.text)
            if res_text.get("ISTATUSCODE", "") == "1":
                status = "SUCCESS"
                upload_disposition_response = str(res_text.get("SZMESSAGE", ""))
            else:
                logger.error(f"upload_c2c_disposition.api.error :: {api_res.text}")
                status = "FAIL"
                upload_disposition_response = str(res_text.get("SZMESSAGE", ""))
        else:
            logger.error(f"upload_c2c_disposition.api.error :: {api_res.text}")
            upload_disposition_response = format_api_response_text(api_res)
            status = "FAIL"

        response = {
            "response": upload_disposition_response,
            "status_code": str(api_res.status_code),
            "loan_id": message["loan_id"],
            "status": status,
        }
    except Exception as e:
        logger.error(f"upload_c2c_disposition_exception: {str(e)}")
        response = {
            "response": "Internal server error",
            "status_code": "500",
            "loan_id": message["loan_id"],
            "status": "FAIL",
        }
    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        response_data = {"payload": {**payload, **message}, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"upload_c2c_disposition.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.error(f"upload_c2c_disposition.save_response.exception :: {str(e)}")
        return False

    if res.status_code != HTTPStatus.CREATED.value:
        logger.error(f"upload_c2c_disposition.save_response.error :: {res.text}")
        return False
    return True


@shared_task(bind=True, name="lat_long_conversion", ignore_result=False)
def lat_long_conversion(self, *args, **kwargs):
    """
    Address conversion API call to recovery service
    {
        "applicant_index": null,
        "address_index": 0,
        "address": "#12/13/1 Layout 560008",
        "loan_id": "v8"
    }
    """
    logger.info("app.tasks.execution.lat_long_conversion")
    payload = kwargs["payload"]
    message = kwargs["message"]
    company_id = payload["company_id"]
    data = payload["data"]
    data = json.loads(data)
    applicant_type = data["applicant_type"]

    url = f"{RECOVERY_SERVICE_BASE_URL}/address_to_coordinates?company_id={company_id}&source=recovery&applicant_type={applicant_type}"

    try:
        logger.debug(f"lat_long_conversion.url: {url}")
        address_res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(message),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"lat_long_conversion.api.status_code: {address_res.status_code}")
        if address_res.status_code == HTTPStatus.CREATED.value:
            res_text = json.loads(address_res.text)
            status = "SUCCESS"
            address_con_response = str(res_text.get("output", ""))
        else:
            logger.error(f"lat_long_conversion.api.error :: {address_res.text}")
            address_con_response = format_api_response_text(address_res)
            status = "FAIL"

        response = {
            "response": address_con_response,
            "status_code": str(address_res.status_code),
            "loan_id": message.get("loan_id", ""),
            "status": status,
        }
    except Exception as e:
        logger.error(f"lat_long_conversion.exception: {str(e)}")
        response = {
            "response": "Internal server error",
            "status_code": "500",
            "loan_id": message.get("loan_id", ""),
            "status": "FAIL",
        }
    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        response_data = {"payload": {**payload, **message}, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"lat_long_conversion.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.error(f"lat_long_conversion.save_response.exception :: {str(e)}")
        return False

    if res.status_code != HTTPStatus.CREATED.value:
        logger.error(f"lat_long_conversion.save_response.error :: {res.text}")
        return False
    return True


# @shared_task(bind=True, name="linked_loan_generate_digital_notice", ignore_result=False)
# def linked_loan_generate_digital_notice(self, *args, **kwargs):
#     """
#     Linked loan API call to notice service
#     """
#     logger.info("app.tasks.execution.linked_loan_generate_digital_notice")
#     payload = kwargs["payload"]
#     message = kwargs["message"]
#     data = payload["data"]
#     data = json.loads(data)
#     linked_loan_id = message["linked_loan_id"]
#     logger.debug(f"linked_loan_generate_digital_notice.payload: {payload}")

#     url = f"{NOTICE_SERVICE_BASE_URL}/generate_linked_loan_notice?preview=False"
#     try:
#         request_payload = {
#             "linked_loan_id": linked_loan_id,
#             "loan_ids": message["loan_ids"],
#             "draft_id": data["draft_id"],
#             "allocation_month": data["allocation_month"],
#             "creditline": data.get("creditline", False),
#             "is_batch": data.get("is_batch", False),
#             "company_id": payload["company_id"],
#         }

#         logger.debug(f"linked_loan_generate_digital_notice.url: {url}")
#         linked_loan_res = requests.request(
#             method="POST",
#             url=url,
#             data=json.dumps(request_payload),
#             headers={
#                 "Content-Type": "application/json",
#                 "X-CG-User": json.dumps(payload["user"]),
#                 "X-Request-ID": payload["request_id"],
#             },
#         )
#         logger.debug(f"inked_loan_generate_digital_notice.api.status_code: {linked_loan_res.status_code}")
#         if linked_loan_res.status_code == 200:
#             res_text = json.loads(linked_loan_res.text)
#             status = "SUCCESS"
#             linked_loan_response = str(res_text.get("output", ""))
#         else:
#             logger.error(f"inked_loan_generate_digital_notice.api.error :: {linked_loan_res.text}")
#             linked_loan_response = format_api_response_text(linked_loan_res)
#             status = "FAIL"
#         response = {
#             "response": linked_loan_response,
#             "status_code": str(linked_loan_res.status_code),
#             "loan_id": linked_loan_id,
#             "status": status,
#         }
#     except Exception as e:
#         logger.error(f"linked_loan_generate_digital_notice.exception: {str(e)}")
#         response = {
#             "response": "Internal server error",
#             "status_code": "500",
#             "loan_id": linked_loan_id,
#             "status": "FAIL",
#         }
#     url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
#     try:
#         response_data = {"payload": {**payload, **message}, "response": response}
#         res = requests.request(
#             method="POST",
#             url=url,
#             data=json.dumps(response_data),
#             headers={
#                 "Content-Type": "application/json",
#                 "X-CG-User": json.dumps(payload["user"]),
#                 "X-Request-ID": payload["request_id"],
#             },
#         )
#         logger.debug(f"linked_loan_generate_digital_notice.save_response.status_code :: {res.status_code}")
#     except Exception as e:
#         logger.error(f"linked_loan_generate_digital_notice.save_response.exception :: {str(e)}")
#         return False

#     if res.status_code != 201:
#         logger.error(f"linked_loan_generate_digital_notice.save_response.error :: {res.text}")
#         return False
#     return True


@shared_task(bind=True, name="indiapost_upload")
def indiapost_upload(self, *args, **kwargs):
    logger.info("app.tasks.execution.indiapost_upload")
    payload = kwargs["payload"]
    message = kwargs["message"]
    data = payload["data"]
    data = json.loads(data)
    message["company_id"] = payload.get("company_id", "")
    message["notice_type"] = data.get("notice_type", "")
    message["allocation_month"] = data.get("allocation_month", "")
    url = f"{SCRAPE_SERVICE_BASE_URL}/speedpost_data_insert"
    try:
        logger.debug(f"indiapost_upload.url: {url}")
        api_res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(message),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"indiapost_upload.api.status_code: {api_res.status_code}")
        if api_res.status_code == HTTPStatus.OK.value:
            res_text = json.loads(api_res.text)
            status = "SUCCESS"
            upload_data_response = str(res_text.get("output", ""))
        else:
            logger.error(f"indiapost_upload.api.error :: {api_res.text}")
            upload_data_response = format_api_response_text(api_res)
            status = "FAIL"

        response = {
            "response": upload_data_response,
            "status_code": str(api_res.status_code),
            "loan_id": message.get("loan_id", ""),
            "status": status,
            "company_id": message.get("company_id", ""),
            "tracking_number": message.get("tracking_no", ""),
        }
    except Exception as e:
        logger.error(f"indiapost_upload.exception {str(e)}")
        response = {
            "response": "Internal server error",
            "status_code": "500",
            "loan_id": message.get("loan_id", ""),
            "status": "FAIL",
            "company_id": message.get("company_id", ""),
            "tracking_number": message.get("tracking_no", ""),
        }
    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        response_data = {"payload": {**payload, **message}, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"indiapost_upload.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.error(f"indiapost_upload.save_response.exception :: {str(e)}")
        return False

    if res.status_code != HTTPStatus.CREATED.value:
        logger.error(f"indiapost_upload.save_response.error :: {res.text}")
        return False
    return True


@shared_task(bind=True, name="indiapost_tracking", ignore_result=False)
def indiapost_tracking(self, *args, **kwargs):
    logger.info("app.tasks.execution.indiapost_tracking")
    payload = kwargs["payload"]
    message = kwargs["message"]
    company_id = message["company_id"]
    tracking_id = message["tracking_id"]
    loan_id = message["loan_id"]
    logger.debug(f"indiapost_tracking.kwargs: {kwargs}")
    url = f"{SCRAPE_SERVICE_BASE_URL}/indiaposttracking/{tracking_id}?company_id={company_id}&loan_id={loan_id}"

    try:
        logger.debug(f"indiapost_tracking.url - {url}")
        api_res = requests.request(
            method="GET",
            url=url,
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"indiapost_tracking.api.status_code: {api_res.status_code}")
        if api_res.status_code == HTTPStatus.OK.value:
            res_text = json.loads(api_res.text)
            status = "SUCCESS"
            indiapost_tracking_response = str(res_text.get("message", ""))
        else:
            logger.error(f"indiapost_tracking.api.error :: {api_res.text}")
            indiapost_tracking_response = format_api_response_text(api_res)
            status = "FAIL"

        response = {
            "response": indiapost_tracking_response,
            "status_code": str(api_res.status_code),
            "loan_id": loan_id,
            "status": status,
            "company_id": company_id,
            "tracking_number": tracking_id,
        }
    except Exception as e:
        logger.error(f"indiapost_tracking.exception: {str(e)}")
        response = {
            "response": "Internal server error",
            "status_code": "500",
            "loan_id": loan_id,
            "status": "FAIL",
            "company_id": company_id,
            "tracking_number": tracking_id,
        }
    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        response_data = {"payload": {**payload, **message}, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"indiapost_tracking.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.error(f"indiapost_tracking.save_response.exception :: {str(e)}")
        return False

    if res.status_code != HTTPStatus.CREATED.value:
        logger.error(f"indiapost_tracking.save_response.error :: {res.text}")
        return False
    return True


# @shared_task(bind=True, name="generate_digital_notice")
# def generate_digital_notice(*args, **kwargs):
#     """
#     self, payload: dict, loan_id: str, auth_token, role, notice_endpoint, company_id,
#         creditline, preview
#     """
#     logger.info("app.tasks.execution.generate_digital_notice")
#     payload = kwargs["payload"]
#     message = kwargs["message"]
#     company_id = payload["company_id"]
#     data = payload["data"]
#     data = json.loads(data)
#     creditline = data["creditline"]

#     url = f"{NOTICE_SERVICE_BASE_URL}/generate-digital-notice?creditline={creditline}&preview=False"
#     post_data = {
#         "draft_id": data["draft_id"],
#         "allocation_month": data["allocation_month"],
#         "delivery_partner": data["delivery_partner"],
#         "all_applicants": data["all_applicants"],
#         "co_applicant": data["co_applicant"],
#         "notice_type": payload["channel"],
#         "creditline": creditline,
#         "loan_ids": [message],
#         "batch_number": payload["batch_id"],
#         "company_id": company_id,
#     }
#     try:
#         notice_res = requests.request(
#             method="POST",
#             url=url,
#             data=json.dumps(post_data),
#             headers={
#                 "Content-Type": "application/json",
#                 "X-CG-User": json.dumps(payload["user"]),
#                 "X-Request-ID": payload["request_id"],
#             },
#         )
#         logger.debug(f"generate_digital_notice.api.status_code: {notice_res.status_code}")
#         if notice_res.status_code == 200:
#             res_text = json.loads(notice_res.text)
#             status = "SUCCESS"
#             notice_response = str(res_text.get("output", ""))
#         else:
#             logger.error(f"generate_digital_notice.api.error :: {notice_res.text}")
#             notice_response = format_api_response_text(notice_res)
#             status = "FAIL"

#         response = {
#             "response": notice_response,
#             "status_code": str(notice_res.status_code),
#             "loan_id": message,
#             "status": status,
#         }
#     except Exception as e:
#         logger.error(f"generate_digital_notice.exception: {str(e)}")
#         response = {
#             "response": "Internal server error",
#             "status_code": "500",
#             "loan_id": message,
#             "status": "FAIL",
#         }
#     url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
#     try:
#         response_data = {"payload": payload, "response": response}
#         res = requests.request(
#             method="POST",
#             url=url,
#             data=json.dumps(response_data),
#             headers={
#                 "Content-Type": "application/json",
#                 "X-CG-User": json.dumps(payload["user"]),
#                 "X-Request-ID": payload["request_id"],
#             },
#         )
#         logger.debug(f"generate_digital_notice.save_response.status_code :: {res.status_code}")
#     except Exception as e:
#         logger.error(f"generate_digital_notice.save_response.exception :: {str(e)}")
#         return False

#     if res.status_code != 201:
#         logger.error(f"generate_digital_notice.save_response.error :: {res.text}")
#         return False
#     return True


@shared_task(bind=True, name="whatsapp_optin", ignore_result=False)
def whatsapp_optin(self, *args, **kwargs):
    logger.info("app.tasks.execution.whatsapp_optin")
    payload = kwargs["payload"]
    loan_id = kwargs["message"]
    url = f"{COMMUNICATION_SERVICE_BASE_URL}/whatsapp/optin"
    try:
        request_payload = {"loan_id": loan_id, "company_id": payload["company_id"]}

        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(request_payload),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"whatsapp_optin.api.status_code: {res.status_code}")
        res_text = json.loads(res.text)
        if res.status_code == HTTPStatus.OK.value:
            if res_text.get("message", "") != "success":
                status = "FAIL"
                res_text = f"{res_text.get('output', '')} - {res_text.get('result','')}"
            else:
                response_text = []
                failed_count = 0
                for _result in res_text.get("result", []):
                    details = _result.get("details")
                    response_messages = details["response_messages"]
                    for response_message in response_messages:
                        if response_message["status"] == "error":
                            failed_count += 1
                            response_text.append(
                                f"{response_message.get('details', '')} - {response_message.get('phone','')}"
                            )
                if failed_count:
                    status = "FAIL"
                    res_text = str(response_text)
                else:
                    status = "SUCCESS"
                    res_text = str(res_text.get("output", ""))
        else:
            logger.error(f"whatsapp_optin.api.error :: {res.text}")
            res_text = format_api_response_text(res)
            status = "FAIL"
        response = {
            "response": res_text,
            "status_code": str(res.status_code),
            "loan_id": loan_id,
            "status": status,
        }
    except Exception as e:
        # TODO change the response type handle it more efficiently
        logger.error(f"whatsapp_optin.exception {str(e)}")
        response = {
            "response": "Internal server error",
            "status_code": "500",
            "loan_id": loan_id,
            "status": "FAIL",
        }

    url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
    try:
        response_data = {"payload": payload, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"whatsapp_optin.save_response.status_code :: {res.status_code}")
    except Exception as e:
        logger.debug(f"whatsapp_optin.save_response.exception :: {str(e)}")
        return False

    if res.status_code != HTTPStatus.CREATED.value:
        logger.error(f"whatsapp_optin.save_response.error :: {res.text}")
        return False
    return True


@shared_task(bind=True, name="communication")
def communication(self, *args, **kwargs):
    logger.info("app.tasks.execution.communication")
    payload = kwargs["payload"]
    channel = payload["channel"]
    additional_loan_dict = kwargs.get("additional_loan_dict", {})
    post_data = json.loads(payload["data"])
    if not isinstance(post_data, dict):
        post_data = json.loads(post_data)
    logger.debug(f"communication.post_data - {post_data}")
    post_data["comm_dict"] = {**post_data["comm_dict"], **additional_loan_dict}
    post_data["type_of_comm"] = channel
    campaign_id = payload["campaign_id"]
    post_data["comm_dict"]["campaign_id"] = campaign_id
    loan_id = kwargs["loan_id"]
    company_id = payload["company_id"]
    user = payload["user"]
    request_id = payload["request_id"]
    company = payload["company"]

    response = post(
        request_type=RequestTypeChoices.communication.value,
        post_data=post_data,
        loan_id=loan_id,
        company_id=company_id,
        user=user,
        request_id=request_id,
        company=company,
        channel=channel,
    )
    if int(response["status_code"]) == HTTPStatus.OK.value:
        post(
            request_type=RequestTypeChoices.remark.value,
            post_data=post_data,
            loan_id=loan_id,
            company_id=company_id,
            user=user,
            request_id=request_id,
            company=company,
            channel=channel,
        )
    try:
        url = f"{QUEUE_SERVICE_BASE_URL}/save_response"
        response_data = {"payload": payload, "response": response}
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response_data),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
                "X-CG-Company": json.dumps(payload["company"]),
            },
        )
        logger.debug(f"communication.save_response.status_code.{campaign_id} :: {res.status_code}")
    except Exception as e:
        logger.error(f"communication.save_response.exception.{campaign_id} :: {str(e)}")
        return False
    if res.status_code != HTTPStatus.CREATED.value:
        logger.info(f"communication.save_response.error.{campaign_id} :: {res.text}")
        return False

    logger.info("communication.close")
    return True


@shared_task(bind=True, name="communication_dtmf_ivr")
def communication_dtmf_ivr(self, *args, **kwargs):
    logger.info("app.tasks.execution.communication_dtmf_ivr")
    payload = kwargs["payload"]
    channel = payload["channel"]
    post_data = json.loads(payload["data"])
    loan_ids = kwargs["loan_ids"]
    company_id = payload["company_id"]
    user = payload["user"]
    request_id = payload["request_id"]
    company = payload["company"]
    post_data["loan_ids"] = loan_ids
    post_data["company_id"] = company_id
    post_data["additional_data"] = kwargs.get("additional_data", {})
    save_dtmf = False
    url = f"{COMMUNICATION_SERVICE_BASE_URL}/bulk/dtmf/ivr"
    dtmf_ivr_api_res = None
    dtmf_response = {
        "status_code": None,
        "res_data": None,
        "res_message": None,
        "error_code": None,
        "error_description": None,
        "error_name": None,
    }
    try:
        logger.debug(f"communication_dtmf_ivr.url: {url}")
        dtmf_ivr_api_res = requests.request(
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
        logger.debug(f"communication_dtmf_ivr.api.response: {dtmf_ivr_api_res}")
        logger.debug(f"communication_dtmf_ivr.api.status_code: {dtmf_ivr_api_res.status_code}")
        dtmf_response["status_code"] = dtmf_ivr_api_res.status_code
        res_text = json.loads(dtmf_ivr_api_res.text)
        if dtmf_ivr_api_res.status_code == HTTPStatus.MULTI_STATUS.value:
            dtmf_response["res_data"] = res_text.get("data", {})
            dtmf_response["res_message"] = res_text.get("output", "")
            dtmf_response["error_code"] = res_text.get("error_code")
            dtmf_response["error_name"] = res_text.get("error_name")
            dtmf_response["error_description"] = res_text.get("error_description")
        else:
            logger.error(f"communication_dtmf_ivr.api.error :: {dtmf_ivr_api_res.text}")
            dtmf_response["res_message"] = format_api_response_text(dtmf_ivr_api_res)
            dtmf_response["error_code"] = res_text.get("error_code", "COM-501")
            dtmf_response["error_name"] = res_text.get("error_name", dtmf_response["res_message"])
            dtmf_response["error_description"] = res_text.get("error_description", dtmf_response["res_message"])
    except Exception as e:
        logger.error(f"communication_dtmf_ivr.exception: {str(e)}")
        dtmf_response["status_code"] = HTTPStatus.INTERNAL_SERVER_ERROR.value
        dtmf_response["res_message"] = "Failed to trigger DTMF IVR"
        dtmf_response["error_code"] = "QUEUE-501"
        dtmf_response["error_name"] = HTTPStatus.INTERNAL_SERVER_ERROR.name
        dtmf_response["error_description"] = HTTPStatus.INTERNAL_SERVER_ERROR.phrase

    save_dtmf = save_dtmf_response(dtmf_response, loan_ids, payload)
    logger.info("communication_dtmf_ivr.close")
    return save_dtmf



def upload_file_to_s3(bucket: str, local_file_name: str, s3_object_name: str, extra_args: dict = None):
    logger.info(f"execution.upload_file_to_s3")
    s3 = _get_s3_client()

    try:
        response = s3.upload_file(local_file_name, bucket, s3_object_name, ExtraArgs=extra_args)

        logger.debug("response: %s", response)

    except ClientError as e:
        logger.error("error in _upload_file_to_s3: %s", e)
        return False

    return True


def _get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
        endpoint_url="https://s3."+AWS_DEFAULT_REGION+".amazonaws.com",
    )


def delete_local_directory(directory: str):
    logger.info(f"execution.delete_local_directory")
    try:
        shutil.rmtree(directory)
    except OSError as e:
        logger.error("error in delete_local_files: %s", e)
        return False

    return True


def flatten_dict_with_custom_path(key: str, details: dict, path: str):

    # base condition
    if not (isinstance(details, list) or isinstance(details, dict)):
        key_ = key + path
        return {key_: details}

    if isinstance(details, list):
        json_ = {}
        for idx, val_ in enumerate(details):
            json_ = {
                **flatten_dict_with_custom_path(key, val_, path=path + LITIGATION_REPORT_DELIMITER + str(idx + 1)),
                **json_,
            }
        return json_

    elif isinstance(details, dict):
        json_ = {}
        for key, value_ in details.items():
            json_ = {**flatten_dict_with_custom_path(key, value_, path=path), **json_}
        return json_

    else:
        return details


def add_key_with_array(loan_details, obj, i=0, j=0):
    for key, value in obj.items():
        if j:
            loan_details[f"{key}_{i+1}_{j+1}"] = value
        else:
            loan_details[f"{key}_{i+1}"] = value
    return loan_details


def get_loan_id_to_loan_map(loans):
    logger.info("app.tasks.execution.get_loan_id_to_loan_map")

    loans_map = {}
    for loan in loans:
        loans_map[loan["loan_id"]] = loan

    return loans_map


def get_loan_details_batch(loan_ids, page_size, company_id, user, company, page_number):
    logger.info(f"app.tasks.execution.get_loan_details_batch")

    url = f"{RECOVERY_SERVICE_BASE_URL.rstrip('/')}/bulk/loan?company_id={company_id}"

    body = {
        "loan_ids": loan_ids,
        "page_number": page_number,
        "page_size": page_size,
        "company_id": company_id,
    }

    headers = {
        "authenticationtoken": user["authentication_token"],
        "Accept": "application/json",
        "content-type": "application/json",
        "X-CG-User": json.dumps(user),
        "X-CG-Company": json.dumps(company),
    }

    try:
        logger.debug(f"app.tasks.execution.get_loan_details_batch || url: {url}")

        resp = requests.request(url=url, method="POST", headers=headers, json=body)
        logger.debug(f"app.tasks.execution.get_loan_details_batch || status_code :: {resp.status_code}")

        if resp.status_code == 200:
            resp = json.loads(resp.text)
            output = resp.get("output", None)
            if not output:
                return None
            return output.get("data", None)
        else:
            logger.error(f"app.tasks.execution.get_loan_details_batch || failed :: {resp.text}")
            logger.error(f"app.tasks.execution.get_loan_details_batch || failed loan ids -\n\n :: {loan_ids}")

            return None

    except Exception as e:

        logger.error(f"app.tasks.execution.get_loan_details_batch || exception :: {str(e)}")
        logger.error(f"app.tasks.execution.get_loan_details_batch || exception in loan ids -\n\n :: {loan_ids}")
        return None


def get_workflow(**kwargs):
    logger.info(f"app.tasks.execution.get_workflow")
    company_id = kwargs["company_id"]
    case_type = kwargs["data"]["case_type"]
    company = kwargs["company"]

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/workflow"

    params = {"company_id": company_id, "case_type": case_type}

    try:
        logger.debug(f"app.tasks.execution.get_workflow.url: {url}")

        workflow_res = requests.request(
            method="GET",
            url=url,
            params=params,
            headers={
                "authenticationtoken": kwargs["token"],
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-CG-Company": json.dumps(company),
            },
        )
        logger.debug(f"app.tasks.execution.get_workflow.status_code :: {workflow_res.status_code}")

        if workflow_res.status_code == 200:
            workflow_res = json.loads(workflow_res.text)
            return workflow_res["data"]
        else:
            logger.error(f"app.tasks.execution.get_workflow response :: {workflow_res.text}")

    except Exception as e:
        logger.error(f"app.tasks.execution.get_workflow exception {str(e)}")

    return False


def get_report_variables(**kwargs):
    logger.info("app.tasks.execution.get_report_variables")
    company_id = kwargs["company_id"]
    case_type = kwargs["data"]["case_type"]
    proceeding = kwargs["data"].get("proceeding")
    report_type = kwargs["report_name"]
    company = kwargs["company"]

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/report-variables"

    params = {
        "company_id": company_id,
        "report_type": report_type,
        "case_type": case_type,
    }

    if report_type in ("step_mis", "mis", "advocate_mis"):
        params["proceeding"] = proceeding if proceeding else "all_proceedings"

    try:
        logger.debug(f"app.tasks.execution.get_report_variables.url: {url}")

        report_variables_res = requests.request(
            method="GET",
            url=url,
            params=params,
            headers={
                "authenticationtoken": kwargs["token"],
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-CG-Company": json.dumps(company),
            },
        )

        if report_variables_res.status_code == 200:
            report_variables_res = json.loads(report_variables_res.text)
            return report_variables_res
        else:
            logger.error(f"app.tasks.execution.get_report_variables || response : {report_variables_res}")

    except Exception as e:
        logger.error(f"app.tasks.execution.get_report_variables || exception : {str(e)}")

    return False


def get_stage_data_fields(**kwargs):
    logger.info("app.tasks.execution.get_stage_data_fields")
    company_id = kwargs["company_id"]
    case_type = kwargs["data"]["case_type"]
    stage_code = kwargs["data"]["stage_codes"][0]
    company = kwargs["company"]

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/stage-data-fields"

    params = {"company_id": company_id, "case_type": case_type, "stage_code": stage_code}

    try:
        logger.debug(f"app.tasks.execution.get_stage_data_fields.url: {url}")

        report_variables_res = requests.request(
            method="GET",
            url=url,
            params=params,
            headers={
                "authenticationtoken": kwargs["token"],
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-CG-Company": json.dumps(company),
            },
        )

        if report_variables_res.status_code == 200:
            report_variables_res = json.loads(report_variables_res.text)
            return report_variables_res["data"]
        else:
            logger.error(f"app.tasks.execution.get_stage_data_fields || response : {report_variables_res}")

    except Exception as e:
        logger.error(f"app.tasks.execution.get_stage_data_fields || exception : {str(e)}")

    return False


def get_workflow_map(workflow):
    logger.info("app.tasks.execution.get_workflow_map")
    workflow_map = {}
    for stage_flow in workflow:
        workflow_map[stage_flow["stage_code"]] = {
            "stage_name": stage_flow["stage_name"],
            "is_billing_stage": stage_flow["is_billing_stage"],
            "is_litigation_stage": stage_flow["is_litigation_stage"],
        }
    return workflow_map


def _get_zip_access_url(company_id: str, batch_id: str):
    bucket_url = S3_CLOUDFRONT_BUCKET_ENDPOINT
    return f"{bucket_url.rstrip('/')}/{S3_LITIGATION_REPORTS_DIRECTORY}/{company_id}/{batch_id}.zip"


def _get_upload_s3_object_name(company_id: str, batch_id: str):
    return f"{S3_LITIGATION_REPORTS_DIRECTORY}/{company_id}/{batch_id}.zip"


def _get_upload_s3_order_object_name(company_id: str, case_id: str, file_name: str):
    return f"{S3_LITIGATION_ORDERS_DIRECTORY}/{company_id}/{case_id}/{file_name}"


def _get_order_access_url(company_id: str, case_id: str, file_name: str):
    bucket_url = S3_CLOUDFRONT_BUCKET_ENDPOINT
    return f"{bucket_url.rstrip('/')}/{S3_LITIGATION_ORDERS_DIRECTORY}/{company_id}/{case_id}/{file_name}"


def download_order_file(order_data, **kwargs):
    payload = kwargs["payload"]
    message = kwargs["message"]

    company_id = message["company_id"]
    case_id = message["case_id"]

    document_type = "Order"
    result = False

    documents = get_documents(**kwargs)

    for dict in order_data:

        order_date_exists = False
        ecourt_order_date = datetime.strptime(dict["Order Date"], "%d %b %Y")

        if documents:
            for document in documents:
                if document["order_date"]:
                    litigation_hearing_order_date = datetime.strptime(document["order_date"], "%Y-%m-%d")
                    if ecourt_order_date == litigation_hearing_order_date:
                        order_date_exists = True
                        break

        if not order_date_exists:

            volume_mount_directory = VOLUME_MOUNT_DIRECTORY
            local_batch_directory_path = os.path.join(volume_mount_directory, "litigation_orders", payload["batch_id"])
            logger.info(f"local_batch_directory_path: {os.path.exists(local_batch_directory_path)}")

            if not os.path.exists(local_batch_directory_path):
                os.makedirs(local_batch_directory_path)

            file_name = dict.get("Filename")
            file_path = dict.get("Filepath")
            if file_path and file_name:
                file_path = file_path.strip("https://")
                file_path = "https://" + file_path

                response = requests.get(file_path)
                pdf = open(local_batch_directory_path + "/" + file_name, "wb")
                pdf.write(response.content)
                pdf.close()

                bucket = S3_BUCKET_NAME
                s3_object_name = _get_upload_s3_order_object_name(company_id, case_id, file_name)
                logger.info("got s3 order object name")

                local_file_path = local_batch_directory_path + "/" + file_name
                extra_args = {"ContentType": "application/pdf"}
                upload_successful = upload_file_to_s3(bucket, local_file_path, s3_object_name, extra_args)
                logger.info(f"upload_status: {upload_successful}")

                if not upload_successful:
                    return False

                order_access_url = _get_order_access_url(company_id, case_id, file_name)
                logger.info(f"order_access_url: {order_access_url}")

                message["document_type"] = document_type
                message["document_link"] = order_access_url
                message["order_date"] = ecourt_order_date.strftime("%Y-%m-%d")

                execution_kwargs = {
                    "payload": payload,
                    "message": message,
                }

                doc_result = create_case_order_entry(**execution_kwargs)
                logger.info(f"Printing document result value :: {doc_result}")
                result = result or doc_result

    return result


def send_email(payload, **kwargs):
    logger.info(f"execution.send_email")

    base_url = COMMUNICATION_SERVICE_BASE_URL.rstrip("/")
    url = f"{base_url}/mail"

    # logger.debug(f"kwargs: {kwargs}")
    payload["module"] = "litigation"

    headers = {
        "authenticationtoken": kwargs["token"],
        "role": kwargs["role"],
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-Request-ID": str(kwargs["request_id"]),
        "X-CG-User": json.dumps(kwargs["user"]),
        "X-CG-Company": json.dumps(kwargs["company"]),
    }

    try:
        logger.debug(f"send_email.url: {url}")

        res = requests.request(method="POST", url=url, json=payload, headers=headers)

        logger.debug(f"send_email.status_code: {res.status_code}")

        if res.status_code in [200, 201]:
            res = res.json()
            return res
        else:
            logger.error(f"queue-service.execution.send_email response :: {res.text}")
            return None

    except Exception as e:
        logger.error(f"queue-service.execution.send_email exception :: {str(e)}")
        return None


def _send_report_via_email(email_type: str, report_access_url: None, **kwargs):
    logger.info(f"execution._send_report_via_email")
    company_id = kwargs["company_id"]
    batch_id = kwargs["batch_id"]
    report_name = kwargs["report_name"]

    if report_access_url:
        report_access_url = report_access_url

    report_name = report_name.title().replace("_", " ")
    if email_type == "data_exists":
        email_body = f"""
            {report_name} Report For Batch Id: {batch_id}
            <br><br>

            Please find the report <a href="{report_access_url}">here</a>

        """
    elif email_type == "no_data":
        email_body = f"""
            {report_name} Report For Batch Id: {batch_id}
            <br><br>

            There is no case data available for your selection. Please select loans where case data is available

        """
    elif email_type == "failure":
        email_body = f"""
            {report_name} Report For Batch Id: {batch_id}
            <br><br>

            It seems that report generation has failed for your selected loans. Please try generating the report again.

        """
    email_body = (
        email_body
        + f"""
        <br><br>

        This email was sent to you by Credgenics (Copyright © 2020 Analog Legalhub Technology
        Solutions Pvt. Ltd. All Rights Reserved).<br>
        This is a computer generated email. Please do not reply to this email.
    """
    )

    payload = {
        "from_data": {"name": "Credgenics Report", "email": "reports@credgenics.com"},
        "subject": f"{report_name} Report For Batch Id: {batch_id}",
        "to_emails": [{"email": kwargs["author"]}],
        "source": "export_report",
        "email_body": email_body,
    }

    send_email(payload, **kwargs)
    logger.info(f"email sent")


def generate_zip(local_directory_path, local_zip_file_path):
    shutil.make_archive(local_zip_file_path, "zip", local_directory_path)


def is_valid_date_format(date: str, date_format: str):
    try:
        datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False


def get_documents(**kwargs):
    logger.info("execution.get_documents")

    payload = kwargs["payload"]
    message = kwargs["message"]

    company_id = message["company_id"]
    case_id = message["case_id"]
    case_type = message["case_type"]

    base_url = LITIGATION_SERVICE_BASE_URL.rstrip("/")
    url = f"{base_url}/case_orders"

    params = {
        "company_id": company_id,
        "case_type": case_type,
        "case_id": case_id,
    }

    try:
        logger.debug(f"get_documents.url :: {url}")
        headers = {
            "role": payload["role"],
            "accept": "application/json",
            "X-Request-ID": str(payload.get("request_id")),
            "X-CG-User": json.dumps(payload.get("user")),
            "X-CG-Company": json.dumps(payload.get("company")),
        }

        result = requests.request(method="GET", url=url, headers=headers, params=params)

        response = result.json()
        logger.debug("response %s", response)

        if result.status_code == 200:
            return response.get("data")

        return None
    except Exception as e:
        logger.error(f"get_documents.exception :: {str(e)}")
        return None


@shared_task(bind=True, name="bulk_allocation_email", ignore_result=False)
def bulk_allocation_email(self, *args, **kwargs):
    logger.info(f"execution.bulk_allocation_email")
    company = kwargs["company"]
    company_trademark = company["trademark"]
    kwargs["approval_status"] = AllocationApprovalStatuses.APPROVED.value
    allocater_email = kwargs["user"].get("email")

    allocations_data = get_agent_allocations(**kwargs)

    if not allocations_data:
        return True

    reporting_manager_emails_set = set()
    allocation_dict = {}

    for allocation_data in allocations_data:
        email = allocation_data["email"]
        if email in allocation_dict.keys():
            allocation_dict[email].append(allocation_data)
        else:
            allocation_dict[email] = [allocation_data]

        if allocation_data["reporting_manager_emails"]:
            reporting_manager_emails = json.loads(allocation_data["reporting_manager_emails"])
            reporting_manager_emails_set.update(set(reporting_manager_emails))

    domain_name = DOMAIN_NAME

    for key, values in allocation_dict.items():

        contactus_link = "https://credgenics.com/contact"

        email_body = f"""Hi {str(key)},<br><br>

        {allocater_email} has allocated the following cases to you.<br><br>
        You can view the complete case details at the respective links in the table below.<br><br>

        <table border='1' style='border-collapse:collapse'>
            <tr>
                <th>Serial No.</th>
                <th>Loan ID</th>
                <th>Case ID</th>
                <th>Matter Type</th>
                <th>Instruction</th>
                <th>Link</th>
            </tr>

        """
        idx = 1
        for index, value in enumerate(values):
            loan_ids = value["loan_ids"]
            case_id = value["case_id"]
            case_type = value["case_type"]
            allocation_instruction = value["allocation_instruction"]
            company_id = kwargs["company_id"]

            for loan_id in loan_ids:
                process_tracking_link = (
                    f"{domain_name}/app/process-tracking/" f"{case_type}?loan_id={loan_id}&company_id={company_id}"
                )
                email_body = (
                    email_body
                    + f"""
                <tr>
                    <td style="text-align:center">{idx}</td>
                    <td style="text-align:center">{loan_id}</td>
                    <td style="text-align:center">{case_id}</td>
                    <td style="text-align:center">{case_type}</td>
                    <td style="text-align:center">{allocation_instruction}</td>
                    <td style="text-align:center"><a href="{process_tracking_link}">View Case Link</a></td>
                </tr>
                """
                )
                idx += 1

        email_body = (
            email_body
            + f"""</table><br><br>

        <a href="{contactus_link}">Contact Us</a><br><br>

        This email was sent to you by Credgenics (Copyright © 2020 Analog Legalhub Technology
         Solutions Pvt. Ltd. All Rights Reserved).<br>
        This is a computer generated email. Please do not reply to this email. """
        )

        payload = {
            "from_data": {"name": "Credgenics", "email": "legal@credgenics.com"},
            "subject": f"Case allocated by {allocater_email} | {company_trademark} | {case_type} | {index+1}-Cases",
            "to_emails": [{"email": str(key)}],
            "email_body": email_body,
            "source": "bulk_agent_allocation",
            "cc_emails": [{"email": email} for email in reporting_manager_emails_set],
        }

        res = send_email(payload, **kwargs)
        logger.info(f"email sent")

        email_ref_id = None
        email_sent = bool(res)

        if email_sent:
            email_ref_id = res.get("unique_mail_id")

        update_dict = {
            "email_sent": email_sent,
            "email_ref_id": email_ref_id,
            "email": str(key),
        }

        update_agent_allocations(update_dict, **kwargs)

    return True


def get_agent_allocations(**kwargs):
    logger.info("execution.get_agent_allocations")

    batch_id = kwargs["batch_id"]
    request_id = kwargs["request_id"]

    company_id = kwargs["company_id"]

    base_url = LITIGATION_SERVICE_BASE_URL.rstrip("/")
    url = f"{base_url}/agent-allocations"

    if kwargs.get("bulk_approval_request"):
        params = {
            "company_id": company_id,
            "approval_batch_id": batch_id,
            "approval_status": kwargs["approval_status"],
        }
    else:
        params = {
            "company_id": company_id,
            "batch_id": batch_id,
            "approval_status": kwargs["approval_status"],
        }

    try:
        logger.debug(f"get_agent_allocations.url :: {url}")
        headers = {
            "authenticationtoken": kwargs["token"],
            "Content-Type": "application/json",
            "X-Request-ID": str(request_id),
            "X-CG-User": json.dumps(kwargs["user"]),
            "X-CG-Company": json.dumps(kwargs["company"]),
        }

        result = requests.request(method="POST", url=url, headers=headers, json=params)

        response = result.json()

        return response.get("data")

    except Exception as e:
        logger.error(f"get_agent_allocations.exception :: {str(e)}")
        return None


def update_agent_allocations(update_dict, **kwargs):
    logger.info("execution.update_agent_allocations")

    batch_id = kwargs["batch_id"]
    request_id = kwargs["request_id"]

    company_id = kwargs["company_id"]

    base_url = LITIGATION_SERVICE_BASE_URL.rstrip("/")
    url = f"{base_url}/agent-allocations"

    body = {
        "company_id": company_id,
        "batch_id": batch_id,
        "is_active": True,
        "email": update_dict["email"],
        "email_sent": update_dict["email_sent"],
        "email_ref_id": update_dict["email_ref_id"],
        "approval_status": kwargs["approval_status"],
    }
    if kwargs.get("bulk_approval_request"):
        del body["batch_id"]
        body["approval_batch_id"] = batch_id

    try:
        logger.debug(f"update_agent_allocations.url :: {url}")
        headers = {
            "authenticationtoken": kwargs["token"],
            "Content-Type": "application/json",
            "X-Request-ID": str(request_id),
            "X-CG-User": json.dumps(kwargs["user"]),
            "X-CG-Company": json.dumps(kwargs["company"]),
        }

        result = requests.request(method="PATCH", url=url, headers=headers, json=body)

        response = result.json()

        return response

    except Exception as e:
        logger.error(f"update_agent_allocations.exception :: {str(e)}")
        return None


@shared_task(bind=True, name="bulk_approval_email", ignore_result=False)
def bulk_approval_email(self, *args, **kwargs):
    logger.info(f"execution.bulk_approval_email")
    company_id = kwargs["company_id"]
    requester_email = kwargs["user"].get("email")

    approval_requests_data = get_approval_requests(**kwargs)

    approvals = approval_requests_data.get("approvals")

    if not approvals:
        return True

    approval_dict = {}

    for approval_data in approvals:
        email = approval_data["approver_email"]
        if email in approval_dict.keys():
            approval_dict[email].append(approval_data)
        else:
            approval_dict[email] = [approval_data]

    domain_name = DOMAIN_NAME

    for key, values in approval_dict.items():

        contactus_link = "https://credgenics.com/contact"

        approval_link = f"{domain_name}/app/litigation-approval-request?company_id={str(company_id)}"

        email_body = f"""Hi {str(key)},<br><br>

        {requester_email} has sought your approvals for<br><br>
        Case Type : {str(values[0]["case_type"])}<br><br>

        Count of Approval Requests : {len(values)}<br><br>

        Link to access Approvals : <a href="{approval_link}">{approval_link}</a><br><br>


        <a href="{contactus_link}">Contact Us</a><br><br>

        This email was sent to you by Credgenics (Copyright © 2020 Analog Legalhub Technology
         Solutions Pvt. Ltd. All Rights Reserved).<br>
        This is a computer generated email. Please do not reply to this email. """

        payload = {
            "from_data": {"name": "Credgenics", "email": "legal@credgenics.com"},
            "subject": f"Approvals requested by {requester_email}",
            "to_emails": [{"email": str(key)}],
            "source": "bulk_approval_request",
            "email_body": email_body,
        }

        res = send_email(payload, **kwargs)
        logger.info(f"email sent")

        email_ref_id = None
        email_sent = bool(res)

        if email_sent:
            email_ref_id = res.get("unique_mail_id")

        email_attempt_failed = not email_sent

        body = {
            "company_id": kwargs["company_id"],
            "creation_batch_id": kwargs["batch_id"],
            "email_sent": email_sent,
            "email_ref_id": email_ref_id,
            "approver_email": str(key),
            "email_attempt_failed": email_attempt_failed,
        }

        update_approval_requests_status(body, **kwargs)

    return True


@shared_task(bind=True, name="bulk_action_email_to_requester", ignore_result=False)
def bulk_action_email_to_requester(self, *args, **kwargs):
    logger.info(f"execution.bulk_action_email_to_requester")
    company_id = kwargs["company_id"]
    next_approver_email = kwargs.get("next_approver_email")
    approver_email = kwargs["user"].get("email")

    kwargs["use_updation_batch_id"] = True
    approval_requests_data = get_approval_requests(**kwargs)

    approvals = approval_requests_data.get("approvals")

    if not approvals:
        return True

    approval_dict = {}

    for approval_data in approvals:
        email = approval_data["requester_email"]
        if email not in approval_dict:
            approval_dict[email] = []

        approval_dict[email].append(approval_data)

    domain_name = DOMAIN_NAME

    action = approvals[0].get("action")
    case_type = approvals[0].get("case_type")

    stage_names = get_stage_names(company_id, case_type, kwargs)

    rejection_reason = approvals[0].get("rejection_reason")
    rejection_reason = f"Rejection Reason: {rejection_reason}<br><br>" if rejection_reason else ""

    request = "request" if len(approvals) == 1 else "requests"
    if action == "approved" and next_approver_email:
        remaining_sentence = f" and has selected {next_approver_email} as the next approver."
        link_heading = "Link to access Approved Requests"
    else:
        remaining_sentence = "."
        link_heading = "Link to access Rejected Requests"

    # TODO integrate approval or rejected requests page link
    # {link_heading}: <a href="{link}">{link}</a><br><br>

    for email, approval_data in approval_dict.items():
        stage_code = approval_data[0].get("stage_code")
        stage_name = "- " + stage_names.get(stage_code)
        approval_link = f""
        rejection_link = f""
        link = approval_link if action == "approved" else rejection_link
        contactus_link = "https://credgenics.com/contact"
        email_body = f"""Hi {email},<br><br>
        {approver_email} has {action} {len(approval_data)} {request} raised by you{remaining_sentence}<br><br>
        Case Type: {case_type}<br><br>
        Process Step: {stage_code} {stage_name}<br><br>
        {rejection_reason}


        <a href="{contactus_link}">Contact Us</a><br><br>
        This email was sent to you by Credgenics (Copyright © 2020 Analog Legalhub Technology Solutions Pvt. Ltd. All Rights Reserved).<br>
        This is a computer generated email. Please do not reply to this email.
        """

        subject = f"Approval requests {action} by {approver_email}"

        body = {
            "from_data": {"name": "Credgenics", "email": "legal@credgenics.com"},
            "subject": subject,
            "to_emails": [{"email": email}],
            "source": "bulk_action_email_to_requester",
            "email_body": email_body,
        }

        send_email_response = send_email(body, **kwargs)
        logger.debug(f"send_email_response: {send_email_response}")

    return True


def get_stage_names(company_id, case_type, kwargs):
    logger.info(f"execution.get_stage_names")

    stages_data = []

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/workflow/stage-names"
    params = {"company_id": company_id, "case_type": case_type, "include_special_stages": True}
    headers = {
        "X-CG-User": json.dumps(kwargs.get("user")),
        "X-CG-Company": json.dumps(kwargs.get("company")),
    }

    try:
        logger.debug(f"update_approval_request url  - {url}")
        result = requests.request(
            method="GET",
            url=url,
            params=params,
            headers=headers,
        )
        logger.debug(f"get_stage_names.status_code: {result.status_code}")
        logger.debug(f"get_stage_names.result: {result.text}")
        data = json.loads(result.text)
        stages_data = data.get("data", [])
    except Exception as e:
        logger.error(f"queue-service.execution.get_stage_names exception: {str(e)}")

    stage_names = {}
    for stage_data in stages_data:
        stage_code = stage_data.get("stage_code")
        stage_name = stage_data.get("stage_name")
        stage_names[stage_code] = stage_name

    return stage_names


def get_approval_requests(**kwargs):
    logger.info("execution.get_approval_requests")

    batch_id = kwargs["batch_id"]
    request_id = kwargs["request_id"]

    company_id = kwargs["company_id"]

    base_url = LITIGATION_SERVICE_BASE_URL.rstrip("/")
    url = f"{base_url}/approval-requests"

    params = {
        "company_id": company_id,
    }

    if kwargs.get("use_updation_batch_id"):
        params["updation_batch_id"] = batch_id
        params["action"] = "approved,rejected"
    else:
        params["creation_batch_id"] = batch_id

    try:
        logger.debug(f"get_approval_requests.url :: {url}")
        headers = {
            "authenticationtoken": kwargs["token"],
            "Content-Type": "application/json",
            "X-Request-ID": str(request_id),
            "X-CG-User": json.dumps(kwargs["user"]),
            "X-CG-Company": json.dumps(kwargs["company"]),
        }

        result = requests.request(method="GET", url=url, headers=headers, params=params)

        response = result.json()

        return response.get("data")

    except Exception as e:
        logger.error(f"get_approval_requests.exception :: {str(e)}")
        return None


def update_approval_requests_status(body, **kwargs):
    logger.info("execution.update_approval_requests_status")

    request_id = kwargs["request_id"]

    base_url = LITIGATION_SERVICE_BASE_URL.rstrip("/")
    url = f"{base_url}/approval-requests-status"

    try:
        logger.debug(f"update_approval_requests_status.url :: {url}")
        headers = {
            "authenticationtoken": kwargs["token"],
            "Content-Type": "application/json",
            "X-Request-ID": str(request_id),
            "X-CG-User": json.dumps(kwargs["user"]),
            "X-CG-Company": json.dumps(kwargs["company"]),
        }

        result = requests.request(method="PATCH", url=url, headers=headers, json=body)

        response = result.json()

        return response

    except Exception as e:
        logger.error(f"update_approval_requests_status.exception :: {str(e)}")
        return None


"""
#####################################################################
                        GENERATE EXCEL NEW VERSION
#####################################################################
"""


def clean_dict_data_remove_keys(dict_list, keys_to_be_retained):
    """METHOD TO CLEAN DICT LIST - by removing the keys mentioned in the list

    Args:
        dict_list (_type_): _description_
        keys_to_be_retained (_type_): _description_

    Returns:
        dict_list: list of dicts
    """
    keys_to_be_removed = []

    if not dict_list:
        return None

    for key in dict_list[0].keys():
        if key not in keys_to_be_retained:
            keys_to_be_removed.append(key)

    for item in dict_list:
        for key in keys_to_be_removed:
            item.pop(key, None)

    return dict_list


def get_case_map(cases):
    logger.info("app.tasks.execution.get_case_map")
    case_map = {}
    case_id_list = []

    for case in cases:
        loan_id = case["loan_id"]
        case_id = case["case_id"]

        case_id_list.append(case_id)

        key = loan_id + LITIGATION_REPORT_DELIMITER + case_id
        case_map[key] = case

    return case_id_list, case_map


def get_advocate_allocation_map(advocate_allocations, user_map, advocate_map, report_type):
    logger.info("app.tasks.execution.get_advocate_allocation_map")

    # advocate_map :: {"loan_case(_stage_iteration)" : [{allocation+user_data}]}
    if not advocate_map:
        advocate_map = {}

    for advocate_allocation in advocate_allocations:
        loan_id = advocate_allocation["loan_id"]
        case_id = advocate_allocation["case_id"]
        stage_code = advocate_allocation["stage_code"]
        iteration = advocate_allocation["iteration"]
        user_id = advocate_allocation["user_id"]

        if report_type == "step_mis":
            key = (
                loan_id
                + LITIGATION_REPORT_DELIMITER
                + case_id
                + LITIGATION_REPORT_DELIMITER
                + str(stage_code)
                + LITIGATION_REPORT_DELIMITER
                + str(iteration)
            )
        else:
            key = loan_id + LITIGATION_REPORT_DELIMITER + case_id

        user = user_map.get(user_id, {})
        advocate_allocation = {**advocate_allocation, **user}

        if advocate_map.get(key):
            advocate_map[key].append(advocate_allocation)
        else:
            advocate_map[key] = [advocate_allocation]
    return advocate_map


def get_cases_data(
    loan_ids_batch, case_page_number, batch_size, company_id, data, report_name, user_details, company_details
):
    logger.info("app.tasks.execution.get_cases")

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/cases"

    payload = {
        "company_id": company_id,
        "loan_ids": loan_ids_batch,
        "case_type": data.get("case_type"),
        "page_size": batch_size,
        "page_number": case_page_number,
    }

    next_hearing_date_start = data.get("next_hearing_date_start")
    next_hearing_date_end = data.get("next_hearing_date_end")
    case_status = data.get("case_status", [])

    if next_hearing_date_start and next_hearing_date_end:
        payload["next_hearing_date_start"] = next_hearing_date_start
        payload["next_hearing_date_end"] = next_hearing_date_end
    if case_status:
        if not (len(case_status) == 1 and case_status[0].lower() == "all"):
            payload["statuses"] = case_status

    if report_name in ("step_mis", "mis", "advocate_mis") and data.get("proceeding"):
        payload["proceeding"] = data["proceeding"]

    try:
        logger.debug(f"app.tasks.execution.get_cases || url: {url}")

        cases_res = requests.request(
            method="POST",
            url=url,
            json=payload,
            headers={
                "authenticationtoken": user_details["authentication_token"],
                "X-CG-User": json.dumps(user_details),
                "X-CG-Company": json.dumps(company_details),
                "Content-Type": "application/json",
            },
        )
        logger.debug(f"app.tasks.execution.get_cases || status_code :: {cases_res.status_code}")

        if cases_res.status_code == 200:
            cases_res = cases_res.json()
            cases_res = cases_res["data"]
            for case in cases_res:
                case["case_status"] = case["status"]
            return cases_res

        else:
            logger.error(f"app.tasks.execution.get_cases || response :: {cases_res.text}")

    except Exception as e:
        logger.error(f"app.tasks.execution.get_cases || exception :: {str(e)}")

    return False


def get_stage_data(
    loan_ids_batch,
    case_row_ids,
    stage_page_size,
    stages_page_number,
    data,
    no_case_row_id_present,
    company_id,
    report_name,
    user_details,
    company_details,
):
    logger.info("app.tasks.execution.get_stage_data")
    stage_creation_from_date = data.get("stage_creation_from_date")
    stage_creation_to_date = data.get("stage_creation_to_date")

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/stages"
    body = {
        "company_id": company_id,
        "loan_ids": loan_ids_batch,
        "case_row_ids": case_row_ids,
        "case_type": data.get("case_type"),
        "page_size": stage_page_size,
        "page_number": stages_page_number,
        "stage_creation_from_date": stage_creation_from_date,
        "stage_creation_to_date": stage_creation_to_date,
        "no_case_row_id_present": no_case_row_id_present,
    }

    if report_name == "step_mis" and data.get("stage_codes"):
        body["stage_codes"] = data["stage_codes"]

    try:
        logger.debug(f"app.tasks.execution.get_stages || url: {url}")

        stages_res = requests.request(
            method="POST",
            url=url,
            json=body,
            headers={
                "authenticationtoken": user_details["authentication_token"],
                "X-CG-User": json.dumps(user_details),
                "X-CG-Company": json.dumps(company_details),
                "Content-Type": "application/json",
            },
        )
        logger.debug(f"app.tasks.execution.get_stages || status_code :: {stages_res.status_code}")

        if stages_res.status_code == 200:
            stages_res = json.loads(stages_res.text)
            stages_res = stages_res["data"]
            for stage in stages_res:
                stage["stage_status"] = stage["status"]
            return stages_res
        else:
            logger.error(f"app.tasks.execution.get_stages ||  response :: {stages_res.text}")

    except Exception as e:
        logger.error(f"app.tasks.execution.get_stages || exception :: {str(e)}")

    return False


def get_reminder_data(
    loan_ids_batch,
    case_ids,
    reminder_page_size,
    reminders_page_number,
    data,
    not_in_case,
    company_id,
    user_details,
    company_details,
):
    logger.info("app.tasks.execution.get_reminder_data")

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/reminders"
    body = {
        "company_id": company_id,
        "loan_ids": loan_ids_batch,
        "case_id": case_ids,
        "case_type": data.get("case_type"),
        "page_number": reminders_page_number,
        "limit": reminder_page_size,
        "not_in_case": not_in_case,
    }

    try:
        logger.debug(f"app.tasks.execution.get_reminder_data  || url: {url}")

        reminders_res = requests.request(
            method="POST",
            url=url,
            json=body,
            headers={
                "authenticationtoken": user_details["authentication_token"],
                "X-CG-User": json.dumps(user_details),
                "Content-Type": "application/json",
                "X-CG-Company": json.dumps(company_details),
            },
        )
        logger.debug(f"app.tasks.execution.get_reminder_data || status_code :: {reminders_res.status_code}")

        if reminders_res.status_code == 200:
            reminders_res = json.loads(reminders_res.text)
            reminders_res = reminders_res["data"]["result"]
            return reminders_res

        else:
            logger.error(f"app.tasks.execution.get_reminder_data || response :: {reminders_res.text}")

    except Exception as e:
        logger.error(f"app.tasks.execution.get_reminder_data || exception :: {str(e)}")

    return False


def get_agent_allocation_data(
    loan_ids_batch,
    case_id_batch,
    page_size,
    page_number,
    data,
    company_id,
    report_type,
    user_details,
    company_details,
    present_in_approved_case,
):
    logger.info("app.tasks.execution.get_agent_allocation_data")

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/agent-allocations"
    body = {
        "company_id": company_id,
        "loan_id": loan_ids_batch,
        "case_id_list": case_id_batch,
        "case_type": data.get("case_type"),
        "page_size": page_size,
        "page_number": page_number,
        "get_advocate_user_details": False,
        "present_in_approved_case": present_in_approved_case,
    }
    if report_type in ("mis", "advocate_mis"):
        body["approval_status"] = "approved"

    try:
        logger.debug(f"app.tasks.execution.get_agent_allocation_data || url: {url}")

        result = requests.request(
            method="POST",
            url=url,
            json=body,
            headers={
                "authenticationtoken": user_details["authentication_token"],
                "X-CG-User": json.dumps(user_details),
                "X-CG-Company": json.dumps(company_details),
                "Content-Type": "application/json",
            },
        )
        logger.debug(f"app.tasks.execution.get_agent_allocation_data || status_code :: {result.status_code}")

        if result.status_code == 200:
            result = result.json()
            result = result["data"]
            return result
        else:
            logger.error(f"app.tasks.execution.get_agent_allocation_data ||  response :: {result.text}")

    except Exception as e:
        logger.error(f"app.tasks.execution.get_agent_allocation_data || exception :: {str(e)}")
        raise e

    return False


def get_headers(report_variables, report_name, stage_codes, stage_specific_variable_ids_list, workflow_map):
    logger.info("app.tasks.execution.get_headers")

    # DEFAULT HEADERS
    if report_name == "ageing":
        default_headers = {
            "loan_id": {"level": "loan", "bold": False, "max_width": len("loan_id")},
            "case_type": {
                "level": "reminder",
                "bold": False,
                "max_width": len("case_type"),
            },
            "case_id": {
                "level": "reminder",
                "bold": False,
                "max_width": len("case_id"),
            },
            "case_status": {"level": "case", "bold": False, "max_width": len("case_status")},
            "current_stage_name": {
                "level": "reminder",
                "bold": False,
                "max_width": len("current_stage_name"),
            },
            "created": {
                "level": "stage",
                "bold": False,
                "max_width": len("created"),
            },
            "next_stage_name": {
                "level": "reminder",
                "bold": False,
                "max_width": len("next_stage_name"),
            },
            "pending_for": {
                "level": "reminder",
                "bold": False,
                "max_width": len("pending_for"),
            },
            "deadline_date": {"level": "reminder", "bold": False, "max_width": len("deadline_date")},
            "tat_breached": {
                "level": "reminder",
                "bold": False,
                "max_width": len("tat_breached"),
            },
            "days_since_tat_breached": {
                "level": "reminder",
                "bold": False,
                "max_width": len("days_since_tat_breached"),
            },
            "dpd": {"level": "reminder", "bold": False, "max_width": len("dpd")},
        }

    elif report_name == "billing":
        default_headers = {
            "loan_id": {"level": "loan", "bold": False, "max_width": len("loan_id")},
            "case_id": {"level": "case", "bold": False, "max_width": len("case_id")},
            "case_type": {
                "level": "case",
                "bold": False,
                "max_width": len("case_type"),
            },
            "proceeding": {
                "level": "case",
                "bold": False,
                "max_width": len("proceeding"),
            },
            "case_status": {"level": "case", "bold": False, "max_width": len("case_status")},
            "stage_code": {
                "level": "stage",
                "bold": False,
                "max_width": len("stage_code"),
            },
            "iteration": {
                "level": "stage",
                "bold": False,
                "max_width": len("iteration"),
            },
            "vendor_id": {
                "level": "stage",
                "bold": False,
                "max_width": len("vendor_id"),
            },
            "vendor_fees": {
                "level": "stage",
                "bold": False,
                "max_width": len("vendor_fees"),
            },
            "litigation_cost": {
                "level": "stage",
                "bold": False,
                "max_width": len("litigation_cost"),
            },
            "tax": {"level": "stage", "bold": False, "max_width": len("tax")},
            "invoice_number": {
                "level": "stage",
                "bold": False,
                "max_width": len("invoice_number"),
            },
            "billing_date": {
                "level": "stage",
                "bold": False,
                "max_width": len("billing_date"),
            },
            "filing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("filing_date"),
            },
            "next_hearing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("next_hearing_date"),
            },
            "last_hearing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("last_hearing_date"),
            },
            "disposed_date": {
                "level": "case",
                "bold": False,
                "max_width": len("disposed_date"),
            },
            "total_cost": {
                "level": "stage",
                "bold": False,
                "max_width": len("total_cost"),
            },
            "author": {
                "level": "stage",
                "bold": False,
                "max_width": len("author"),
            },
            "created": {
                "level": "stage",
                "bold": False,
                "max_width": len("created"),
            },
        }

    elif report_name == "advocate_mis":
        default_headers = {
            "loan_id": {"level": "loan", "bold": False, "max_width": len("loan_id")},
            "case_type": {
                "level": "case",
                "bold": False,
                "max_width": len("case_type"),
            },
            "case_id": {"level": "case", "bold": False, "max_width": len("case_id")},
            "proceeding": {
                "level": "case",
                "bold": False,
                "max_width": len("proceeding"),
            },
            "last_completed_step": {
                "level": "case",
                "bold": False,
                "max_width": len("last_completed_step"),
            },
            # dynamically created data field
            "next_stage_code_list_comma_separated_": {
                "level": "reminder",
                "bold": False,
                "max_width": len("next_stage_code_list_"),
            },
            "case_status": {"level": "case", "bold": False, "max_width": len("case_status")},
            "author": {
                "level": "stage",
                "bold": False,
                "max_width": len("author"),
            },
            "created": {
                "level": "stage",
                "bold": False,
                "max_width": len("created"),
            },
            # dynamically created data field
            "case_documents_": {
                "level": "case",
                "bold": False,
                "max_width": len("case_documents_"),
            },
        }

    elif report_name == "mis":
        default_headers = {
            "loan_id": {"level": "loan", "bold": False, "max_width": len("loan_id")},
            "case_type": {
                "level": "stage",
                "bold": False,
                "max_width": len("case_type"),
            },
            "case_id": {"level": "stage", "bold": False, "max_width": len("case_id")},
            "case_status": {"level": "case", "bold": False, "max_width": len("case_status")},
            "proceeding": {
                "level": "case",
                "bold": False,
                "max_width": len("proceeding"),
            },
            "last_completed_step": {
                "level": "case",
                "bold": False,
                "max_width": len("last_completed_step"),
            },
            "last_hearing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("last_hearing_date"),
            },
            "last_hearing_summary": {
                "level": "case",
                "bold": False,
                "max_width": len("last_hearing_summary"),
            },
            "filing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("filing_date"),
            },
            "e_court_status": {
                "level": "case",
                "bold": False,
                "max_width": len("e_court_status"),
            },
            "disposed_date": {
                "level": "case",
                "bold": False,
                "max_width": len("disposed_date"),
            },
            # dynamically created data field
            "next_stage_code_list_comma_separated_": {
                "level": "reminder",
                "bold": False,
                "max_width": len("next_stage_code_list_"),
            },
            "next_hearing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("next_hearing_date"),
            },
            "next_hearing_preparation": {
                "level": "case",
                "bold": False,
                "max_width": len("next_hearing_preparation"),
            },
            # dynamically created data field
            "case_documents_": {
                "level": "case",
                "bold": False,
                "max_width": len("case_documents_"),
            },
        }

    elif report_name == "step_mis":
        default_headers = {
            "loan_id": {"level": "loan", "bold": False, "max_width": len("loan_id")},
            "case_type": {
                "level": "stage",
                "bold": False,
                "max_width": len("case_type"),
            },
            "case_id": {"level": "stage", "bold": False, "max_width": len("case_id")},
            "case_status": {"level": "case", "bold": False, "max_width": len("case_status")},
            "stage_code": {
                "level": "stage",
                "bold": False,
                "max_width": len("stage_code"),
            },
            "stage_status": {"level": "stage", "bold": False, "max_width": len("stage_status")},
            "proceeding": {
                "level": "case",
                "bold": False,
                "max_width": len("proceeding"),
            },
            "hearing_date": {
                "level": "stage",
                "bold": False,
                "max_width": len("hearing_date"),
                "is_litigation_var": True,
            },
            "last_completed_step": {
                "level": "case",
                "bold": False,
                "max_width": len("last_completed_step"),
            },
            "last_hearing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("last_hearing_date"),
                "is_litigation_var": True,
            },
            "last_hearing_summary": {
                "level": "case",
                "bold": False,
                "max_width": len("last_hearing_summary"),
                "is_litigation_var": True,
            },
            "filing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("filing_date"),
                "is_litigation_var": True,
            },
            "e_court_status": {
                "level": "case",
                "bold": False,
                "max_width": len("e_court_status"),
                "is_litigation_var": True,
            },
            "disposed_date": {
                "level": "case",
                "bold": False,
                "max_width": len("disposed_date"),
                "is_litigation_var": True,
            },
            "next_stage_code": {
                "level": "case",
                "bold": False,
                "max_width": len("next_stage_code"),
                "is_litigation_var": True,
            },
            "next_hearing_date": {
                "level": "case",
                "bold": False,
                "max_width": len("next_hearing_date"),
                "is_litigation_var": True,
            },
            "next_hearing_preparation": {
                "level": "case",
                "bold": False,
                "max_width": len("next_hearing_preparation"),
                "is_litigation_var": True,
            },
            "author": {
                "level": "stage",
                "bold": False,
                "max_width": len("author"),
            },
            "created": {
                "level": "stage",
                "bold": False,
                "max_width": len("created"),
            },
            "editor": {
                "level": "stage",
                "bold": False,
                "max_width": len("editor"),
            },
            "updated": {
                "level": "stage",
                "bold": False,
                "max_width": len("updated"),
            },
        }

    if stage_codes and report_name == "step_mis":
        is_litigation_stage = workflow_map[stage_codes[0]]["is_litigation_stage"]
        # if not a litigation_var, do not show values for default headers
        if not is_litigation_stage:
            updated_default_headers = {}
            for header, header_value in default_headers.items():
                if not header_value.get("is_litigation_var"):
                    updated_default_headers[header] = header_value
            default_headers = updated_default_headers

    variables = sorted(report_variables, key=lambda d: d["priority"])

    report_headers = {}
    for variable in variables:
        # only keeping relevant info in report_variables which are step specific
        if stage_codes and report_name == "step_mis" and stage_specific_variable_ids_list:
            if variable["variable_id"] in stage_specific_variable_ids_list:
                report_headers[variable["name"]] = {
                    "level": variable["level"],
                    "bold": False,
                    "max_width": len(variable["name"]),
                    "array_length": 0,
                    "is_array": variable["is_array"],
                }
        else:
            report_headers[variable["name"]] = {
                "level": variable["level"],
                "bold": False,
                "max_width": len(variable["name"]),
                "array_length": 0,
                "is_array": variable["is_array"],
            }

    headers = {**default_headers, **report_headers}

    return headers


def calculate_width_of_elements(row_data_list: list, headers: dict, workflow_map: dict):
    """CLEAN DATA & FIND MAX WIDTH

    Args:
        row_data_list (_type_): _description_
        headers (_type_): _description_
        workflow_map (_type_): _description_
    """
    logger.info("app.tasks.execution.calculate_width_of_elements")
    if len(row_data_list) == 0:
        return headers, row_data_list

    for index, row in enumerate(row_data_list):
        for header, header_value in headers.items():
            level = header_value["level"]
            if row[level] is None:
                continue

            for key, value in row[level].items():

                # DATA CLEANING =>
                if level == "stage":
                    if key == "stage_code":
                        if value and workflow_map.get(str(value)):
                            value = f"{value} - {workflow_map[str(value)]['stage_name']}"
                            row_data_list[index][level]["stage_code"] = value

                    if key == "vendor_id":
                        if not value:
                            value = "N/A"
                            row_data_list[index][level][key] = value

                if level == "case":
                    if key == "last_completed_step":
                        if value and workflow_map.get(str(value)):
                            value = f"{value} - {workflow_map[str(value)]['stage_name']}"
                            row_data_list[index][level][key] = value

                    if key == "next_stage_code":
                        if value and workflow_map.get(str(value)):
                            value = f"{value} - {workflow_map[str(value)]['stage_name']}"
                            row_data_list[index][level]["next_stage_code"] = value

                # WIDTH & ARRAY LEN CALCULATION =>
                if header == key:
                    if isinstance(value, str):
                        if len(value) > headers[header]["max_width"]:
                            headers[header]["max_width"] = len(value)
                    elif isinstance(value, list):
                        if len(value) > headers[header]["array_length"]:
                            headers[header]["array_length"] = len(value)
                            for _ in value:
                                if isinstance(_, str):
                                    if len(_) > headers[header]["max_width"]:
                                        headers[header]["max_width"] = len(_)
                # (dynamic loan,advocate list variables)  :: array length calculation
                elif level in ("loan", "advocate") and header_value.get("is_array", False):
                    tokenized_key = key.split(LITIGATION_REPORT_DELIMITER)
                    if tokenized_key[0] == header:
                        # create multiple header approach
                        if not headers[header].get("indexed_header_keys"):
                            headers[header]["indexed_header_keys"] = {key}
                        else:
                            headers[header]["indexed_header_keys"].add(key)

    return headers, row_data_list


def get_variable_id_list_for_stage(stage_required_fields):
    logger.info("app.tasks.execution.get_variable_id_list_for_stage")
    variable_id_list = [variable["variable_id"] for variable in stage_required_fields]
    return variable_id_list


def _get_prerequisite(**kwargs):
    """
    Should be inside producer functions - gets all the prerequisites for litigation report consumer
    """
    logger.info("app.tasks.execution._get_prerequisite")
    report_name = kwargs["report_name"]
    batch_id = kwargs["batch_id"]
    workflow = get_workflow(**kwargs)
    logger.info(f"app.tasks.execution._get_prerequisite || {batch_id} || got workflow")
    report_variables = get_report_variables(**kwargs)
    stage_specific_variable_ids_list = []
    stage_codes = kwargs["data"].get("stage_codes")
    logger.info(f"app.tasks.execution._get_prerequisite || {batch_id} || got report variables")
    if report_name == "step_mis" and stage_codes:
        stage_required_fields = get_stage_data_fields(**kwargs)
        logger.info(f"app.tasks.execution._get_prerequisite || {batch_id} || got stage required fields")
        if stage_required_fields:
            stage_specific_variable_ids_list = get_variable_id_list_for_stage(stage_required_fields)

    if not workflow or not report_variables:
        logger.error(
            f"app.tasks.execution._get_prerequisite || {batch_id} ||no_data :: workflow: {bool(workflow)}, report_variables: {bool(report_variables)}"
        )
        raise Exception("app.tasks.execution._get_prerequisite.no_data")

    workflow_map = get_workflow_map(workflow)
    report_variables = report_variables["data"]

    headers = get_headers(report_variables, report_name, stage_codes, stage_specific_variable_ids_list, workflow_map)
    (
        loan_level_headers,
        case_level_headers,
        stage_level_headers,
        reminder_level_headers,
        advocate_level_headers,
    ) = get_required_headers_per_level(headers)

    advocate_level_report_variables = []
    is_require_advocate_data = False
    for variable in report_variables:
        if variable.get("level") == "advocate":
            advocate_level_report_variables.append(variable["name"])
            is_require_advocate_data = True
    advocate_level_headers.extend(advocate_level_report_variables)

    advocate_user_map = {}
    if is_require_advocate_data:
        advocate_user_map = get_advocate_user_details(kwargs["company"], advocate_level_headers)

    return (
        workflow_map,
        is_require_advocate_data,
        advocate_user_map,
        headers,
        loan_level_headers,
        case_level_headers,
        stage_level_headers,
        reminder_level_headers,
        advocate_level_headers,
    )


def get_advocate_user_details(company, advocate_level_headers):
    logger.info("app.tasks.execution.get_advocate_user_details")
    all_users = get_users(company)
    all_users = clean_dict_data_remove_keys(all_users, advocate_level_headers)
    user_map = {}
    for user in all_users:
        if user["profession"] == "advocate":
            user_map[user["user_id"]] = user
    return user_map


def update_headers_before_report_generation(headers):
    logger.info("app.tasks.execution.update_headers_before_report_generation")
    new_headers = {}
    dynamic_array_variable_map = {}
    for header, header_value in headers.items():
        if (
            header_value["level"] in ("loan", "advocate")
            and header_value.get("is_array", False)
            and header_value.get("indexed_header_keys", {})
        ):
            indexed_header_keys = list(header_value["indexed_header_keys"])
            indexed_header_keys.sort()
            dynamic_array_variable_map[header] = {"indexed_header_keys": indexed_header_keys}

            # create new set of headers
            for indexed_header in header_value["indexed_header_keys"]:
                new_headers[indexed_header] = {
                    "level": header_value["level"],
                    "bold": header_value["bold"],
                    "max_width": header_value["max_width"],
                    "array_length": 0,
                    "is_array": False,
                }
        else:
            new_headers[header] = header_value

    return new_headers, dynamic_array_variable_map


def create_response_data_for_queue_litigation_report(**kwargs):
    logger.info("app.tasks.execution.create_response_data_for_queue_litigation_report")

    queue = kwargs["queue"]
    type_of_task = "_".join(queue.split("_")[1:])
    data = kwargs["data"]
    generic_data = data["loan_ids"]
    total_loans = len(generic_data)

    return {
        "company_id": kwargs["company_id"],
        "author": kwargs["author"],
        "token": kwargs["token"],
        "queue": kwargs["queue"],
        "batch_id": kwargs["batch_id"],
        "batch_number": "1",
        "total_batches": 1,
        "type_of_task": type_of_task,
        "total_loans": total_loans,
        "data": data,
        "loan_id": None,
    }


def extract_loan_ids_from_list(data):
    loan_id_list = []
    for loan in data:
        loan_id = loan.get("loan_id")
        if loan_id is not None:
            loan_id_list.append(loan_id)
    return loan_id_list


"""
Method to produce messages for each loan batch inside the litigation report
"""


@shared_task(bind=True, name="create_litigation_report_messages", ignore_result=False)
def create_litigation_report_messages(self, *args, **kwargs):
    logger.info("app.tasks.execution.create_litigation_report_messages")
    BATCH_SIZE = LITIGATION_REPORT_BATCH_SIZE
    queue = kwargs["queue"]
    start_time = time.time()
    data = kwargs["data"]
    company_id = kwargs["company_id"]
    batch_id = kwargs["batch_id"]
    report_name = kwargs["report_name"]
    redis_keys = LitigationReportRedisKeys(batch_id=batch_id)

    if report_name == "ageing":
        BATCH_SIZE = int(BATCH_SIZE / 2 + 1)

    logger.debug(
        f"app.tasks.execution.create_litigation_report_messages || company_id: {company_id}, batch_id: {batch_id}, report_name: {report_name}, request_id : {kwargs.get('request_id')}"
    )
    logger.debug(
        f"app.tasks.execution.create_litigation_report_messages || {batch_id}  || loan_ids length: {len(kwargs['data']['loan_ids'])}"
    )

    try:
        redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
        redis_instance.setex(redis_keys.task_state, 24 * 60 * 60, ReportStatus.IN_PROGRESS.value)

        loan_ids = data["loan_ids"]
        loan_ids_batches = [loan_ids[i : i + BATCH_SIZE] for i in range(0, len(loan_ids), BATCH_SIZE)]
        redis_instance.setex(redis_keys.batch_count, 24 * 60 * 60, len(loan_ids_batches))

        (
            workflow_map,
            is_require_advocate_data,
            advocate_user_map,
            headers,
            loan_level_headers,
            case_level_headers,
            stage_level_headers,
            reminder_level_headers,
            advocate_level_headers,
        ) = _get_prerequisite(**kwargs)
        litigation_report_prerequisites = {
            "workflow_map": workflow_map,
            "is_require_advocate_data": is_require_advocate_data,
            "advocate_user_map": advocate_user_map,
            "headers": headers,
            "loan_level_headers": loan_level_headers,
            "case_level_headers": case_level_headers,
            "stage_level_headers": stage_level_headers,
            "reminder_level_headers": reminder_level_headers,
            "advocate_level_headers": advocate_level_headers,
            "user": kwargs["user"],
            "company": kwargs["company"],
            "proceeding": kwargs.get("proceeding"),
            "matter_type": kwargs["data"].get("case_type"),
            "report_name": kwargs["report_name"],
            "data": kwargs["data"],
            "author": kwargs["user"]["author"],
            "token": kwargs["user"]["authentication_token"],
            "role": kwargs["user"]["role"],
            "request_id": kwargs["request_id"],
        }
        redis_instance.setex(redis_keys.batch_kwargs, 24 * 60 * 60, json.dumps(litigation_report_prerequisites))

        response_data_on_completion = create_response_data_for_queue_litigation_report(**kwargs)
        litigation_report_callback_kwargs = {
            "response_data": response_data_on_completion,
            "company_id": company_id,
            "batch_id": batch_id,
            "report_name": report_name,
            "headers": headers,
            "report_start_time": start_time,
            "user": kwargs["user"],
            "company": kwargs["company"],
            "author": kwargs["user"]["author"],
            "token": kwargs["user"]["authentication_token"],
            "role": kwargs["user"]["role"],
            "request_id": kwargs["request_id"],
        }
        redis_instance.setex(redis_keys.callback_kwargs, 24 * 60 * 60, json.dumps(litigation_report_callback_kwargs))

    except Exception as e:
        logger.error(f"exception.app.tasks.create_litigation_report_messages || {batch_id} || {str(e)}")
        traceback.print_exc()
        _send_report_via_email(email_type="failure", report_access_url=None, **kwargs)
        if redis_instance:
            redis_instance.set(redis_keys.task_state, ReportStatus.COMPLETED.value)
        return False

    tasks = []
    for batch_number, loan_id_batch in enumerate(loan_ids_batches):
        task_kwargs = {
            "batch_id": batch_id,
            "batch_id_batch_number": batch_number,
            "loan_ids": loan_id_batch,
        }
        tasks.append(create_report_chunk.s(**task_kwargs))
    chord(
        group(tasks),
        body=report_callback.s(
            batch_id=batch_id,
        ),
    ).apply_async(queue=queue)
    logger.info(f"app.tasks.create_litigation_report_messages : tasks created || {batch_id}")
    return True


@shared_task(bind=True, name="create_report_chunk", ignore_result=False)
def create_report_chunk(self, *args, **kwargs):
    logger.info("app.tasks.execution.create_report_chunk")
    batch_id = kwargs["batch_id"]
    batch_id_batch_number = kwargs["batch_id_batch_number"]
    loan_ids_batch = kwargs["loan_ids"]
    redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])

    BATCH_SIZE = LITIGATION_REPORT_BATCH_SIZE
    start = time.time()
    batch_id_log = f"{batch_id} .{batch_id_batch_number}"
    logger.info(f"app.tasks.execution.create_report_chunk || {batch_id_log} || loan_ids : {loan_ids_batch}")

    redis_keys = LitigationReportRedisKeys(batch_id=batch_id)
    redis_keys.set_batch_number_key(batch_number=batch_id_batch_number)
    task_state = redis_instance.get(redis_keys.task_state).decode()
    kwargs = redis_instance.get(redis_keys.batch_kwargs)
    if task_state != ReportStatus.IN_PROGRESS.value or not kwargs:
        logger.info(
            f"app.tasks.execution.create_report_chunk :: halting report generation || {batch_id} .{batch_id_batch_number} ||  report_status: {task_state} "
        )
        return True

    try:
        kwargs = json.loads(kwargs)
        data = kwargs["data"]
        report_name = kwargs["report_name"]
        chunks = ChunkClass(LITIGATION_REPORT_DIRECTORY, batch_id, PICKLE_EXTENSTION)
        user_details = kwargs["user"]
        company_details = kwargs["company"]
        company_id = company_details["company_id"]
        is_require_advocate_data = kwargs["is_require_advocate_data"]
        case_level_headers = kwargs["case_level_headers"]
        reminder_level_headers = kwargs["reminder_level_headers"]
        advocate_level_headers = kwargs["advocate_level_headers"]
        stage_level_headers = kwargs["stage_level_headers"]
        advocate_user_map = kwargs["advocate_user_map"]
        workflow_map = kwargs["workflow_map"]
        proceeding = kwargs["proceeding"]
        matter_type = kwargs["matter_type"]
        headers = kwargs["headers"]

        loan_data = []
        case_data = []
        stage_data = []
        row_data_list = []
        case_map = {}
        loan_map = {}
        stage_map = {}
        reminder_map = {}

        # LOAN_DATA
        loan_data = get_loan_details_batch(
            loan_ids=loan_ids_batch,
            company_id=company_id,
            page_size=BATCH_SIZE,
            user=kwargs["user"],
            company=kwargs["company"],
            page_number=1,
        )

        if not loan_data:
            logger.info(f"app.tasks.execution.create_report_chunk || {batch_id_log} || no more loan_data")
            return True

        # no data cleaning in case of loan_variable, as we can have any nested variable present
        # loan_data = clean_dict_data_remove_keys(loan_data, loan_level_headers)
        loan_ids_batch = extract_loan_ids_from_list(loan_data)

        loan_list = copy.deepcopy(loan_data)
        loan_data = []
        logger.info(f"execution.create_report_chunk || flatten loan dict for a batch")
        for loan_detail in loan_list:
            defaults = loan_detail.pop("defaults")
            case_tracking_details = loan_detail.pop("case_tracking_details", None)
            loan_detail = {**loan_detail, **defaults[-1]}
            loan_data.append(flatten_dict_with_custom_path(None, loan_detail, ""))
        loan_map = get_loan_id_to_loan_map(loan_data)

        master_case_id_list = []
        master_case_row_ids = []
        master_reminder_left = []
        reminders_left = []
        # loan_id~case_id~current_stage_code~next_stage_code
        reminder_data_inserted_set = set()

        # CASE_DATA
        case_data = []
        case_page_number = 0
        while True:
            case_page_number = case_page_number + 1
            case_data = get_cases_data(
                loan_ids_batch,
                case_page_number,
                BATCH_SIZE,
                company_id,
                data,
                report_name,
                user_details,
                company_details,
            )
            if not case_data:
                break

            case_data = convert_multiple_loan_id_response(case_data)
            case_data = clean_dict_data_remove_keys(case_data, case_level_headers)
            case_id_list, case_map = get_case_map(case_data)

            # GET case_row_ids
            case_row_ids = []
            for loan_id_case_id_key, case in case_map.items():
                case_row_ids.append(case.get("id"))
            master_case_row_ids.extend(case_row_ids)
            master_case_id_list.extend(case_id_list)

            # GET REMINDERS
            if report_name in ("mis", "advocate_mis"):

                case_ids = COMMA.join(case_id_list)
                reminder_data = []
                reminder_map = {}
                reminder_page_number = 0
                not_in_case = False
                master_reminder_left = []
                while True:
                    reminder_page_number = reminder_page_number + 1
                    reminder_data = get_reminder_data(
                        loan_ids_batch,
                        case_ids,
                        BATCH_SIZE,
                        reminder_page_number,
                        data,
                        not_in_case,
                        company_id,
                        kwargs["user"],
                        company_details,
                    )
                    if not reminder_data:
                        break
                    elif reminder_data:
                        reminder_data = convert_multiple_loan_id_response(reminder_data)
                        reminder_data = clean_dict_data_remove_keys(reminder_data, reminder_level_headers)
                    master_reminder_left.extend(reminder_data)
                # remove data collission from reminders
                reminder_map = create_reminder_map(case_map=case_map, reminders_list=master_reminder_left, workflow_map=workflow_map)

            # AGENT_ALLOCATION DATA
            advocate_map = {}
            if is_require_advocate_data:
                present_in_approved_case = True
                advocate_map = get_agent_allocation_map(
                    loan_ids_batch,
                    case_id_list,
                    data,
                    company_id,
                    company_details,
                    user_details,
                    BATCH_SIZE,
                    report_name,
                    advocate_level_headers,
                    advocate_user_map,
                    present_in_approved_case,
                )

            # STAGE_DATA
            stage_data = []
            reminder_data = []
            stage_page_number = 0
            no_case_row_id_present = False
            stage_map = {}
            while True:
                stage_page_number = stage_page_number + 1
                stage_data = get_stage_data(
                    loan_ids_batch,
                    case_row_ids,
                    BATCH_SIZE,
                    stage_page_number,
                    data,
                    no_case_row_id_present,
                    company_id,
                    report_name,
                    kwargs["user"],
                    company_details,
                )

                if not stage_data:
                    break

                stage_data = convert_multiple_loan_id_response(stage_data)
                stage_data = clean_dict_data_remove_keys(stage_data, stage_level_headers)
                stage_map = get_stage_map(stage_data, stage_map=stage_map, report_name=report_name)
                reminder_data = []

                # GET REMINDERS
                if report_name == "ageing":
                    case_ids = COMMA.join(case_id_list)
                    reminder_data = []
                    reminder_page_number = 0
                    not_in_case = False
                    while True:
                        reminder_page_number = reminder_page_number + 1
                        reminder_data = get_reminder_data(
                            loan_ids_batch,
                            case_ids,
                            BATCH_SIZE,
                            reminder_page_number,
                            data,
                            not_in_case,
                            company_id,
                            kwargs["user"],
                            company_details,
                        )
                        if not reminder_data and not reminders_left:
                            break
                        elif reminder_data:
                            reminder_data = convert_multiple_loan_id_response(reminder_data)
                            reminder_data = clean_dict_data_remove_keys(reminder_data, reminder_level_headers)
                            master_reminder_left.extend(reminder_data)
                        stages_provided = True
                        row_data_list, reminders_left = create_row_data_list_for_ageing(
                            loan_map,
                            case_map,
                            stage_map,
                            master_reminder_left,
                            stages_provided,
                            reminder_data_inserted_set,
                        )
                        master_reminder_left = reminders_left
                        headers, row_data_list = calculate_width_of_elements(row_data_list, headers, workflow_map)
                        chunks.save_data(row_data_list)

                elif report_name not in ("mis", "advocate_mis"):
                    headers = create_sub_excel(
                        chunks,
                        loan_map,
                        case_map,
                        advocate_map,
                        stage_data,
                        stage_map,
                        reminder_map,
                        report_name,
                        proceeding,
                        workflow_map,
                        headers,
                        matter_type,
                        user=kwargs["user"],
                        company=kwargs["company"],
                    )

            if report_name in ("mis", "advocate_mis"):
                headers = create_sub_excel(
                    chunks,
                    loan_map,
                    case_map,
                    advocate_map,
                    stage_data,
                    stage_map,
                    reminder_map,
                    report_name,
                    proceeding,
                    workflow_map,
                    headers,
                    matter_type,
                    user=kwargs["user"],
                    company=kwargs["company"],
                )

        # LOAN -> REMINDER DATA [No Case, No Stage present]
        reminders_left = []
        master_reminder_left = []
        if report_name == "ageing":
            reminder_data = []
            reminder_page_number = 0
            master_case_id_list = COMMA.join(master_case_id_list)
            not_in_case = True
            while True:
                # GET ALL REMINDERS FOR STAGES? -> 5000
                reminder_page_number = reminder_page_number + 1
                reminder_data = get_reminder_data(
                    loan_ids_batch,
                    master_case_id_list,
                    BATCH_SIZE,
                    reminder_page_number,
                    data,
                    not_in_case,
                    company_id,
                    kwargs["user"],
                    company_details,
                )
                if not reminder_data and not reminders_left:
                    break
                elif reminder_data:
                    reminder_data = convert_multiple_loan_id_response(reminder_data)
                    reminder_data = clean_dict_data_remove_keys(reminder_data, reminder_level_headers)
                    master_reminder_left.extend(reminder_data)
                logger.info(f"tasks.execution.create_report_chunk || {batch_id} || special reminders exists")
                # DUMP DATA ==>
                stages_provided = False
                row_data_list, reminders_left = create_row_data_list_for_ageing(
                    loan_map, case_map, stage_map, master_reminder_left, stages_provided, reminder_data_inserted_set
                )
                headers, row_data_list = calculate_width_of_elements(row_data_list, headers, workflow_map)
                chunks.save_data(row_data_list)

        # LOAN -> STAGE DATA [No Case present]
        if report_name == "step_mis":
            stage_data = []
            reminder_data = []
            stage_page_number = 0
            no_case_row_id_present = True
            case_row_ids = None

            # GET AGENT ALLOCATION DATA
            advocate_map = {}
            if is_require_advocate_data:
                present_in_approved_case = False
                advocate_map = get_agent_allocation_map(
                    loan_ids_batch,
                    master_case_id_list,
                    data,
                    company_id,
                    company_details,
                    user_details,
                    BATCH_SIZE,
                    report_name,
                    advocate_level_headers,
                    advocate_user_map,
                    present_in_approved_case,
                )

            while True:
                stage_page_number = stage_page_number + 1
                not_in_case = True
                stage_data = get_stage_data(
                    loan_ids_batch,
                    case_row_ids,
                    BATCH_SIZE,
                    stage_page_number,
                    data,
                    no_case_row_id_present,
                    company_id,
                    report_name,
                    kwargs["user"],
                    company_details,
                )
                if not stage_data:
                    break

                reminder_map = {}
                stage_data = convert_multiple_loan_id_response(stage_data)
                stage_data = clean_dict_data_remove_keys(stage_data, stage_level_headers)
                stage_map = get_stage_map(stage_data)
                logger.info(f"tasks.execution.create_report_chunk || {batch_id} || special cases exists")
                row_data_list = create_row_data_list(
                    loan_map,
                    case_map,
                    advocate_map,
                    stage_data,
                    stage_map,
                    reminder_map,
                    report_name,
                    proceeding,
                    workflow_map,
                    matter_type,
                    kwargs["company"],
                )
                headers, row_data_list = calculate_width_of_elements(row_data_list, headers, workflow_map)
                chunks.save_data(row_data_list)

        # converting any sets to lists:
        for header_key, header_value in headers.items():
            if header_value.get("indexed_header_keys"):
                header_value["indexed_header_keys"] = list(header_value["indexed_header_keys"])
        redis_instance.setex(redis_keys.headers, 24 * 60 * 60, json.dumps(headers))
    except Exception as e:
        logger.error(f"app.tasks.create_report_chunk.exception || {batch_id} || {str(e)}")
        traceback.print_exc()
        if redis_instance:
            redis_instance.set(redis_keys.task_state, ReportStatus.LOAN_BATCH_FAILED.value)
        return False
    finally:
        redis_instance.decrby(redis_keys.batch_count, 1)

    logger.debug(
        f"\n app.tasks.execution.create_report_chunk_chunk || {batch_id_log} ||TIME FOR REPORT CHUNK - {batch_id_batch_number} GENERATION : {time.time() - start}"
    )

    # CALLBACK FUNCTION
    try:
        del loan_data
        del case_data
        del stage_data
        del case_map
        del loan_map
        del stage_map
        del row_data_list

    except Exception as e:
        logger.error(f"app.tasks.create_report_chunk.psudo_callback || {batch_id_log} || {str(e)}")
    return True


@shared_task(bind=True, name="report_callback", ignore_result=False)
def report_callback(self, *args, **kwargs):

    batch_id = kwargs["batch_id"]
    logger.info(f"app.tasks.execution.report_callback  || {batch_id} ")

    redis_keys = LitigationReportRedisKeys(batch_id=batch_id)
    redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
    task_state = redis_instance.get(redis_keys.task_state).decode()
    batch_failed = False
    if task_state == ReportStatus.LOAN_BATCH_FAILED.value:
        batch_failed = True
    logger.info(
        f"app.tasks.execution.report_callback :: generating report || {batch_id} || report_status: {task_state}"
    )

    task_state = redis_instance.set(redis_keys.task_state, ReportStatus.COMPLETED.value)
    kwargs = redis_instance.get(redis_keys.callback_kwargs)

    try:

        kwargs = json.loads(kwargs)
        headers = kwargs["headers"]
        company_id = kwargs["company_id"]
        batch_id = kwargs["batch_id"]
        report_name = kwargs["report_name"]
        chunks = ChunkClass(LITIGATION_REPORT_DIRECTORY, batch_id, PICKLE_EXTENSTION)
        chunks.create_file_list()
        response_data = kwargs["response_data"]
        report_start_time = kwargs["report_start_time"]
        start = time.time()

        if batch_failed:
            raise Exception("failure")

        headers = calculate_final_headers(headers, batch_id, redis_keys, redis_instance)

        headers, dynamic_array_variable_map = update_headers_before_report_generation(headers)
        report_name = generate_report(company_id, report_name, chunks, headers, dynamic_array_variable_map)

        # pass these to local paths
        local_directory_path = chunks.excel_file_path
        local_zip_file_path = os.path.join(chunks.zip_file_path, "excel_zips")

        logger.debug(f"app.tasks.execution.report_callback || {batch_id}  || generating zip")
        generate_zip(local_directory_path, local_zip_file_path)

        logger.debug(f"app.tasks.execution.report_callback || {batch_id}  || uploading zip on s3")
        bucket = S3_BUCKET_NAME
        s3_object_name = _get_upload_s3_object_name(company_id, batch_id)
        logger.info("got s3 object name")
        local_zip_file_path = f"{local_zip_file_path}.zip"
        upload_successful = upload_file_to_s3(bucket, local_zip_file_path, s3_object_name)
        logger.info(f"app.tasks.execution.report_callback || upload_successful: {upload_successful}")

        if not upload_successful:
            raise Exception

        zip_access_url = _get_zip_access_url(company_id, batch_id)
        logger.info(f"app.tasks.execution.report_callback || {batch_id} || zip_access_url: {zip_access_url}")

        logger.info(f"app.tasks.execution.report_callback  || {batch_id} || sending email")
        _send_report_via_email(email_type="data_exists", report_access_url=zip_access_url, **kwargs)

        status = "SUCCESS"
        response = {
            "response": "data_exists",
            "status_code": 200,
            "kwargs": response_data,
            "status": status,
            "request_id": str(kwargs["request_id"]),
        }

    except Exception as e:
        logger.error(f"app.tasks.execution.report_callback || {batch_id} || exception {str(e)}")
        if str(e) == "no_data":
            _send_report_via_email(email_type="no_data", report_access_url=None, **kwargs)
        else:
            _send_report_via_email(email_type="failure", report_access_url=None, **kwargs)

        status = "FAIL"

        response = {
            "response": str(e),
            "status_code": 400,
            "kwargs": response_data,
            "status": status,
            "request_id": str(kwargs["request_id"]),
        }

    logger.info(
        f"app.tasks.execution.report_callback || {batch_id} || TIME FOR WHOLE REPORT CALLBACK : {time.time() - start}"
    )
    logger.info(
        f"app.tasks.execution.report_callback || {batch_id}  || TIME FOR WHOLE REPORT GENERATION : {time.time() - report_start_time}"
    )

    url = f"{QUEUE_SERVICE_BASE_URL}/update/batch-execution-status"

    try:
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(response),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(kwargs["request_id"]),
                "X-CG-User": json.dumps(kwargs["user"]),
            },
        )
        logger.debug(
            f"app.tasks.report_callback.execution_response_update || {batch_id}  || status_code :: {res.status_code}"
        )
    except Exception as e:
        logger.error(f"app.tasks.report_callback.execution_response_update  || {batch_id} || exception :: {str(e)}")
        return False
    finally:
        logger.debug(f"app.tasks.report_callback  || {batch_id} ||  deleting files from location - {chunks.base_path}")
        shutil.rmtree(chunks.base_path)
    if res.status_code not in (200, 201):
        logger.error(f"app.tasks.report_callback.execution_response_update || {batch_id} || status :: str({res.text})")
        return False
    return True


def calculate_final_headers(original_headers, batch_id, redis_keys, redis_instance):
    logger.info(f"app.tasks.execution.calculate_final_headers || {batch_id}")
    try:
        header_key_list = redis_instance.keys(f"*{redis_keys.headers}*")
        for header_key in header_key_list:
            header_key = header_key.decode()
            headers = redis_instance.get(header_key).decode()
            headers = json.loads(headers)
            original_headers = get_final_headers(original_headers, headers)
        return original_headers
    except Exception as e:
        logger.error(f"exception.app.tasks.execution.calculate_final_headers || {batch_id} || {str(e)}")
        traceback.print_exc()
        traceback.print_stack()
        raise e


def get_final_headers(original_headers, new_headers):
    for header_key, original_header_value in original_headers.items():
        new_header_value = new_headers[header_key]

        original_header_value["max_width"] = max(original_header_value["max_width"], new_header_value["max_width"])

        if original_header_value.get("indexed_header_keys") or new_header_value.get("indexed_header_keys"):
            if isinstance(original_header_value.get("indexed_header_keys", None), list):
                new_header_indexed_keys = set(new_header_value.get("indexed_header_keys", set()))
                original_header_value["indexed_header_keys"].union(new_header_indexed_keys)
            elif isinstance(new_header_value.get("indexed_header_keys", None), list):
                original_header_value["indexed_header_keys"] = set(new_header_value["indexed_header_keys"])
        if original_header_value.get("array_length"):
            if new_header_value.get("array_length"):
                original_header_value["array_length"] = max(
                    original_header_value["array_length"], new_header_value["array_length"]
                )
        else:
            if new_header_value.get("array_length"):
                original_header_value["array_length"] = new_header_value["array_length"]

    return original_headers


def write_data(value, type_, title_headers, is_timestamp, worksheet, headers, row_index, key, level):
    if key in headers.keys() and headers[key]["level"] == level:
        if type_ != "<class 'list'>":
            if is_timestamp and value:
                value = value.split()[0]

            try:
                col_index = title_headers.index(key)
                worksheet.write(row_index + 1, col_index, str(value or ""))
            except Exception as e:
                logger.error(f"app.tasks.execution.write_data || str || err writing the value for title : {key} || {e}")

        else:
            for index, each_value in enumerate(value):
                if is_timestamp and each_value:
                    each_value = each_value.split()[0]
                header = f"{key}{LITIGATION_REPORT_DELIMITER}{index+1}"
                try:
                    col_index = title_headers.index(header)
                    worksheet.write(row_index + 1, col_index, str(each_value or ""))
                except Exception as e:
                    logger.error(
                        f"app.tasks.execution.write_data || list || err writing the value for title : {header} || {e}"
                    )


def generate_report(company_id, report_name, chunks, headers, dynamic_array_variable_map):
    logger.info("app.tasks.execution.generate_report")
    try:
        start = time.time()
        logger.info(f"execution.generate_excel")
        logger.debug(f"generate_excel - {company_id} - {report_name}")
        folder_path = chunks.excel_file_path
        file_name = f"{report_name}.xlsx"
        workbook = xlsxwriter.Workbook(f"{os.path.join(folder_path,file_name)}")

        worksheet = workbook.add_worksheet()

        # STORING "header":{max_width} in title_headers
        title_headers = {}
        for header in headers:
            if headers[header].get("is_array"):
                length = headers[header]["array_length"]

                if length == 0:
                    title_headers[header] = {"max_width": headers[header]["max_width"]}

                for i in range(length):
                    array_header = f"{header}{LITIGATION_REPORT_DELIMITER}{i+1}"
                    title_headers[array_header] = {"max_width": headers[header]["max_width"]}
            else:
                title_headers[header] = {"max_width": headers[header]["max_width"]}
        bold = workbook.add_format({"bold": True})

        # ADDING COLUMN WIDTH IN EXCEL FOR EACH COLUMN
        # SETTING DEFAULT WIDTH FOR HEADERS
        column_index = 0
        row_index = 0
        title_case_headers = []
        title_headers_list = []

        for title_header in title_headers:
            tokenised_title_header = title_header.split(LITIGATION_REPORT_DELIMITER)
            header = tokenised_title_header[0]
            # skip if already added
            if header in dynamic_array_variable_map.keys():

                if not dynamic_array_variable_map[header].get("added_in_report", False):
                    dynamic_array_variable_map[header]["added_in_report"] = True

                    for sorted_header in dynamic_array_variable_map[header]["indexed_header_keys"]:
                        title_headers_list.append(sorted_header)
                        title_case_headers.append(
                            sorted_header.title().replace("_", " ").replace(LITIGATION_REPORT_DELIMITER, " ")
                        )
                        worksheet.set_column(column_index, column_index, title_headers[title_header]["max_width"])
                        column_index += 1

            else:
                title_headers_list.append(title_header)
                title_case_headers.append(
                    title_header.title().replace("_", " ").replace(LITIGATION_REPORT_DELIMITER, " ")
                )
                worksheet.set_column(column_index, column_index, title_headers[title_header]["max_width"])
                column_index += 1

        # ADDING ROW HEADERS
        worksheet.write_row(0, 0, tuple(title_case_headers), bold)
        title_headers = title_headers_list

        # WRITE EXCEL
        logger.debug("tasks.execution.generate_report || write_excel_now")
        logger.debug(f"tasks.execution.generate_report || chunks count - {chunks.counter}")
        if chunks.counter == 0:
            raise Exception("no_data")

        row_index = 0
        while chunks.counter > 0:
            row_data_list = chunks.pop_data()
            if len(row_data_list) == 0 and row_index == 0:
                raise Exception("no_data")

            for row in row_data_list:
                for row_level, row_value in row.items():
                    for key, value in row_value.items():
                        is_timestamp = is_valid_date_format(str(value), "%Y-%m-%d %H:%M:%S.%f")
                        type_ = str(type(value))
                        write_data(
                            value, type_, title_headers, is_timestamp, worksheet, headers, row_index, key, "loan"
                        )
                        write_data(
                            value, type_, title_headers, is_timestamp, worksheet, headers, row_index, key, "case"
                        )
                        write_data(
                            value, type_, title_headers, is_timestamp, worksheet, headers, row_index, key, "stage"
                        )

                        if report_name in ("step_mis", "mis", "advocate_mis"):
                            write_data(
                                value,
                                type_,
                                title_headers,
                                is_timestamp,
                                worksheet,
                                headers,
                                row_index,
                                key,
                                "advocate",
                            )

                        if report_name in ("ageing", "mis", "advocate_mis"):
                            write_data(
                                value,
                                type_,
                                title_headers,
                                is_timestamp,
                                worksheet,
                                headers,
                                row_index,
                                key,
                                "reminder",
                            )
                row_index += 1

        ## REPLACE COLUMN NAMES
        logger.info("app.tasks.execution.replace_column_names")
        for header, value in headers.items():
            key = None

            if value["level"] == "case":
                if header == "e_court_status":
                    key = "court_status"

            elif value["level"] == "stage":
                if header == "stage_code":
                    key = "process_step"
                elif header == "deadline_date":
                    key = "tat"

            elif value["level"] == "reminder":
                if header == "deadline_date":
                    key = "tat"
                if header == "next_stage_code_list_comma_separated_":
                    key = "next_step_code"

            # common header change
            if header == "next_stage_code":
                key = "next_step"
            elif header == "created":
                key = "step_creation_date"
            elif header == "author":
                key = "created_by"

            elif report_name == "step_mis":
                if header == "updated":
                    key = "updated/approved_on_date"
                elif header == "editor":
                    key = "updated_by/approved_by"

            # replace key with the name =>
            if key:
                replaced_header = key.title().replace("_", " ")
                logger.debug(f"replacing value ==> header : {header} ==> replaced_header : {replaced_header}")
                col_index = title_headers.index(header)
                logger.debug(f"col_index => {col_index}")
                worksheet.write(0, col_index, replaced_header, bold)

        # CLOSE EXCEL
        workbook.close()
        del row_data_list
        del title_headers

        logger.debug(f"app.tasks.execution.generate_report || TIME FOR REPORT GENERATION : {time.time() - start}")
        return file_name
    except Exception as e:
        logger.error(f"app.tasks.execution.generate_report || exception :: {str(e)}")
        traceback.print_exc()
        raise e


def get_cases(**kwargs):
    logger.info(f"execution.get_cases")
    data = kwargs["data"]
    company_id = kwargs["company_id"]

    url = f"{LITIGATION_SERVICE_BASE_URL.rstrip('/')}/cases"

    payload = {
        "company_id": company_id,
        "loan_ids": data["loan_ids"],
        "case_type": data.get("case_type"),
        "page_size": kwargs.get("page_size", 5000),
        "page_number": kwargs.get("page_number", 1),
    }

    next_hearing_date_start = data.get("next_hearing_date_start")
    next_hearing_date_end = data.get("next_hearing_date_end")

    if next_hearing_date_start and next_hearing_date_end:
        payload["next_hearing_date_start"] = next_hearing_date_start
        payload["next_hearing_date_end"] = next_hearing_date_end

    if kwargs["report_name"] in ("step_mis", "mis", "advocate_mis") and data.get("proceeding"):
        payload["proceeding"] = data["proceeding"]

    try:
        logger.debug(f"get_cases.url: {url}")

        cases_res = requests.request(
            method="POST",
            url=url,
            json=payload,
            headers={
                "authenticationtoken": kwargs["token"],
                "X-CG-User": json.dumps(kwargs["user"]),
                "X-CG-Company": json.dumps(kwargs["company"]),
                "Content-Type": "application/json",
            },
        )
        logger.debug(f"get_cases.status_code :: {cases_res.status_code}")

        if cases_res.status_code == 200:
            cases_res = cases_res.json()
            return cases_res["data"]
        else:
            logger.error(f"queue-service.execution.get_cases response :: {cases_res.text}")

    except Exception as e:
        logger.error(f"queue-service.execution.get_cases exception :: {str(e)}")

    return False


def get_stage_map(stage_list, stage_map: dict = None, report_name: str = None):
    logger.info("app.tasks.execution.create_stage_map")

    if report_name not in ("mis", "advocate_mis"):
        stage_map = {}

    for stage in stage_list:
        loan_id = stage["loan_id"]
        case_id = stage["case_id"]
        stage_code = stage["stage_code"]
        key = loan_id + DELIMITER + case_id + DELIMITER + str(stage_code)

        if report_name == "mis" and stage_map.get(key):
            pass
        else:
            stage_map[key] = stage
    return stage_map


def calculate_days(to_, from_):
    return (to_ - datetime.strptime(from_, "%Y-%m-%d").date()).days


def create_row_data_list(
    loan_map,
    case_map,
    advocate_allocation_map,
    stage_list,
    stage_map,
    reminder_map,
    report_name,
    proceeding,
    workflow_map,
    matter_type,
    company,
):
    logger.info("app.tasks.execution.create_row_data_list")
    row_data_list = []

    if report_name == "step_mis":
        for stage in stage_list:

            loan_id = stage["loan_id"]
            case_id = stage["case_id"]

            loan = loan_map[loan_id]
            case = case_map.get(loan_id + DELIMITER + case_id, {})

            # custom variables || STAGE
            stage_data = json.loads(stage["data"] or "{}") or {}
            del stage["data"]
            stage = {**stage_data, **stage}

            # stage data clean up || CASE
            case = copy.deepcopy(case)
            case_nested_data = json.loads(case.get("data", "{}"))

            # stage -> case
            if stage.get("case_details_under_approval"):
                # adding custom variables || CASE
                case_details_under_approval = json.loads(stage["case_details_under_approval"] or "{}") or {}
                case_data_under_approval = case_details_under_approval.get("data") or {}
                case_nested_data = {**case_nested_data, **case_data_under_approval}
                del case_details_under_approval["data"]
                # adding fixed fields || CASE
                for key, value in case_details_under_approval.items():
                    if case_details_under_approval[key] is not None:
                        case[key] = value

            if proceeding and case.get("proceeding") != proceeding:
                continue

            advocate = {}
            if stage.get("stage_code"):
                advocate = advocate_allocation_map.get(
                    loan_id
                    + LITIGATION_REPORT_DELIMITER
                    + case_id
                    + LITIGATION_REPORT_DELIMITER
                    + str(stage["stage_code"])
                    + LITIGATION_REPORT_DELIMITER
                    + str(stage["iteration"]),
                    {},
                )
                advocate = flatten_dict_with_custom_path(None, advocate, "")

            row_data_list.append(
                {"loan": loan, "case": {**case_nested_data, **case}, "stage": stage, "advocate": advocate}
            )

    elif report_name in ("mis", "advocate_mis"):
        for loan_id_case_id, case in case_map.items():
            loan_id = case["loan_id"]
            last_completed_stage_code = case["last_completed_step"]
            stage_key = loan_id_case_id + LITIGATION_REPORT_DELIMITER + str(last_completed_stage_code)

            if not last_completed_stage_code:
                continue

            loan = loan_map.get(loan_id, None)
            case_nested_data = json.loads(case["data"] or "{}")
            last_completed_step = stage_map.get(stage_key)

            if not last_completed_step:
                continue

            last_completed_stage_data = json.loads(last_completed_step["data"] or "{}")
            case["case_documents_"] = (
                UI_SERVICE_BASE_URL.rstrip("/")
                + f"/app/process-tracking/{matter_type}?loan_id={loan_id}&cg_customer_id={loan.get('cg_customer_id','')}&case_id={case.get('case_id','')}&highlight={'document'}&company_id={company['company_id']}&trademark={company['trademark']}"
            )

            reminder = {}
            if report_name in ("mis", "advocate_mis"):
                reminder = reminder_map.get(loan_id_case_id, {})

            reminder = {}
            if report_name in ("mis", "advocate_mis"):
                reminder = reminder_map.get(loan_id_case_id, {})

            advocate = {}
            advocate = advocate_allocation_map.get(loan_id_case_id, {})
            advocate = flatten_dict_with_custom_path(None, advocate, "")

            row_data_list.append(
                {
                    "loan": loan,
                    "case": {**case_nested_data, **case},
                    "stage": {**last_completed_stage_data, **last_completed_step},
                    "reminder": reminder,
                    "advocate": advocate,
                }
            )

    elif report_name == "billing":
        for stage in stage_list:
            if workflow_map[str(stage["stage_code"])]["is_billing_stage"]:
                loan_id = stage["loan_id"]
                case_id = stage["case_id"]

                loan = loan_map.get(loan_id)
                case = case_map.get(loan_id + DELIMITER + case_id)

                # skip the stage, if the case is under approval
                if not loan or not case:
                    continue

                case_nested_data = json.loads(case["data"] or "{}") or {}
                stage_nested_data = json.loads(stage["data"] or "{}") or {}

                if stage["vendor_fees"] is None:
                    stage["vendor_fees"] = 0
                if stage["litigation_cost"] is None:
                    stage["litigation_cost"] = 0
                if stage["tax"] is None:
                    stage["tax"] = 0

                stage["total_cost"] = stage["vendor_fees"] + stage["litigation_cost"] + stage["tax"]
                stage["total_cost"] = format(stage["total_cost"], ".2f")

                row_data_list.append(
                    {
                        "loan": loan,
                        "case": {**case_nested_data, **case},
                        "stage": {**stage_nested_data, **stage},
                    }
                )

    logger.info("app.tasks.execution.create_row_data_list || got row_data_list")
    logger.info(f"app.tasks.execution.create_row_data_list || row_data_list length: {len(row_data_list)}")
    return row_data_list


def create_row_data_list_for_ageing(
    loan_map, case_map, stage_map, reminder_list, stages_provided_for_reminders, reminder_data_inserted_set
):
    logger.info("tasks.execution.create_row_data_list_for_ageing")
    reminders_left = []
    row_data_list = []
    case_keys = list(case_map.keys())
    today = datetime.now().date()

    for reminder in reminder_list:
        loan_id = reminder["loan_id"]
        case_id = reminder["case_id"]
        current_stage_code = reminder.get("current_stage_code")
        next_stage_code = reminder.get("next_stage_code")
        unique_loan_case = loan_id + DELIMITER + case_id
        unique_loan_case_stage = (
            loan_id + DELIMITER + case_id + DELIMITER + str(current_stage_code) + DELIMITER + str(next_stage_code)
        )

        # help in saving duplicacy
        if not (unique_loan_case in case_keys or (case_id == "1")):
            logger.debug(
                f"tasks.execution.create_row_list_for_ageing || discarding reminder in reminders_list array : {unique_loan_case}"
            )
            continue
        elif unique_loan_case_stage in reminder_data_inserted_set:
            continue
        else:
            reminder_data_inserted_set.add(unique_loan_case_stage)

        loan = loan_map.get(loan_id)
        case = {}
        stage = {}

        # if case & stage exists for the reminder =>
        case_map_key = loan_id + DELIMITER + case_id
        case = case_map.get(case_map_key, {})
        if case:
            stage_code = reminder.get("current_stage_code")
            stage_map_key = loan_id + DELIMITER + case_id + DELIMITER + str(stage_code)
            stage = stage_map.get(stage_map_key)

            if stage is None and stages_provided_for_reminders:
                logger.debug(
                    f"tasks.execution.create_row_list_for_ageing || adding element in reminders_list array : loan_id : {loan_id} ; case_id : {case_id} ; stage_code : {stage_code}"
                )
                # handling infinite loop when stage is not present because of batching or stage does not exists in the stages table
                if reminder.get("iteration_count") is None:
                    reminder["iteration_count"] = 1
                elif reminder["iteration_count"] == MAX_LIMIT_OF_ITERATION_REMINDERS:
                    continue
                else:
                    reminder["iteration_count"] += 1
                reminders_left.append(reminder)
                continue

            case_nested_data = json.loads(case.get("data", "{}"))
            case = {**case_nested_data, **case}

            stage_nested_data = json.loads(stage.get("data", "{}"))
            stage = {**stage_nested_data, **stage}

        # calculate days
        if reminder["reminder_start_date"]:
            reminder["pending_for"] = calculate_days(today, reminder["reminder_start_date"])

        if reminder["deadline_date"]:
            days_since_tat_breached = calculate_days(today, reminder["deadline_date"])
            if days_since_tat_breached > 0:
                reminder["tat_breached"] = "Yes"
                reminder["days_since_tat_breached"] = days_since_tat_breached
            else:
                reminder["tat_breached"] = "No"
        else:
            reminder["tat_breached"] = "No"

        if loan["date_of_default"]:
            reminder["dpd"] = calculate_days(today, loan["date_of_default"])

        row_data_list.append({"loan": loan, "case": case, "stage": stage, "reminder": reminder})

    return row_data_list, reminders_left


def create_case_order_entry(**kwargs):
    logger.info("execution.entry into case_orders")
    payload = kwargs["payload"]
    message = kwargs["message"]

    post_data = {
        "company_id": message.get("company_id"),
        "case_id": message.get("case_id"),
        "case_type": message.get("case_type"),
        "document_type": message.get("document_type"),
        "document_link": message.get("document_link"),
        "order_date": message.get("order_date"),
    }

    base_url = LITIGATION_SERVICE_BASE_URL.rstrip("/")
    url = f"{base_url}/create_case_order"

    try:
        logger.info(f"create_case_order_entry.url :: {url}")
        headers = {
            "role": payload.get("role"),
            "X-Request-ID": str(payload.get("request_id")),
            "X-CG-User": json.dumps(payload.get("user")),
            "X-CG-Company": json.dumps(payload.get("company")),
        }

        result = requests.request(method="POST", url=url, headers=headers, json=post_data)

        response = result.json()
        logger.debug("response: %s", response)

        if result.status_code == 201:
            logger.info(f"created case_order entry")
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"create_case_order_entry.error :: {str(e)}")
        return False


def create_sub_excel(
    chunks,
    loan_map,
    case_map,
    advocate_map,
    stage_data,
    stage_map,
    reminder_map,
    report_name,
    proceeding,
    workflow_map,
    headers,
    matter_type,
    user,
    company,
):
    row_data_list = create_row_data_list(
        loan_map,
        case_map,
        advocate_map,
        stage_data,
        stage_map,
        reminder_map,
        report_name,
        proceeding,
        workflow_map,
        matter_type,
        company,
    )
    headers, row_data_list = calculate_width_of_elements(row_data_list, headers, workflow_map)
    chunks.save_data(row_data_list)
    return headers


def create_reminder_map(case_map, reminders_list, workflow_map):
    try:
        logger.info("execution.create_reminder_map")
        reminder_map = {}
        loan_id_case_id_list = list(case_map.keys())

        for reminder in reminders_list:
            reminder_loan_id_case_id = reminder["loan_id"] + LITIGATION_REPORT_DELIMITER + reminder["case_id"]
            if reminder_loan_id_case_id in loan_id_case_id_list:
                if reminder_map.get(reminder_loan_id_case_id):
                    reminder_map[reminder_loan_id_case_id].add(reminder["next_stage_code"])
                else:
                    next_stage_code_set = {reminder["next_stage_code"]}
                    reminder_map[reminder_loan_id_case_id] = next_stage_code_set

        for loan_id_case_id, next_stage_code_set in reminder_map.items():
            comma_separated_stage_codes = ""
            for stage_code in next_stage_code_set:
                comma_separated_stage_codes += str(stage_code) + " - " + workflow_map[str(stage_code)]["stage_name"] + " ,"

            reminder = {"next_stage_code_list_comma_separated_": comma_separated_stage_codes.rstrip(",")}
            reminder_map[loan_id_case_id] = reminder

        return reminder_map
    except Exception as e:
        logger.error(f"exception || execution.create_reminder_map : {str(e)}")
        traceback.print_exc()
        raise e


def get_agent_allocation_map(
    loan_ids_batch,
    case_id_list,
    data,
    company_id,
    company_details,
    user_details,
    BATCH_SIZE,
    report_name,
    advocate_level_headers,
    advocate_user_map,
    present_in_approved_case,
):
    advocate_map = {}
    advocate_data = []
    advocate_page_number = 0
    while True:
        advocate_page_number += 1
        advocate_data = get_agent_allocation_data(
            loan_ids_batch=loan_ids_batch,
            case_id_batch=case_id_list,
            data=data,
            company_id=company_id,
            company_details=company_details,
            user_details=user_details,
            page_number=advocate_page_number,
            page_size=BATCH_SIZE,
            report_type=report_name,
            present_in_approved_case=present_in_approved_case,
        )
        if not advocate_data:
            break

        advocate_data = convert_multiple_loan_id_response(advocate_data)
        advocate_data = clean_dict_data_remove_keys(advocate_data, advocate_level_headers)
        advocate_map = get_advocate_allocation_map(advocate_data, advocate_user_map, advocate_map, report_name)
    return advocate_map


def convert_multiple_loan_id_response(
    response
):
    logger.info("tasks.execution.convert_multiple_loan_id_response")

    required_response = []
    for data in response:
        current_modified_response_list = []
        if data.get("loan_ids"):
            for loan_id in data["loan_ids"]:
                modified_data_entry = copy.deepcopy(data)
                del modified_data_entry["loan_ids"]

                modified_data_entry["loan_id"] = loan_id
                current_modified_response_list.append(modified_data_entry)

            required_response.extend(current_modified_response_list)
        else:
            required_response.append(data)

    return required_response