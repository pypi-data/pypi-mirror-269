# import requests
# import json
# from ....settings import (
#     COMMUNICATION_SERVICE_BASE_URL,
#     NOTICE_SERVICE_BASE_URL,
#     REDIS,
#     QUEUE_SERVICE_BASE_URL,
# )
# import logging
# import os
# import redis
# from ....utils import get_s3_client
# import shutil
# from botocore.exceptions import ClientError
# from xlsxwriter import Workbook
# import re
# from cg_kafka.producer.JSONProducer import JSONProducer
# from ....settings import MERGE_NOTICE_CLIENT_ID, MERGE_NOTICE_TOPIC, NUMBER_OF_PARTITIONS_FOR_MERGE_NOTICE_TOPIC
# from ....choices import EXCEL_WORKSHEET_HYPERLINK_LIMIT, MERGE_FILE_NAME_REPLACE_CHARACTER

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# redis_conf = REDIS
# redis_obj = redis.Redis(host=redis_conf["HOST"], port=redis_conf["PORT"])

# s3 = get_s3_client()

# numbers = re.compile(r"(\d+)")
# non_numbers = re.compile(r"(\D+)")


# def file_system_Sort(value):
#     parts = non_numbers.split(value)
#     parts[1::2] = list(map(lambda y: str.lower(y), parts[1::2]))
#     parts[1::2] = map(str, parts[1::2])
#     part = "".join(parts)
#     parts = numbers.split(part)
#     parts[1::2] = map(int, parts[1::2])
#     return parts


# def generate_notices_zip(local_pdf_directory_path, local_zip_file_path):
#     logger.info("notice_callback.commons.generate_notices")
#     if os.path.exists(local_pdf_directory_path):
#         dir_content = os.listdir(local_pdf_directory_path)
#         if len(dir_content) > 0:
#             shutil.make_archive(local_zip_file_path, "zip", local_pdf_directory_path)
#             return True
#     return False


# def upload_file_to_s3(s3, local_file_name, bucket, s3_object_name):
#     logger.info("notice_callback.commons.upload_file_to_s3")
#     try:
#         response = s3.upload_file(local_file_name, bucket, s3_object_name, ExtraArgs={"ACL": "public-read"})
#     except ClientError as e:
#         logger.error(f"notice_callback.commons.upload_file_to_s3.exception : {str(e)}")
#         return False

#     return True


# def changeCamelCaseToSnakeCase(str):
#     str = "".join("_" + i.lower() if i.isupper() else i for i in str).lstrip("_")
#     str = "".join("_" if i == " " else i for i in str)
#     return str


# def generate_tracking_excel(**kwargs):
#     logger.info("notice_callback.commons.generate_tracking_excel")
#     file_path = kwargs["file_path"]
#     notices = kwargs["notice_data"]
#     is_linked_loan = kwargs.get("is_linked_loan", False)

#     workbook = Workbook(filename=file_path)
#     worksheet = workbook.add_worksheet()
#     links_written_in_worksheet = 0

#     row = 0
#     col = 0

#     worksheet.write_string(row, col, "system_id")
#     worksheet.write_string(row, col + 1, "loan_id")
#     worksheet.write_string(row, col + 2, "file_name")
#     worksheet.write_string(row, col + 3, "tracking_no")
#     worksheet.write_string(row, col + 4, "allocation_month")
#     worksheet.write_string(row, col + 5, "notice_type")
#     worksheet.write_string(row, col + 6, "notice_id")
#     worksheet.write_string(row, col + 7, "notice_link")
#     worksheet.write_string(row, col + 8, "batch_id")

#     if is_linked_loan:
#         worksheet.write_string(0, 9, "linked_loan_id")

#     address_headers_set = set()
#     for notice in notices:
#         if notice["primary_address"]:
#             for key in json.loads(notice["primary_address"]):
#                 address_headers_set.add(key)

#     start_index = 10 if is_linked_loan else 9

#     for i, key in enumerate(address_headers_set):
#         worksheet.write_string(row, col + i + start_index, changeCamelCaseToSnakeCase(key))

#     row += 1

#     for notice in notices:
#         worksheet.write_string(row, col, str(notice["id"]))
#         worksheet.write_string(row, col + 1, "'" + str(notice["loan_id"]))
#         worksheet.write_string(row, col + 2, notice["local_pdf_file_name"])
#         worksheet.write_string(row, col + 3, str(notice["tracking_id"] or ""))
#         worksheet.write_string(row, col + 4, str(notice["allocation_month"] or ""))
#         worksheet.write_string(row, col + 5, str(notice["notice_type"] or ""))
#         worksheet.write_string(row, col + 6, notice["notice_id"])
#         if links_written_in_worksheet < EXCEL_WORKSHEET_HYPERLINK_LIMIT:
#             if str(notice["s3_link"]):
#                 worksheet.write_url(row, col + 7, str(notice["s3_link"] or ""))
#                 links_written_in_worksheet += 1
#         else:
#             worksheet.write_string(row, col + 7, str(notice["s3_link"] or ""))

