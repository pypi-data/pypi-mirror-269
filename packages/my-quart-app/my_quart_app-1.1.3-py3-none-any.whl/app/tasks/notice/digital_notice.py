# import json
# import logging
# import os
# import uuid

# import redis
# from celery import shared_task

# from app.tasks.notice.loan_service import get_loan_data
# from app.tasks.notice.notice_service import (
#     get_notice_generation_data,
#     insert_into_db,
#     upload_notices_to_s3,
# )

# from ...settings import (
#     NOTICE_SERVICE_BASE_URL,
#     RECOVERY_SERVICE_BASE_URL,
#     REDIS,
#     S3_BUCKET_ENDPOINT,
#     S3_BUCKET_NAME,
# )
# from .helpers import (
#     doc2pdf_converter,
#     generate_qrcode_doc,
#     get_dsc_on_notice_pdf,
#     logs_tracker,
#     make_notice_doc_file,
# )

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# @shared_task(
#     bind=True,
#     name="handle_generate_digital_notice",
#     ignore_result=False,
#     acks_late=False,
# )
# def handle_generate_digital_notice(self, *args, **kwargs):
#     logger.info("notice.handle_generate_digital_notice")
#     is_task_success = False

#     logs_loan_id = kwargs["linked_loan"]["linked_loan_id"] if kwargs.get("linked_loan") else kwargs.get("loan_ids")[0]
#     logger.info(f"notice.handle_generate_digital_notice.kwargs :: {kwargs}")
#     logger.info(f"notice.handle_generate_digital_notice.loan_id :: {logs_loan_id}")
#     logger.info(f"notice.handle_generate_digital_notice.batch_id :: {kwargs['batch_id']}")

#     try:
#         redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#         notice_kwargs = json.loads(redis_instance.get(f"notice_kwargs_{kwargs['batch_id']}").decode("utf-8"))
#         redis_instance.close()
#         # In case key is not present in redis
#         if not notice_kwargs:
#             logger.error("notice.handle_generate_digital_notice.exception: notice_kwargs not found in redis")
#             raise Exception("notice_kwargs not found in redis")

#         kwargs = {**kwargs, **notice_kwargs}
#         logger.debug(f"notice.generate_digital_notices.kwargs : {kwargs}")

#         local_batch_directory_path = kwargs["local_batch_directory_path"]
#         local_draft_file_path = kwargs["local_draft_file_path"]
#         local_doc_directory_path = kwargs["local_doc_directory_path"]
#         local_pdf_directory_path = kwargs["local_pdf_directory_path"]
#         local_qr_code_directory_path = kwargs["local_qr_code_directory_path"]
#         preview = kwargs.get("preview", False)
#         request_id = str(uuid.uuid4())

#         os.makedirs(local_doc_directory_path, exist_ok=True)
#         os.makedirs(local_pdf_directory_path, exist_ok=True)
#         os.makedirs(local_qr_code_directory_path, exist_ok=True)

#         # For linked loans
#         if kwargs.get("linked_loan"):
#             linked_loan_dict = kwargs["linked_loan"]
#             linked_loan_id = linked_loan_dict.get("linked_loan_id", "")
#             loan_ids = linked_loan_dict.get("loan_ids", [])

#             if linked_loan_id in (None, "") or len(loan_ids) == 0:
#                 raise Exception(f"Invalid linked loan id {linked_loan_id}")
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
#             "type_of_task": "digital",
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
#             "local_merged_pdf_directory_path": kwargs["local_merged_pdf_directory_path"],
#             "local_merged_pdf_zip_file_path": kwargs["local_merged_pdf_zip_file_path"],
#             "NOTICE_SERVICE_BASE_URL": NOTICE_SERVICE_BASE_URL,
#             "user": kwargs["user"],
#             "is_linked_loan": kwargs["is_linked_loan"],
#             "case_type": kwargs.get("case_type"),
#             "case_id": kwargs.get("case_id"),
#             "iteration": kwargs.get("iteration"),
#             "stage_code": kwargs.get("stage_code"),
#             "request_id": request_id,
#             "draft_fields_redis_key": kwargs["draft_fields_redis_key"],
#             "company": kwargs["company"],
#             "enable_qrcode": kwargs["enable_qrcode"],
#         }

#         if preview:
#             notice_generation_kwargs["s3_link_uuid"] = kwargs["s3_link_uuid"]

#         generate_digital_notice(**notice_generation_kwargs)

#         message = "Linked loan digital notice generated" if kwargs.get("linked_loan_id") else "Digital notice generated"

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
#         logger.error(f"notice.handle_generate_digital_notice.exception: {str(e)}")

#         logs_tracker_req_body = {
#             "response": str({"message": str(e)}),
#             "kwargs": {
#                 "batch_id": kwargs["batch_id"],
#                 "batch_number": kwargs["batch_number"],
#                 "total_batches": 1,
#                 "author": kwargs.get("author"),
#                 "company_id": kwargs.get("company_id"),
#                 "loan_id": logs_loan_id,
#                 "total_loans": 1,
#                 "user": kwargs.get("user", {}),
#                 "company": kwargs.get("company", {}),
#             },
#             "status_code": 400,
#             "status": "FAIL",
#         }
#     finally:
#         logs_tracker(logs_tracker_req_body, kwargs.get("X-Request-Id"))
#         return is_task_success


# def generate_digital_notice(**kwargs):
#     logger.info("tasks.notice.generate_digital_notice")
#     logger.info(f"notice.handle_generate_digital_notice.batch_id :: {kwargs['batch_id']}")

