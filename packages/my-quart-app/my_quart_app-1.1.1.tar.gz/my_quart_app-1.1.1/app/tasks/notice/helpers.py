# import json
# import logging
# import redis
# import requests


# from ...utils import get_s3_client
# from ...settings import (
#     REDIS,
#     QUEUE_SERVICE_BASE_URL,
# )

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# redis_conf = REDIS
# redis_obj = redis.Redis(host=redis_conf["HOST"], port=redis_conf["PORT"])

# s3 = get_s3_client()


# def logs_tracker(response, request_id):
#     url = f"{QUEUE_SERVICE_BASE_URL}/save_batch_response"
#     user = response.get("kwargs").get("user")
#     company = response.get("kwargs").get("company")
#     response_kwargs = response["kwargs"]
#     batch_id = response_kwargs["batch_id"]
#     req_body = {
#         "response": {
#             "response": json.dumps(response["response"]),
#             "batch_id": str(batch_id),
#             "status": str(response["status"]),
#             "status_code": str(response["status_code"]),
#             "loan_id": str(response_kwargs["loan_id"]),
#             "company_id": company["company_id"],
#         },
#         "payload": {"batch_id": batch_id, "type": "notice"},
#     }
#     try:
#         res = requests.request(
#             method="POST",
#             url=url,
#             json=req_body,
#             headers={
#                 "Content-Type": "application/json",
#                 "X-Request-Id": request_id,
#                 "X-CG-User": json.dumps(user),
#                 "X-CG-Company": json.dumps(company),
#             },
#         )
#         logger.info(f"physical_notice_generation.execution_response_update.status_code :: {res.status_code}")
#         logger.debug(f"helper.logs_tracker.res : {res.text}")
#     except Exception as e:
#         logger.info(f"physical_notice_generation.execution_response_update.exception :: {str(e)}")
#         return False
#     if res.status_code not in (200, 201):
#         logger.info(f"physical_notice_generation.execution_response_update.status :: str({res.text})")
#         return False
#     return True


# def map_formatter(loan_address_map, address_file_map, files_s3_map):
#     logger.info("notice.map_formatter")

#     final_map_list = []
#     for loan_id, address_list in loan_address_map.items():
#         # https://credgenics.atlassian.net/browse/POD2-1691
#         # creating address_set here to make sure that the notices on the same combination of ("Name1 X Property Address1") are not duplicated in the report
#         address_set = set()
#         for addresses in address_list:
#             address = addresses[0]
#             if address in address_set:
#                 continue
#             else:
#                 address_set.add(address)
#             if address_file_map.get(address):
#                 final_map = {}
#                 final_map["loan_id"] = loan_id
#                 filename = address_file_map[address].get("filename")
#                 final_map["local_pdf_file_name"] = filename
#                 final_map["primary_address"] = address_file_map[address].get("primary_address")
#                 final_map["tracking_id"] = address_file_map[address].get("tracking_id")
#                 final_map["s3_link_uuid"] = files_s3_map.get(filename, ["", ""])[0]
#                 final_map["s3_link"] = files_s3_map.get(filename, ["", ""])[1]
#                 final_map["created"] = str(address_file_map[address].get("created"))
#                 final_map["borrower_type"] = addresses[1]
#                 final_map["notice_id"] = str(address_file_map[address].get("notice_id"))
#                 final_map["address_type"] = addresses[2]
#                 final_map_list.append(final_map)
#     return final_map_list


# def get_draft_fields(**kwargs):
#     logger.info("tasks.notice.helper.get_draft_fields")
#     local_batch_directory_path = kwargs["local_batch_directory_path"]
#     local_draft_file_path = kwargs["local_draft_file_path"]
#     BUCKET_NAME = kwargs["BUCKET_NAME"]
#     company_id = kwargs["company_id"]
#     draft_id = kwargs["draft_id"]
#     os.makedirs(local_batch_directory_path, exist_ok=True)

#     try:
#         s3.download_file(
#             BUCKET_NAME,
#             "drafts/" + str(company_id) + "/" + draft_id + ".docx",
#             local_draft_file_path,
#         )
#     except Exception as e:
#         logger.error(f"tasks.notice.helpers.get_draft_fields.download_exception: {str(e)}")
#         return "Unable to download draft from s3"

