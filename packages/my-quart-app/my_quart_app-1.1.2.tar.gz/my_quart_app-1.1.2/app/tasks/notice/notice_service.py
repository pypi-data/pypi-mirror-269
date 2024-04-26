# import json
# from app.settings import NOTICE_SERVICE_BASE_URL, REDIS, NOTICE_COMPANIES_WITH_PROPERTY_ADDRESS_HANDLING
# import os
# import copy
# import random
# from datetime import datetime
# from num2words import num2words
# import logging
# import re
# from dateutil.parser import parse
# import string
# from app.tasks.notice.loan_service import get_borrower_language
# from app.utils import get_s3_client
# import requests
# import redis

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# s3 = get_s3_client()


# def get_notice_generation_data(**kwargs):
#     logger.info(f"tasks.notice.get_notice_generation_data.batch_id :: {kwargs['batch_id']}")

#     company_id = kwargs.get("company_id", "")
#     draft_id = kwargs.get("draft_id", "")
#     loan_ids = kwargs.get("loan_ids", "")
#     allocation_month = kwargs.get("allocation_month", "")
#     batch_number = kwargs.get("batch_number", "")
#     document_type = kwargs.get("document_type")
#     case_id = kwargs.get("case_id", "")
#     iteration = kwargs.get("iteration", "null")
#     stage_code = kwargs.get("stage_code", "null")
#     linked_loan_id = kwargs.get("linked_loan_id", "")

#     logger.debug(f"notice.get_notice_generation_data.kwargs : {kwargs}")

#     try:
#         master_table_dict = {}
#         table_dict_list = []
#         changed_dt_list = []
#         address_set = set()
#         address_tables = set()

#         loan_data = kwargs["loan_data"]

#         if loan_data:
#             for loan in loan_data:
#                 loan_id = loan.get("loan_id", "")
#                 question_dict = loan.get("question_dict", "")
#                 languages = get_borrower_language(question_dict)
#                 languages["draft_language"] = kwargs.get("language")
#                 allocation_month = question_dict.get("allocation_month", "")
#                 kwargs["allocation_month"] = allocation_month

#                 # axis_bank condition
#                 if company_id == "d2d50f3e-4b79-40d7-b9dd-6cadb0b30141" and question_dict["loan_type"] == "Credit Card":
#                     question_dict["loan_id"] = question_dict.get("credit_card_number", "")
#                     loan_id = question_dict.get("credit_card_number", "")

#                 kwargs["loan_id"] = loan_id
#                 kwargs["question_dict"] = question_dict
#                 para_table_list = get_para_table_dicts(address_set, address_tables, **kwargs)
#                 if isinstance(para_table_list, str):
#                     return para_table_list
#                 changed_dt, table_dict = para_table_list[0], para_table_list[1]
#                 table_dict_list.append(table_dict)
#                 changed_dt_list.append(changed_dt)
#         else:
#             logger.error("get_notice_generation_data.exception: Cannot find data for the given loan")
#             raise Exception("Cannot find data for the given loan")

#         for i in range(len(table_dict_list)):
#             for key, val in table_dict_list[i].items():
#                 if key not in master_table_dict:
#                     master_table_dict[key] = table_dict_list[i][key]
#                 else:
#                     master_table_dict[key].extend(table_dict_list[i][key])

#         is_master_table_dict_empty = True

#         for key, val in master_table_dict.items():
#             if len(val) != 0:
#                 is_master_table_dict_empty = False

#         master_table_dict_list = duplicate_table_populator(master_table_dict, kwargs["draft_fields"])
#         master_table_dict = master_table_dict_list[0]
#         duplicated_tables_dict = master_table_dict_list[1]

#         if kwargs["mode"] == "physical" and is_master_table_dict_empty:
#             logger.error(
#                 "get_notice_generation_data.exception: Either draft does not have address tables or loan doesn't have addresses"
#             )
#             raise Exception("Either draft does not have address tables or loan doesn't have addresses")

#         if kwargs["is_linked_loan"]:
#             loan_ids = ", ".join(loan_ids)
#         else:
#             # For normal loan, we get list of one loan_id so we need to extract this
#             loan_ids = str(loan_ids[0])

#         kwargs["loan_ids"] = loan_ids
#         changed_dt["loan_ids"] = loan_ids

#         notice_data = {
#             "changed_dt": changed_dt,
#             "draft_id": draft_id,
#             "batch_number": batch_number,
#             "document_type": document_type,
#             "notice_type": kwargs.get("notice_type", ""),
#             "case_type": kwargs.get("case_type", ""),
#             "case_id": case_id,
#             "iteration": iteration,
#             "stage_code": stage_code,
#             "is_in_case": kwargs.get("is_in_case", ""),
#             "master_table_dict": master_table_dict,
#             "duplicated_tables_dict": duplicated_tables_dict,
#             "linked_loan_id": linked_loan_id,
#             "languages": languages,
#             "address_set": address_set,
#             "address_tables": address_tables,
#         }
#         return notice_data
#     except Exception as e:
#         raise Exception(f"get_notice_generation_data.exception :: {str(e)}")


# def if_duplicated_table(table_wise_keys, source_key, dup_key):
#     logger.info(f"notice.if_duplicated_table")
#     source_key_identifier = source_key.split("_")[0] + "_" + source_key.split("_")[1]
#     dup_key_identifier = dup_key.split("_")[0] + "_" + dup_key.split("_")[1]
#     return True if table_wise_keys[source_key_identifier] == table_wise_keys[dup_key_identifier] else False


# def duplicate_table_populator(master_table, draft_fields):
#     logger.info(f"notice_service.duplicate_table_populator")
#     table_wise_keys = {}
#     for key, val in master_table.items():
#         table_identifier = key.split("_", 2)[0] + "_" + key.split("_", 2)[1]
#         for j in range(len(draft_fields)):
#             if not table_wise_keys.get(table_identifier):
#                 table_wise_keys[table_identifier] = []
#             if table_identifier in draft_fields[j]:
#                 merge_field = draft_fields[j]
#                 merge_field = (
#                     merge_field.split("_", 4)[-1] if "cell_1" in merge_field else merge_field.split("_", 2)[-1]
#                 )
#                 table_wise_keys[table_identifier].append(merge_field)

#     for key, val in table_wise_keys.items():
#         table_wise_keys[key].sort()
#     keys = {}
#     for key, val in master_table.items():
#         table_name = key.split("_", 4)[-1]
#         if keys.get(table_name):
#             if if_duplicated_table(table_wise_keys, keys[table_name][-2], key):
#                 keys[table_name].insert(-1, key)
#                 keys[table_name][-1] += 1
#         else:
#             keys[table_name] = [key, 1]

#     new_master_table = {}
#     for key, val in keys.items():
#         if val[-1] > 1:
#             source_table = master_table.get(val[0])
#             source_key = val[0]
#             source_table_identifier = source_key.split("_", 2)[0]
#             dups_table = val[1:-1]
#             for i in range(len(dups_table)):
#                 new_master_table[dups_table[i]] = copy.deepcopy(source_table)
#                 del master_table[dups_table[i]]
#                 dup_table_identifier = dups_table[i].split("_", 2)[0]
#                 for index in range(len(new_master_table[dups_table[i]])):
#                     rows = new_master_table[dups_table[i]][index]
#                     for field, value in rows.items():
#                         if source_table_identifier in field:
#                             new_field = field.split(source_table_identifier + "_")[-1]
#                             new_field = dup_table_identifier + "_" + new_field
#                             new_master_table[dups_table[i]][index][new_field] = new_master_table[dups_table[i]][index][
#                                 field
#                             ]