#     try:
#         kwargs["X-Request-Id"] = kwargs["request_id"]
#         local_pdf_directory_path = kwargs.get("local_pdf_directory_path")
#         redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])

#         draft_fields = redis_instance.get(kwargs["draft_fields_redis_key"])
#         if not draft_fields:
#             logger.error("tasks.generate_digital_notice.exception: Unable to fetch draft details from redis")
#             raise Exception("tasks.generate_digital_notice.exception: Unable to fetch draft details from redis")

#         draft_fields = json.loads(draft_fields.decode("utf-8"))
#         redis_instance.close()
#         preview = kwargs.get("preview", False)
#         draft_details = kwargs.get("draft_details", {})
#         kwargs["draft_name"] = draft_details.get("draft_name")
#         kwargs["notice_type"] = draft_details.get("notice_type")
#         kwargs["is_vernacular"] = draft_details.get("is_vernacular")
#         kwargs["is_in_case"] = draft_fields.get("is_in_case")
#         kwargs["language"] = draft_details.get("language")
#         kwargs["draft_fields"] = draft_fields.get(kwargs.get("draft_id"))
#         kwargs["is_dsc_enabled"] = draft_details.get("is_dsc_enabled")
#         kwargs["dsc_placement"] = draft_details.get("dsc_placement")

#         loan_data = get_loan_data(**kwargs)

#         if not loan_data:
#             logger.error("generate_digital_notice.get_loan_data_res.err : Can't find loan data")
#             raise Exception("Cannot find data for the given loan")
#         if isinstance(loan_data, str):
#             logger.error(f"generate_digital_notice.get_loan_data_res.err : {loan_data}")
#             raise Exception(loan_data)

#         if len(kwargs.get("loan_ids", [])) != len(loan_data["company_data"]):
#             logger.error(f"generate_digital_notice.get_loan_data_res.err : Can't find data for all the loans")
#             raise Exception("Can't find data for all the loans")

#         kwargs["loan_data"] = loan_data["company_data"]
#         kwargs["loan_address_map"] = {}
#         notice_data = get_notice_generation_data(**kwargs)

#         kwargs["filenames"] = []
#         kwargs["index"] = 1

#         languages = notice_data.get("languages", {})
#         kwargs["notice_data"] = notice_data
#         master_table_dict = notice_data["master_table_dict"]
#         duplicated_tables_dict = notice_data["duplicated_tables_dict"]
#         kwargs["notice_data"]["master_table_dict"] = {
#             **master_table_dict,
#             **duplicated_tables_dict,
#         }

#         notice_file_data = make_notice_doc_file(**kwargs)

#         input_file, output_file = (
#             notice_file_data["input_file_path"],
#             notice_file_data["output_file_path"],
#         )
#         kwargs["input_file"] = input_file
#         kwargs["output_file"] = output_file
#         output_folder = local_pdf_directory_path

#         if kwargs.get("enable_qrcode", False):
#             generate_qrcode_doc(**kwargs)

#         doc2pdf_converter(output_folder, **kwargs)

#         if kwargs["is_dsc_enabled"]:
#             get_dsc_on_notice_pdf(**kwargs)
#             kwargs["is_dsc_signed"] = True

#         kwargs["filenames"].append(output_file)
#         changed_dt = notice_data.get("changed_dt", {})

#         db_data = {
#             "barcode": changed_dt.get("barcode"),
#             "applicant_type": changed_dt["applicant_type"],
#             "borrower_type": changed_dt["applicant_type"],
#             "address_index": changed_dt["address_index"],
#             "batch_number": kwargs.get("batch_number", ""),
#             "notice_reference_number": changed_dt["notice_reference_number"],
#             "applicant_notice_reference_number": changed_dt["applicant_notice_reference_number"],
#             "co_applicant_notice_reference_number": changed_dt["co_applicant_notice_reference_number"],
#             "applicant_language": languages.get("applicant_language"),
#             "co_applicant_language": languages.get("co_applicant_language"),
#             "draft_language": languages.get("draft_language"),
#             "notice_variables_data": changed_dt,
#         }

#         kwargs["db_data"] = db_data
#         upload_response = upload_notices_to_s3(**kwargs)

#         kwargs["loan_allocation_map"] = get_loan_allocation_month_mapping(kwargs["loan_data"])

#         if os.path.exists(input_file):
#             os.remove(input_file)
#         if os.path.exists(output_file):
#             os.remove(output_file)

#         if not preview:
#             kwargs["s3_link_ids"] = upload_response["s3_link_ids"]
#             kwargs["s3_object_urls"] = upload_response["s3_object_urls"]
#             kwargs["primary_notice_data"] = {
#                 "s3_link_uuid": upload_response["s3_link_ids"][0],
#                 "s3_link": upload_response["s3_object_urls"][0],
#             }
#             insert_into_db(**kwargs)

#     except Exception as e:
#         raise Exception(f"tasks.notice.generate_digital_notice.exception :: {str(e)}")


# def get_loan_allocation_month_mapping(loan_data):
#     loan_allocation_map = {}
#     logger.info("generate_physical_notice.get_loan_allocation_month_mapping")
#     for loan in loan_data:
#         loan_id = loan["loan_id"]
#         allocation_month = loan["question_dict"]["allocation_month"]
#         loan_allocation_map[loan_id] = allocation_month
#     return loan_allocation_map