#     if os.path.exists(local_draft_file_path):
#         try:
#             document = MailMerge(local_draft_file_path)
#             draft_fields = list(document.get_merge_fields())
#             document.close()
#             return {draft_id: draft_fields}
#         except Exception as e:
#             logger.error(f"get_draft_fields.mailmerge_exception: {str(e)}")
#             return f"get_draft_fields.mailmerge_exception: {str(e)}"
#     else:
#         logger.debug(f"get_draft_fields.local_path_err: Draft not present at location {local_draft_file_path}")
#         return f"Draft not present at location {local_draft_file_path}"


# def make_notice_doc_file(**kwargs):
#     logger.info("notice.helpers.make_notice_doc_file")
#     logger.info(f"tasks.notice.make_notice_doc_file.batch_id :: {kwargs['batch_id']}")

#     data = kwargs["notice_data"]
#     changed_dt = data["changed_dt"]
#     loan_id = changed_dt["loan_ids"]
#     table_dict = data.get("master_table_dict", "")
#     index = kwargs.get("index", "")
#     local_draft_file_path = kwargs["local_draft_file_path"]
#     local_doc_directory_path = kwargs["local_doc_directory_path"]
#     local_pdf_directory_path = kwargs["local_pdf_directory_path"]
#     local_qr_code_directory_path = kwargs["local_qr_code_directory_path"]
#     local_merged_pdf_directory_path = kwargs["local_merged_pdf_directory_path"]
#     notice_id = kwargs.get("notice_id", "")
#     type_of_task = kwargs["type_of_task"]

#     try:
#         if not os.path.exists(local_draft_file_path):
#             logger.error(f"notice.make_notice_doc_file.local_draft_file_path.err : local draft file doesn't exist")
#             raise Exception(f"Could not locate draft on the local file system")

#         # Axis bank condition
#         if kwargs["company_id"] == "d2d50f3e-4b79-40d7-b9dd-6cadb0b30141" and changed_dt["loan_type"] in [
#             "Credit Card"
#         ]:
#             changed_dt["loan_id"] = changed_dt["credit_card_number"]

#         document = MailMerge(local_draft_file_path)

#         if table_dict:
#             for key, val in table_dict.items():
#                 document.merge_rows(key, val)

#         if type_of_task == "physical":
#             changed_dt["notice_id"] = str(notice_id)

#         document.merge(**changed_dt)

#         os.makedirs(local_doc_directory_path, exist_ok=True)
#         os.makedirs(local_pdf_directory_path, exist_ok=True)
#         os.makedirs(local_qr_code_directory_path, exist_ok=True)

#         if local_merged_pdf_directory_path:
#             os.makedirs(local_merged_pdf_directory_path, exist_ok=True)

#         if type_of_task == "digital":
#             if kwargs.get("linked_loan_id"):
#                 loan_id = kwargs["linked_loan_id"]
#             loan_id = loan_id.replace("/", "_") if "/" in loan_id else loan_id
#             filename = loan_id.strip().replace(" ", "_") + "_" + str(index)
#         elif type_of_task == "physical":
#             filename = str(notice_id).strip().replace(" ", "_")

#         input_file = os.path.join(local_doc_directory_path, f"{filename}.docx")
#         output_file = os.path.join(local_pdf_directory_path, f"{filename}.pdf")

#         document.write(input_file, kwargs.get("is_vernacular", ""))
#         document.close()

#         notice_file_data = {
#             "input_file_path": input_file,
#             "output_file_path": output_file,
#             "filename": filename,
#         }
#         logger.debug(f"helpers.make_notice_doc_file.notice_file_data : {notice_file_data}")
#         return notice_file_data
#     except Exception as e:
#         raise Exception(f"make_notice_doc_file.exception: {str(e)}")


