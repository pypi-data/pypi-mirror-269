# import shutil
# from celery import shared_task
# import redis
# from app.settings import (
#     NOTICE_VOLUME_MOUNT_DIRECTORY,
#     REDIS,
#     S3_BUCKET_ENDPOINT,
#     S3_BUCKET_NAME,
#     QUEUE_SERVICE_BASE_URL,
# )
# from app.tasks.notice.notice_callback.commons import (
#     delete_redis_keys,
#     generate_notices_zip,
#     generate_failed_notices_report_excel,
#     generate_tracking_excel,
#     generate_tracking_excel_with_merged_pdf_file_mapping,
#     send_batch_completion_email,
#     upload_file_to_s3,
#     generate_unused_tracking_ids_excel,
#     get_batch_notices,
#     create_merge_pdf_and_zip,
# )

# from app.utils import get_s3_client
# import os
# import logging
# import requests
# import json
# import asyncio

# logger = logging.getLogger(__name__)


# @shared_task(bind=True, name="generate_physical_notices_batch_callback")
# def generate_physical_notices_batch_callback(self, *args, **kwargs):

#     redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#     callback_kwargs = json.loads(redis_instance.get(f"callback_kwargs_{kwargs['batch_id']}").decode("utf-8"))
#     redis_instance.close()

#     if not callback_kwargs:
#         logger.error(
#             f"notice_callback.generate_physical_notice_batch_callback.error: callback_kwargs not found on redis"
#         )
#         return False

#     kwargs = {**kwargs, **callback_kwargs}

#     logger.info(f"notice_callback.physical_notice.generate_physical_notices_batch_callback.kwargs: {kwargs}")

#     message_flag = False
#     try:
#         kwargs["X-Request-Id"] = kwargs["request_id"]
#         s3 = get_s3_client()

#         volume_mount_directory = NOTICE_VOLUME_MOUNT_DIRECTORY
#         local_batch_directory_path = os.path.join(volume_mount_directory, "batches", kwargs["batch_id"])

#         local_draft_file_path = os.path.join(local_batch_directory_path, f'{kwargs["draft_id"]}.docx')
#         local_doc_directory_path = os.path.join(local_batch_directory_path, "docs")
#         local_pdf_directory_path = os.path.join(local_batch_directory_path, "pdfs")
#         local_zip_file_path_without_format = os.path.join(local_batch_directory_path, "notices")
#         local_zip_file_path = local_zip_file_path_without_format + ".zip"
#         local_tracking_excel_file_path = os.path.join(local_batch_directory_path, "tracking.xlsx")
#         local_batch_report_file_path = os.path.join(local_batch_directory_path, "report.xlsx")
#         local_tracking_ids_excel_path = os.path.join(local_batch_directory_path, "tracking_ids.xlsx")

#         local_merged_pdf_directory_path = kwargs["local_merged_pdf_directory_path"]
#         local_merged_pdf_zip_file_path = kwargs["local_merged_pdf_zip_file_path"] + ".zip"

#         s3_zip_file_path = f"physical_notice_zip/{kwargs['batch_id']}.zip"
#         s3_zip_file_link = f"{S3_BUCKET_ENDPOINT}/{s3_zip_file_path}"

#         s3_tracking_excel_path = f"physical_notice_reports/tracking/{kwargs['batch_id']}.xlsx"
#         s3_tracking_excel_link = f"{S3_BUCKET_ENDPOINT}/{s3_tracking_excel_path}"

#         # temp fix for tracking report : with file name mapping
#         local_tracking_excel_file_with_merge_file_name_mapping_path = os.path.join(
#             local_batch_directory_path, "tracking_with_merge_file_name_mapping.xlsx"
#         )
#         s3_tracking_excel_with_merge_file_name_mapping_path = (
#             f"physical_notice_reports/tracking/{kwargs['batch_id']}_with_merge_file_name_mapping.xlsx"
#         )
#         s3_tracking_excel_with_merge_file_name_mapping_link = (
#             f"{S3_BUCKET_ENDPOINT}/{s3_tracking_excel_with_merge_file_name_mapping_path}"
#         )
#         kwargs[
#             "local_tracking_excel_file_with_merge_file_name_mapping_path"
#         ] = local_tracking_excel_file_with_merge_file_name_mapping_path
#         kwargs[
#             "s3_tracking_excel_with_merge_file_name_mapping_path"
#         ] = s3_tracking_excel_with_merge_file_name_mapping_path
#         kwargs[
#             "s3_tracking_excel_with_merge_file_name_mapping_link"
#         ] = s3_tracking_excel_with_merge_file_name_mapping_link

