# import uuid
# from celery import shared_task

# from app.settings import (
#     NOTICE_SERVICE_BASE_URL,
#     RECOVERY_SERVICE_BASE_URL,
#     REDIS,
#     S3_BUCKET_ENDPOINT,
#     S3_BUCKET_NAME,
# )
# from app.tasks.notice.helpers import (
#     generate_notice_for_all_addresses,
#     logs_tracker,
#     map_formatter,
# )
# import logging
# import redis
# import json

# from app.tasks.notice.loan_service import get_loan_data
# from app.tasks.notice.notice_service import (
#     get_notice_generation_data,
#     insert_into_db,
#     upload_notices_to_s3,
# )

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# failed_notice_id_list = []


# @shared_task(bind=True, name="generate_physical_notices", ignore_result=False, acks_late=False)
# def generate_physical_notices(self, *args, **kwargs):
#     logger.info("notice.generate_physical_notices")
#     logs_loan_id = kwargs["linked_loan"]["linked_loan_id"] if kwargs.get("linked_loan") else kwargs.get("loan_ids")[0]
#     logger.info(f"notice.generate_physical_notices.loan_id :: {logs_loan_id}")
#     logger.info(f"notice.generate_physical_notices.batch_id :: {kwargs['batch_id']}")

#     try:
#         redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#         notice_kwargs = json.loads(redis_instance.get(f"notice_kwargs_{kwargs['batch_id']}").decode("utf-8"))
#         redis_instance.close()
#         # In case key is not present in redis
#         if not notice_kwargs:
#             logger.error("notice.generate_physical_notices.exception: notice_kwargs not found in redis")
#             raise Exception("notice.generate_physical_notices.exception: notice_kwargs not found in redis")

#         kwargs = {**kwargs, **notice_kwargs}
#         logger.debug(f"notice.generate_physical_notices.kwargs : {kwargs}")

#         local_batch_directory_path = kwargs["local_batch_directory_path"]
#         local_draft_file_path = kwargs["local_draft_file_path"]
#         local_doc_directory_path = kwargs["local_doc_directory_path"]
#         local_pdf_directory_path = kwargs["local_pdf_directory_path"]
#         local_qr_code_directory_path = kwargs["local_qr_code_directory_path"]
#         local_merged_pdf_directory_path = kwargs["local_merged_pdf_directory_path"]
#         local_merged_pdf_zip_file_path = kwargs["local_merged_pdf_zip_file_path"]
#         preview = kwargs.get("preview", False)
#         request_id = str(uuid.uuid4())

#         # For linked loans
#         if kwargs.get("linked_loan"):
#             linked_loan_dict = kwargs["linked_loan"]
#             linked_loan_id = linked_loan_dict.get("linked_loan_id", "")
#             loan_ids = linked_loan_dict.get("loan_ids", [])

#             if linked_loan_id in (None, "") or len(loan_ids) == 0:
#                 raise Exception(f"notice.generate_physical_notices.exception: Empty loan_ids for this linked loan")
#         # For normal loans
#         else:
#             loan_ids = kwargs["loan_ids"]

#         notice_generation_kwargs = {
#             "company_id": kwargs["company_id"],
#             "draft_id": kwargs["draft_id"],
#             "draft_details": kwargs["draft_details"],
#             "loan_ids": loan_ids,
#             "linked_loan_id": linked_loan_id if kwargs.get("linked_loan") else "",
#             "allocation_month": kwargs["allocation_month"],
#             "author": kwargs["author"],
#             "role": kwargs["role"],
#             "batch_number": kwargs["batch_number"],
#             "batch_id": kwargs["batch_id"],
#             "document_type": kwargs["document_type"],
#             "mode": kwargs["mode"],
#             "type_of_task": "physical",
#             "preview": preview,
#             "auth_token": kwargs["token"],
#             "BUCKET_NAME": S3_BUCKET_NAME,
#             "S3_BUCKET_ENDPOINT": S3_BUCKET_ENDPOINT,
#             "RECOVERY_SERVICE_BASE_URL": RECOVERY_SERVICE_BASE_URL,
#             "local_pdf_directory_path": local_pdf_directory_path,
#             "local_doc_directory_path": local_doc_directory_path,
#             "local_batch_directory_path": local_batch_directory_path,
#             "local_draft_file_path": local_draft_file_path,
#             "local_qr_code_directory_path": local_qr_code_directory_path,
#             "local_merged_pdf_directory_path": local_merged_pdf_directory_path,
#             "local_merged_pdf_zip_file_path": local_merged_pdf_zip_file_path,
#             "NOTICE_SERVICE_BASE_URL": NOTICE_SERVICE_BASE_URL,
#             "use_tracking_ids": kwargs.get("use_tracking_ids", False),
#             "physical_notice_trackings_ids_redis_key": kwargs.get("physical_notice_trackings_ids_redis_key", ""),
#             "user": kwargs["user"],
#             "is_linked_loan": kwargs["is_linked_loan"],
#             "request_id": request_id,
#             "draft_fields_redis_key": kwargs["draft_fields_redis_key"],
#             "company": kwargs["company"],
#             "initial_notice_id_redis_key": kwargs["initial_notice_id_redis_key"],
#             "enable_qrcode": kwargs["enable_qrcode"],
#             "merged_lot_size": kwargs.get("merged_lot_size"),
#         }