# def doc2pdf_converter(output_folder, **kwargs):
#     logger.info("notice.doc2pdf_converter")
#     logger.info(f"tasks.notice.doc2pdf_converter.batch_id :: {kwargs['batch_id']}")
#     logger.debug(
#         f"input_file: '{kwargs['input_file']}', output_file: '{kwargs['output_file']}', author: '{kwargs['author']}'"
#     )

#     author = kwargs["author"]
#     input_file, output_file = kwargs["input_file"], kwargs["output_file"]

#     random_instance_id = uuid.uuid4().hex
#     try:
#         os.makedirs(output_folder, exist_ok=True)
#         folder = output_folder
#         # random_instance_number = random.randint(0,10000000000000000)

#         # cmd_output = run(
#         #     [
#         #         "/Applications/LibreOffice.app/Contents/MacOS/soffice",
#         #         f"-env:UserInstallation=file:///tmp/LibreOffice_Conversion_{random_instance_id}{author}",
#         #         "--headless",
#         #         "--convert-to",
#         #         "pdf:writer_pdf_Export",
#         #         "--outdir",
#         #         f"{folder}",
#         #         f"{input_file}",
#         #     ],
#         #     capture_output=True,
#         # )

#         cmd_output = run(
#             [
#                 "soffice",
#                 f"-env:UserInstallation=file:///tmp/LibreOffice_Conversion_{random_instance_id}{author}",
#                 "--headless",
#                 "--convert-to",
#                 "pdf:writer_pdf_Export",
#                 "--outdir",
#                 f"{folder}",
#                 f"{input_file}",
#             ],
#             capture_output=True,
#         )

#         stdout, stderr = cmd_output.stdout, cmd_output.stderr
#         try:
#             shutil.rmtree(f"/tmp/LibreOffice_Conversion_{random_instance_id}{author}")
#         except Exception as e:
#             logger.error(f"soffice env removal error - {e}")

#         if stderr:
#             logger.error(f"doc2pdf_converter.stderr: {stderr}")
#             logger.debug(f"doc2pdf_converter.stdout: {stdout}")
#             if "source file" in str(stderr):
#                 raise Exception(f"stderr - {stderr}")

#         if not stdout:
#             raise Exception(f"no stdout err- {stderr}")

#         if not os.path.exists(output_file):
#             logger.error("doc2pdf_converter.err : Abort Code:27 error")
#             raise Exception("Abort Code:27 error, output_file doesn't exist")
#     except Exception as e:
#         logger.error(f"doc2pdf_converter.exception: {str(e)}, random_instance_id :: {random_instance_id}")
#         raise Exception(f"doc2pdf_converter.exception: {str(e)}")


# def get_dsc_on_notice_pdf(**kwargs):
#     logger.info("notice.get_dsc_on_notice_pdf")
#     logger.info(f"tasks.notice.get_dsc_on_notice_pdf.batch_id :: {kwargs['batch_id']}")

#     pdf_file_path = kwargs["output_file"]
#     dsc_placement = kwargs["dsc_placement"]
#     filename_with_extension = pdf_file_path.split("/")[-1]
#     filename = filename_with_extension.split(".pdf")[0]

#     try:
#         with open(pdf_file_path, "rb") as pdf_file:
#             encoded_string = base64.b64encode(pdf_file.read())

#         timestamp = datetime.now().strftime("%d%m%Y%H:%M:%S")
#         cs = hashlib.md5(f"{TRUECOPY_API_KEY}{timestamp}".encode()).hexdigest()[0:16]

#         url = TRUECOPY_BASE_URL

#         headers = {
#             "Content-Type": "application/json",
#         }

#         if dsc_placement == "all":
#             dsc_placement_value = "[410:110]"
#         elif dsc_placement == "signature":
#             dsc_placement_value = "[410:110]"
#         else:
#             return False

#         req_payload = {
#             "pfxid": TRUECOPY_ID,
#             "pfxpwd": TRUECOPY_PWD,
#             "accessid": TRUECOPY_ACCESS_ID,
#             "timestamp": timestamp,
#             "cs": cs,
#             "filename": filename + "_signed.pdf",
#             "signloc": dsc_placement_value,
#             "filepwd": "",
#             "contents": encoded_string,
#         }

