# import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# @shared_task(bind=True, name="assign_generate_notice_preview_queue")
# def assign_generate_notice_preview_queue(self, *args, **kwargs):
#     logger.info("assign_generate_notice_preview_queue")
#     redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])

#     logger.debug(f"assign_generate_notice_preview_queue.kwargs: {kwargs}")

#     queue = kwargs["queue"]
#     mode = kwargs["mode"]
#     batch_id = kwargs["batch_id"]

#     if mode == "digital":
#         type_of_task = "digital"
#     else:
#         type_of_task = "physical"
#         initial_notice_id_redis_key = f"initial_notice_id_redis_key_{batch_id}"
#         redis_instance.setex(initial_notice_id_redis_key, 24 * 60 * 60, json.dumps(1001))

#     if kwargs.get("linked_loans"):
#         linked_loan = kwargs["linked_loans"][0]
#         loan_ids = linked_loan.get("loan_ids", [])
#     else:
#         loan_ids = kwargs["loan_ids"]

#     physical_notice_trackings_ids_redis_key = ""
#     tasks = []

#     task_kwargs = {
#         "company_id": kwargs["company_id"],
#         "draft_id": kwargs["draft_id"],
#         "draft_details": kwargs["draft_details"],
#         "loan_ids": loan_ids,
#         "allocation_month": kwargs["allocation_month"],
#         "author": kwargs["author"],
#         "token": kwargs["token"],
#         "mode": kwargs["mode"],
#         "role": kwargs["role"],
#         "queue": queue,
#         "batch_id": batch_id,
#         "batch_number": kwargs["batch_number"],
#         "total_batches": 1,
#         "type_of_task": type_of_task,
#         "total_loans": 1,
#         "document_type": kwargs["document_type"],
#         "physical_notice_trackings_ids_redis_key": physical_notice_trackings_ids_redis_key,
#         "X-Request-Id": kwargs["X-Request-Id"],
#         "s3_link_uuid": kwargs["s3_link_uuid"],
#         "preview": True,
#         "user": kwargs["user"],
#         "linked_loan": linked_loan if kwargs.get("linked_loans") else {},
#         "is_linked_loan": kwargs["is_linked_loan"],
#         "request_id": kwargs["request_id"],
#         "local_batch_directory_path": kwargs["local_batch_directory_path"],
#         "local_draft_file_path": kwargs["local_draft_file_path"],
#         "local_doc_directory_path": kwargs["local_doc_directory_path"],
#         "local_pdf_directory_path": kwargs["local_pdf_directory_path"],
#         "local_pdf_directory_path": kwargs["local_pdf_directory_path"],
#         "local_qr_code_directory_path": kwargs["local_qr_code_directory_path"],
#         "local_merged_pdf_directory_path": kwargs["local_merged_pdf_directory_path"],
#         "local_merged_pdf_zip_file_path": kwargs["local_merged_pdf_zip_file_path"],
#         "BUCKET_NAME": kwargs["BUCKET_NAME"],
#         "draft_fields_redis_key": kwargs["draft_fields_redis_key"],
#         "company": kwargs["company"],
#         "initial_notice_id_redis_key": initial_notice_id_redis_key if mode == "physical" else None,
#         "enable_qrcode": kwargs["enable_qrcode"],
#     }

#     callback_kwargs = {
#         "queue": kwargs["queue"],
#         "batch_id": batch_id,
#         "batch_number": kwargs["batch_number"],
#         "company_id": kwargs["company_id"],
#         "token": kwargs["token"],
#         "role": kwargs["role"],
#         "draft_id": kwargs["draft_id"],
#         "type_of_task": type_of_task,
#         "author": kwargs["author"],
#         "user": kwargs["user"],
#         "request_id ": kwargs["X-Request-Id"],
#         "company": kwargs["company"],
#     }

#     task_kwargs = _dict_key_filter(task_kwargs, ["loan_ids", "linked_loan"])
#     redis_instance.setex(f"notice_kwargs_{batch_id}", 24 * 60 * 60, json.dumps(task_kwargs))
#     redis_instance.setex(f"callback_kwargs_{batch_id}", 24 * 60 * 60, json.dumps(callback_kwargs))
#     redis_instance.close()

#     if mode == "digital":
#         if kwargs["is_linked_loan"]:
#             tasks.append(handle_generate_digital_notice.s(**{"batch_id": batch_id, "linked_loan": linked_loan}))
#             chord(
#                 group(tasks),
#                 body=generate_digital_notice_preview_callback.s(batch_id=batch_id),
#             ).apply_async(queue=queue)
#         else:
#             tasks.append(handle_generate_digital_notice.s(**{"batch_id": batch_id, "loan_ids": loan_ids}))
#             chord(
#                 group(tasks),
#                 body=generate_digital_notice_preview_callback.s(batch_id=batch_id),
#             ).apply_async(queue=queue)

#     else:
#         if kwargs["is_linked_loan"]:
#             tasks.append(generate_physical_notices.s(**{"batch_id": batch_id, "linked_loan": linked_loan}))
#             chord(
#                 group(tasks),
#                 body=generate_physical_notice_preview_callback.s(batch_id=batch_id),
#             ).apply_async(queue=queue)
#         else:
#             tasks.append(generate_physical_notices.s(**{"batch_id": batch_id, "loan_ids": loan_ids}))
#             chord(
#                 group(tasks),
#                 body=generate_physical_notice_preview_callback.s(batch_id=batch_id),
#             ).apply_async(queue=queue)

#     return True