#     return [master_table, new_master_table]


# def get_para_table_dicts(address_set, address_tables, **kwargs):
#     logger.info(f"notice.get_para_table_dicts")
#     logger.debug(f"notice.get_para_table_dicts: {kwargs}")
#     try:
#         company_id = kwargs.get("company_id", "")
#         allocation_month = kwargs.get("allocation_month", "")
#         question_dict = kwargs.get("question_dict", "")
#         notice_type = kwargs.get("notice_type", "")
#         local_batch_directory_path = kwargs["local_batch_directory_path"]
#         local_draft_file_path = os.path.join(local_batch_directory_path, f'{kwargs.get("draft_id","")}.docx')
#         kwargs["local_draft_file_path"] = local_draft_file_path

#         logger.info(f"notice.get_para_table_dicts")
#         logger.debug(f"notice.get_para_table_dicts: {kwargs}")

#         # Change this variable name
#         dt = question_dict

#         changed_dt = {}
#         changed_dt = copy.deepcopy(dt)
#         applicant_count = 1

#         for i in range(applicant_count):
#             changed_dt = {}
#             changed_dt = copy.deepcopy(dt)
#             changed_dt["company_id"] = company_id
#             perform_mailmerge_res = perform_mailmerge(dt, changed_dt, **kwargs)
#             if isinstance(perform_mailmerge_res, str):
#                 return perform_mailmerge_res

#             # if not dt.get("applicant_name", ""):
#             #     raise Exception("get_para_table_dicts.exception: Missing applicant_name")

#             changed_dt["name"] = dt.get("applicant_name", "")
#             changed_dt["contact_number"] = str(dt.get("applicant_contact_number", ""))

#             if dt.get("applicant_address", "") not in [None, "", []]:
#                 changed_dt["address_text"] = dt["applicant_address"][i].get("applicant_address_text", "")
#                 changed_dt["city"] = dt["applicant_address"][i].get("applicant_city", "")
#                 changed_dt["state"] = dt["applicant_address"][i].get("applicant_state", "")
#                 changed_dt["pincode"] = str(dt["applicant_address"][i].get("applicant_pincode", ""))
#             changed_dt["address_index"] = i
#             changed_dt["applicant_type"] = applicant_type = "applicant"
#             changed_dt["allocation_month"] = allocation_month

#             if dt.get("notice_reference_number", "") in [None, "", []]:
#                 get_notice_reference_number(dt, changed_dt, "notice_reference_number", notice_type)

#             if dt.get("applicant_notice_reference_number", "") in [None, "", []]:
#                 get_notice_reference_number(dt, changed_dt, "applicant_notice_reference_number", notice_type)

#             if dt.get("co_applicant_notice_reference_number", "") in [None, "", []]:
#                 get_notice_reference_number(dt, changed_dt, "co_applicant_notice_reference_number", notice_type)

#             kwargs["company_id"] = company_id
#             kwargs["changed_dt"] = changed_dt
#             table_dict = populate_table_rows(address_set, address_tables, **kwargs)
#         return [changed_dt, table_dict]
#     except Exception as e:
#         raise Exception(f"{str(e)}")


# def populate_table_rows(address_set, address_tables, **kwargs):
#     logger.info("notice.populate_table_rows")
#     question_dict = kwargs.get("question_dict", "")
#     # doc = MailMerge(kwargs['local_draft_file_path'])
#     # fields = list(doc.get_merge_fields())
#     fields = kwargs.get("draft_fields", [])
#     # doc.close()
#     cell_1s = []
#     row_dict = {}
#     fields.sort()
#     table_no = 0
#     table_map = {}
#     parsed_tables = set()
#     table_identifier = ""

#     for i in range(len(fields)):
#         if "table" in fields[i]:
#             row_dict[fields[i]] = ""
#             if "cell_1" in fields[i]:
#                 cell_1s.append((fields[i]))

#     kwargs["cell_1s"] = cell_1s

#     for i in range(len(cell_1s)):
#         table_identifier = cell_1s[i].split("_", 2)[0] + "_" + cell_1s[i].split("_", 2)[1]
#         tag = cell_1s[i].split("_", 4)[-1]
#         tag = tag.split("_")[0]
#         if tag == "co":
#             tag = "co_applicant"
#         for j in range(len(fields)):
#             if table_identifier in fields[j] and ("address_text" in fields[j] or "builder_address" in fields[j]):
#                 address_tables.add(tag)

#         if tag in address_tables:
#             if not table_map.get(tag):
#                 table_map[tag] = []
#             table_map[tag].append(str(table_no + 1))
#         else:
#             if not table_map.get(cell_1s[i]):
#                 table_map[cell_1s[i]] = []
#             table_map[cell_1s[i]].append(str(table_no + 1))
#         table_no += 1

#     table_dict = {}
#     kwargs["row_dict"] = row_dict
#     kwargs["fields"] = fields
#     kwargs["table_map"] = table_map
#     if question_dict.get("property", "") not in ("", [], None):
#         kwargs["property_address"] = question_dict.get("property", "")

#     for i in range(len(cell_1s)):
#         merge_list = []
#         table_name = cell_1s[i].split("_", 4)[-1].split("_")[0]
#         kwargs["current_cell_1_cell"] = cell_1s[i]
#         if table_name == "co":
#             table_name += "_applicant"
#         kwargs["table_name"] = table_name
#         if table_name == "applicant":
#             merge_list = mediator(question_dict, address_set, **kwargs)
#         elif table_name in address_tables:
#             qd = question_dict.get(table_name, "")
#             if qd not in ("", None, []):
#                 merge_list = mediator(qd, address_set, **kwargs)
#         else:
#             merge_list = populate_from_changed_dt(**kwargs)

#         table_dict[cell_1s[i]] = merge_list
#         del merge_list

#     return table_dict


# def populate_from_changed_dt(**kwargs):
#     fields = kwargs.get("fields", "")
#     row_dict = kwargs.get("row_dict", "")
#     merge_list = []
#     changed_dt = kwargs.get("changed_dt", "")
#     merge_dict_copy = row_dict.copy()
#     for i in range(len(fields)):
#         if "cell_1" in fields[i]:
#             merge_field = fields[i].split("_", 4)[-1]
#         else:
#             merge_field = fields[i].split("_", 2)[-1]

#         merge_dict_copy[fields[i]] = changed_dt.get(merge_field, "")

#     merge_list.append(merge_dict_copy)
#     del merge_dict_copy

#     return merge_list


# def mediator(qd, address_set, **kwargs):
#     logger.info("notice.mediator")

#     if isinstance(qd, list):
#         table_data = []
#         for l in range(len(qd)):
#             response = []
#             qd1 = qd[l]
#             response = populate_rows(qd1, address_set, **kwargs)
#             for k in range(len(response)):
#                 table_data.append(response[k])
#             del response

#         return table_data
#     else:
#         return populate_rows(qd, address_set, **kwargs)


# def populate_rows(qd, address_set, **kwargs):
#     logger.info("notice.populate_rows")

#     merge_list = []
#     table_name = kwargs["table_name"]
#     fields = kwargs["fields"]
#     row_dict = kwargs["row_dict"]
#     company_id = kwargs["company_id"]
#     table_map = kwargs["table_map"]
#     property_address = {}
#     loan_address_map = kwargs["loan_address_map"]
#     loan_id = kwargs["loan_id"]
#     primary_name, primary_address, primary_address_type = "", "", ""
#     if kwargs.get("property_address", "") not in ("", [], None):
#         property_address = kwargs.get("property_address", "")
#     cell_1s = kwargs["cell_1s"]

