"""
tasks.py
Usage: Contains all generic tasks
"""

import json
import requests
import logging
import uuid
from datetime import datetime

from celery import shared_task
from celery.result import AsyncResult
from celery import group, chord

# from app.tasks.notice.digital_notice import handle_generate_digital_notice
# from app.tasks.notice.physical_notice import generate_physical_notices

# from ..tasks.notice.notice_callback.physical_notice import (
#     generate_physical_notices_batch_callback,
# )

# TODO import this from celery_app
from ..settings import (
    DTMF_CHUNK_SIZE,
    QUEUE_SERVICE_BASE_URL,
)

from .execution import (
    communication,
    address_conversion,
    upload_data,
    upload_disposition,
    whatsapp_optin,
    whatsapp_optin,
    indiapost_upload,
    indiapost_tracking,
    lat_long_conversion,
    upload_c2c_disposition,
    communication_dtmf_ivr,
    add_ecourt_case,
    update_ecourt_case,
    fetch_ecourt_case_orders,
    update_approval_request,
    create_litigation_report_messages,
)
from .delegator import delegator

from .callback import batch_callback, callback
from ..utils import _make_batch, _dict_key_filter, list_chunker
from ..choices import TypeOfTaskChoices, CHANNELS, RequestTypeChoices


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task(name="testing", bind=True)
def testing(uuid):
    """
    Task testing
    """
    result = AsyncResult(uuid)
    logger.info(f"Validate email address: {uuid}")

    exc = result.get(propagate=False)
    print("Task {0} raised exception: {1!r}\n{2!r}".format(uuid, exc, result.traceback))


@shared_task(bind=True, name="task_test")
def task_test(_):
    """
    Task testing
    """
    logger.info(f"This is task testing from queue")
    return True


@shared_task(bind=True, name="new_task_test")
def new_task_test(_):
    """
    Task testing
    """
    print("This is new task testing from queue")
    return True


@shared_task(bind=True, name="error_handler")
def error_handler(uuid):
    """
    Error handle task
    """
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print("Task {0} raised exception: {1!r}\n{2!r}".format(uuid, exc, result.traceback))
    return True