#         s3_report_batch_excel_path = f"physical_notice_reports/reports/{kwargs['batch_id']}.xlsx"
#         s3_report_batch_excel_link = f"{S3_BUCKET_ENDPOINT}/{s3_report_batch_excel_path}"
#         s3_tracking_ids_excel_path = f"physical_notice_reports/reports/{kwargs['batch_id']}_tracking_ids.xlsx"
#         s3_tracking_ids_excel_link = f"{S3_BUCKET_ENDPOINT}/{s3_tracking_ids_excel_path}"
#         batch_name = kwargs.get("batch_name")
#         batch_id = kwargs.get("batch_id")

#         kwargs["local_pdf_directory_path"] = local_pdf_directory_path
#         kwargs["local_zip_file_path"] = local_zip_file_path
#         kwargs["s3_zip_file_path"] = s3_zip_file_path
#         kwargs["s3_zip_file_link"] = s3_zip_file_link
#         kwargs["s3_tracking_excel_path"] = s3_tracking_excel_path
#         kwargs["s3_tracking_excel_link"] = s3_tracking_excel_link
#         kwargs["s3_report_batch_excel_path"] = s3_report_batch_excel_path
#         kwargs["s3_report_batch_excel_link"] = s3_report_batch_excel_link
#         kwargs["s3_tracking_ids_excel_path"] = s3_tracking_ids_excel_path
#         kwargs["s3_tracking_ids_excel_link"] = s3_tracking_ids_excel_link

#         notice_data = get_batch_notices(**kwargs)
#         if isinstance(notice_data, list):
#             notice_data = sorted(notice_data, key=lambda x: int(x["local_pdf_file_name"].split(".")[0]))
#         else:
#             logger.error(
#                 "notice_callback.physical_notice.generate_physical_notices_batch_callback || batch notices data couldn't be retrived"
#             )
#             raise Exception(
#                 "notice_callback.physical_notice.generate_physical_notices_batch_callback || batch notices data couldn't be retrived"
#             )

#         kwargs["notice_data"] = notice_data
#         merged_lot_size = kwargs.get("merged_lot_size", None)
#         notices_zip_generated = False
#         merging_process_success = False
#         count_of_notices = len(notice_data)

#         if batch_name:
#             merged_lot_zip_name = f"{batch_name}_{batch_id}_{count_of_notices}"
#         else:
#             merged_lot_zip_name = f"{batch_id}_{count_of_notices}"

#         s3_merged_pdf_zip_file_path = f"physical_notice_reports/merged_files/{merged_lot_zip_name}"
#         s3_merged_pdf_zip_file_link = f"{S3_BUCKET_ENDPOINT}/{s3_merged_pdf_zip_file_path}" + ".zip"
#         kwargs["s3_merged_pdf_zip_file_path"] = s3_merged_pdf_zip_file_path
#         kwargs["s3_merged_pdf_zip_file_link"] = s3_merged_pdf_zip_file_link

#         if len(notice_data):
#             if merged_lot_size:
#                 notice_id_merged_file_name_mapping = asyncio.run(create_merge_pdf_and_zip(**kwargs))
#                 logger.debug(
#                     "app.tasks.notice.notice_callback.physical_notice.generate_physical_notices_batch_callback || MERGE_NOTICE DONE"
#                 )
#                 if isinstance(notice_id_merged_file_name_mapping, bool):
#                     logger.error("couldn't create merge lot")
#                     merging_process_success = False
#                 else:
#                     logger.debug(
#                         f"notice_callback.notice_id_merged_file_name_mapping: {notice_id_merged_file_name_mapping}"
#                     )
#                     kwargs["notice_id_merged_file_name_mapping"] = notice_id_merged_file_name_mapping
#                     merging_process_success = True
#             notices_zip_generated = generate_notices_zip(
#                 local_pdf_directory_path=local_pdf_directory_path,
#                 local_zip_file_path=local_zip_file_path_without_format,
#             )
#             if notices_zip_generated:
#                 upload_file_to_s3(s3, local_zip_file_path, S3_BUCKET_NAME, s3_zip_file_path)
#                 kwargs["notices_zip_generated"] = True

