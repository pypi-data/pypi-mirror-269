# import requests
# import json
# from urllib.error import URLError
# from app.settings import RECOVERY_SERVICE_BASE_URL
# import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# def get_loan_data(**kwargs):
#     logger.info(f"tasks.notice.helpers.get_loan_data")
#     logger.info(f"tasks.notice.helpers.get_loan_data.batch_id :: {kwargs['batch_id']}")

#     url = RECOVERY_SERVICE_BASE_URL.rstrip("/") + f"/notice/loan/details"

#     headers = {
#         "authenticationtoken": kwargs.get("user").get("authentication_token"),
#         "role": kwargs.get("user").get("role"),
#         "Content-Type": "application/json",
#         "X-CG-User": json.dumps(kwargs.get("user", {})),
#         "X-Request-Id": kwargs.get("X-Request-Id", ""),
#         "X-CG-Company": json.dumps(kwargs.get("company", {})),
#     }
#     req_payload = {
#         "loan_ids": kwargs.get("loan_ids", ""),
#         "allocation_month": kwargs.get("allocation_month", ""),
#         "creditline": kwargs.get("creditline", ""),
#         "company_id": kwargs.get("company_id", ""),
#     }

#     logger.debug(f"tasks.notice.helpers.get_loan_data.url: {url}")
#     logger.debug(f"tasks.notice.helpers.get_loan_data.req_payload: {req_payload}")

#     try:
#         response = requests.post(url=url, data=json.dumps(req_payload), headers=headers, timeout=60)
#         logger.debug(f"get_loan_data.response.status_code : {response.status_code}")
#     except URLError as url_error:
#         try:
#             ResponseData = url_error.read().decode("utf8", "ignore")
#             logger.debug(f"get_loan_data.URLError.ResponseData: {str(ResponseData)}")
#         except Exception as exc:
#             logger.error(f"get_loan_data.URLError.ResponseData.exception: {str(exc)}")
#         logger.error(f"get_loan_data.URLError: {str(url_error)}")
#         raise Exception(f"get_loan_data.URLError: {str(url_error)}")
#     except TimeoutError as te:
#         logger.error(f"get_loan_data.TimeoutError: {str(te)}")
#         raise Exception(f"get_loan_data.TimeoutError: {str(te)}")
#     except ConnectionError as ce:
#         logger.error(f"get_loan_data.ConnectionError: {str(ce)}")
#         raise Exception(f"get_loan_data.ConnectionError: {str(ce)}")
#     except Exception as e:
#         logger.error(f"error name: {e.__class__.__name__}")
#         logger.error(f"error args: {e.args}")
#         logger.error(f"error: {str(e)}")
#         raise Exception(f"get_loan_data.general_exception: {str(e)}")

#     if response.status_code != 200:
#         logger.debug(f"loan_service.get_loan_data.err_response : {response.text}")
#         raise Exception(f"get_loan_data.err_response: {response.text}")

#     loan_data = json.loads(response.text)
#     return loan_data.get("output", {})


# def get_borrower_language(question_dict):
#     applicant_language = question_dict.get("applicant_language")
#     co_applicants = question_dict.get("co_applicant", [])
#     co_applicant_language = ""
#     for co_applicant in co_applicants:
#         co_applicant_language = co_applicant.get("co_applicant_language")
#     return {
#         "applicant_language": applicant_language,
#         "co_applicant_language": co_applicant_language,
#     }
