"""
delegator.py
Usage: All delegator tasks
"""
import json
from datetime import datetime
from celery.canvas import chain
import requests
from ..settings import (
    LITIGATION_SERVICE_BASE_URL,
    SCRAPE_SERVICE_BASE_URL,
    NOTICE_SERVICE_BASE_URL,
    QUEUE_SERVICE_BASE_URL,
    COMMUNICATION_SERVICE_BASE_URL,
)
import logging
from celery import shared_task, group, chord
from .execution import optin, send_communications
from .report import calculate_report_data
from ..utils import _dict_key_filter

logger = logging.getLogger(__name__)


@shared_task(bind=True, name="chord_callback")
def chord_callback(self, *args, **kwargs):
    """
    Chord callback
    """
    print("Chord callback")
    return True


@shared_task(bind=True, name="execution_batch_number_callback")
def execution_batch_number_callback(self, *args, **kwargs):
    """
    Execution batch number callback
    """
    batch_number = kwargs["batch_number"]
    batch_id = kwargs["batch_id"]
    queue = kwargs["queue"]
    last_batch = kwargs["last_batch"]
    user = (kwargs["user"],)
    request_id = kwargs["request_id"]
    batch_status = {}
    success = []
    failed = []
    optin_partial_tasks = []
    total_batches = None
    execution_data_url = f"{QUEUE_SERVICE_BASE_URL}/execution_data?batch_number={batch_number}&batch_id={batch_id}"
    try:
        execution_data = requests.request(
            method="GET",
            url=execution_data_url,
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(user),
                "X-Request-ID": request_id,
            },
        )
        logger.info(
            f"execution_data.status_code_{batch_id} :: {execution_data.status_code}"
        )
    except Exception as e:
        logger.info(f"execution_data.exception_{batch_id} :: {str(e)}")
        self.retry(queue=queue, kwargs=kwargs, countdown=20, max_retries=5)

    if execution_data.status_code not in (200, 201):
        logger.info(f"execution_data.text_{batch_id} :: {execution_data.text}")
        self.retry(queue=queue, kwargs=kwargs, countdown=20, max_retries=5)

    execution_data = json.loads(execution_data.text)
    print(f"{execution_data} - execution_data")
    for data in execution_data["data"]:

        response = json.loads(data["response"])
        status_code = response["status_code"]
        loan_id = data["loan_id"]
        status = data["status"]
        total_batches = data["total_batches"]

        if status == "SUCCESS":
            success.append(loan_id)
        if status == "FAIL":
            failed.append(
                {
                    "reason": str(response["response"]),
                    "loan_id": loan_id,
                    "status_code": status_code,
                }
            )

    batch_status["failed"] = failed
    batch_status["success"] = success

    batch_status_update_url = f"{QUEUE_SERVICE_BASE_URL}/batch_status_update"

    try:
        batch_data = requests.request(
            method="POST",
            url=batch_status_update_url,
            data=json.dumps(
                {
                    "batch_id": batch_id,
                    "batch_number": batch_number,
                    "batch_status": batch_status,
                    "total_batches": total_batches,
                }
            ),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(user),
                "X-Request-ID": request_id,
            },
        )
        logger.info(
            f"batch_status_update.status_code_{batch_id} :: {batch_data.status_code}"
        )

    except Exception as e:
        logger.info(f"batch_status_update.exception{batch_id} :: {str(e)}")
        self.retry(queue=queue, kwargs=kwargs, countdown=20, max_retries=5)

    if batch_data.status_code not in (200, 201):
        logger.info(f"batch_status_update.text_{batch_id} :: {batch_data.text}")
        self.retry(queue=queue, kwargs=kwargs, countdown=20, max_retries=5)

    batch_data = json.loads(batch_data.text)
    data = batch_data["data"][0]
    extras = json.loads(data["extras"])
    batch_number = data["batch_number"]

    type_of_task = data["type_of_task"]
    total_batches = data["total_batches"]
    company_id = data["company_id"]
    author = data["author"]
    total_loans = data["total_loans"]

    loan_ids = extras["loan_ids"]
    queue = extras["queue"]
    user = extras["user"]
    request_id = extras["request_id"]
    payload = extras["payload"]
    template_id = payload.get("template_id", None)
    if type_of_task in ("dtmf_ivr"):
        template_name = payload.get("template_name", None)
        rule_id = payload.get("rule_id", None)
        rule_name = payload.get("rule_name", None)
        applied_filter = payload.get("applied_filter", None)
    else:
        template_name = payload.get("comm_dict", {}).get("template_name", None)
        rule_id = payload.get("comm_dict", {}).get("rule_id", None)
        rule_name = payload.get("comm_dict", {}).get("rule_name", None)
        applied_filter = payload.get("comm_dict", {}).get("applied_filter", None)
    if last_batch:
        calculate_report_data_kwargs = {
            "company_id": company_id,
            "queue": queue,
            "author": author,
            "batch_id": batch_id,
            "type_of_task": type_of_task,
            "total_loans": total_loans,
            "template_name": template_name,
            "template_id": template_id,
            "rule_id": rule_id,
            "rule_name": rule_name,
            "applied_filter": applied_filter,
            "user": user,
            "request_id": request_id,
        }
        calculate_report_data.apply_async(
            queue=queue, kwargs=calculate_report_data_kwargs
        )
        return True

    if str(batch_number) == str(total_batches):
        last_batch = True
    if loan_ids not in ([], None):
        for loan_id in loan_ids:
            if type_of_task in (
                "email",
                "sms",
                "voice",
                "whatsapp",
                "call",
                "dtmf_ivr",
            ):
                communication_kwargs = {
                    "loan_id": loan_id,
                    "company_id": company_id,
                    "queue": queue,
                    "author": author,
                    "batch_id": batch_id,
                    "batch_number": batch_number,
                    "total_batches": total_batches,
                    "type_of_task": type_of_task,
                    "total_loans": total_loans,
                    "comm_type": payload["type_of_comm"],
                    "payload": payload,
                    "user": user,
                    "request_id": request_id,
                }
                optin_partial_tasks.append(
                    send_communications.s(**communication_kwargs)
                )
            else:
                optin_kwargs = {
                    "loan_id": loan_id,
                    "company_id": company_id,
                    "queue": queue,
                    "author": author,
                    "batch_id": batch_id,
                    "batch_number": batch_number,
                    "total_batches": total_batches,
                    "type_of_task": type_of_task,
                    "total_loans": total_loans,
                    "user": user,
                    "request_id": request_id,
                }
                optin_partial_tasks.append(optin.s(**optin_kwargs))
        chord(
            group(optin_partial_tasks),
            body=execution_batch_number_callback.s(
                queue=queue,
                batch_id=batch_id,
                batch_number=batch_number,
                last_batch=last_batch,
                user=user,
                request_id=request_id,
            ),
        ).apply_async(queue=queue)
    return True