#         if (notices_zip_generated) or (merged_lot_size and merging_process_success):
#             kwargs["file_path"] = local_tracking_excel_file_path
#             generate_tracking_excel(**kwargs)
#             upload_file_to_s3(
#                 s3,
#                 local_tracking_excel_file_path,
#                 S3_BUCKET_NAME,
#                 s3_tracking_excel_path,
#             )

#         kwargs["merging_process_success"] = merging_process_success

#         if merging_process_success:
#             generate_tracking_excel_with_merged_pdf_file_mapping(**kwargs)
#             upload_file_to_s3(
#                 s3,
#                 local_tracking_excel_file_with_merge_file_name_mapping_path,
#                 S3_BUCKET_NAME,
#                 s3_tracking_excel_with_merge_file_name_mapping_path,
#             )

#         # generate unused tracking ids excel
#         kwargs["local_tracking_ids_excel_path"] = local_tracking_ids_excel_path
#         local_tracking_ids_excel_file_generated_flag = generate_unused_tracking_ids_excel(**kwargs)
#         if local_tracking_ids_excel_file_generated_flag:
#             upload_file_to_s3(
#                 s3,
#                 local_tracking_ids_excel_path,
#                 S3_BUCKET_NAME,
#                 s3_tracking_ids_excel_path,
#             )
#         kwargs["local_tracking_ids_excel_file_generated_flag"] = local_tracking_ids_excel_file_generated_flag

#         kwargs["local_batch_report_file_path"] = local_batch_report_file_path
#         batch_report_data = generate_failed_notices_report_excel(**kwargs)
#         kwargs["batch_report_data"] = batch_report_data
#         if os.path.exists(local_batch_report_file_path):
#             upload_file_to_s3(
#                 s3,
#                 local_batch_report_file_path,
#                 S3_BUCKET_NAME,
#                 s3_report_batch_excel_path,
#             )
#         send_batch_completion_email(**kwargs)

#         url = f"{QUEUE_SERVICE_BASE_URL}/update_batch_response"
#         data = {
#             "batch_id": kwargs["batch_id"],
#             "s3_error_report_excel_path": s3_report_batch_excel_path,
#             "s3_batch_report_excel_path": s3_tracking_excel_path,
#         }
#         headers = {
#             "Content-Type": "application/json",
#             "X-CG-User": json.dumps(kwargs["user"]),
#             "X-Request-ID": kwargs["request_id"],
#             "X-CG-Company": json.dumps(kwargs["company"]),
#         }

#         update_response = requests.request(method="PATCH", url=url, json=data, headers=headers)
#         logger.debug(
#             "physical_notice.generate_physical_notices_batch_callback.update_batch_operations url: %s,status_code: %s",
#             url,
#             update_response.status_code,
#         )

#         if update_response.status_code != 200:
#             logger.error(
#                 "physical_notice.generate_physical_notices_batch_callback.update_batch_operations response: %s",
#                 update_response.text,
#             )

#         message_flag = True
#     except Exception as e:
#         logger.error(f"generate_physical_notices_batch_callback.global_exception : {str(e)}")
#     finally:
#         delete_redis_keys(kwargs["batch_id"])
#         return message_flag


# @shared_task(bind=True, name="generate_physical_notice_preview_callback")
# def generate_physical_notice_preview_callback(self, *args, **kwargs):
#     logger.info("generate_physical_notice_preview_callback")
#     logger.debug(f"generate_physical_notice_preview_callback.kwargs: {kwargs}")

#     volume_mount_directory = NOTICE_VOLUME_MOUNT_DIRECTORY
#     local_batch_directory_path = os.path.join(volume_mount_directory, "previews", kwargs["batch_id"])

#     shutil.rmtree(local_batch_directory_path, ignore_errors=True)
#     logger.debug(f"generate_physical_notice_preview_callback.dir_removal.info :{local_batch_directory_path} deleted")
#     delete_redis_keys(kwargs["batch_id"])

#     return True