#     address_name = ""
#     KEY = table_name + "_address"
#     borrower_type = table_name.lower()
#     if qd.get(KEY, ""):
#         for z in range(len(qd.get(KEY, ""))):
#             merge_dict_copy = row_dict.copy()
#             if qd[KEY][z].get(table_name + "_address_text", "") not in ["", None, []]:
#                 address_name = qd[KEY][z].get(table_name + "_address_text", "") + qd.get(table_name + "_name", "")
#                 if address_name not in address_set:
#                     if qd.get(table_name + "_name", "") or table_name in [
#                         "property",
#                         "auctioned",
#                     ]:
#                         address_set.add(address_name)

#                     for i in range(len(fields)):
#                         if "cell_1" in fields[i]:
#                             tag = fields[i].split("_", 4)[-1].strip("_").strip(" ")
#                         else:
#                             tag = fields[i].split("_", 2)[-1].strip("_").strip(" ")

#                         if isinstance(qd.get(tag, ""), str) and qd.get(tag, "") not in [
#                             "",
#                             None,
#                         ]:
#                             val = remove_special_characters(qd.get(tag, ""))
#                         else:
#                             val = qd.get(tag, "")
#                         merge_dict_copy[fields[i]] = val

#                         if merge_dict_copy[fields[i]] == "":
#                             if isinstance(qd[KEY][z].get(tag, ""), str) and qd[KEY][z].get(tag, "") not in ["", None]:
#                                 val = remove_special_characters(qd[KEY][z].get(tag, ""))
#                             else:
#                                 val = qd[KEY][z].get(tag, "")
#                             merge_dict_copy[fields[i]] = val

#                         # loan_address_map_population
#                         if "name" in tag and val != "":
#                             primary_name = val
#                         if "address_text" in tag and val != "":
#                             primary_address = val

#                         address_type_key = table_name + "_address_type"

#                         if qd[KEY][z].get(address_type_key, ""):
#                             primary_address_type = qd[KEY][z][address_type_key]

#                         if tag == "borrower_type" and fields[i].split("_", 2)[1] in table_map[table_name]:
#                             merge_dict_copy[fields[i]] = "(" + table_name.title() + ")"

#                         kwargs["field"] = fields[i]
#                         merge_dict_copy["loan_id"] = loan_id
#                         # merge_dict_copy = iifl_check(qd, merge_dict_copy, **kwargs)

#                         if z != 0 and any(value in fields[i] for value in ["contact_number", "email"]):
#                             merge_dict_copy[fields[i]] = ""

#                         if table_name == "applicant" and "reference" in tag:
#                             changed_dt_key = tag.split("_", 2)[-1] + "_" + str(z + 1)
#                             merge_dict_copy[fields[i]] = kwargs["changed_dt"].get(changed_dt_key, "")

#                     merge_list.append(merge_dict_copy)
#                     del merge_dict_copy
#                 else:
#                     for i in range(len(fields)):
#                         if "cell_1" in fields[i]:
#                             tag = fields[i].split("_", 4)[-1].strip("_").strip(" ")
#                         else:
#                             tag = fields[i].split("_", 2)[-1].strip("_").strip(" ")

#                         if isinstance(qd.get(tag, ""), str) and qd.get(tag, "") not in [
#                             "",
#                             None,
#                         ]:
#                             val = remove_special_characters(qd.get(tag, ""))
#                         else:
#                             val = qd.get(tag, "")
#                         merge_dict_copy[fields[i]] = val
#                         if merge_dict_copy[fields[i]] == "":
#                             if isinstance(qd[KEY][z].get(tag, ""), str) and qd[KEY][z].get(tag, "") not in ["", None]:
#                                 val = remove_special_characters(qd[KEY][z].get(tag, ""))
#                             else:
#                                 val = qd[KEY][z].get(tag, "")
#                             merge_dict_copy[fields[i]] = val

#                         # loan_address_map_population
#                         if "name" in tag and val != "":
#                             primary_name = val
#                         if "address_text" in tag and val != "":
#                             primary_address = val

#                         address_type_key = table_name + "_address_type"

#                         if qd[KEY][z].get(address_type_key, ""):
#                             primary_address_type = qd[KEY][z][address_type_key]

#                         if tag == "borrower_type" and fields[i].split("_", 2)[1] in table_map[table_name]:
#                             merge_dict_copy[fields[i]] = "(" + table_name.title() + ")"

#                         if z != 0 and any(value in fields[i] for value in ["contact_number", "email"]):
#                             merge_dict_copy[fields[i]] = ""

#             primary_key = (primary_name + primary_address, borrower_type, primary_address_type)
#             loan_id = kwargs["loan_id"]
#             if not loan_address_map.get(loan_id):
#                 loan_address_map[loan_id] = [primary_key]
#             else:
#                 if primary_key not in loan_address_map[loan_id]:
#                     loan_address_map[loan_id].append(primary_key)

#     elif (
#         qd.get(table_name + "_builder_address") not in ("", [], None)
#         and f"{table_name}_builder" in kwargs["current_cell_1_cell"]
#     ):
#         address_name = qd.get(table_name + "_builder_name", "") + qd[table_name + "_builder_address"]
#         if address_name not in address_set:
#             address_set.add(address_name)
#             merge_dict_copy = row_dict.copy()
#             for i in range(len(fields)):
#                 if "cell_1" in fields[i]:
#                     tag = fields[i].split("_", 4)[-1].strip("_").strip(" ")
#                 else:
#                     tag = fields[i].split("_", 2)[-1].strip("_").strip(" ")

#                 if isinstance(qd.get(tag, ""), str) and qd.get(tag, "") not in [
#                     "",
#                     None,
#                 ]:
#                     val = remove_special_characters(qd.get(tag, ""))
#                 else:
#                     val = qd.get(tag, "")

#                 merge_dict_copy[fields[i]] = val
#             merge_list.append(merge_dict_copy)
#             del merge_dict_copy

#     elif qd.get(table_name + "_address_text", "") not in ("", [], None):
#         address_name = qd.get(table_name + "_address_text", "") + qd.get(table_name + "_name", "")
#         merge_dict_copy = row_dict.copy()

#         if address_name not in address_set:
#             if qd.get(table_name + "_name", "") or table_name in [
#                 "property",
#                 "auctioned",
#             ]:
#                 address_set.add(address_name)
#             for i in range(len(fields)):
#                 if "cell_1" in fields[i]:
#                     tag = fields[i].split("_", 4)[-1].strip("_").strip(" ")
#                 else:
#                     tag = fields[i].split("_", 2)[-1].strip("_").strip(" ")

#                 if isinstance(qd.get(tag, ""), str) and qd.get(tag, "") not in [
#                     "",
#                     None,
#                 ]:
#                     val = remove_special_characters(qd.get(tag, ""))
#                 else:
#                     val = qd.get(tag, "")
#                 merge_dict_copy[fields[i]] = val

#                 # loan_address_map_population
#                 if "name" in tag and val != "":
#                     primary_name = val
#                 if "address_text" in tag and val != "":
#                     primary_address = val

#                 address_type_key = table_name + "_address_type"
#                 if qd.get(address_type_key, ""):
#                     primary_address_type = qd[address_type_key]

