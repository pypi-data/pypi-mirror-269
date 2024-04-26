"""
callback.py
Usage: All callback tasks
"""
import json
import requests
import os

from app.utils import generate_billing_report

# from app.tasks.notice.notice_callback.commons import delete_redis_keys
from ..settings import QUEUE_SERVICE_BASE_URL
import logging
from celery import shared_task
from .report import (
    calculate_report_data,
    campaign_result,
    batch_result,
)
from .execution import (
    delete_local_directory,
    bulk_allocation_email,
    bulk_approval_email,
    update_approval_requests_status,
    bulk_action_email_to_requester,
)
from ..choices import TypeOfTaskChoices, QueueTypeChoices
from ..settings import QUEUE_SERVICE_BASE_URL, VOLUME_MOUNT_DIRECTORY

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task(bind=True, name="batch_callback")
def batch_callback(self, *args, **kwargs):
    payload = kwargs["payload"]
    queue = kwargs["queue"]
    batch_number = payload["batch_number"]
    batch_id = payload["batch_id"]
    type_of_task = payload["type_of_task"]

    batch_status = {}
    success = []
    failed = []

    if type_of_task == TypeOfTaskChoices.notifications.value:
        return True

    execution_data_url = f"{QUEUE_SERVICE_BASE_URL}/execution_data?batch_number={batch_number}&batch_id={batch_id}"
    try:
        execution_data = requests.request(
            method="GET",
            url=execution_data_url,
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
        )

        logger.info(f"execution_data.status_code_{batch_id} :: {execution_data.status_code}")

    except Exception as e:
        logger.info(f"execution_data.exception_{batch_id} :: {str(e)}")
        self.retry(queue=queue, kwargs=kwargs, countdown=20, max_retries=5)

    if execution_data.status_code not in (200, 201):
        logger.info(f"execution_data.text_{batch_id} :: {execution_data.text}")
        self.retry(queue=queue, kwargs=kwargs, countdown=20, max_retries=5)

    execution_data = execution_data.json()
    for data in execution_data["data"]:
        print(f"batch_callback - execution_data - {data} - {type_of_task}")
        response = json.loads(data["response"])
        status_code = response["status_code"]
        loan_id = data["loan_id"]
        total_batches = data["total_batches"]
        status = data["status"]

        if status_code in (200, 201) and status != "FAIL":
            success.append(loan_id)
        else:
            if type_of_task == TypeOfTaskChoices.scrape_indiapost.value:
                failed.append(
                    {
                        "reason": str(response["response"]),
                        "loan_id": loan_id,
                        "company_id": data["company_id"],
                        "tracking_id": response["tracking_id"],
                        "status_code": status_code,
                    }
                )
            else:
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
            headers={
                "Content-Type": "application/json",
                "X-CG-User": json.dumps(payload["user"]),
                "X-Request-ID": payload["request_id"],
            },
            json={
                "batch_id": batch_id,
                "batch_number": batch_number,
                "batch_status": batch_status,
                "total_batches": total_batches,
            },
        )

        logger.info(f"batch_status_update.status_code_{batch_id} :: {batch_data.status_code}")

    except Exception as e:
        logger.info(f"batch_status_update.exception{batch_id} :: {str(e)}")
        self.retry(queue=queue, kwargs=kwargs, countdown=20, max_retries=5)
    if type_of_task != TypeOfTaskChoices.upload_c2c_disposition.value:
        calculate_report_data.apply_async(queue=queue, kwargs=payload)
    return True


@shared_task(bind=True, name="callback")
def callback(self, *args, **kwargs):
    """
    Redirects to separate queue for generating report
    """
    logger.info(f"app.tasks.callback.callback")

    payload = kwargs["payload"]
    type = payload.get("type", "")
    channel = payload.get("channel", "")

    if type == TypeOfTaskChoices.ecourt_tracking.value and channel == TypeOfTaskChoices.fetch_ecourt_case_orders.value:
        volume_mount_directory = VOLUME_MOUNT_DIRECTORY
        local_batch_directory_path = os.path.join(volume_mount_directory, "litigation_orders", payload.get("batch_id"))
        if os.path.exists(local_batch_directory_path):
            delete_local_directory(local_batch_directory_path)
            logger.debug(f"{local_batch_directory_path} deleted")
            return True

    if type == TypeOfTaskChoices.upload_c2c_disposition.value or type == TypeOfTaskChoices.ecourt_tracking.value:
        return True

    # campaign_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        if type == "communication":
            kwargs["updated_end_time_flag"] = True
            logger.info(f"callback.campaign_id {payload['campaign_id']}")

            campaign_result.apply_async(
                kwargs=kwargs,
                queue=f"{self.app.conf.QUEUE_NAME}_{QueueTypeChoices.result.value}",
            )
        else:
            logger.info(f"callback.batch_id {payload.get('batch_id')}")
            if kwargs["payload"].get("should_send_email", True):
                batch_result.apply_async(
                    kwargs=kwargs,
                    queue=f"{self.app.conf.QUEUE_NAME}_{QueueTypeChoices.result.value}",
                )
        if type == TypeOfTaskChoices.litigation_approval_request.value:
            payload["token"] = payload.get("user").get("authentication_token")

            bulk_approval_email.apply_async(kwargs=payload, queue=payload["queue"])
            data = json.loads(payload["data"])

            generate_billing_report(payload["user"], payload["company"], payload["batch_id"], data["case_type"])

            payload["bulk_approval_request"] = True
            bulk_allocation_email.apply_async(kwargs=payload, queue=payload["queue"])

            bulk_action_email_to_requester.apply_async(kwargs=payload, queue=payload["queue"])

            body = {
                "company_id": payload["company_id"],
                "updation_batch_id": payload["batch_id"],
                "approval_processing": False,
            }
            update_approval_requests_status(body, **payload)

    except Exception as e:
        logger.error(f"callback.exception :: {str(e)}")
        return False
    return True