#         worksheet.write_string(row, col + 8, kwargs["batch_id"])

#         if is_linked_loan:
#             worksheet.write_string(row, col + 9, "'" + str(notice["linked_loan_id"] or ""))

#         if notice["primary_address"]:
#             address = json.loads(notice["primary_address"])
#             for i, key in enumerate(address_headers_set):
#                 worksheet.write_string(row, col + i + start_index, str(address.get(key, "")))
#         row += 1

#     for i, key in enumerate(address_headers_set):
#         try:
#             if "cell_1" in key:
#                 key = key.split("table_1_cell_1_")[1]
#             elif "table_1_" in key:
#                 key = key.split("table_1_")[1]
#             key = key.split("_")[0] if "address" in key else key.replace("_", " ")
#         except Exception as e:
#             logger.error(f"key spilitting error: {str(e)}, {key}")
#         worksheet.write_string(0, 0 + i + start_index, changeCamelCaseToSnakeCase(key))

#     workbook.close()


# def generate_tracking_excel_with_merged_pdf_file_mapping(**kwargs):
#     logger.info("notice_callback.commons.generate_tracking_excel_with_merged_pdf_file_mapping")
#     file_path = kwargs["local_tracking_excel_file_with_merge_file_name_mapping_path"]
#     notices = kwargs["notice_data"]
#     is_linked_loan = kwargs.get("is_linked_loan", False)
#     is_merged_lot = True if kwargs.get("merged_lot_size", None) else False
#     notice_id_merged_file_name_mapping = kwargs.get("notice_id_merged_file_name_mapping", {})

#     workbook = Workbook(filename=file_path)
#     worksheet = workbook.add_worksheet()
#     links_written_in_worksheet = 0

#     row = 0
#     col = 0

#     worksheet.write_string(row, col, "system_id")
#     worksheet.write_string(row, col + 1, "loan_id")
#     worksheet.write_string(row, col + 2, "file_name")
#     worksheet.write_string(row, col + 3, "tracking_no")
#     worksheet.write_string(row, col + 4, "allocation_month")
#     worksheet.write_string(row, col + 5, "notice_type")
#     worksheet.write_string(row, col + 6, "notice_id")
#     worksheet.write_string(row, col + 7, "notice_link")
#     worksheet.write_string(row, col + 8, "batch_id")

#     if is_merged_lot and is_linked_loan:
#         worksheet.write_string(row, col + 9, "linked_loan_id")
#         worksheet.write_string(row, col + 10, "merged_lot_file_name")
#     elif is_linked_loan:
#         worksheet.write_string(row, col + 9, "linked_loan_id")
#     elif is_merged_lot:
#         worksheet.write_string(row, col + 9, "merged_lot_file_name")

#     address_headers_set = set()
#     for notice in notices:
#         if notice["primary_address"]:
#             for key in json.loads(notice["primary_address"]):
#                 address_headers_set.add(key)

#     if is_merged_lot and is_linked_loan:
#         start_index = 11
#     elif is_linked_loan or is_merged_lot:
#         start_index = 10
#     else:
#         start_index = 9

#     for i, key in enumerate(address_headers_set):
#         worksheet.write_string(row, col + i + start_index, changeCamelCaseToSnakeCase(key))

#     row += 1

#     for notice in notices:
#         worksheet.write_string(row, col, str(notice["id"]))
#         worksheet.write_string(row, col + 1, "'" + str(notice["loan_id"]))
#         worksheet.write_string(row, col + 2, notice["local_pdf_file_name"])
#         worksheet.write_string(row, col + 3, str(notice["tracking_id"] or ""))
#         worksheet.write_string(row, col + 4, str(notice["allocation_month"] or ""))
#         worksheet.write_string(row, col + 5, str(notice["notice_type"] or ""))
#         worksheet.write_string(row, col + 6, notice["notice_id"])
#         if links_written_in_worksheet < EXCEL_WORKSHEET_HYPERLINK_LIMIT:
#             if str(notice["s3_link"]):
#                 worksheet.write_url(row, col + 7, str(notice["s3_link"] or ""))
#                 links_written_in_worksheet += 1
#         else:
#             worksheet.write_string(row, col + 7, str(notice["s3_link"] or ""))
#         worksheet.write_string(row, col + 8, kwargs["batch_id"])