#                 if tag == "borrower_type" and fields[i].split("_", 2)[1] in table_map[table_name]:
#                     merge_dict_copy[fields[i]] = "(" + table_name.title() + ")"

#                 kwargs["field"] = fields[i]
#                 merge_dict_copy["loan_id"] = loan_id
#                 # merge_dict_copy = iifl_check(qd, merge_dict_copy, **kwargs)

#                 if table_name == "applicant" and "reference" in tag:
#                     changed_dt_key = tag.split("_", 2)[-1] + "_" + str(z + 1)
#                     merge_dict_copy[fields[i]] = kwargs["changed_dt"].get(changed_dt_key, "")

#             merge_list.append(merge_dict_copy)
#             del merge_dict_copy
#         else:
#             for i in range(len(fields)):
#                 if "cell_1" in fields[i]:
#                     tag = fields[i].split("_", 4)[-1].strip("_").strip(" ")
#                 else:
#                     tag = fields[i].split("_", 2)[-1].strip("_").strip(" ")

#                 if isinstance(qd.get(tag, ""), str) and qd.get(tag, "") not in [
#                     "",
#                     None,
#                 ]:
#                     val = remove_special_characters(qd.get(tag, ""))
#                 else:
#                     val = qd.get(tag, "")
#                 merge_dict_copy[fields[i]] = val

#                 # loan_address_map_population
#                 if "name" in tag and val != "":
#                     primary_name = val
#                 if "address_text" in tag and val != "":
#                     primary_address = val

#                 address_type_key = table_name + "_address_type"
#                 if qd.get(address_type_key, ""):
#                     primary_address_type = qd[address_type_key]

#                 if tag == "borrower_type" and fields[i].split("_", 2)[1] in table_map[table_name]:
#                     merge_dict_copy[fields[i]] = "(" + table_name.title() + ")"

#         primary_key = (primary_name + primary_address, borrower_type, primary_address_type)
#         loan_id = kwargs["loan_id"]
#         if not loan_address_map.get(loan_id):
#             loan_address_map[loan_id] = [primary_key]
#         else:
#             if primary_key not in loan_address_map[loan_id]:
#                 loan_address_map[loan_id].append(primary_key)
#     kwargs["loan_address_map"] = loan_address_map

#     if company_id in (NOTICE_COMPANIES_WITH_PROPERTY_ADDRESS_HANDLING):
#         if (
#             len(property_address) > 0
#             and table_name != "property"
#             and (
#                 "property_address_text" in [merge_field.split("_", 4)[-1] for merge_field in cell_1s]
#                 or any([merge_field.startswith("property_address_text") for merge_field in kwargs["draft_fields"]])
#             )
#         ):
#             populate_property_address(qd, merge_list, address_set, **kwargs)

#     return merge_list


# def perform_mailmerge(dt, changed_dt, **kwargs):
#     logger.info("notice.perform_mailmerge")
#     for key in dt:
#         if dt[key] in (None, [], "nan", "Nan", "none", "None", "NAN", "NONE"):
#             changed_dt[key] = ""
#         elif isinstance(dt[key], int) or isinstance(dt[key], float):
#             # Logic of open_int_or_float
#             changed_dt[key] = open_int_or_float(key, dt[key])
#         elif isinstance(dt[key], str) and dt[key] not in ["", None]:
#             # Remove special characters for all the values except email
#             if any(
#                 key_str in key
#                 for key_str in [
#                     "chassis_number",
#                     "engine_number",
#                     "vehicle_registration_number",
#                     "make_and_model",
#                 ]
#             ):
#                 dt[key] = remove_special_characters(dt[key], "*")
#             elif all([False if str in key else True for str in ["email", "payment_link"]]):
#                 dt[key] = remove_special_characters(dt[key])
#             if key == "barcode":
#                 dt[key] = "(" + dt[key].upper() + ")"
#             changed_dt[key] = open_str(key, dt[key])

#         if dt[key] not in (None, "", []):
#             if "date" in key:
#                 changed_dt[key] = open_date(key, dt[key])

#             if isinstance(dt[key], list) and key != "defaults":
#                 open_list(changed_dt, dt[key], -1, -1)
#                 del changed_dt[key]
#             elif key == "defaults":
#                 del changed_dt["defaults"]
#             elif isinstance(dt[key], dict):
#                 open_dict(changed_dt, dt[key], 0, 0)

#     if "total_claim_amount" in dt and dt["total_claim_amount"] not in ["", None, []]:
#         changed_dt["total_claim_amount"] = format(dt["total_claim_amount"], ".2f")

#     changed_dt["present_date"] = datetime.now().strftime("%d/%m/%Y")

#     merge_fields = kwargs["draft_fields"]

#     in_words = [i for i in merge_fields if "_in_words" in i]

#     for var in in_words:
#         if "cell_1" in var:
#             var = var.split("_", 4)[-1]
#         elif "table_" in var:
#             var = var.split("_", 2)[-1]
#         amount_key = var.split("_in_words")[0]
#         if amount_key in changed_dt and changed_dt[amount_key] not in ("", None, []):
#             changed_dt[var] = convert_num2words(changed_dt[amount_key])
#         elif (
#             "defaults" in dt
#             and amount_key in dt["defaults"][-1]
#             and dt["defaults"][-1][amount_key] not in ("", None, [])
#         ):
#             changed_dt[var] = convert_num2words(dt["defaults"][-1][amount_key])

#     changed_dt2 = copy.deepcopy(changed_dt)
#     for key, val in changed_dt2.items():
#         if key.endswith("_1_1"):
#             tag = key.split("_1_1")[0] + "_1"
#             changed_dt[tag] = val
#         elif key.endswith("_1") and not key.startswith("applicant"):
#             tag = key.split("_1")[0]
#             changed_dt[tag] = val

#     if changed_dt.get("company_id", "") == "d2d50f3e-4b79-40d7-b9dd-6cadb0b30141":
#         axis_check(changed_dt)

#     return True


# def remove_special_characters(input_str, additional_exceptions=""):
#     logger.info("notice.remove_special_characters")
#     logger.debug(f"input_str : {input_str}")
#     input_str = input_str.replace("\\n", "")
#     input_str = input_str.replace("\n", "")
#     input_str = input_str.replace("/n", "")
#     # Matches individual characters of the input_str, the pattern is that except A-Z, a-z, 0-9 replace all other listed characters with ''(empty character)
#     exception_str = f"[^A-Za-z0-9+ _,-/.@:()\[\]&#{additional_exceptions}]+"
#     output_str = re.sub(exception_str, "", input_str)
#     logger.debug(f"output_str : {output_str}")
#     return output_str


# def get_notice_reference_number(dt, changed_dt, key, notice_type):

#     if dt.get("notice_date", "") not in ["", None, []] and is_date(dt.get("notice_date", "")):
#         try:
#             changed_dt[key] = (
#                 str(dt["loan_id"])
#                 + "-"
#                 + notice_type.upper()
#                 + "-"
#                 + datetime.strptime(dt["notice_date"], "%Y-%m-%d").strftime("%d%m%Y")
#                 + "-"
#                 + str(random.randint(1000, 9999))
#             )
#         except Exception as e:
#             logger.error(f"date type is wrong. error handled: {str(e)}")
#             changed_dt[key] = (
#                 str(dt["loan_id"])
#                 + "-"
#                 + notice_type.upper()
#                 + "-"
#                 + datetime.now().strftime("%d%m%Y")
#                 + "-"
#                 + str(random.randint(1000, 9999))
#             )