@shared_task(bind=True, name="delegator", ignore_result=False)
def delegator(self, *args, **kwargs):
    """
    Delegator
    """
    batch_id = kwargs["batch_id"]
    url = (
        f"{QUEUE_SERVICE_BASE_URL}/get_batch_number?batch_number=1&batch_id={batch_id}"
    )
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
        self.retry(kwargs=kwargs, countdown=20, max_retries=5)

    if batch_data.status_code not in (200, 201):
        logger.info(f"get_batch_number.text :: {batch_data.text}")
        self.retry(kwargs=kwargs, countdown=20, max_retries=5)

    batch_data = json.loads(batch_data.text)

    data = batch_data["data"][0]
    extras = json.loads(data["extras"])
    batch_number = data["batch_number"]
    type_of_task = data["type_of_task"]
    total_batches = data["total_batches"]
    company_id = data["company_id"]
    author = data["author"]
    total_loans = data["total_loans"]

    loan_ids = extras["loan_ids"]
    queue = extras["queue"]
    user = extras["user"]
    request_id = extras["request_id"]
    payload = extras["payload"]

    if loan_ids not in ([], None):
        optin_partial_tasks = []
        for loan_id in loan_ids:
            if type_of_task in (
                "email",
                "sms",
                "voice",
                "whatsapp",
                "call",
                "whatsapp_bot",
                "dtmf_ivr",
            ):
                communication_kwargs = {
                    "loan_id": loan_id,
                    "company_id": company_id,
                    "queue": queue,
                    "author": author,
                    "batch_id": batch_id,
                    "batch_number": batch_number,
                    "total_batches": total_batches,
                    "type_of_task": type_of_task,
                    "total_loans": total_loans,
                    "comm_type": payload["type_of_comm"],
                    "payload": payload,
                    "user": user,
                    "request_id": request_id,
                }
                optin_partial_tasks.append(
                    send_communications.s(**communication_kwargs)
                )
            else:
                optin_kwargs = {
                    "loan_id": loan_id,
                    "company_id": company_id,
                    "queue": queue,
                    "author": author,
                    "batch_id": batch_id,
                    "batch_number": batch_number,
                    "total_batches": total_batches,
                    "type_of_task": type_of_task,
                    "total_loans": total_loans,
                    "user": user,
                    "request_id": request_id,
                }
                optin_partial_tasks.append(optin.s(**optin_kwargs))
    chord(
        group(optin_partial_tasks),
        body=execution_batch_number_callback.s(
            queue=queue,
            batch_id=batch_id,
            batch_number=batch_number,
            last_batch=True if total_batches == 1 else False,
            user=user,
            request_id=request_id,
        ),
    ).apply_async(queue=queue)
    return True