#         # To make filename based on s3_link_uuid which is actually batch_id
#         if preview:
#             notice_generation_kwargs["s3_link_uuid"] = kwargs["s3_link_uuid"]

#         generate_physical_notice(**notice_generation_kwargs)

#         message = (
#             "Linked loan physical notice generated" if kwargs.get("linked_loan_id") else "Physical notice generated"
#         )

#         logs_tracker_req_body = {
#             "response": {"message": f"{message}"},
#             "kwargs": {
#                 "batch_id": kwargs["batch_id"],
#                 "author": kwargs["user"]["email"],
#                 "company_id": kwargs["company"]["company_id"],
#                 "loan_id": logs_loan_id,
#                 "user": kwargs["user"],
#                 "company": kwargs["company"],
#             },
#             "status_code": 200,
#             "status": "SUCCESS",
#         }
#     except Exception as e:
#         logger.error(f"generate_physical_notices.exception :: {str(e)}")
#         logs_tracker_req_body = {
#             "response": {"message": str(e), "notice_id_list": failed_notice_id_list},
#             "kwargs": {
#                 "batch_id": kwargs["batch_id"],
#                 "author": kwargs["user"]["email"],
#                 "company_id": kwargs["company"]["company_id"],
#                 "loan_id": logs_loan_id,
#                 "user": kwargs["user"],
#                 "company": kwargs["company"],
#             },
#             "status_code": 400,
#             "status": "FAIL",
#         }
#     finally:
#         logs_tracker(logs_tracker_req_body, kwargs.get("X-Request-Id"))
#         failed_notice_id_list.clear()


# def generate_physical_notice(**kwargs):
#     logger.info("notice.generate_physical_notice")
#     logger.info(f"notice.generate_physical_notice.batch_id :: {kwargs['batch_id']}")

#     logger.debug(f"notice.generate_physical_notice.kwargs: {kwargs}")
#     preview = kwargs.get("preview", False)
#     kwargs["X-Request-Id"] = kwargs["request_id"]
#     failed_tracking_id_list = []

#     try:
#         redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#         draft_fields = redis_instance.get(kwargs["draft_fields_redis_key"]).decode("utf-8")

#         if not draft_fields:
#             raise Exception("tasks.generate_physical_notice.exception: Unable to fetch draft details from redis")

#         draft_fields = json.loads(draft_fields)

#         draft_details = kwargs.get("draft_details", {})
#         kwargs["draft_name"] = draft_details.get("draft_name")
#         kwargs["notice_type"] = draft_details.get("notice_type")
#         kwargs["case_type"] = draft_details.get("case_type")
#         kwargs["is_vernacular"] = draft_details.get("is_vernacular")
#         kwargs["language"] = draft_details.get("language")
#         kwargs["draft_fields"] = draft_fields.get(kwargs.get("draft_id"))
#         kwargs["is_in_case"] = False

#         if kwargs["case_type"] not in ("", None):
#             kwargs["is_in_case"] = True

#         loan_data = get_loan_data(**kwargs)

