import json

from ..settings import USER_SERVICE_BASE_URL, API_USER_AUTHENTICATION_TOKEN
from ..choices import API_USER_DETAILS
import traceback
import requests as r

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_users(company):
    logger.info(f"user_service.get_users")
    user = API_USER_DETAILS
    user["authentication_token"] = API_USER_AUTHENTICATION_TOKEN
    url = USER_SERVICE_BASE_URL.rstrip("/") + "/internal/company/users"
    headers = {
        "authenticationtoken": user.get("authentication_token"),
        "role": user["role"],
        "Content-Type": "application/json",
        "X-CG-User": json.dumps(user),
        "X-CG-Company": json.dumps(company),
    }

    req_payload = {
        "company_id": company["company_id"],
    }

    logger.info(f"user_service.get_users.url: {url}")
    logger.debug(f"user_service.get_users.req_payload: {req_payload}")

    try:
        response = r.request("POST", url=url, json=req_payload, headers=headers, timeout=300)
        logger.debug(f"user_service.get_users.req_status : {response.status_code}")
        if response.status_code != 200:
            logger.error(f"exception.user_service.get_users.req_err : {response.text}")
            raise Exception(response.text)
        data = response.json()
        data = data["data"]
        if data["users"]:
            return data["users"]
        else:
            raise Exception("no_user_data_found")
    except Exception as e:
        error_msg = f"exception.user_service.get_users : {e}"
        logger.error(
            error_msg,
            "".join(traceback.format_tb(e.__traceback__)),
        )
        raise Exception(error_msg)