#     else:
#         changed_dt[key] = (
#             str(dt["loan_id"])
#             + "-"
#             + notice_type.upper()
#             + "-"
#             + datetime.now().strftime("%d%m%Y")
#             + "-"
#             + str(random.randint(1000, 9999))
#         )


# def populate_property_address(qd, merge_list, address_set, **kwargs):
#     table_name = kwargs["table_name"]
#     fields = kwargs["fields"]
#     row_dict = kwargs["row_dict"]
#     company_id = kwargs["company_id"]
#     table_map = kwargs["table_map"]
#     property_address = {}
#     loan_address_map = kwargs["loan_address_map"]
#     loan_id = kwargs["loan_id"]
#     address_name = ""
#     if kwargs.get("property_address", "") not in ("", [], None):
#         property_address = kwargs.get("property_address", "")

#     for p_address in property_address:
#         if p_address.get("property_address_text", "") not in ("", [], None):
#             merge_dict_copy = row_dict.copy()
#             for i in range(len(fields)):
#                 if "cell_1" in fields[i]:
#                     tag = fields[i].split("_", 4)[-1].strip("_").strip(" ")
#                 else:
#                     tag = fields[i].split("_", 2)[-1].strip("_").strip(" ")

#                 if "name" in tag and fields[i].split("_", 2)[1] in table_map[table_name]:
#                     address_name = p_address.get("property_address_text", "") + qd.get(tag, "")
#                     primary_name = qd.get(tag, "")
#                     break

#             if address_name not in address_set:
#                 address_set.add(address_name)
#                 for i in range(len(fields)):
#                     if "cell_1" in fields[i]:
#                         tag = fields[i].split("_", 4)[-1].strip("_").strip(" ")
#                     else:
#                         tag = fields[i].split("_", 2)[-1].strip("_").strip(" ")

#                     if "name" in tag:
#                         merge_dict_copy[fields[i]] = qd.get(tag, "")
#                     elif "borrower_type" not in tag:
#                         tag = tag.split(table_name + "_")[-1]
#                         tag = "property_" + tag
#                         merge_dict_copy[fields[i]] = p_address.get(tag, "")
#                         if "address_text" in tag and p_address.get(tag, "") != "":
#                             primary_address = p_address.get(tag, "")

#                     if tag == "borrower_type" and fields[i].split("_", 2)[1] in table_map[table_name]:
#                         merge_dict_copy[fields[i]] = "(" + table_name.title() + ")"

#                     kwargs["field"] = fields[i]

#                 merge_list.append(merge_dict_copy)
#                 del merge_dict_copy

#             else:
#                 for i in range(len(fields)):
#                     if "cell_1" in fields[i]:
#                         tag = fields[i].split("_", 4)[-1].strip("_").strip(" ")
#                     else:
#                         tag = fields[i].split("_", 2)[-1].strip("_").strip(" ")

#                     if "name" in tag:
#                         merge_dict_copy[fields[i]] = qd.get(tag, "")
#                     elif "borrower_type" not in tag:
#                         tag = tag.split(table_name + "_")[-1]
#                         tag = "property_" + tag
#                         merge_dict_copy[fields[i]] = p_address.get(tag, "")
#                         if "address_text" in tag and p_address.get(tag, "") != "":
#                             primary_address = p_address.get(tag, "")

#             primary_key = primary_name + primary_address
#             loan_id = kwargs["loan_id"]
#             borrower_type = table_name

#             if not loan_address_map.get(loan_id):
#                 loan_address_map[loan_id] = [(primary_key, borrower_type, primary_address)]
#             else:
#                 loan_address_map[loan_id].append((primary_key, borrower_type, primary_address))
#             kwargs["loan_address_map"] = loan_address_map


# def open_int_or_float(key, value):
#     if (
#         "amount" in key
#         or "charges" in key
#         or "dues" in key
#         or key in ["expected_emi", "late_fee", "other_penalty", "overdue_charges"]
#     ) and value not in ("", None, []):
#         res = format(value, ".2f")
#     else:
#         res = str(value)

#     return res


# def open_str(key, value):
#     if (
#         "amount" in key
#         or "charges" in key
#         or "dues" in key
#         or key in ["expected_emi", "late_fee", "other_penalty", "overdue_charges"]
#     ) and value not in ("", None, []):
#         try:
#             res = format(float(value), ".2f")
#         except:
#             res = str(value.strip())
#     else:
#         res = str(value.strip())

#     return res


# def open_date(key, value):
#     changed_value = ""
#     logger.debug(f"open_date.value:: {value}")
#     if isinstance(value, datetime):
#         try:
#             changed_value = value.strftime("%d/%m/%Y")
#         except Exception as e:
#             logger.error(f"datetime type date conversion error:: {str(e)}")
#             changed_value = str(value)
#     elif isinstance(value, str):
#         try:
#             changed_value = datetime.strptime(value.split(" ")[0], "%Y-%m-%d").strftime("%d/%m/%Y")
#         except Exception as e:
#             logger.error(f"str type date conversion error:: {str(e)}")
#             changed_value = str(value.split(" ")[0])
#     elif value in ["", None]:
#         return ""

#     return changed_value


# def open_dict(changed_dt, dicti, list_no, i):
#     for key, val in dicti.items():
#         if isinstance(val, list):
#             open_list(changed_dt, val, i, i)
#         elif isinstance(val, dict):
#             open_dict(changed_dt, val, list_no, i)
#         elif isinstance(val, int) or isinstance(val, float):
#             if list_no > -1:
#                 changed_dt[key + "_" + str(list_no + 1) + "_" + str(i + 1)] = open_int_or_float(key, val)
#             else:
#                 changed_dt[key + "_" + str(i + 1)] = open_int_or_float(key, val)
#         elif "date" in key and val not in ("", None, []):
#             if list_no > -1:
#                 changed_dt[key + "_" + str(list_no + 1) + "_" + str(i + 1)] = open_date(key, val)
#             else:
#                 changed_dt[key + "_" + str(i + 1)] = open_date(key, val)
#         elif isinstance(val, str) and val not in ["", None]:
#             if "email" not in key:
#                 val = remove_special_characters(val)
#             if list_no > -1:
#                 changed_dt[key + "_" + str(list_no + 1) + "_" + str(i + 1)] = open_str(key, val)
#             else:
#                 changed_dt[key + "_" + str(i + 1)] = open_str(key, val)
#         elif val in (None, []):
#             if list_no > -1:
#                 changed_dt[key + "_" + str(list_no + 1) + "_" + str(i + 1)] = ""
#             else:
#                 changed_dt[key + "_" + str(i + 1)] = ""
#         else:
#             if list_no > -1:
#                 changed_dt[key + "_" + str(list_no + 1) + "_" + str(i + 1)] = str(val.strip())
#             else:
#                 changed_dt[key + "_" + str(i + 1)] = str(val.strip())

#         if "applicant_address_text" in key:
#             co = ""
#             if "co" in key:
#                 co = "co_"

#             val = format_address(
#                 dicti.get(co + "applicant_address_text", ""),
#                 dicti.get(co + "applicant_state", ""),
#                 str(dicti.get(co + "applicant_pincode", "")),
#                 dicti.get(co + "applicant_city", ""),
#             )
#             if list_no > -1:
#                 changed_dt[key + "_" + str(list_no + 1) + "_" + str(i + 1)] = val
#             else:
#                 changed_dt[key + "_" + str(i + 1)] = val