#         if not loan_data:
#             logger.error("generate_physical_notice.get_loan_data_res.err : Can't find loan data")
#             raise Exception(
#                 "generate_physical_notice.get_loan_data_res.err: Empty loan_data response for the given loan"
#             )
#         if isinstance(loan_data, str):
#             logger.error(f"generate_physical_notice.get_loan_data_res.err : {loan_data}")
#             raise Exception(f"generate_physical_notice.get_loan_data_res.err: {loan_data}")
#         if len(kwargs.get("loan_ids", [])) != len(loan_data["company_data"]):
#             logger.error(f"generate_physical_notice.get_loan_data_res.err : Can't find data for all the loans")
#             raise Exception(f"generate_physical_notice.get_loan_data_res.err: Cant find details for all the loans")

#         kwargs["loan_data"] = loan_data["company_data"]
#         kwargs["loan_address_map"] = {}

#         # To get the key value pairs for merging with the notice document, where key is the merge field with corresponding value from the db records
#         notice_data = get_notice_generation_data(**kwargs)

#         if isinstance(notice_data, str):
#             logger.debug(f"generate_physical_notice.get_notice_generation_data.err : {notice_data}")
#             raise Exception(f"generate_physical_notice.err : {notice_data}")
#         else:
#             kwargs["notice_data"] = notice_data
#             kwargs["filenames"] = []
#             kwargs["tracking_ids"] = []
#             kwargs["local_pdf_file_names"] = []
#             kwargs["primary_addresses"] = []
#             kwargs["address_file_map"] = {}
#             kwargs["loan_allocation_map"] = get_loan_allocation_month_mapping(kwargs["loan_data"])

#             response, notice_id_list, failed_tracking_id_list = generate_notice_for_all_addresses(**kwargs)

#             global failed_notice_id_list
#             failed_notice_id_list = notice_id_list
#             kwargs["notice_id_list"] = notice_id_list

#             if response != "success":
#                 raise Exception(response)

#             if not preview:
#                 changed_dt = notice_data.get("changed_dt", {})
#                 db_data = {
#                     "applicant_type": changed_dt["applicant_type"],
#                     "address_index": changed_dt["address_index"],
#                     "batch_number": kwargs.get("batch_number", ""),
#                     "notice_reference_number": changed_dt["notice_reference_number"],
#                     "applicant_notice_reference_number": changed_dt["applicant_notice_reference_number"],
#                     "co_applicant_notice_reference_number": changed_dt["co_applicant_notice_reference_number"],
#                     "notice_variables_data": changed_dt,
#                 }
#                 kwargs["db_data"] = db_data
#                 kwargs["files_s3_map"] = {}

#             upload_response = upload_notices_to_s3(**kwargs)

#             if not preview:
#                 logger.debug(f"generate_physical_notice.upload_response: {upload_response}")
#                 kwargs["loan_address_file_s3_map"] = {}
#                 loan_address_file_s3_map_list = map_formatter(
#                     kwargs["loan_address_map"],
#                     kwargs["address_file_map"],
#                     kwargs["files_s3_map"],
#                 )
#                 kwargs["loan_address_file_s3_map_list"] = loan_address_file_s3_map_list
#                 kwargs["s3_link_ids"] = upload_response["s3_link_ids"]
#                 kwargs["s3_object_urls"] = upload_response["s3_object_urls"]

#                 for data in loan_address_file_s3_map_list:
#                     if str(data["notice_id"]) == str(kwargs["notice_id_list"][0]):
#                         kwargs["primary_notice_data"] = {
#                             "s3_link": data["s3_link"],
#                             "s3_link_uuid": data["s3_link_uuid"],
#                         }
#                 insert_into_db(**kwargs)

#     except Exception as e:
#         if failed_tracking_id_list:
#             failed_tracking_ids_key = f'failed_tracking_id_{kwargs.get("batch_id","")}'
#             redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#             redis_instance.lpush(failed_tracking_ids_key, *failed_tracking_id_list)
#             redis_instance.close()
#         raise Exception(f"generate_physical_notice.exception :: {str(e)}")


# def get_loan_allocation_month_mapping(loan_data):
#     loan_allocation_map = {}
#     logger.info("generate_physical_notice.get_loan_allocation_month_mapping")
#     for loan in loan_data:
#         loan_id = loan["loan_id"]
#         allocation_month = loan["question_dict"]["allocation_month"]
#         loan_allocation_map[loan_id] = allocation_month
#     return loan_allocation_map