#         if is_merged_lot and is_linked_loan:
#             worksheet.write_string(row, col + 9, "'" + str(notice["linked_loan_id"] or ""))
#             worksheet.write_string(
#                 row,
#                 col + 10,
#                 str(notice_id_merged_file_name_mapping[int(notice["notice_id"])]) or "",
#             )
#         elif is_linked_loan:
#             worksheet.write_string(row, col + 9, "'" + str(notice["linked_loan_id"] or ""))
#         elif is_merged_lot:
#             worksheet.write_string(
#                 row,
#                 col + 9,
#                 str(notice_id_merged_file_name_mapping[int(notice["notice_id"])]) or "",
#             )

#         if notice["primary_address"]:
#             address = json.loads(notice["primary_address"])
#             for i, key in enumerate(address_headers_set):
#                 worksheet.write_string(row, col + i + start_index, str(address.get(key, "")))
#         row += 1

#     for i, key in enumerate(address_headers_set):
#         try:
#             if "cell_1" in key:
#                 key = key.split("table_1_cell_1_")[1]
#             elif "table_1_" in key:
#                 key = key.split("table_1_")[1]
#             key = key.split("_")[0] if "address" in key else key.replace("_", " ")
#         except Exception as e:
#             logger.error(f"key spilitting error: {str(e)}, {key}")
#         worksheet.write_string(0, 0 + i + start_index, changeCamelCaseToSnakeCase(key))

#     workbook.close()

#     logger.info("notice_callback.commons.generate_tracking_excel :: tracking_excel generated")


# def get_batch_notices(**kwargs):
#     logger.info("notice_callback.commons.get_batch_notices")
#     try:
#         url = f"{NOTICE_SERVICE_BASE_URL.rstrip('/')}/notices"
#         headers = {
#             "authenticationtoken": kwargs.get("token", ""),
#             "role": kwargs.get("role", ""),
#             "Content-type": "application/json",
#             "X-Request-Id": kwargs.get("X-Request-Id", ""),
#             "X-CG-User": json.dumps(kwargs.get("user", {})),
#             "X-CG-Company": json.dumps(kwargs.get("company", {})),
#         }
#         params = {"company_id": kwargs["company_id"], "batch_id": kwargs["batch_id"]}

#         get_resp = requests.get(url=url, params=params, headers=headers)

#         logger.debug(f"notice_callback.commons.get_batch_notices.get_notices.url: {url}")
#         logger.debug(
#             f"notice_callback.commons.get_batch_notices.get_notices.response.status_code: {get_resp.status_code}"
#         )

#     except Exception as e:
#         logger.error(f"notice_callback.commons.get_batch_notices.get_notices.exception: {str(e)}")
#         return str(e)

#     result = json.loads(get_resp.text)
#     return result["data"]


# def send_batch_completion_email(**kwargs):
#     logger.debug("notice_callback.commons.send_batch_completion_email")

#     contactus_link = ""
#     (
#         zip_file_s3_link,
#         tracking_file_s3_link,
#         batch_report_s3_link,
#         s3_tracking_ids_excel_link,
#         notices_zip_generated,
#     ) = (
#         kwargs.get("s3_zip_file_link", ""),
#         kwargs.get("s3_tracking_excel_link", ""),
#         kwargs.get("s3_report_batch_excel_link", ""),
#         kwargs.get("s3_tracking_ids_excel_link", ""),
#         kwargs.get("notices_zip_generated"),
#     )

#     s3_tracking_excel_with_merge_file_name_mapping_link = kwargs.get(
#         "s3_tracking_excel_with_merge_file_name_mapping_link", ""
#     )
#     merging_process_success = kwargs.get("merging_process_success")
#     hyperlink_tracking_file_with_file_name_mapping = ""

#     hyperlink_error_report = ""
#     hyperlink_zip_file = ""
#     hyperlink_tracking_file = ""
#     hyperlink_tracking_ids_file = ""
#     batch_report_data = kwargs["batch_report_data"]
#     failed = batch_report_data["failed"]
#     success = batch_report_data["success"]
#     failed_loans_count = len(failed)
#     succes_loans_count = batch_report_data["success_count"]
#     total_loans_count = failed_loans_count + succes_loans_count

#     notice_type = kwargs.get("notice_type", "Physical")
#     local_zip_file_path = kwargs.get("local_zip_file_path", "")

#     company_details = kwargs["company"]
#     draft_details = kwargs["draft_details"]

#     if kwargs["batch_report_data"]["failed"]:
#         hyperlink_error_report = f"<a href='{batch_report_s3_link}'>Physical Notices failed Report</a>.<br><br>"

#     if kwargs["local_tracking_ids_excel_file_generated_flag"]:
#         hyperlink_tracking_ids_file = (
#             f"<a href='{s3_tracking_ids_excel_link}'>Failed & unused tracking ids</a>.<br><br>"
#         )

#     if merging_process_success:
#         hyperlink_tracking_file_with_file_name_mapping = f"<a href='{s3_tracking_excel_with_merge_file_name_mapping_link}'>Excel file containing notice details with merge notice file mapping</a>.<br><br>"