@shared_task(bind=True, name="assign_optin_batch_queue")
def assign_optin_batch_queue(self, *args, **kwargs):
    batch_list = []
    batch_id = kwargs["batch_id"]
    user = kwargs.get("user")
    request_id = kwargs.get("request_id")
    queue = kwargs["queue"]
    data = kwargs["data"]
    loan_ids = data["loan_ids"]
    payload = _dict_key_filter(data, ["loan_ids"])
    company_id = data["company_id"]
    author = kwargs["author"]
    logger.info(f"payload :: {payload}")
    # type_of_task = queue.split('_')[1]
    if data.get("type_of_comm", "") == "dtmf_ivr":
        type_of_task = "dtmf_ivr"
    else:
        type_of_task = queue.split("_", 1)[1]

    total_loans = len(loan_ids)

    for batch in _make_batch(loan_ids, 2000):
        batch_list.append(batch)

    for index, loan_batch in enumerate(batch_list, 1):
        url = f"{QUEUE_SERVICE_BASE_URL}/initialize_monitor"
        try:
            res = requests.request(
                method="POST",
                url=url,
                data=json.dumps(
                    {
                        "batch_id": batch_id,
                        "batch_number": str(index),
                        "total_batches": len(batch_list),
                        "type_of_task": type_of_task,
                        "author": author,
                        "company_id": company_id,
                        "total_loans": total_loans,
                        "extras": {
                            "loan_ids": loan_batch,
                            "queue": queue,
                            "payload": payload,
                            "user": user,
                            "request_id": request_id,
                            "triggered_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        },
                    }
                ),
                headers={
                    "Content-Type": "application/json",
                    "X-CG-User": json.dumps(user),
                    "X-Request-ID": request_id,
                },
            )
            logger.info(f"initialize_monitor.status_code :: {res.status_code}")
        except Exception as e:
            logger.info(f"initialize_monitor.exception :: {str(e)}")
            return False

        if res.status_code not in (200, 201):
            logger.info(f"initialize_monitor.text :: {res.text}")
            return False
    delegator.apply_async(queue=queue, kwargs=kwargs)
    return True


@shared_task(bind=True, name="delegate")
def delegate(self, *args, **kwargs):
    """
    Delegates bulk operations to queue
    Delegates the signature tasks to queue using chord workflow
    """
    logger.info(f"app.tasks.tasks.delegate")
    logger.debug(f"delegate.kwargs: {kwargs}")
    tasks = []
    queue = kwargs["queue"]
    batch_id = kwargs["batch_id"]
    type = kwargs["type"]
    channel = kwargs["channel"]
    logger.info(f"delegate.batch_id {batch_id}")

    generic_data = json.loads(kwargs["loan_data"])
    next_approver_email = generic_data[0].get("next_approver_email") if isinstance(generic_data[0], dict) else ""
    payload = _dict_key_filter(kwargs, ["loan_data"])
    callback_payload = dict(payload)
    callback_payload["next_approver_email"] = next_approver_email

    for message in generic_data:
        task_kwargs = {
            "payload": payload,
            "message": message,
        }

        if type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_tracking.value:
            tasks.append(indiapost_tracking.s(**task_kwargs))
        elif type == TypeOfTaskChoices.lat_long_conversion.value:
            tasks.append(lat_long_conversion.s(**task_kwargs))
        elif type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_upload.value:
            tasks.append(indiapost_upload.s(**task_kwargs))
        elif type == TypeOfTaskChoices.upload_c2c_disposition.value:
            tasks.append(upload_c2c_disposition.s(**task_kwargs))
        elif type == TypeOfTaskChoices.optin.value:
            tasks.append(whatsapp_optin.s(**task_kwargs))
        elif type == TypeOfTaskChoices.ecourt_tracking.value and channel == TypeOfTaskChoices.add_ecourt_case.value:
            tasks.append(add_ecourt_case.s(**task_kwargs))
        elif type == TypeOfTaskChoices.ecourt_tracking.value and channel == TypeOfTaskChoices.update_ecourt_case.value:
            tasks.append(update_ecourt_case.s(**task_kwargs))
        elif (
            type == TypeOfTaskChoices.ecourt_tracking.value
            and channel == TypeOfTaskChoices.fetch_ecourt_case_orders.value
        ):
            tasks.append(fetch_ecourt_case_orders.s(**task_kwargs))
        elif type == TypeOfTaskChoices.litigation_approval_request.value:
            tasks.append(update_approval_request.s(**task_kwargs))

    data = json.loads(callback_payload["data"])
    data = _dict_key_filter(
        data,
        [
            "allocation_month",
            "creditline",
            "delivery_partner",
            "all_applicants",
            "co_applicant",
            "applicant_type",
            "notice_type",
            "source",
            "notify_type",
            "reminder_offset",
            "reminder_offset_type",
            "trigger_time",
        ],
    )
    callback_payload["data"] = json.dumps(data)

    logger.info("delegate.assign.chord: %s", batch_id)
    logger.debug(f"delegate.callback_data: {callback_payload}")

    chord(group(tasks), body=callback.s(queue=queue, payload=callback_payload)).apply_async(queue=queue)
    logger.info("delegate.assigned.chord: %s", batch_id)
    return True


@shared_task(bind=True, name="assign_generic_batch_queue")
def assign_generic_batch_queue(self, *args, **kwargs):
    """
    Assign generic batch to queue
    """
    batch_id = kwargs["batch_id"]
    queue = kwargs["queue"]
    type_of_task = kwargs["type_of_task"]
    if type_of_task == TypeOfTaskChoices.speedpost_upload.value:
        generic_data = kwargs["data"]["loan_data"]
        comm_data = _dict_key_filter(kwargs["data"], ["loan_data"])
        payload = _dict_key_filter(kwargs, ["data"])
        payload = {**payload, **comm_data}
    else:
        generic_data = kwargs["data"]
        payload = _dict_key_filter(kwargs, ["data"])
    total_loans = len(generic_data)
    url = f"{QUEUE_SERVICE_BASE_URL}/initialize_monitor"
    try:
        res = requests.request(
            method="POST",
            url=url,
            data=json.dumps(
                {
                    "batch_id": batch_id,
                    "type_of_task": type_of_task,
                    "batch_number": "1",
                    "total_batches": 1,
                    "author": payload["author"],
                    "company_id": payload["company_id"],
                    "total_loans": total_loans,
                    "extras": {
                        "loan_ids": generic_data,
                        "queue": queue,
                        "payload": payload,
                        "triggered_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    },
                }
            ),
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )
        logger.info(f"initialize_monitor.assign_generic_batch_queue.status_code :: {res.status_code}")
    except Exception as e:
        logger.info(f"initialize_monitor.assign_generic_batch_queue.exception :: {str(e)}")
        return False

    if res.status_code not in (200, 201):
        logger.info(f"initialize_monitor.assign_generic_batch_queue.text :: {res.text}")
        return False

    payload["batch_number"] = "1"
    payload["total_batches"] = 1
    payload["total_loans"] = total_loans
    payload["triggered_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if type_of_task == TypeOfTaskChoices.address_conversion_lat_long.value:
        address_conversion_tasks = []
        for index, message in enumerate(generic_data):
            logger.info("assign_generic_batch_queue.index: %s", index)
            task_kwargs = {
                "payload": payload,
                "message": message,
            }
            address_conversion_tasks.append(address_conversion.s(**task_kwargs))

        chord(
            group(address_conversion_tasks),
            body=batch_callback.s(queue=queue, payload=payload),
        ).apply_async(queue=queue)
    elif type_of_task == TypeOfTaskChoices.speedpost_upload.value:
        upload_data_tasks = []
        for index, message in enumerate(generic_data):
            logger.info("assign_generic_batch_queue.index: %s", index)
            task_kwargs = {
                "payload": payload,
                "message": message,
            }
            upload_data_tasks.append(upload_data.s(**task_kwargs))

        chord(
            group(upload_data_tasks),
            body=batch_callback.s(queue=queue, payload=payload),
        ).apply_async(queue=queue)
    elif type_of_task == TypeOfTaskChoices.upload_c2c_disposition.value:
        upload_c2c_disposition = []
        for index, message in enumerate(generic_data):
            logger.info("assign_generic_batch_queue.index: %s", index)
            task_kwargs = {
                "payload": payload,
                "message": message,
            }
            upload_c2c_disposition.append(upload_disposition.s(**task_kwargs))

        chord(
            group(upload_c2c_disposition),
            body=batch_callback.s(queue=queue, payload=payload),
        ).apply_async(queue=queue)

    return True


@shared_task(bind=True, name="assign_report_download_queue")
def assign_report_download_queue(self, *args, **kwargs):
    """
    Assign report download to queue
    """
    logger.info(f"app.tasks.tasks.assign_report_download_queue")
    queue = kwargs["queue"]
    type_of_task = "_".join(queue.split("_")[1:])
    data = kwargs["data"]
    generic_data = data["loan_ids"]
    total_loans = len(generic_data)

    try:
        url = f"{QUEUE_SERVICE_BASE_URL}/initialize_monitor"
        request_body = {
            "batch_id": kwargs["batch_id"],
            "batch_number": "1",
            "total_batches": 1,
            "type_of_task": type_of_task,
            "author": kwargs["author"],
            "company_id": kwargs["company_id"],
            "total_loans": total_loans,
            "extras": {
                "token": kwargs["token"],
                "role": kwargs["role"],
                "queue": queue,
                "batch": data,
                "triggered_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        }
        headers = {
            "Content-Type": "application/json",
            "X-Request-Id": str(kwargs["request_id"]),
            "X-CG-User": json.dumps(kwargs["user"]),
        }

        response = requests.request(
            method="POST",
            url=url,
            json=request_body,
            headers=headers,
        )

        logger.debug(f"initialize_monitor.status_code :: {response.status_code}")

    except Exception as e:
        logger.error(f"initialize_monitor.exception :: {str(e)}")
        return False

    if response.status_code not in (200, 201):
        logger.error(f"initialize_monitor.text :: {response.text}")
        return False

    task_kwargs = {
        "company_id": kwargs["company_id"],
        "author": kwargs["author"],
        "token": kwargs["token"],
        "role": kwargs["role"],
        "queue": queue,
        "batch_id": kwargs["batch_id"],
        "batch_number": "1",
        "total_batches": 1,
        "data": kwargs["data"],
        "report_name": kwargs["report_name"],
        "request_id": kwargs["request_id"],
        "user": kwargs["user"],
        "company": kwargs["company"],
    }

    create_litigation_report_messages.s(**task_kwargs).apply_async(queue=queue)
    return True


@shared_task(bind=True, name="delegate_campaign")
def delegate_campaign(self, *args, **kwargs):
    """
    Delegates campaigns to queue
    Delegates the signature tasks to queue using chord workflow
    Campaigns : Email, sms, voice, whatsapp, whatsapp_bot, dtmf_ivr
    """
    logger.info(f"app.tasks.tasks.delegate_campaign")
    logger.debug(f"delegate_campaign.kwargs: {kwargs}")
    tasks = []
    campaign_id = kwargs["campaign_id"]
    campaign_dict = {"campaign_id": campaign_id, "source": "queue"}
    generic_data = json.loads(kwargs["loan_data"])
    payload = _dict_key_filter(kwargs, ["loan_data", "additional_loan_data"])
    additional_loan_data = kwargs.get("additional_loan_data", {})
    task_kwargs = {"payload": payload}
    task_kwargs["queue"] = kwargs["queue"]
    channel = kwargs["channel"]
    try:
        if channel in CHANNELS:
            if channel == RequestTypeChoices.dtmf_ivr.value:
                for loan_ids in list_chunker(generic_data, DTMF_CHUNK_SIZE):
                    task_kwargs["loan_ids"] = loan_ids
                    additional_data = {
                        loan_id: {
                            **additional_loan_data.get(loan_id, {}),
                            **campaign_dict,
                        }
                        for loan_id in loan_ids
                    }
                    task_kwargs["additional_data"] = additional_data
                    tasks.append(communication_dtmf_ivr.s(**task_kwargs))
                logger.info(f"delegate_campaign.campaign_id.chord.assign.communication_dtmf_ivr: {campaign_id}")
            else:
                for loan_id in generic_data:
                    task_kwargs["loan_id"] = loan_id
                    task_kwargs["additional_loan_dict"] = additional_loan_data.get(loan_id, {})
                    tasks.append(communication.s(**task_kwargs))
                logger.info(f"delegate_campaign.campaign_id.chord.assign: {campaign_id}")
            logger.info(f"tasks.delegate_campaign.campaign_id.chord.assigned: {campaign_id}")
            chord_id = chord(group(tasks), body=callback.s(payload=payload)).apply_async(queue=kwargs["queue"])
    except Exception as e:
        logger.error(f"delegate_campaign.exception :: {str(e)}")
        return False
    return True