#         response = requests.post(url=url, json=req_payload, headers=headers, timeout=300)
#         encoded_response = response.text
#         logger.debug(f"True copy api response status code: {response.status_code}")
#         if response.status_code != 200:
#             logger.debug(f"True copy api response: {response.text}")
#         b64_decoded_response = base64.b64decode(encoded_response, validate=True)
#         pdf_file = open(pdf_file_path, "wb")
#         pdf_file.write(b64_decoded_response)
#         pdf_file.close()
#     except Exception as e:
#         logger.error(f"notice.helpers.get_dsc_on_notice_pdf.exception :: {str(e)}")
#         raise Exception(f"notice.helpers.get_dsc_on_notice_pdf.exception :: {str(e)}")


# def generate_notice_for_all_addresses(**kwargs):
#     logger.info("notice.generate_notice_for_all_addresses")
#     logger.info(f"notice.generate_notice_for_all_addresses.batch_id :: {kwargs['batch_id']}")

#     preview = kwargs.get("preview", False)
#     notice_data = kwargs.get("notice_data", "")
#     master_table_dict = notice_data["master_table_dict"]
#     duplicated_tables_dict = notice_data["duplicated_tables_dict"]
#     local_pdf_directory_path = kwargs["local_pdf_directory_path"]
#     address_file_map = kwargs["address_file_map"]
#     draft_fields = kwargs.get("draft_fields", [])
#     table_1_fields = []

#     for i in range(len(draft_fields)):
#         if "table_1" in draft_fields[i]:
#             table_1_fields.append(draft_fields[i])

#     index_p = 0
#     tracking_ids_batch = []
#     failed_tracking_id_list = []

#     # total_length = 0

#     # for key, val in master_table_dict.items():
#     #     list_len = len(val)
#     #     total_length += list_len

#     address_tables = kwargs["notice_data"]["address_tables"]
#     if "property" in address_tables:
#         address_tables.remove("property")
#     if "auctioned" in address_tables:
#         address_tables.remove("auctioned")
#     borrower_address_count = 0
#     for key, value in master_table_dict.items():
#         borrower_type = key.split("_")[4]
#         if borrower_type == "co":
#             borrower_type += "_applicant"
#         if borrower_type in address_tables:
#             borrower_address_count += len(value)

#     redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#     next_initial_notice_id = redis_instance.incrby(kwargs["initial_notice_id_redis_key"], borrower_address_count)
#     redis_instance.close()

#     initial_notice_id = next_initial_notice_id - 1
#     notice_id_list = [
#         notice_id for notice_id in range(initial_notice_id - borrower_address_count + 1, next_initial_notice_id)
#     ]
#     total_length = len(notice_id_list)
#     failed_tracking_ids_key = f'failed_tracking_id_{kwargs.get("batch_id","")}'

#     if kwargs["use_tracking_ids"]:
#         for i in range(total_length):
#             physical_notice_trackings_ids_redis_key = kwargs.get("physical_notice_trackings_ids_redis_key", "")
#             tracking_id = get_next_tracking_id(physical_notice_trackings_ids_redis_key)
#             if tracking_id:
#                 tracking_ids_batch.append(tracking_id)
#             else:
#                 break

#         if total_length != len(tracking_ids_batch):
#             logger.error(f"notice.generate_notice_for_all_addresses.tracking_ids.err : Not enough tracking ids")
#             return f"Insufficient tracking ids. Atleast required: {total_length}", notice_id_list, tracking_ids_batch

#     try:
#         for key, val in master_table_dict.items():
#             table_reference = key.split("_", 2)
#             table_reference = table_reference[0] + "_" + table_reference[1]
#             if table_reference == "table_1":
#                 primary_cell = key
#                 break

#         file_name_sequence_counter = total_length

#         notice_id = initial_notice_id
#         for key in reversed(master_table_dict):
#             val = master_table_dict[key]

#             if val:
#                 val.reverse()
#             table_reference = key.split("_", 2)
#             table_reference = table_reference[0] + "_" + table_reference[1]

#             borrower_type = key.split("_", 4)[-1].split("_", 1)[0]
#             if borrower_type == "co":
#                 borrower_type = "co_applicant"
#             borrower_type += "_"