#     if notices_zip_generated:
#         hyperlink_zip_file = f"<a href='{zip_file_s3_link}'>Zip file containing all notices</a>.<br><br>"
#     if notices_zip_generated:
#         hyperlink_tracking_file = f"<a href='{tracking_file_s3_link}'>Excel file containing notice details</a>.<br><br>"

#     if kwargs["is_linked_loan"]:
#         subject = f"Linked Loan Physical Notice Batch Report for {company_details['company_name']} | notice type - {draft_details['notice_type']} batch id - {kwargs['batch_id']}"
#         starter = f"Linked Loan Physical notices"
#         loans = "linked loans"
#     else:
#         subject = f"Physical Notice Batch Report for {company_details['company_name']} | notice type - {draft_details['notice_type']} batch id - {kwargs['batch_id']}"
#         starter = f"Physical notices"
#         loans = "loans"

#     user_email_payload = {
#         "from_data": {"name": "Credgenics", "email": "legal@credgenics.com"},
#         "subject": f"{subject}",
#         "to_emails": [{"email": kwargs["author"]}],
#         "source": "notice_generation_batch_completion",
#         "email_body": f"""Hi,<br><br>

#         {starter} for {kwargs['batch_id']} have been generated, links for relevant files are provided below.<br><br>

#         company_id: {kwargs.get('company_id')}<br>
#         total {loans}: {total_loans_count}<br>
#         succes {loans}: {succes_loans_count}<br>
#         failed {loans}: {failed_loans_count}<br><br>

#         {hyperlink_zip_file}
#         {hyperlink_tracking_file}
#         {hyperlink_tracking_file_with_file_name_mapping}
#         {hyperlink_error_report}
#         {hyperlink_tracking_ids_file}


#         <a href="{contactus_link}">Contact Us</a><br><br>

#         This email was sent to you by Credgenics (Copyright © 2020 Analog Legalhub Technology Solutions Pvt. Ltd. All Rights Reserved).<br>
#         This is a computer generated email. Please do not reply to this email. """,
#     }

#     send_email(
#         user_email_payload,
#         kwargs["token"],
#         kwargs["role"],
#         kwargs["batch_id"],
#         kwargs["user"],
#         company_details,
#     )

#     credgengics_physical_notice_email_payload = {
#         "from_data": {"name": "Credgenics", "email": "legal@credgenics.com"},
#         "subject": f"{subject}",
#         "to_emails": [{"email": "physical.notice@credgenics.com"}],
#         "source": "notice_generation_batch_completion",
#         "email_body": f"""Hi,<br><br>

#         {starter} for {kwargs['batch_id']} have been generated, links for relevant files are provided below.<br><br>

#         company_id: {kwargs.get('company_id')}<br>
#         total {loans}: {total_loans_count}<br>
#         succes {loans}: {succes_loans_count}<br>
#         failed {loans}: {failed_loans_count}<br><br>

#         {hyperlink_zip_file}
#         {hyperlink_tracking_file}
#         {hyperlink_tracking_file_with_file_name_mapping}
#         {hyperlink_error_report}
#         {hyperlink_tracking_ids_file}

#         <a href="{contactus_link}">Contact Us</a><br><br>

#         This email was sent to you by Credgenics (Copyright © 2020 Analog Legalhub Technology Solutions Pvt. Ltd. All Rights Reserved).<br>
#         This is a computer generated email. Please do not reply to this email. """,
#     }
#     send_email(
#         credgengics_physical_notice_email_payload,
#         kwargs["token"],
#         kwargs["role"],
#         kwargs["batch_id"],
#         kwargs["user"],
#         company_details,
#     )


# def send_email(payload, token, role, request_id, user, company):
#     logger.info("notice_callback.commons.send_email")
#     base_url = COMMUNICATION_SERVICE_BASE_URL
#     url = f"{base_url}/mail"
#     logger.debug(f"notice_callback.commons.send_email.url : {url}")
#     payload["module"] = "notice"

#     headers = {
#         "authenticationtoken": token,
#         "role": role,
#         "accept": "application/json",
#         "Content-Type": "application/json",
#         "X-Request-Id": str(request_id),
#         "X-CG-User": json.dumps(user),
#         "X-CG-Company": json.dumps(company),
#     }

#     result = requests.request(
#         method="POST",
#         url=url,
#         headers=headers,
#         json=payload,
#     )
#     logger.debug(f"notice_callback.commons.send_email.response.status_code : {result.status_code}")

#     if result.status_code != 200:
#         logger.debug(f"notice_callback.commons.send_email.response.err : {result.text}")
#         return json.loads(result.text)

#     data = json.loads(result.text)

#     if data:
#         email_data = data.get("data")
#         unique_mail_id = email_data.get("unique_mail_id")
#         status = data.get("output")