# def open_list(changed_dt, lst, list_no, iterator):
#     for i in range(len(lst)):
#         if isinstance(lst[i], dict):
#             open_dict(changed_dt, lst[i], list_no, i)
#         elif isinstance(lst[i], list):
#             open_list(changed_dt, lst[i], list_no, i)


# def convert_num2words(num):
#     logger.info("notice.convert_num2words")
#     logger.debug(f"notice.convert_num2words.num: '{num}'")

#     try:
#         decimal_val = ""
#         integer_val = str(num).split(".")[0]

#         if isinstance(num, str):
#             try:
#                 num = float(num)
#             except Exception as e:
#                 raise Exception(f"notice.convert_num2words.string_amount_conversion.exception:: {str(e)}")

#         if isinstance(num, float):
#             num = str(num) + "0"
#             integer_val, decimal_val = num.split(".")
#             decimal_val = decimal_val[:2]
#             num = integer_val + "." + "".join(decimal_val)
#             paise2words = num2words(decimal_val, lang="en_IN")

#         rupees2words = num2words(integer_val, lang="en_IN")

#         num2words_string = "Rupees " + rupees2words

#         if decimal_val and decimal_val != "00":
#             num2words_string = (
#                 num2words_string + " and " + paise2words + (" paisa" if decimal_val[0] == "0" else " paise")
#             )
#         formatted_num2words_string = " ".join(
#             " ".join(str.strip().split("-")) for str in num2words_string.title().split(",")
#         )
#         formatted_words_list = formatted_num2words_string.split("And")

#         if len(formatted_words_list) > 1:
#             formatted_num2words_string = (
#                 formatted_words_list[0].strip()
#                 + " "
#                 + formatted_words_list[1].strip()
#                 + " and "
#                 + formatted_words_list[2].strip()
#                 if len(formatted_words_list) >= 3
#                 else formatted_words_list[0].strip() + " and " + formatted_words_list[1].strip()
#             )
#         logger.debug(f"notice.convert_num2words.formatted_num2words_string: '{formatted_num2words_string}'")
#         return formatted_num2words_string + " Only"
#     except:
#         logger.error(f"error: unsupported format of variable 'num', other than int, float and string e.g.:(6,6.0,'6') ")
#         return ""


# def is_date(string, fuzzy=False):
#     try:
#         parse(string, fuzzy=fuzzy)
#         return True
#     except ValueError:
#         return False


# def axis_check(changed_dt):
#     logger.info("notice.axis_check")
#     logger.debug(
#         f"applicant_address_text_1: {changed_dt.get('applicant_address_text_1','')}, applicant_address_text_2: {changed_dt.get('applicant_address_text_1','')}, 'applicant_address_text_3': {changed_dt.get('applicant_address_text_3','')}"
#     )
#     permanent_address_text, current_adddres_text, work_address_text = "", "", ""
#     permanent_address_city, current_address_city, work_address_city = "", "", ""
#     permanent_address_state, current_address_state, work_address_state = "", "", ""
#     permanent_address_pincode, current_address_pincode, work_address_pincode = (
#         "",
#         "",
#         "",
#     )
#     (
#         permanent_address_text_index,
#         current_address_text_index,
#         work_address_text_index,
#     ) = ("", "", "")
#     for i in range(9):
#         if changed_dt.get("applicant_address_type_" + str(i + 1), "").lower() == "permanent":
#             permanent_address_text = changed_dt.get("applicant_address_text_" + str(i + 1), "")
#             permanent_address_city = changed_dt.get("applicant_city_" + str(i + 1), "")
#             permanent_address_state = changed_dt.get("applicant_state" + str(i + 1), "")
#             permanent_address_pincode = changed_dt.get("applicant_pincode" + str(i + 1), "")
#             permanent_address_text_index = str(i + 1)
#         elif changed_dt.get("applicant_address_type_" + str(i + 1), "").lower() == "current":
#             current_adddres_text = changed_dt.get("applicant_address_text_" + str(i + 1), "")
#             current_address_city = changed_dt.get("applicant_city_" + str(i + 1), "")
#             current_address_state = changed_dt.get("applicant_state" + str(i + 1), "")
#             current_address_pincode = changed_dt.get("applicant_pincode" + str(i + 1), "")
#             current_address_text_index = str(i + 1)
#         elif changed_dt.get("applicant_address_type_" + str(i + 1), "").lower() == "work":
#             work_adddres_text = changed_dt.get("applicant_address_text_" + str(i + 1), "")
#             work_address_city = changed_dt.get("applicant_city_" + str(i + 1), "")
#             work_address_state = changed_dt.get("applicant_state" + str(i + 1), "")
#             work_address_pincode = changed_dt.get("applicant_pincode" + str(i + 1), "")
#             work_address_text_index = str(i + 1)
#     if permanent_address_text:
#         (
#             changed_dt["applicant_address_text_1"],
#             changed_dt["applicant_address_text_" + permanent_address_text_index],
#         ) = (
#             changed_dt["applicant_address_text_" + permanent_address_text_index],
#             changed_dt["applicant_address_text_1"],
#         )
#         (changed_dt["applicant_city_1"], changed_dt["applicant_city_" + permanent_address_text_index],) = (
#             changed_dt["applicant_city_" + permanent_address_text_index],
#             changed_dt["applicant_city_1"],
#         )
#         (changed_dt["applicant_state_1"], changed_dt["applicant_state_" + permanent_address_text_index],) = (
#             changed_dt["applicant_state_" + permanent_address_text_index],
#             changed_dt["applicant_state_1"],
#         )
#         (changed_dt["applicant_pincode_1"], changed_dt["applicant_pincode_" + permanent_address_text_index],) = (
#             changed_dt["applicant_pincode_" + permanent_address_text_index],
#             changed_dt["applicant_pincode_1"],
#         )
#         (
#             changed_dt["applicant_address_type_1"],
#             changed_dt["applicant_address_type_" + permanent_address_text_index],
#         ) = (
#             changed_dt["applicant_address_type_" + permanent_address_text_index],
#             changed_dt["applicant_address_type_1"],
#         )
#     elif current_adddres_text:
#         (
#             changed_dt["applicant_address_text_1"],
#             changed_dt["applicant_address_text_" + current_address_text_index],
#         ) = (
#             changed_dt["applicant_address_text_" + current_address_text_index],
#             changed_dt["applicant_address_text_1"],
#         )
#         (changed_dt["applicant_city_1"], changed_dt["applicant_city_" + current_address_text_index],) = (
#             changed_dt["applicant_city_" + current_address_text_index],
#             changed_dt["applicant_city_1"],
#         )
#         (changed_dt["applicant_state_1"], changed_dt["applicant_state_" + current_address_text_index],) = (
#             changed_dt["applicant_state_" + current_address_text_index],
#             changed_dt["applicant_state_1"],
#         )
#         (changed_dt["applicant_pincode_1"], changed_dt["applicant_pincode_" + current_address_text_index],) = (
#             changed_dt["applicant_pincode_" + current_address_text_index],
#             changed_dt["applicant_pincode_1"],
#         )
#         (
#             changed_dt["applicant_address_type_1"],
#             changed_dt["applicant_address_type_" + current_address_text_index],
#         ) = (
#             changed_dt["applicant_address_type_" + current_address_text_index],
#             changed_dt["applicant_address_type_1"],
#         )
#     elif work_address_text:
#         (changed_dt["applicant_address_text_1"], changed_dt["applicant_address_text_" + work_address_text_index],) = (
#             changed_dt["applicant_address_text_" + work_address_text_index],
#             changed_dt["applicant_address_text_1"],
#         )
#         (changed_dt["applicant_city_1"], changed_dt["applicant_city_" + work_address_text_index],) = (
#             changed_dt["applicant_city_" + work_address_text_index],
#             changed_dt["applicant_city_1"],
#         )
#         (changed_dt["applicant_state_1"], changed_dt["applicant_state_" + work_address_text_index],) = (
#             changed_dt["applicant_state_" + work_address_text_index],
#             changed_dt["applicant_state_1"],
#         )
#         (changed_dt["applicant_pincode_1"], changed_dt["applicant_pincode_" + work_address_text_index],) = (
#             changed_dt["applicant_pincode_" + work_address_text_index],
#             changed_dt["applicant_pincode_1"],
#         )
#         (changed_dt["applicant_address_type_1"], changed_dt["applicant_address_type_" + work_address_text_index],) = (
#             changed_dt["applicant_address_type_" + work_address_text_index],
#             changed_dt["applicant_address_type_1"],
#         )