#             primary_address_dt = {}
#             temp_address = {}
#             length = len(val) if val else 0
#             for index in range(length):
#                 tracking_id = ""
#                 for k, v in val[index].items():
#                     if table_reference in k and v not in [None, ""]:
#                         temp = k.split(borrower_type)
#                         try:
#                             temp = temp[0] + temp[1]
#                         except:
#                             temp = temp[0]
#                         temp = temp.replace(table_reference, "table_1")
#                         primary_address_dt[temp] = v
#                 empty_fields = 0
#                 for i in range(len(table_1_fields)):
#                     if primary_address_dt.get(table_1_fields[i], "") == "":
#                         empty_fields += 1
#                 if len(table_1_fields) == empty_fields:
#                     file_name_sequence_counter -= 1
#                     continue
#                 temp_address = val[index]
#                 val.pop(index)

#                 barcode = "(" + tracking_ids_batch[index_p] + ")" if tracking_ids_batch else ""
#                 primary_address_dt["barcode"] = barcode
#                 tracking_id = tracking_ids_batch[index_p] if tracking_ids_batch else ""
#                 master_table_dict[primary_cell].append(primary_address_dt)
#                 if len(str(file_name_sequence_counter)) != len(str(total_length)):
#                     total_length_temp = str(total_length)
#                     file_name_sequence_counter_temp = str(file_name_sequence_counter)
#                     diff = abs(len(total_length_temp) - len(file_name_sequence_counter_temp))
#                     file_name_sequence_counter_temp = "0" * diff + file_name_sequence_counter_temp
#                 else:
#                     file_name_sequence_counter_temp = str(file_name_sequence_counter)

#                 kwargs["index"] = file_name_sequence_counter_temp
#                 kwargs["notice_data"]["master_table_dict"] = master_table_dict | duplicated_tables_dict
#                 kwargs["notice_id"] = notice_id
#                 notice_file_data = make_notice_doc_file(**kwargs)
#                 file_name_sequence_counter -= 1

#                 notice_id -= 1
#                 input_file, output_file, filename = (
#                     notice_file_data["input_file_path"],
#                     notice_file_data["output_file_path"],
#                     notice_file_data["filename"],
#                 )
#                 kwargs["input_file"] = input_file
#                 kwargs["output_file"] = output_file
#                 output_folder = local_pdf_directory_path

#                 if kwargs.get("enable_qrcode", False):
#                     generate_qrcode_doc(**kwargs)

#                 doc2pdf_converter(output_folder, **kwargs)
#                 make_even_pages(output_file, filename, local_pdf_directory_path)

#                 kwargs["tracking_ids"] += tracking_ids_batch
#                 # redis_instance.lpush(failed_tracking_ids_key, *tracking_ids_batch)
#                 # return res, notice_id_list
#                 kwargs["filenames"].append(output_file)
#                 filename = filename + ".pdf"
#                 kwargs["local_pdf_file_names"].append(filename)
#                 kwargs["primary_addresses"].append(json.dumps(primary_address_dt))

#                 if preview:
#                     return "success", notice_id_list, failed_tracking_id_list

#                 primary_address_text = primary_address_dt.get("table_1_address_text", "")
#                 primary_name = primary_address_dt.get("table_1_cell_1_name", "")
#                 primary_key = primary_name + primary_address_text

#                 if not address_file_map.get(primary_key):
#                     address_file_map[primary_key] = {
#                         "filename": filename,
#                         "primary_address": json.dumps(primary_address_dt),
#                         "tracking_id": tracking_id,
#                         "created": datetime.now(),
#                         "notice_id": kwargs["notice_id"],
#                     }
#                 else:
#                     address_file_map[primary_key] = {
#                         "filename": filename,
#                         "primary_address": json.dumps(primary_address_dt),
#                         "tracking_id": tracking_id,
#                         "created": datetime.now(),
#                         "notice_id": kwargs["notice_id"],
#                     }

#                 primary_address_dt.clear()
#                 val.insert(index, temp_address)
#                 master_table_dict[primary_cell].pop()
#                 index_p += 1