#         return (status, unique_mail_id)
#     return None, None


# def generate_unused_tracking_ids_excel(**kwargs):
#     logger.info("notice_callback.commons.generate_unused_tracking_ids_excel")

#     # EXTRACT DATA
#     local_batch_report_file_path = kwargs["local_tracking_ids_excel_path"]
#     failed_tracking_ids_key = f'failed_tracking_id_{kwargs.get("batch_id","")}'
#     failed_tracking_ids = pop_all_values_from_redis_key(failed_tracking_ids_key)
#     unused_tracking_ids_key = f"physical_notice_tracking_ids_{kwargs['batch_id']}"
#     unused_tracking_ids = pop_all_values_from_redis_key(unused_tracking_ids_key)

#     # GENERATE EXCEL
#     if failed_tracking_ids or unused_tracking_ids:
#         workbook = Workbook(filename=local_batch_report_file_path)
#         worksheet = workbook.add_worksheet()
#         # headings
#         row = 0
#         column = 0
#         bold = workbook.add_format({"bold": True})
#         worksheet.write(row, column, "tracking_id", bold)
#         worksheet.write(row, column + 1, "failed/unused", bold)
#         worksheet.set_column(0, 1, len("failed/unused"))
#         row = row + 1

#         if failed_tracking_ids:
#             for id in failed_tracking_ids:
#                 worksheet.write(row, column, str(id))
#                 worksheet.write(row, column + 1, "failed")
#                 row = row + 1

#         if unused_tracking_ids:
#             for id in unused_tracking_ids:
#                 worksheet.write(row, column, str(id))
#                 worksheet.write(row, column + 1, "unused")
#                 row = row + 1

#         workbook.close()
#         return True
#     return False


# def generate_failed_notices_report_excel(**kwargs):
#     logger.info("notice_callback.commons.generate_failed_notices_report_excel")

#     local_batch_report_file_path = kwargs["local_batch_report_file_path"]
#     batch_report_data = get_batch_report_data(**kwargs)
#     workbook = Workbook(filename=local_batch_report_file_path)
#     worksheet = workbook.add_worksheet()
#     failed = batch_report_data["failed"]

#     if failed:
#         row = 0
#         col = 0
#         cell0_0 = "linked_loan_id" if "linked_loan" in kwargs["type_of_task"] else "loan_id"
#         headers = ["loan_id", "reason", "status_code", "notice_id"]
#         for i, key in enumerate(headers):
#             worksheet.write_string(row, col + i, key)
#         row += 1
#         failed_records = []
#         for record in failed:
#             if len(record.get("notice_id_list", [])):
#                 for notice_id in record["notice_id_list"]:
#                     failed_record = {
#                         "reason": record["reason"],
#                         "loan_id": record["loan_id"],
#                         "status_code": record["status_code"],
#                         "notice_id": notice_id,
#                     }
#                     failed_records.append(failed_record)
#             else:
#                 failed_records.append({**record, "notice_id": None})

#         for record in failed_records:
#             for i, key in enumerate(headers):
#                 if key == "loan_id":
#                     worksheet.write_string(row, col + i, "'" + str(record.get(key, "")))
#                 else:
#                     worksheet.write_string(row, col + i, str(record.get(key, "")))
#             row += 1
#         worksheet.write_string(0, 0, cell0_0)
#         workbook.close()
#     return batch_report_data


# def get_batch_report_data(**kwargs):
#     logger.info("notice_callback.commons.get_batch_report_data")

#     batch_id = kwargs["batch_id"]
#     batch_status = {}
#     success = []
#     failed = []

#     execution_data_url = f"{QUEUE_SERVICE_BASE_URL}/batch_data"
#     req_body = {
#         "type": "notice",
#         "batch_id": batch_id,
#         "channel": "physical" if kwargs["is_linked_loan"] else "linked_loan_physical",
#     }

#     logger.debug(f"notice_callback.commons.get_batch_report_data.url : {execution_data_url}")

#     try:
#         execution_data = requests.request(
#             method="POST",
#             url=execution_data_url,
#             headers={
#                 "X-CG-User": json.dumps(kwargs.get("user", {})),
#                 "X-Request-Id": kwargs.get("X-Request-Id", ""),
#                 "X-CG-Company": json.dumps(kwargs.get("company", {})),
#             },
#             json=req_body,
#         )
#         logger.debug(f"notice_callback.commons.get_batch_report_data.status_code : {execution_data.status_code}")

#     except Exception as e:
#         logger.error(f"execution_data.exception_{batch_id} :: {str(e)}")
#         raise Exception(str(e))

#     if execution_data.status_code != 200:
#         logger.error(f"execution_data.text_{batch_id} :: {execution_data.text}")
#         raise Exception(f"batch_data api failed with status_code {execution_data.status_code}")
#         # self.retry(queue=queue, kwargs=kwargs, countdown=20, max_retries=5)