# def format_address(address_text, state, pincode, city):
#     logger.info("notice.format_address")
#     logger.debug(f"address_text: '{address_text}', state: '{state}', pincode: '{pincode}', city: '{city}'")
#     # if state != 'Delhi':
#     #   address_text = address_text.replace(state, '')
#     # if city != 'Delhi':
#     #   address_text = address_text.replace(city, '')

#     if address_text in ("", [], "nan", "Nan", "none", "None", "NAN", "NONE", None):
#         logger.debug(f"address_text: '{address_text}'")
#         address_text = ""
#         return address_text

#     if pincode:
#         address_text = address_text.replace(pincode, "")
#     address_text = address_text.replace("  ", " ")
#     address_text = address_text.replace(" ,", ",")
#     address_text = address_text.replace(",,,", "")
#     address_text = address_text.replace(",,", ",")
#     address_text = address_text.replace(", -", "")
#     address_text = address_text.replace(",", ", ")
#     address_text = address_text.replace("\\n", "")
#     address_text = address_text.replace("\n", "")
#     address_text = address_text.replace("/n", "")
#     address_text = address_text.replace("State", "")
#     address_text = address_text.replace("City", "")
#     address_text = re.sub("[^A-Za-z0-9 ,:\-/.@()\[\]&#+]+", "", address_text)
#     address_text = address_text.replace("  ", " ")
#     address_text = address_text.strip()

#     if address_text in ("", [], "nan", "Nan", "none", "None", "NAN", "NONE", None):
#         logger.debug(f"address_text: '{address_text}'")
#         address_text = ""
#         return address_text

#     if address_text[-1] in (",", " ", "-"):
#         logger.debug(f"address_text: '{address_text}'")
#         return address_text[:-1]
#     if address_text[-2:] == ", ":
#         logger.debug(f"address_text: '{address_text}'")
#         return address_text[:-2]
#     logger.debug(f"address_text: '{address_text}'")
#     return address_text


# def upload_notices_to_s3(**kwargs):
#     logger.info("notice.upload_notices_to_s3")
#     logger.info(f"notice.upload_notices_to_s3.batch_id :: {kwargs['batch_id']}")

#     redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#     files_s3_map = kwargs.get("files_s3_map", {})
#     filenames = kwargs["filenames"]
#     BUCKET_NAME = kwargs["BUCKET_NAME"]
#     S3_BUCKET_ENDPOINT = kwargs["S3_BUCKET_ENDPOINT"]
#     s3_link_ids = []
#     s3_object_urls = []
#     s3_folder = "preview_notice_links" if kwargs.get("preview") else "notice_links"

#     try:
#         for output_file in filenames:
#             file = open(output_file, "rb")
#             s3_link_uuid = kwargs["s3_link_uuid"] if kwargs.get("s3_link_uuid") else gen_short_key(12)
#             s3.upload_file(
#                 file.name,
#                 BUCKET_NAME,
#                 s3_folder + "/" + s3_link_uuid + ".pdf",
#                 ExtraArgs={"ACL": "public-read", "ContentType": "application/pdf"},
#             )

#             s3_object_url = f"{S3_BUCKET_ENDPOINT.rstrip('/')}/{s3_folder}/{s3_link_uuid}.pdf"
#             # s3.upload_file(file.name, BUCKET_NAME, 'notice_links/' + s3_link_uuid + '.pdf', ExtraArgs={'ACL':'public-read'})

#             # s3.copy_object(Bucket = BUCKET_NAME, Key = 'notice_links/' + s3_link_uuid + '.pdf', CopySource = BUCKET_NAME + '/' + 'notice_links/' + s3_link_uuid + '.pdf', ContentType='application/pdf', MetadataDirective='REPLACE')

#             # s3_object_url = f"{S3_BUCKET_ENDPOINT.rstrip('/')}/notice_links/{s3_link_uuid}.pdf"
#             # s3.put_object_acl(ACL='public-read', Bucket= BUCKET_NAME, Key='notice_links/' + s3_link_uuid + '.pdf')
#             output_file = output_file.split("/")[-1]
#             if not files_s3_map.get(output_file):
#                 files_s3_map[output_file] = [s3_link_uuid, s3_object_url]

#             file.close()
#             s3_link_ids.append(s3_link_uuid)
#             s3_object_urls.append(s3_object_url)
#             kwargs["files_s3_map"] = files_s3_map

#         return {"s3_link_ids": s3_link_ids, "s3_object_urls": s3_object_urls}
#     except Exception as e:
#         if kwargs.get("tracking_ids"):
#             failed_tracking_ids_key = f'failed_tracking_id_{kwargs.get("batch_id","")}'
#             redis_instance.lpush(failed_tracking_ids_key, *kwargs.get("tracking_ids"))
#             redis_instance.close()
#         logger.error(f"upload_notices_to_s3.upload_failure : {str(e)}")
#         raise Exception(f"upload_notices_to_s3.exception :: {str(e)}")


# def gen_short_key(length=6):
#     valid_chars = string.ascii_letters + string.digits
#     short_key = ""
#     for i in range(length):
#         short_key += random.SystemRandom().choice(valid_chars)
#     return short_key


# def insert_into_db(**kwargs):
#     logger.info("notice.insert_into_db")
#     logger.info(f"notice.insert_into_db.batch_id :: {kwargs['batch_id']}")
#     loan_allocation_map = kwargs["loan_allocation_map"]
#     is_linked_loan = True if kwargs.get("is_linked_loan") else False
#     is_in_case = False

#     if kwargs.get("is_in_case", ""):
#         is_in_case = True

#     if "physical" in kwargs["mode"].lower():
#         notice_mode = "physical"
#         kwargs["document_type"] = "Notice"
#     else:
#         notice_mode = "digital"

#     data_to_dump = []

#     if notice_mode == "digital":
#         if isinstance(kwargs["loan_ids"], str):
#             loan_ids = kwargs["loan_ids"].split(", ")
#         else:
#             loan_ids = kwargs["loan_ids"]

#         s3_link_ids = kwargs.get("s3_link_ids", [])
#         s3_object_urls = kwargs.get("s3_object_urls", [])