#         kwargs["address_file_map"] = address_file_map
#         kwargs["tracking_ids"] += tracking_ids_batch
#         return "success", notice_id_list, tracking_ids_batch
#     except Exception as e:
#         logger.error(f"generate_notice_for_all_addresses.exception: {str(e)}")
#         failed_tracking_id_list = tracking_ids_batch
#         return str(e), notice_id_list, failed_tracking_id_list


# def get_next_tracking_id(redis_key):
#     logger.info(f"notice.helpers.get_next_tracking_id")
#     redis_ = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#     id = redis_.lpop(redis_key)
#     if id:
#         id = id.decode("utf-8")
#     else:
#         id = ""
#     logger.debug(f"get_next_tracking_id.id: {id}")
#     return id


# def make_even_pages(filepath, filename, local_pdf_directory_path):
#     logger.info(f"notice.helpers.make_even_pages")

#     logger.debug(f"{filepath}, {filename},{local_pdf_directory_path}")
#     pdf = PyPDF2.PdfFileReader(open(filepath, "rb"))
#     no_of_pages = pdf.getNumPages()
#     if no_of_pages % 2 != 0:
#         outPdf = PyPDF2.PdfFileWriter()
#         outPdf.appendPagesFromReader(pdf)
#         outPdf.addBlankPage()
#         temp_file = os.path.join(local_pdf_directory_path, f"temp_{filename}.pdf")
#         outPdf.write(open(temp_file, "wb"))
#         shutil.copyfile(temp_file, filepath)
#         os.remove(temp_file)
#     return


# def get_directory_and_file_paths(**kwargs):
#     volume_mount_directory = NOTICE_VOLUME_MOUNT_DIRECTORY
#     preview = kwargs.get("preview", False)

#     if preview:
#         local_batch_directory_path = os.path.join(volume_mount_directory, "previews", kwargs["batch_id"])
#     else:
#         local_batch_directory_path = os.path.join(volume_mount_directory, "batches", kwargs["batch_id"])

#     local_draft_file_path = os.path.join(local_batch_directory_path, f'{kwargs["draft_id"]}.docx')
#     local_doc_directory_path = os.path.join(local_batch_directory_path, "docs")
#     local_pdf_directory_path = os.path.join(local_batch_directory_path, "pdfs")
#     local_qr_code_directory_path = os.path.join(local_batch_directory_path, "qrcodes")
#     local_merged_pdf_directory_path = os.path.join(local_batch_directory_path, "merged_pdf")
#     local_merged_pdf_zip_file_path = os.path.join(local_batch_directory_path, "compressed_merged_lot")
#     return (
#         local_batch_directory_path,
#         local_draft_file_path,
#         local_doc_directory_path,
#         local_pdf_directory_path,
#         local_qr_code_directory_path,
#         local_merged_pdf_directory_path,
#         local_merged_pdf_zip_file_path,
#     )


# def generate_qrcode_doc(**kwargs):
#     logger.info(f"tasks.notice.generate_qrcode_doc.batch_id :: {kwargs['batch_id']}")
#     try:
#         input_doc_file_path = kwargs["input_file"]
#         doc_filename = input_doc_file_path.split("/")[-1].rstrip(".docx")
#         changed_dt = kwargs["notice_data"]["changed_dt"]
#         payment_link = changed_dt.get("payment_link", None)
#         local_qr_code_directory_path = kwargs["local_qr_code_directory_path"]

#         if payment_link:
#             qr_code_file_path = os.path.join(local_qr_code_directory_path, f"{doc_filename}.png")
#             doc_file = docx.Document(input_doc_file_path)
#             qr_code = pyqrcode.create(payment_link)
#             qr_code.png(qr_code_file_path, scale=5)
#             doc_file.add_picture(qr_code_file_path)
#             last_paragraph = doc_file.paragraphs[-1]
#             last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
#             doc_file.save(input_doc_file_path)
#         else:
#             raise Exception("Missing payment_link")
#     except Exception as e:
#         raise Exception(f"generate_qrcode_doc.exception: {str(e)}")