#     execution_data = execution_data.json()
#     if not execution_data["output"]["batch_data"]:
#         logger.error(f"get_batch_report_data.batch_data_api.exception: batch_data is empty")
#         raise Exception(f"batch_data api gave empty response with status_code {execution_data.status_code}")

#     batch_loans_data = execution_data["output"]["batch_loans_data"]
#     failed_loans_data = []
#     success_loans_data = []

#     for data in batch_loans_data:
#         if data["status"] == "SUCCESS":
#             success_loans_data.append(data)
#         else:
#             failed_loans_data.append(data)

#     # If none of the loan_id failed
#     if len(batch_loans_data) == 0:
#         success = json.loads(execution_data["output"]["batch_data"][0]["loan_data"])
#     else:
#         for failed_data in failed_loans_data:
#             response = json.loads(failed_data.get("response"))
#             message = response.get("message", "")
#             notice_id_list = response.get("notice_id_list", [])
#             status_code = failed_data.get("status_code")
#             loan_id = failed_data.get("loan_id")
#             failed.append(
#                 {
#                     "reason": str(message),
#                     "loan_id": loan_id,
#                     "status_code": status_code,
#                     "notice_id_list": notice_id_list,
#                 }
#             )
#     total_loans = int(execution_data["output"]["batch_data"][0]["total_loans"])

#     batch_status["success"] = success
#     batch_status["failed"] = failed
#     batch_status["success_count"] = total_loans - len(failed)

#     del failed_loans_data
#     del success_loans_data
#     del batch_loans_data
#     return batch_status


# def delete_redis_keys(batch_id):
#     redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#     keys_list = [
#         f"notice_kwargs_{batch_id}",
#         f"notice_draft_{batch_id}",
#         f"callback_kwargs_{batch_id}",
#         f"initial_notice_id_{batch_id}",
#     ]
#     redis_instance.delete(*keys_list)
#     redis_instance.close()
#     return


# def pop_all_values_from_redis_key(key_name):
#     redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#     val_list = redis_instance.lrange(key_name, 0, -1)
#     if len(val_list) > 0:
#         val_list = [item.decode("utf-8") for item in val_list]
#         return val_list
#     redis_instance.close()
#     return None


# def get_notice_id_and_loan_id_mappings(notice_data: list, is_linked_loan: bool, initial_notice_id: int, batch_id: str):
#     """
#     Method to get these mappings -
#         {loan_id : [notice_id]}
#         {notice_id : loan_id}
#         sorted [loan_id] acc to notice_id ASC
#     """
#     logger.info("notice_callback.commons.get_notice_id_loan_id_mapping")
#     # {loan_id : [notice_id]}
#     loan_id_notice_id_list_map = {}
#     # {notice_id : loan_id}
#     notice_id_loan_id_mapping = {}

#     redis_instance = redis.Redis(host=redis_conf["HOST"], port=redis_conf["PORT"])
#     last_notice_id = int(redis_instance.get(f"initial_notice_id_redis_key_{batch_id}"))
#     redis_instance.close()

#     if is_linked_loan:
#         loan_id_key = "linked_loan_id"
#     else:
#         loan_id_key = "loan_id"

#     for el in notice_data:
#         notice_id_loan_id_mapping[int(el["notice_id"])] = el[loan_id_key]

#         if loan_id_notice_id_list_map.get(el[loan_id_key]) is None:
#             loan_id_notice_id_list_map[el[loan_id_key]] = {int(el["notice_id"])}
#         else:
#             loan_id_notice_id_list_map[el[loan_id_key]].add(int(el["notice_id"]))

#     # sorted [loan_id] acc to notice_id ASC
#     loan_id_list_sorted_acc_to_notice_id = []
#     i = -1

#     for notice_id in range(initial_notice_id, last_notice_id):
#         loan_id = notice_id_loan_id_mapping.get(notice_id)

#         if loan_id:
#             if i >= 0:
#                 if loan_id != loan_id_list_sorted_acc_to_notice_id[i]:
#                     loan_id_list_sorted_acc_to_notice_id.append(loan_id)
#                     i = i + 1
#             else:
#                 loan_id_list_sorted_acc_to_notice_id.append(loan_id)
#                 i = i + 1

#     logger.info("notice_callback.commons.get_notice_id_loan_id_mapping completed")
#     return (
#         loan_id_notice_id_list_map,
#         notice_id_loan_id_mapping,
#         loan_id_list_sorted_acc_to_notice_id,
#     )