#         for loan_id in loan_ids:
#             for i in range(len(s3_link_ids)):
#                 data_dict = {}
#                 data_dict["loan_id"] = loan_id
#                 data_dict["notice_type"] = kwargs.get("notice_type", "")
#                 data_dict["document_type"] = kwargs.get("document_type", "")
#                 data_dict["s3_link"] = s3_object_urls[i]
#                 data_dict["s3_link_uuid"] = s3_link_ids[i]
#                 data_dict["data"] = kwargs.get("db_data", {})
#                 data_dict["author"] = kwargs.get("author", "")
#                 data_dict["role"] = kwargs.get("role", "")
#                 data_dict["allocation_month"] = loan_allocation_map[data_dict["loan_id"]]
#                 data_dict["case_type"] = kwargs.get("case_type", "")
#                 data_dict["is_in_case"] = is_in_case
#                 data_dict["case_id"] = kwargs.get("case_id", "")
#                 data_dict["stage_code"] = kwargs.get("stage_code", 0)
#                 data_dict["iteration"] = kwargs.get("iteration", 0)
#                 data_dict["is_linked_loan"] = is_linked_loan
#                 data_dict["linked_loan_id"] = kwargs.get("linked_loan_id", "")
#                 data_dict["batch_id"] = kwargs.get("batch_id", "")
#                 data_dict["notice_mode"] = notice_mode
#                 data_dict["company_id"] = kwargs.get("company_id", "")
#                 data_dict["created"] = str(datetime.now())
#                 data_dict["is_dsc_signed"] = kwargs.get("is_dsc_signed", False)
#                 data_dict["dsc_placement"] = kwargs.get("dsc_placement")
#                 data_dict["primary_notice_data"] = kwargs["primary_notice_data"]
#                 data_to_dump.append(data_dict)
#     else:
#         loan_address_file_s3_map_list = kwargs["loan_address_file_s3_map_list"]
#         for row in loan_address_file_s3_map_list:
#             row["company_id"] = kwargs.get("company_id", "")
#             row["notice_type"] = kwargs.get("notice_type", "")
#             row["document_type"] = kwargs.get("document_type")
#             row["data"] = copy.deepcopy(kwargs.get("db_data", {}))
#             row["author"] = kwargs.get("author", "")
#             row["role"] = kwargs.get("role")
#             row["allocation_month"] = loan_allocation_map[row["loan_id"]]
#             row["case_type"] = kwargs.get("case_type")
#             row["is_in_case"] = kwargs.get("is_in_case", False)
#             row["case_id"] = kwargs.get("case_id", "")
#             row["stage_code"] = kwargs.get("stage_code", 0)
#             row["iteration"] = kwargs.get("iteration", 0)
#             row["is_linked_loan"] = is_linked_loan
#             row["linked_loan_id"] = kwargs.get("linked_loan_id")
#             row["batch_id"] = kwargs["batch_id"]
#             row["tracking_ids"] = kwargs.get("tracking_ids", [])
#             row["notice_mode"] = notice_mode
#             row["primary_notice_data"] = kwargs["primary_notice_data"]
#             if row.get("tracking_id"):
#                 row["notice_tracking_data"] = get_notice_tracking_data(row, **kwargs)
#         data_to_dump = loan_address_file_s3_map_list

#         for data in data_to_dump:
#             data["data"]["borrower_type"] = data["borrower_type"]

#     try:
#         url = f"{NOTICE_SERVICE_BASE_URL.rstrip('/')}/v2/notices"
#         headers = {
#             "authenticationtoken": kwargs.get("auth_token", ""),
#             "role": kwargs.get("role", ""),
#             "Content-type": "application/json",
#             "X-Request-Id": kwargs.get("X-Request-Id", ""),
#             "X-CG-User": json.dumps(kwargs.get("user", {})),
#             "X-CG-Company": json.dumps(kwargs.get("company", {})),
#         }

#         insert_result_resp = requests.post(
#             url=url,
#             json={"payload": data_to_dump, "company_id": kwargs["company_id"]},
#             data=json.dumps({"payload": data_to_dump, "company_id": kwargs["company_id"]}),
#             headers=headers,
#         )

#         logger.debug(f"notice.insert_into_db.url : {url}")
#         logger.debug(f"notice.insert_into_db.response.status_code : {insert_result_resp.status_code}")
#         insert_result = json.loads(insert_result_resp.text)
#         if insert_result.get("message") != "SUCCESS":
#             raise Exception(f"{insert_result.get('data')}")

#     except Exception as e:
#         # delete the notices from EFS in case of db insertion failure
#         if notice_mode == "physical":
#             generated_notice_pdfs_path = kwargs["local_pdf_directory_path"]
#             pdf_files_to_remove = [
#                 os.path.join(generated_notice_pdfs_path, f"{notice_id}.pdf")
#                 for notice_id in kwargs.get("notice_id_list", [])
#             ]
#             generated_notice_docs_path = kwargs["local_doc_directory_path"]
#             docx_files_to_remove = [
#                 os.path.join(generated_notice_docs_path, f"{notice_id}.docx")
#                 for notice_id in kwargs.get("notice_id_list", [])
#             ]

#             for file in docx_files_to_remove:
#                 os.remove(file)
#             for file in pdf_files_to_remove:
#                 os.remove(file)

#         logger.error(f"notice.insert_into_db.exception : {str(e)}")
#         raise Exception(f"notice.insert_into_db.exception : {str(e)}")


# def get_notice_tracking_data(notice_details, **kwargs):
#     logger.info("notice.get_notice_tracking_data")
#     notice_address_data = json.loads(notice_details["primary_address"])

#     speedpost_metadata = {
#         "speedpost_id": notice_details.get("tracking_id", ""),
#         "speedpost_tarrif": "",
#         "booked_at": "",
#         "delivery_location": "",
#         "article_type": "",
#         "speedpost_tariff": "",
#         "speedpost_booked_on": "",
#         "speedpost_delivery_status": "In-transit",
#         "speedpost_undelivered_reason": "",
#         "customer_name": notice_address_data.get("table_1_cell_1_name", ""),
#         "recipient_type": notice_address_data.get("table_1_borrower_type", ""),
#         "field_type": "",
#         "customer_address": notice_address_data.get("table_1_address_text", ""),
#         "customer_pincode": notice_address_data.get("table_1_pincode", ""),
#         "speedpost_destination_pincode": notice_address_data.get("table_1_pincode", ""),
#         "speedpost_delivery_confirmed_on": "",
#         "applicant_type": notice_address_data.get("table_1_borrower_type", ""),
#         "address_type": notice_details["address_type"],
#         "applicant_index": "",
#         "address_index": "",
#         "city": notice_address_data.get("table_1_city", ""),
#         "state": notice_address_data.get("table_1_state", ""),
#         "notice_reference_number": notice_details.get("data", {}).get("notice_reference_number"),
#         "applicant_notice_reference_number": notice_details.get("data", {}).get("applicant_notice_reference_number"),
#         "co_applicant_notice_reference_number": notice_details.get("data", {}).get(
#             "co_applicant_notice_reference_number"
#         ),
#         "events": [],
#         "speedpost_upload_datetime": str(datetime.now()),
#     }

#     speedpost_db_data = {
#         "company_id": notice_details.get("company_id", ""),
#         "loan_id": notice_details.get("loan_id", ""),
#         "notice_type": notice_details.get("notice_type", ""),
#         "s3_link": notice_details.get("s3_link", ""),
#         "s3_link_uuid": notice_details.get("s3_link_uuid", ""),
#         "document_type": "Speedpost",
#         "data": json.dumps(speedpost_metadata),
#         "allocation_month": notice_details.get("allocation_month", ""),
#         "notice_batch_id": kwargs["batch_id"],
#         "tracking_id": notice_details["tracking_id"],
#     }

#     return speedpost_db_data