# def merge_pdf_of_individual_lot(
#     notice_ids_to_merged,
#     local_pdf_directory_path,
#     local_merged_pdf_directory_path,
#     merged_file_name,
# ):
#     """
#     # MERGED File Name:
#     # <notice_type>_<merged serial number>_<first notice id>_<last notice id>
#     """
#     logger.info("notice_callback.commons.merge_pdf_of_individual_lot")
#     file_list = notice_ids_to_merged

#     logger.debug(f"Merging files, processing lot : {notice_ids_to_merged}")

#     with fitz.open() as merge_file_result:
#         for file in file_list:
#             file_name = local_pdf_directory_path + "/" + str(file) + ".pdf"
#             try:
#                 with fitz.open(file_name) as mfile:
#                     merge_file_result.insert_pdf(mfile)
#             except Exception as e:
#                 logger.error(f"Exception occured while merging the pdf files : {e}")
#                 return False
#         merge_file_result.save(local_merged_pdf_directory_path + "/" + merged_file_name)
#         logger.debug(f"Merging files success, processed lot : {notice_ids_to_merged}")

#     return True


# def create_merge_list_batches(
#     loan_id_notice_id_list_map,
#     loan_id_list_sorted_acc_to_notice_id,
#     custom_batch_size,
# ):
#     """
#     CREATE BATCHES FOR MERGING NOTICEs
#     """
#     logger.info("notice_callback.commons.create_merge_list_batches")
#     merge_file_list = [[]]
#     idx = 0

#     for loan_id in loan_id_list_sorted_acc_to_notice_id:
#         notice_id_list = list(loan_id_notice_id_list_map[loan_id])
#         notice_id_list.sort()
#         if len(notice_id_list) > custom_batch_size:
#             merge_file_list.append(notice_id_list)
#             idx = idx + 1
#         elif len(merge_file_list[idx]) + len(notice_id_list) <= custom_batch_size:
#             merge_file_list[idx].extend(notice_id_list)
#         else:
#             merge_file_list.append([])
#             idx = idx + 1
#             merge_file_list[idx].extend(notice_id_list)

#     logger.debug(f"tasks.notice.notice_callbacks_commons.create_merge_list_batches: {merge_file_list}")
#     return merge_file_list


# def get_merged_file_name_mapping(notice_type, merged_file_list):
#     """
#     METHOD to get merged file name mappings for each notice_id to be put in tracking_id excel
#     """
#     logger.info("notice_callback.commons.get_merged_file_name_mapping")
#     map_file_name = {}
#     for count, arr in enumerate(merged_file_list):
#         file_name = notice_type + "_" + str(count + 1) + "_" + str(arr[0]) + "_" + str(arr[len(arr) - 1]) + ".pdf"
#         for notice_id in arr:
#             map_file_name[notice_id] = file_name

#     logger.debug(f"tasks.notice.notice_callbacks_commons.get_merged_file_name_mapping: {map_file_name}")
#     return map_file_name


# async def create_merge_pdf_and_zip(**kwargs):
#     """
#     METHOD TO MERGE NOTICEs AND ZIP THEM
#     """
#     logger.info("tasks.notice.notice_callback.commons.create_merge_pdf_and_zip")
#     logger.debug(f"tasks.notice.notice_callback.commons.create_merge_pdf_and_zip kwargs : {kwargs}")

#     local_merged_pdf_directory_path = kwargs["local_merged_pdf_directory_path"]
#     local_pdf_directory_path = kwargs["local_pdf_directory_path"]

#     local_pdf_directory_path = kwargs["local_pdf_directory_path"]
#     local_merged_pdf_directory_path = kwargs["local_merged_pdf_directory_path"]
#     local_merged_pdf_zip_file_path = kwargs["local_merged_pdf_zip_file_path"]

#     merged_lot_size = kwargs.get("merged_lot_size")
#     notice_data = kwargs["notice_data"]
#     notice_type = kwargs["notice_type"]
#     is_linked_loan = kwargs["is_linked_loan"]
#     initial_notice_id = kwargs["initial_notice_id"]
#     batch_id = kwargs["batch_id"]
#     count_of_notices = len(notice_data)
#     batch_name = kwargs.get("batch_name")
#     request_id = kwargs["request_id"]
#     local_batch_directory_path = kwargs["local_batch_directory_path"]

#     if batch_name:
#         batch_name = format_batch_name(batch_name)
#         merged_lot_zip_name = f"{batch_name}_{batch_id}_{count_of_notices}"
#     else:
#         merged_lot_zip_name = f"{batch_id}_{count_of_notices}"

#     # GET {notice_id: loan_id}, {loan_id:[notice_id]} & [loan_id]
#     (
#         loan_id_notice_id_list_map,
#         notice_id_loan_id_map,
#         loan_id_list_sorted_acc_to_notice_id,
#     ) = get_notice_id_and_loan_id_mappings(notice_data, is_linked_loan, initial_notice_id, batch_id)
#     logger.info("tasks.notice.notice_callback.commons.merge_pdf notice_id:loan_id mappings created")

#     # CREATE BATCHES FOR MERGING NOTICES :
#     merge_file_list_batches = create_merge_list_batches(
#         loan_id_notice_id_list_map,
#         loan_id_list_sorted_acc_to_notice_id,
#         merged_lot_size,
#     )
#     logger.info("tasks.notice.notice_callback.commons.create_merge_pdf_and_zip merge lists created")

#     # CREATE FILE NAME MAPPING WITH LOAN_IDS :
#     notice_id_merged_file_name_mapping = get_merged_file_name_mapping(notice_type, merge_file_list_batches)
#     logger.info("tasks.notice.notice_callback.commons.create_merge_pdf_and_zip file name mappings created")

#     logger.info("tasks.notice.notice_callback.commons.create_merge_pdf_and_zip merging pdfs now")

#     try:
#         kafka_producer = JSONProducer(client_id=MERGE_NOTICE_CLIENT_ID)
#         logger.debug(
#             "app.tasks.notice.notice_callback.commons.create_merge_pdf_and_zip || Notice_merge producer initialised"
#         )
#         await kafka_producer.start()
#         logger.debug(
#             "app.tasks.notice.notice_callback.commons.create_merge_pdf_and_zip || Notice_merge producer started"
#         )
#     except Exception as e:
#         logger.error(
#             f"app.tasks.notice.notice_callback.commons.create_merge_pdf_and_zip || kafkaProducer.err :: {str(e)}"
#         )
#         logger.error(
#             "app.tasks.notice.notice_callback.commons.create_merge_pdf_and_zip || Messages won't be produced to merge_pdf topic"
#         )
#         return notice_id_merged_file_name_mapping

#     # CREATE EVENTS FOR MERGE NOTICE HERE ---
#     try:
#         remaining_tasks_count_key = f"{batch_id}_remaining_tasks"
#         merge_pdf_success_redis_key = f"{batch_id}_merge_pdf_success"

#         redis_ = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#         # adding "~" because of namespace at cg_redis on notice_merge consumer end
#         redis_.set("~" + remaining_tasks_count_key, len(merge_file_list_batches))
#         redis_.set("~" + merge_pdf_success_redis_key, 1)

#         logger.debug(
#             "app.tasks.notice.notice_callback.commons.create_merge_pdf_and_zip || Writing messages for notice_merge topic"
#         )
#         merged_pdf_count = len(merge_file_list_batches)
#         for idx, notice_ids_to_merged in enumerate(merge_file_list_batches):
#             merged_file_name = notice_id_merged_file_name_mapping[notice_ids_to_merged[0]].strip()
#             message = {
#                 "notice_ids_to_merged": notice_ids_to_merged,
#                 "local_pdf_directory_path": local_pdf_directory_path,
#                 "local_merged_pdf_directory_path": local_merged_pdf_directory_path,
#                 "local_zip_file_path": local_merged_pdf_zip_file_path,
#                 "merged_file_name": merged_file_name,
#                 "total_files": merged_pdf_count,
#                 "local_batch_directory_path": local_batch_directory_path,
#                 "batch_id": batch_id,
#                 "notice_type": notice_type,
#                 "zip_file_name": "physical_notice_zip/" + merged_lot_zip_name,
#                 "batch_name": batch_name,
#                 "remaining_tasks_count": remaining_tasks_count_key,
#                 "merge_pdf_success_redis_key": merge_pdf_success_redis_key,
#                 "request_id": request_id,
#                 "user": kwargs.get("user"),
#                 "company": kwargs.get("company"),
#                 "merge_called_through_kafka": False,
#             }
#             await kafka_producer.send(
#                 topic=MERGE_NOTICE_TOPIC,
#                 value=message,
#                 partition=idx % int(NUMBER_OF_PARTITIONS_FOR_MERGE_NOTICE_TOPIC),
#             )

#         await kafka_producer.stop()
#     except Exception as e:
#         logger.error(
#             f"app.tasks.notice.notice_callback.commons.create_merge_pdf_and_zip || Error while producing message or writing to topic :: {str(e)}"
#         )

#     return notice_id_merged_file_name_mapping


# def format_batch_name(batch_name):
#     logger.info("tasks.notice.notice_callback.commons.format_batch_name")
#     special_characters = ["!", "-", "_", ".", "*", "'", "(", ")"]
#     new_batch_name = ""
#     replace_character = MERGE_FILE_NAME_REPLACE_CHARACTER
#     for i in batch_name:
#         if (
#             not ((i >= "a" and i <= "z") or (i >= "A" and i <= "Z") or (i >= "0" and i <= "9"))
#             and i not in special_characters
#         ):
#             new_batch_name += replace_character
#         else:
#             new_batch_name += i
#     return new_batch_name
