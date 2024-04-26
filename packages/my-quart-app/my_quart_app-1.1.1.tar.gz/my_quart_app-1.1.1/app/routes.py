"""
routes.py
Usage: Serves API's
"""
from app.validator_new import (
    CampaignCount,
    CampaignErrorsV1,
    CampaignFilter,
    Campaign,
    CampaignSummary,
    CampaignUpdate,
    GetCampaignData,
    CampaignDetails,
    SaveBatchResponse,
    SaveResponse,
    UpdateBatchRecord,
    CampaignCancel,
    CampaignStatus,
    CampaignErrors,
    CampaignReattempt,
    CampaignExport,
)
import json
import uuid
import datetime
from quart import request, current_app as app, make_response, g, Blueprint
from quart_schema import validate_request, validate_querystring
import logging

# from app.tasks.notice.helpers import get_directory_and_file_paths, get_draft_fields
from .service import (
    get_campaign_errors,
    generate_campaign_search_query_string,
    generate_filter_dict,
    retrigger_campaign,
    get_communication_details,
    get_full_campaign_data,
    get_campaign_report_data,
    trigger_campaign_export,
    send_campaign_export_report,
    get_campaigns_data,
    policy_control_check,
    get_mc_failure_details,
    get_mc_failure_campaign_report,
    get_master_campaign_details,
)
from .settings import (
    BASE_ROUTE,
    COMMUNICATION_SERVICE_BASE_URL,
    ATTEMPTED_DATE,
    CAMPAIGN_MAX_LIMIT,
)
from .choices import (
    TypeOfTaskChoices,
    RequestTypeChoices,
    QueueTypeChoices,
    DB_SUCCESS,
    DEFAULT_EMPTY_RESPONSE,
    DB_ERROR_RESPONSE,
    CAMPAIGN_SUBMODULE,
    CampaignDeliveryTypeChoices,
    CampaignTriggerTypeChoices,
    CAMPAIGNS_TABLE,
    MASTER_CAMPAIGN_CHANNEL,
    DATA_SCIENCE,
)

from cg_utils.authentication import login_required, get_service_permissions, verify_permission

# from .tasks.notice_preview import assign_generate_notice_preview_queue
from cg_utils import asynclient, get_profile_masked_variables
from .utils import (
    api_payload_validator,
    _dict_key_filter,
    get_campaign_summary,
    create_query,
    get_communication_masked_data,
    get_excluded_columns,
)
from .validator import (
    BatchOperationInput,
    GetBatchInput,
    ResponseInput,
    GetBatchData,
)
from .tasks.tasks import (
    delegate,
    delegate_campaign,
    assign_report_download_queue,
)
from .tasks.report import campaign_update
from http import HTTPStatus

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bp = Blueprint("queue", __name__, url_prefix=BASE_ROUTE)


@bp.route("/public/healthz", methods=["GET"])
async def _get_healthz():
    return "OK", HTTPStatus.OK.value


@bp.route("/public/permissions", methods=["GET"])
async def _get_service_permissions():
    response_json, status_code = await get_service_permissions()
    return await make_response(json.dumps(response_json), status_code)


@bp.route("/initialize_monitor", methods=["POST"])
@login_required
async def initialize_monitor():
    """
    initialize_monitor
    """
    data = await request.get_json()
    insert_dict = {}
    insert_dict["batch_id"] = data["batch_id"]
    insert_dict["batch_number"] = data["batch_number"]
    insert_dict["total_batches"] = data["total_batches"]
    insert_dict["type_of_task"] = data["type_of_task"]
    insert_dict["author"] = data["author"]
    insert_dict["company_id"] = data["company_id"]
    insert_dict["total_loans"] = data["total_loans"]
    insert_dict["extras"] = json.dumps(data["extras"])

    try:
        await app.db.insert(table="queue_monitor", values=insert_dict)
    except Exception as e:
        app.logger.error(f"queue-service.routes.initialize_monitor exception :: {str(e)}")
        return await make_response(json.dumps({"success": False, "message": f"{str(e)}"}), 400)
    return await make_response(json.dumps({"success": True, "message": "Initialize monitor successfully"}), 200)


@bp.route("/execution_response", methods=["POST"])
@login_required
async def execution_response(*args, **kwargs):
    """
    execution_response
    """
    insert_dict = {}
    data = await request.get_json()
    execution_kwargs = data.get("kwargs", {})

    insert_dict["batch_id"] = execution_kwargs["batch_id"]
    insert_dict["batch_number"] = execution_kwargs["batch_number"]
    insert_dict["total_batches"] = execution_kwargs["total_batches"]
    insert_dict["type_of_task"] = execution_kwargs["type_of_task"]
    insert_dict["author"] = execution_kwargs["author"]
    insert_dict["company_id"] = execution_kwargs["company_id"]
    insert_dict["loan_id"] = str(execution_kwargs["loan_id"])
    insert_dict["total_loans"] = execution_kwargs["total_loans"]
    insert_dict["status"] = data["status"]
    insert_dict["request_id"] = request.headers.get("X-Request-Id")

    if execution_kwargs.get("type_of_task", "") == TypeOfTaskChoices.scrape_indiapost.value:
        insert_dict["response"] = json.dumps(
            {
                "response": data["response"],
                "status_code": data["status_code"],
                "tracking_id": execution_kwargs.get("tracking_id", ""),
            }
        )
    else:
        insert_dict["response"] = json.dumps({"response": data["response"], "status_code": data["status_code"]})
        if "row_number" in execution_kwargs:
            insert_dict["row_number"] = int(execution_kwargs["row_number"])
    await app.db.insert(table="queue_monitor", values=insert_dict)
    return await make_response(
        json.dumps({"success": True, "message": "Execution response update successfully"}),
        200,
    )


@bp.route("/update/batch-execution-status", methods=["POST"])
@login_required
async def update_execution_response(*args, **kwargs):
    app.logger.info(f"app.routes.update_execution_response")
    data = await request.get_json()
    execution_kwargs = data.get("kwargs", {})

    batch_id = execution_kwargs["batch_id"]
    type_of_task = execution_kwargs["type_of_task"]
    company_id = execution_kwargs["company_id"]
    status = data["status"]
    response = json.dumps({"response": data["response"], "status_code": data["status_code"]})

    update_query = f"UPDATE queue_monitor SET response = '{response}',status = '{status}' where company_id = '{company_id}' and type_of_task = '{type_of_task}' and batch_id = '{batch_id}'"
    try:
        await app.db.execute_raw_update_query(update_query)
        return await make_response(
            json.dumps({"success": True, "message": "Execution response update successfully"}),
            200,
        )
    except Exception as e:
        app.logger.error(f"exception.app.routes.update_execution_response || {str(e)}")
        return await make_response(
            json.dumps({"success": False, "message": "Batch status could not be updated"}),
            500,
        )


@bp.route("/get_batch_number", methods=["GET"])
@login_required
async def get_batch_number(*args, **kwargs):
    """
    returns operation_batch_number
    """
    app.logger.info(f"app.routes.get_batch_number")
    batch_number = request.args["batch_number"]
    batch_id = request.args["batch_id"]
    if batch_number == "all":
        where = {"batch_id='%s' and loan_id is null and response is null": batch_id}
    else:
        where = {
            "batch_number='%s'": str(batch_number),
            "batch_id='%s' and loan_id is null and response is null": batch_id,
        }
    try:
        queue_data = await app.db.select(
            table="queue_monitor",
            columns=[
                "batch_status",
                "batch_id",
                "total_batches",
                "status",
                "batch_number",
                "email_sent",
                "created::VARCHAR",
                "updated::VARCHAR",
                "type_of_task",
                "extras",
                "company_id",
                "author",
                "total_loans",
                "loan_id",
                "response",
            ],
            where=where,
        )
    except Exception as e:
        app.logger.error(
            f"queue-service.routes.get_batch_number exception :: {str(e)}, message: batch number data failed."
        )
        return await make_response(
            json.dumps(
                {
                    "success": False,
                    "message": "batch number data failed",
                    "data": str(e),
                }
            ),
            400,
        )
    app.logger.debug("queue_data: %s", queue_data)
    if not isinstance(queue_data, list) or queue_data == [] or isinstance(queue_data, str):
        app.logger.error(f"queue-service.routes.get_batch_number, message: batch number data failed")
        return await make_response(
            json.dumps(
                {
                    "success": False,
                    "message": "batch number data failed",
                    "data": queue_data,
                }
            ),
            400,
        )

    return await make_response(
        json.dumps(
            {
                "success": True,
                "message": "batch number data successfully",
                "data": queue_data,
            }
        ),
        200,
    )


@bp.route("/execution_data", methods=["GET"])
@login_required
async def execution_data(*args, **kwargs):
    """
    returns execution data
    """
    app.logger.info(f"app.routes.execution_data")
    batch_number = request.args["batch_number"]
    batch_id = request.args["batch_id"]
    try:
        queue_data = await app.db.select(
            table="queue_monitor",
            columns=[
                "batch_status",
                "batch_id",
                "total_batches",
                "status",
                "batch_number",
                "email_sent",
                "created::VARCHAR",
                "updated::VARCHAR",
                "type_of_task",
                "extras",
                "company_id",
                "author",
                "total_loans",
                "loan_id",
                "response",
                "row_number",
                "request_id",
            ],
            where={
                "batch_number='%s'": str(batch_number),
                "batch_id='%s' and loan_id is not null and response is not null": batch_id,
            },
        )
    except Exception as e:
        app.logger.error(f"queue-serviceroutes.execution_data exception:: {str(e)}, message: execution data failed.")
        return await make_response(
            json.dumps({"success": False, "message": "execution data failed", "data": str(e)}),
            400,
        )
    app.logger.debug("queue_data:%s", queue_data)

    if not isinstance(queue_data, list) or queue_data == [] or isinstance(queue_data, str):
        app.logger.error(f"queue-service.routes.execution_data, message: execution data failed")
        return await make_response(
            json.dumps(
                {
                    "success": False,
                    "message": "execution data failed",
                    "data": queue_data,
                }
            ),
            400,
        )

    return await make_response(
        json.dumps(
            {
                "success": True,
                "message": "execution data successfully",
                "data": queue_data,
            }
        ),
        200,
    )


@bp.route("/batch_status_update", methods=["POST"])
@login_required
async def batch_status_update(*args, **kwargs):
    """
    update the status of a batch
    """
    insert_dict = {}
    data = await request.get_json()
    batch_number = data["batch_number"]
    batch_id = data["batch_id"]
    insert_dict["batch_status"] = json.dumps(data["batch_status"])

    await app.db.update(
        table="queue_monitor",
        values=insert_dict,
        where={
            "batch_number='%s' and loan_id is null and response is null": batch_number,
            "batch_id='%s'": batch_id,
        },
    )
    if str(batch_number) == str(data["total_batches"]):
        where = {
            "batch_number='%s' and loan_id is null and response is null": batch_number,
            "batch_id='%s'": batch_id,
        }
    else:
        where = {
            "batch_number='%s' and loan_id is null and response is null": str(int(batch_number) + 1),
            "batch_id='%s'": batch_id,
        }
    queue_data = await app.db.select(
        table="queue_monitor",
        columns=[
            "batch_status",
            "batch_id",
            "total_batches",
            "status",
            "batch_number",
            "email_sent",
            "created::VARCHAR",
            "updated::VARCHAR",
            "type_of_task",
            "extras",
            "company_id",
            "author",
            "total_loans",
            "loan_id",
            "response",
        ],
        where=where,
    )
    app.logger.debug("queue_data:%s", queue_data)
    if not isinstance(queue_data, list) or queue_data == [] or isinstance(queue_data, str):
        app.logger.error(f"queue-service.routes.batch_status_update, message: batch status data failed")
        return await make_response(
            json.dumps(
                {
                    "success": False,
                    "message": "batch status data failed",
                    "data": queue_data,
                }
            ),
            400,
        )

    return await make_response(
        json.dumps(
            {
                "success": True,
                "message": "batch status data successfully",
                "data": queue_data,
            }
        ),
        200,
    )


@bp.route("/batch_operations", methods=["POST"], endpoint="batch_operation")
@login_required
# @verify_permission(submodules=["speedpost_upload_activation", "whatsapp_campaigns"])
@api_payload_validator(BatchOperationInput)
async def batch_operations(*args, **kwargs):
    """
    perform bulk operation

    """
    app.logger.info("app.routes.batch_operations")
    data = await request.get_data()
    data = json.loads(data)
    user = g.user
    company = g.company
    type = data.get("type")
    channel = data.get("channel", "")
    loan_data = data.get("loan_data", [])
    author = user.get("email", None)
    if not author:
        return await make_response(
            json.dumps({"message": "failed", "output": f"No email id found on account."}),
            HTTPStatus.BAD_REQUEST.value,
        )
    if loan_data in (None, []):
        return await make_response(
            json.dumps({"message": "failed", "output": "No loan data provided"}),
            HTTPStatus.BAD_REQUEST.value,
        )
    output_msg = "Batch operation"
    if type == TypeOfTaskChoices.upload_c2c_disposition.value:
        queue = f"{app.config['QUEUE_NAME']}_c2c_disposition"
        output_msg = "Upload c2c disposition"
    elif type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_upload.value:
        queue = f"{app.config['QUEUE_NAME']}_indiapost_upload"
        output_msg = "Data upload"
    elif type == TypeOfTaskChoices.lat_long_conversion.value:
        queue = f"{app.config['QUEUE_NAME']}_generic"
        output_msg = "Address conversion"
    elif type == TypeOfTaskChoices.scrape.value and channel == TypeOfTaskChoices.indiapost_tracking.value:
        queue = f"{app.config['QUEUE_NAME']}_indiapost_tracking"
        output_msg = "Indiapost tracking"
    elif type == TypeOfTaskChoices.optin.value:
        queue = f"{app.config['QUEUE_NAME']}_optin"
        output_msg = "Optin"
    elif type == TypeOfTaskChoices.ecourt_tracking.value:
        queue = f"{app.config['QUEUE_NAME']}_ecourt_tracking"
    elif type == TypeOfTaskChoices.litigation_approval_request.value:
        queue = f"{app.config['QUEUE_NAME']}_litigation_approval_request"
        output_msg = "Litigation Approval Request"
    app.logger.info(f"batch_operations.queue: {queue}")

    batch_id = uuid.uuid4().hex
    batch_data = {}
    batch_data["type"] = type
    batch_data["channel"] = channel
    batch_data["batch_id"] = batch_id
    batch_data["company_id"] = data.get("company_id", None)
    batch_data["author"] = author
    batch_data["role"] = user.get("role")
    batch_data["author_id"] = user.get("user_id")
    batch_data["loan_data"] = json.dumps(loan_data)
    batch_data["total_loans"] = str(len(loan_data))
    batch_data["data"] = json.dumps(_dict_key_filter(data, ["loan_data", "company_id", "type", "channel", "loan_ids"]))

    try:
        db_res = await app.db.insert(table="batch_operations", values=batch_data)
        app.logger.debug(f"batch_operations.created.result :: {db_res}")
        app.logger.debug(f"batch_operations_data :: {batch_data}")
        if db_res != DB_SUCCESS:
            return await make_response(
                json.dumps({"message": "failed", "output": f"{output_msg} assignment failed"}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
        batch_data["request_id"] = request.headers.get("X-Request-Id", "")
        batch_data["user"] = user
        batch_data["queue"] = queue
        batch_data["company"] = company

        res = delegate.apply_async(queue=queue, kwargs=batch_data)
        app.logger.info(f"batch_operations.batch_id :: {batch_id}")

    except Exception as e:
        app.logger.error(f"batch_operations.exception :: {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": f"{output_msg} assignment failed"}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": f"{output_msg} assignment success",
                "data": batch_id,
            }
        ),
        HTTPStatus.OK.value,
    )


@bp.route("/save_batch_response", methods=["POST"], endpoint="save_batch_response")
@login_required
@api_payload_validator(ResponseInput)
async def save_batch_response(*args, **kwargs):
    """
    save response of batch operation
    """
    app.logger.info("app.routes.save_batch_response")
    data = await request.get_data()
    data = json.loads(data)

    response = data["response"]
    payload = data["payload"]
    response["batch_id"] = payload["batch_id"]

    type = payload["type"]
    if type == TypeOfTaskChoices.notice.value:
        table = "notice_loans"
    elif type == TypeOfTaskChoices.scrape.value:
        table = "indiapost_loans"
    else:
        table = "batch_loans"
    try:
        db_res = await app.db.insert(table=table, values=response)
    except Exception as e:
        app.logger.error(f"save_batch_response.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    if db_res != DB_SUCCESS:
        return await make_response(
            json.dumps({"message": "failed", "output": f"{table} response creation failed"}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": f"{table} response creation success",
            }
        ),
        HTTPStatus.CREATED.value,
    )


@bp.route("/get_batch_data", methods=["GET"], endpoint="get_batch_data_")
@login_required
@api_payload_validator(GetBatchData)
async def get_batch_data(*args, **kwargs):
    app.logger.info("app.routes.get_batch_data")
    data = await request.get_data()
    data = json.loads(data)
    batch_id_list = data["batch_id"]
    company_id = data["company_id"]

    try:
        batch_data = await app.db.select(
            table="batch_operations",
            columns=[
                "batch_id",
                "data",
            ],
            where={"batch_id=any(array%s)": batch_id_list, "company_id='%s'": company_id, "is_deleted=%r": False},
        )
        app.logger.info(f"get_batch_data.success")
        return await make_response(
            json.dumps(
                {
                    "message": "success",
                    "output": batch_data,
                }
            ),
            HTTPStatus.OK.value,
        )
    except Exception as e:
        app.logger.error(f"get_batch_data.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@bp.route("/batch_data", methods=["POST"], endpoint="get_batch_data")  # 204 changes
@login_required
# @verify_permission(submodules=["speedpost_upload_activation", "whatsapp_campaigns"])
@api_payload_validator(GetBatchInput)
async def batch_data(*args, **kwargs):
    """
    Fetch metadata and failed records of a batch operation
    """
    app.logger.info("app.routes.batch_data")
    data = await request.get_data()
    data = json.loads(data)
    channel = data.get("channel", "")
    type = data.get("type", "")
    columns = ["status", "response", "status_code", "loan_id"]
    if type == TypeOfTaskChoices.notice.value:
        table = "notice_loans"
    elif type == TypeOfTaskChoices.scrape.value:
        table = "indiapost_loans"
        columns.append("tracking_number")
        columns.append("company_id")
    else:
        table = "batch_loans"
    batch_id = data["batch_id"]
    try:
        if type == TypeOfTaskChoices.notice.value:
            where = {"batch_id='%s'": batch_id, "is_deleted=%s": False}
        else:
            where = {"batch_id='%s'": batch_id, "status='%s'": "FAIL"}

        batch_loans_data = await app.db.select(
            table=table,
            columns=columns,
            where=where,
        )

        batch_data = await app.db.select(
            table="batch_operations",
            columns=[
                "batch_id",
                "type",
                "channel",
                "created::VARCHAR",
                "data",
                "author",
                "role",
                "company_id",
                "total_loans",
                "loan_data",
            ],
            where={"batch_id='%s'": batch_id, "type='%s'": type, "is_deleted=%s": False},
        )
        app.logger.info(f"batch_data.success")
    except Exception as e:
        app.logger.error(f"batch_data.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    if (not isinstance(batch_loans_data, list) or isinstance(batch_loans_data, str)) and (
        not isinstance(batch_data, list) or isinstance(batch_data, str)
    ):
        return await make_response(
            json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": {
                    "batch_loans_data": batch_loans_data,
                    "batch_data": batch_data,
                },
            }
        ),
        HTTPStatus.OK.value,
    )


#############################################################################################
######################## Campaigns apis #####################################################
#############################################################################################


@bp.route("/campaign_data", methods=["POST"], endpoint="get_campaign_data")
@login_required
# @verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_request(GetCampaignData)
async def campaign_data(*args, data: GetCampaignData, **kwargs):
    """
    Fetch metadata and records of a campaign
    """
    app.logger.info("app.routes.campaign_data")
    data = data.dict()
    trigger_report_flag = data.get("trigger_report_flag", False)
    channel = data["channel"]
    table = f"campaign_{channel}"
    campaign_id = data["campaign_id"]
    updated_end_time_flag = data.get("updated_end_time_flag", False)
    is_deleted = data.get("is_deleted", False)
    profile_id = data.get("profile_id")
    masking = data.get("masking", False)
    attempted_live = False
    comm_failed_count = None
    if updated_end_time_flag:
        try:
            query = f"update campaigns set latest_triggered_time= NOW() where campaign_id='{campaign_id}';"
            await app.campaign_db.execute_raw_update_query(query)
        except Exception as e:
            app.logger.error(f"campaign_data.updated_end_time_flag: error{str(e)}")

        app.logger.info(f"routes.campaign.delegate_campaign.campaign_id :: {campaign_id}")
    try:
        campaign_data = await app.campaign_db.select(
            table="campaigns",
            columns=[
                "campaign_id",
                "name",
                "channel",
                "created::VARCHAR",
                "data",
                "type",
                "author",
                "role",
                "company_id",
                "total_loans",
                "description",
                "loan_data",
            ],
            where={"campaign_id='%s'": campaign_id, "channel='%s'": channel, "is_deleted = %s": is_deleted},
        )
        app.logger.info(f"campaign_data.success")
        if not isinstance(campaign_data, list) or isinstance(campaign_data, str):
            return await make_response(
                json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
        elif not campaign_data:
            return await make_response(
                json.dumps({"message": "failed", "output": "invalid campaign_id provided"}),
                HTTPStatus.BAD_REQUEST.value,
            )
        campaign_created_date = campaign_data[0].get("created")
        company_id = campaign_data[0]["company_id"]
        if campaign_created_date:
            campaign_created_date = campaign_created_date.split(" ")[0]
        campaign_created_date = datetime.datetime.strptime(campaign_created_date, "%Y-%m-%d").date()
        if campaign_created_date > ATTEMPTED_DATE and not trigger_report_flag:
            # COMM LEVEL DATA FOR FAILURE
            table = f"{channel}_failure"
            channel_campaigns_columns = [
                "'FAIL' as status",
                "error as response",
                "status_code",
                "loan_id",
                "created::VARCHAR",
                "error_code",
                "applicant_type",
                "contact_to",
            ]
            attempted_live = True
            channel_campaign_data = await app.comm_db.select(
                table=table,
                columns=channel_campaigns_columns,
                where={"company_id='%s'": company_id, "campaign_id='%s'": campaign_id, "is_deleted = %s": is_deleted},
            )
            if not isinstance(channel_campaign_data, list) or isinstance(channel_campaign_data, str):
                return await make_response(
                    json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
                    HTTPStatus.INTERNAL_SERVER_ERROR.value,
                )
            comm_failed_count = len(channel_campaign_data)
            if masking and profile_id:
                masked_variables = await get_profile_masked_variables(
                    company_id=company_id, permission_group_id=profile_id
                )
                app.logger.info(f"campaign_data.masked_variables {masked_variables}")
                if masked_variables:
                    for idx, channel_data in enumerate(channel_campaign_data):
                        channel_campaign_data[idx] = await get_communication_masked_data(
                            channel_data, masked_variables, channel, channel_data["applicant_type"]
                        )

        else:
            channel_campaigns_columns = [
                "status",
                "response",
                "status_code",
                "loan_id",
                "created::VARCHAR",
                "error_code",
            ]
            channel_campaign_data = await app.campaign_db.select(
                table=table,
                columns=channel_campaigns_columns,
                where={"campaign_id='%s'": campaign_id, "is_deleted = %s": is_deleted},
            )

            if not isinstance(channel_campaign_data, list) or isinstance(channel_campaign_data, str):
                return await make_response(
                    json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
                    HTTPStatus.INTERNAL_SERVER_ERROR.value,
                )

    except Exception as e:
        app.logger.error(f"campaign_data.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": {
                    "channel_campaign_data": channel_campaign_data,
                    "campaign_data": campaign_data,
                    "attempted_live": attempted_live,
                    "comm_failed_count": comm_failed_count,
                },
            }
        ),
        HTTPStatus.OK.value,
    )


@bp.route("/campaign_export", methods=["POST"], endpoint="campaign_export")
@login_required
@verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_request(GetCampaignData)
async def campaign_export(*args, data: GetCampaignData, **kwargs):
    app.logger.info("app.routes.campaign_export")
    data = data.dict()

    channel = data["channel"]
    table = f"campaign_{channel}"
    campaign_id = data["campaign_id"]
    is_deleted = data.get("is_deleted", False)
    try:
        campaign_export = await app.campaign_db.select(
            table=table,
            columns=["status", "response", "status_code", "loan_id"],
            where={"campaign_id='%s'": campaign_id, "status='%s'": "FAIL", "is_deleted = %s": is_deleted},
        )
        app.logger.info(f"campaign_export.success")
    except Exception as e:
        app.logger.error(f"campaign_export.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    if not isinstance(campaign_export, list) or isinstance(campaign_export, str):
        return await make_response(
            json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    if campaign_export == []:
        return await make_response(DEFAULT_EMPTY_RESPONSE, HTTPStatus.OK.value)

    return await make_response(
        json.dumps({"message": "success", "output": campaign_export}),
        HTTPStatus.OK.value,
    )


@bp.route("/get_campaigns", methods=["POST"], endpoint="get_campaigns")
@login_required
@verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_request(CampaignDetails)
async def get_campaigns(*args, data: CampaignDetails, **kwargs):
    """
    Get campaign details
    """
    output = []
    app.logger.info("app.routes.get_campaigns")
    data = data.dict()
    company_id = data["company_id"]
    page_number = data["page_number"] - 1
    page_size = data["page_size"]
    is_deleted = data["is_deleted"]
    query_arg = data.get("query_arg", None)
    search_type = data.get("search_type", "campaign_name")
    filter = data.get("filter", None)
    parent_campaign_id = data.get("parent_campaign_id")
    offset = page_number * page_size
    is_master_campaign_request = data["is_master_campaign_request"]
    limit = page_size
    filter_data = ""
    try:
        filter_data = await generate_filter_dict(filter)
        filter_data = f" and {filter_data}" if filter_data else filter_data
    except Exception as e:
        app.logger.error(f"Exception occurred in creating filter_data {str(e)}")
    search_query_string = generate_campaign_search_query_string(search_type, query_arg.strip()) if query_arg else ""

    try:
        query = f"select count(campaign_id) over() as total_campaigns, company_id, data as comm_data, report_url, campaign_id, name, channel, to_char(created, 'YYYY-MM-DD HH24:MI:SS') as trigger_time, to_char(latest_triggered_time, 'YYYY-MM-DD HH24:MI:SS') as latest_trigger_time, SPLIT_PART(author, '@', 1) as author, description, created, latest_triggered_time, trigger_status, trigger_progress_count, delivery_status, delivery_progress_count, is_stopped, trigger_stop_count, total_loans, current_delivery_count, current_trigger_count, current_delivery_status, current_trigger_status, helicarrier_trigger,queue_duration, sub_campaigns_count from campaigns where company_id='{company_id}' and is_deleted = {is_deleted} {search_query_string} {filter_data}"
        if parent_campaign_id:
            query += f" AND parent_campaign_id = '{parent_campaign_id}' order by created DESC;"
        elif is_master_campaign_request:
            query += f" AND master_campaign = True order by created DESC offset {offset} limit {limit};"
        else:
            query += f" AND master_campaign = False AND parent_campaign_id is NULL order by created DESC offset {offset} limit {limit};"
        campaign_data = await app.campaign_db.execute_raw_select_query(query)
        app.logger.debug(f"get_campaigns.campaign_data :: {campaign_data}")
    except Exception as e:
        app.logger.error(f"get_campaigns.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    if not isinstance(campaign_data, list):
        return await make_response(
            json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    elif not campaign_data:
        return await make_response(json.dumps(DEFAULT_EMPTY_RESPONSE), HTTPStatus.OK.value)

    try:
        for data in campaign_data:
            channel = data["channel"]
            author = data.get("author")
            created = data.pop("created", None)
            total_loans = data.get("total_loans")
            current_delivery_count = data.get("current_delivery_count")
            current_trigger_count = data.get("current_trigger_count")
            current_delivery_status = data.get("current_delivery_status")
            current_trigger_status = data.get("current_trigger_status")
            helicarrier_trigger = data.get("helicarrier_trigger")
            latest_triggered_time = data.pop("latest_triggered_time", None)
            if author not in ("", None):
                author = author.split(".")
                data_author = " ".join([i.capitalize() for i in author])
            else:
                data_author = author
            total_campaigns = data.get("total_campaigns", 0)
            campaign_dict = data
            comm_data = json.loads(data["comm_data"])

            if channel != RequestTypeChoices.dtmf_ivr.value:
                if not isinstance(comm_data, dict):
                    comm_data = json.loads(comm_data)
                if comm_data.get("template_name"):
                    template_name = comm_data["template_name"]
                elif comm_data.get("comm_dict", {}).get("template_name"):
                    template_name = comm_data["comm_dict"]["template_name"]
                else:
                    template_name = ""
                rule_id = comm_data.get("rule_id", "")
                rule_name = comm_data.get("rule_name", "")
                selected_transactions = comm_data.get("selected_transactions", False)
            else:
                template_name = comm_data.get("template_name", "")
                rule_id = comm_data.get("rule_id", "")
                rule_name = comm_data.get("rule_name", "")
                selected_transactions = comm_data.get("selected_transactions", False)
            data.pop("comm_data", None)
            data["template_name"] = template_name
            data["rule_id"] = rule_id
            data["rule_name"] = rule_name
            data["rule_type"] = comm_data.get("rule_type", "automatic") if rule_id else ""
            data["selected_transactions"] = selected_transactions
            is_stopped = data.get("is_stopped")
            trigger_stop_count = data.get("trigger_stop_count")
            trigger_percentage = 0
            delivery_percentage = 0

            if helicarrier_trigger:
                delivery_status = current_delivery_status
                trigger_status = current_trigger_status
                trigger_progress_count = f"{current_trigger_count}/{total_loans}"
                delivery_progress_count = f"{current_delivery_count}/{total_loans}"
            else:
                delivery_progress_count = data.get("delivery_progress_count")
                trigger_progress_count = data.get("trigger_progress_count")
                delivery_status = data.get("delivery_status")
                trigger_status = data.get("trigger_status")

            if delivery_status == CampaignDeliveryTypeChoices.partial_completed.value:
                delivery_status = CampaignDeliveryTypeChoices.completed.value
            if trigger_status == CampaignTriggerTypeChoices.partial_completed.value:
                trigger_status = CampaignTriggerTypeChoices.completed.value
            if (
                trigger_status == CampaignTriggerTypeChoices.completed.value
                and latest_triggered_time
                and created
                and not campaign_dict.get("queue_duration")
                and latest_triggered_time != created
            ):
                queue_duration = latest_triggered_time - created
                if queue_duration < datetime.timedelta(minutes=1):
                    queue_duration = "< 1 min"
                campaign_dict["queue_duration"] = str(queue_duration).split(".")[0]
            if is_stopped:
                trigger_progress_count = f"{trigger_stop_count}/{total_loans}"
                if trigger_status == CampaignTriggerTypeChoices.completed.value:
                    trigger_status = CampaignTriggerTypeChoices.stopped.value
                else:
                    trigger_status = CampaignTriggerTypeChoices.stopping.value
            if trigger_progress_count:
                count_value = trigger_progress_count.split("/")
                trigger_percentage = (
                    str((int(count_value[0]) / int(count_value[1])) * 100) if int(count_value[1]) else 0
                )
            if delivery_progress_count:
                count_value = delivery_progress_count.split("/")
                delivery_percentage = (
                    str((int(count_value[0]) / int(count_value[1])) * 100) if int(count_value[1]) else 0
                )
            campaign_dict["trigger_status"] = trigger_status
            campaign_dict["trigger_progress_count"] = trigger_progress_count
            campaign_dict["trigger_percentage"] = trigger_percentage
            campaign_dict["delivery_status"] = delivery_status
            campaign_dict["delivery_progress_count"] = delivery_progress_count
            campaign_dict["delivery_percentage"] = delivery_percentage
            campaign_dict["author"] = data_author
            campaign_dict["total_campaigns"] = total_campaigns
            if is_master_campaign_request:
                campaign_dict["channel_count"] = data["sub_campaigns_count"]
                campaign_dict["source"] = comm_data["mc_source"] if comm_data.get("mc_source") else DATA_SCIENCE
            app.logger.info(
                f"get_campaigns.delivery_status {delivery_progress_count}---{delivery_status} ---{total_campaigns}"
            )
            output.append(campaign_dict)

        return await make_response(
            json.dumps(
                {
                    "message": "success",
                    "output": output,
                }
            ),
            HTTPStatus.OK.value,
        )
    except Exception as e:
        app.logger.error(f"get_campaigns.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@bp.route("/save_response", methods=["POST"], endpoint="save_response")
@login_required
# @verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_request(SaveResponse)
async def save_response(*args, data: SaveResponse, **kwargs):
    """
    Save response of a campaign
    """
    app.logger.info(f"app.routes.save_response")
    data = data.dict()
    try:
        response = data["response"]
        payload = data["payload"]
        response["campaign_id"] = payload["campaign_id"]
        table = f"campaign_{payload['channel']}"
        app.logger.debug(f"save_response.response.{payload['campaign_id']} {response}")
        db_res = await app.campaign_db.insert(table=table, values=response)
        if db_res != 1:
            return await make_response(
                json.dumps({"message": "failed", "output": f"{table} response creation failed"}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
    except Exception as e:
        app.logger.error(f"save_response.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": "campaign creation success",
            }
        ),
        HTTPStatus.CREATED.value,
    )


@bp.route(
    "/save_campaign_batch_response",
    methods=["POST"],
    endpoint="save_campaign_batch_response",
)
@login_required
# @verify_permission(submodules=["dtmf_ivr_campaigns"])
@validate_request(SaveBatchResponse)
async def save_campaign_batch_response(*args, data: SaveBatchResponse, **kwargs):
    """
    Save multiple records for a campaign

    """
    app.logger.info(f"app.routes.save_campaign_batch_response")
    data = data.dict()
    insert_values = ""
    try:
        insert_list = data["insert_list"]
        payload = data["payload"]
        table = f"campaign_{payload['channel']}"
        insert_base_string = "INSERT INTO {0} (campaign_id, status, response, status_code, loan_id, error_code, error_name, error_description) VALUES {1}"
        app.logger.debug(f"save_campaign_batch_response.response.{payload['campaign_id']} {insert_list}")
        for insert in insert_list:
            insert["response"] = insert["response"].replace("'", "''")
            values = " ('{campaign_id}', '{status}', '{response}', '{status_code}', '{loan_id}', '{error_code}', '{error_name}', '{error_description}'),".format(
                campaign_id=insert["campaign_id"],
                status=insert["status"],
                response=insert["response"],
                status_code=insert["status_code"],
                loan_id=insert["loan_id"],
                error_code=insert["error_code"],
                error_name=insert["error_name"],
                error_description=insert["error_description"],
            )
            insert_values += values
        insert_values = insert_values[:-1]
        excluded_columns = [
            "status",
            "response",
            "status_code",
            "loan_id",
            "error_code",
            "error_name",
            "error_description",
        ]
        final_query = insert_base_string.format(table, insert_values)
        final_query += f" ON CONFLICT (campaign_id,loan_id) DO UPDATE SET {get_excluded_columns(excluded_columns)};"
        db_res = await app.campaign_db.execute_raw_insert_query(final_query)
        if not (db_res and isinstance(db_res, int)):
            app.logger.error(f"save_campaign_batch_response.db.error {db_res}")
            return await make_response(
                json.dumps({"message": "failed", "output": f"{table} response creation failed"}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
    except Exception as e:
        app.logger.error(f"save_campaign_batch_response.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": "campaign creation success",
            }
        ),
        HTTPStatus.CREATED.value,
    )


# @bp.route("/report", methods=["POST"], endpoint="get_campaign_report")
# @login_required
# @verify_permission(submodules=CAMPAIGN_SUBMODULE)
# @validate_request(ReportSchema)
# async def report(*args, data: ReportSchema, **kwargs):
#     """
#     Generate report for a campaign
#     """
#     app.logger.info(f"app.routes.report")
#     data = data.dict()
#     campaign_id = data["campaign_id"]
#     channel = data["channel"]
#     queue = f"{app.config['QUEUE_NAME']}_{QueueTypeChoices.reporting.value}"
#     user = g.user
#     author = user.get("email", None)
#     if not author:
#         return await make_response(
#             json.dumps({"message": "failed", "output": f"No email id found on account."}),
#             HTTPStatus.BAD_REQUEST.value,
#         )
#     data["author"] = author
#     data["user"] = user
#     data["company"] = g.company
#     data["request_id"] = request.headers.get("X-Request-Id", "")
#     data["queue"] = queue
#     try:
#         campaign_comm_export.apply_async(queue=queue, kwargs=data)

#         app.logger.info(f"report.campaign_id :: {campaign_id}")
#     except Exception as e:
#         app.logger.error(f"report.exception :: {str(e)}")
#         return await make_response(
#             json.dumps({"message": "failed", "output": f"{channel} report generation failed"}),
#             HTTPStatus.INTERNAL_SERVER_ERROR.value,
#         )
#     return await make_response(
#         json.dumps(
#             {
#                 "message": "success",
#                 "output": f"Report will be shared on your email :: {author}",
#             }
#         ),
#         HTTPStatus.OK.value,
#     )


@bp.route("/campaign", methods=["POST"], endpoint="create_campaign")
@login_required
# @verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_request(Campaign)
async def campaign(*args, data: Campaign, **kwargs):
    """
    Communication campaign creation
    """
    app.logger.info(f"app.routes.campaign")
    data = data.dict()
    allocation_month = data.get("allocation_month", None)
    if not data.get("rule_id"):
        data.pop("rule_id")
        data.pop("rule_name")
        data.pop("ai_author_ids")
    app.logger.debug(f"Allocation Month: {allocation_month}")
    company = g.company
    company_id = data.get("company_id", None)
    campaign_data = data["campaign_data"]
    channel = campaign_data["channel"]
    if not company.get("country_isd_code"):
        return await make_response(
            json.dumps(
                {
                    "message": "failed",
                    "output": "country isd code not found",
                }
            ),
            HTTPStatus.BAD_REQUEST.value,
        )
    communication_control_response = await policy_control_check(company_id, channel)
    if communication_control_response["status_code"] != HTTPStatus.OK.value:
        return await make_response(
            json.dumps(
                {
                    "message": communication_control_response["message"],
                    "output": communication_control_response["output"],
                }
            ),
            communication_control_response["status_code"],
        )
    try:
        if allocation_month.lower() != "overall":
            allocation_month_ = (
                datetime.datetime.strptime(allocation_month, "%Y-%m-%d").replace(day=1).strftime("%Y-%-m-%d")
            )
            if allocation_month_ != allocation_month:
                return await make_response(
                    json.dumps(
                        {
                            "message": "failed",
                            "output": "allocation month format is not correct",
                        }
                    ),
                    HTTPStatus.BAD_REQUEST.value,
                )
    except Exception as e:
        app.logger.error(f"campaign.format_allocation.exception: {str(e)}")
        return await make_response(
            json.dumps(
                {
                    "message": "failed",
                    "output": "allocation month format is not correct",
                }
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    user = g.user
    author = user.get("email", None)
    if not author:
        return await make_response(
            json.dumps({"message": "failed", "output": f"No email id found on account."}),
            HTTPStatus.BAD_REQUEST.value,
        )
    loan_data = data.get("loan_data", [])
    total_loans = len(loan_data)
    if total_loans > int(CAMPAIGN_MAX_LIMIT):
        return await make_response(
            json.dumps(
                {
                    "message": "failed",
                    "output": f"Maximum request length exceeded. Max request length allowed is {CAMPAIGN_MAX_LIMIT}",
                }
            ),
            HTTPStatus.BAD_REQUEST.value,
        )
    campaign_id = uuid.uuid4().hex
    # additional_loan_data key is used for additional details that needs to passed to communication service for a particular loan
    additional_loan_data = data.get("additional_loan_data", {})
    campaign_data["campaign_id"] = campaign_id
    campaign_data["company_id"] = company_id
    campaign_data["author"] = author
    campaign_data["role"] = user.get("role")
    campaign_data["author_id"] = user.get("user_id")
    campaign_data["loan_data"] = json.dumps(loan_data)
    campaign_data["total_loans"] = str(total_loans)
    campaign_data["delivery_progress_count"] = f"0/{campaign_data['total_loans']}"
    campaign_data["trigger_progress_count"] = f"0/{campaign_data['total_loans']}"
    data = _dict_key_filter(data, ["campaign_data", "loan_data", "company_id", "additional_loan_data"])

    queue = f"{app.config['QUEUE_NAME']}_{channel}"

    if channel == RequestTypeChoices.dtmf_ivr.value:
        data["comm_dict"] = {}
    campaign_data["data"] = json.dumps(data)

    try:
        db_res = await app.campaign_db.insert(table="campaigns", values=campaign_data)
        app.logger.debug(f"campaign.created.result :: {db_res}")
        app.logger.debug(f"campaign.campaign_data :: {campaign_data}")

        if db_res != DB_SUCCESS:
            return await make_response(
                json.dumps(
                    {
                        "message": "failed",
                        "output": f"{channel} campaign creation failed",
                    }
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
        trigger_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        campaign_data["request_id"] = request.headers.get("X-Request-Id", "")
        campaign_data["queue"] = queue
        campaign_data["user"] = user
        campaign_data["trigger_time"] = trigger_time
        campaign_data["company"] = company
        if channel in (
            RequestTypeChoices.dtmf_ivr.value,
            RequestTypeChoices.whatsapp.value,
            RequestTypeChoices.sms.value,
        ):  # this check is for bfi only
            # added key additional_loan_data to add the bfi related data in comm_dict
            campaign_data["additional_loan_data"] = additional_loan_data
        res = delegate_campaign.apply_async(queue=queue, kwargs=campaign_data)
        app.logger.info(f"campaign.campaign_id :: {campaign_id}")
    except Exception as e:
        app.logger.error(f"campaign.exception :: {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": f"{channel} campaign creation failed"}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": f"{channel} campaign creation success",
                "data": campaign_id,
            }
        ),
        HTTPStatus.OK.value,
    )


@bp.route("/campaign/summary", methods=["POST"], endpoint="campaign_summary")
@login_required
@verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_request(CampaignSummary)
async def campaign_summary(*args, data: CampaignSummary, **kwargs):
    """
    Fetches communication summary of a single campaign

    """
    app.logger.info("app.routes.campaign_summary")
    data = data.dict()
    company_id = data.get("company_id", None)
    campaign_id = data.get("campaign_id", None)
    channel = data.get("channel", None)
    is_deleted = data.get("is_deleted", False)
    campaign_date = data["created"]
    completion_summary = data.get("completion_summary", False)
    attempted_live = False
    failure_count = 0
    filters = None
    trigger_errors = []
    campaign_export_output = {}
    campaign_data = {}
    if channel != "NA":
        try:
            export_comm_url = f"{COMMUNICATION_SERVICE_BASE_URL}/campaigns/count?company_id={company_id}&campaign_id={campaign_id}&channel={channel}&campaign_summary=True&is_deleted={is_deleted}"
            app.logger.debug(f"campaign_summary.export_campaign.url: {export_comm_url}")
            campaign_export = await asynclient.get(
                url=export_comm_url,
                headers={"Content-Type": "application/json"},
            )
            app.logger.debug(f"campaign_summary.export_campaign.status_code: {campaign_export.status_code}")
            if campaign_export.status_code != HTTPStatus.OK.value:
                app.logger.error(f"campaign_summary.export_campaign.error {campaign_export.text}")
                return await make_response(
                    json.dumps(
                        {
                            "message": "failed",
                            "output": "Failed to fetch campaign summary details",
                        }
                    ),
                    HTTPStatus.FAILED_DEPENDENCY.value,
                )
        except Exception as e:
            app.logger.error(f"campaign_summary.export_campaign.exception: {str(e)}")
            return await make_response(
                json.dumps(
                    {
                        "message": "failed",
                        "output": f"Failed to fetch campaign summary details: {str(e)}",
                    }
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
        # convert date strings to datetime objects
        campaign_date = datetime.datetime.strptime(campaign_date, "%Y-%m-%d").date()
        if campaign_date > ATTEMPTED_DATE:
            app.logger.info("campaign_summary.export_campaign.attempted_live")
            attempted_live = True
        campaign_metadata = await get_campaigns_data(company_id=company_id, campaign_id=campaign_id)
        if campaign_metadata:
            filters = campaign_metadata.get("filters")
        campaign_data["filters"] = filters
        campaign_export = json.loads(campaign_export.text)
        campaign_export_output = campaign_export.get("output", [])
        if not campaign_export_output:
            if not attempted_live:
                return await make_response(
                    json.dumps(
                        {
                            "message": "success",
                            "output": f"No summary details found for campaign: {campaign_id}",
                            "data": campaign_data,
                        }
                    ),
                    HTTPStatus.OK.value,
                )
            else:
                campaign_export_output = {}
        else:
            # using data of index 0 of campaign_export_output as we are fetching and returning summary of a single campaign
            campaign_export_output = campaign_export_output[0]
        if attempted_live:
            include_attempted_condition = ""
            if channel == RequestTypeChoices.email.value:
                include_attempted_condition = "and include_attempted = true"
            try:
                query = f"select error_name, count(*) as count from {channel}_failure where company_id = '{company_id}' and campaign_id = '{campaign_id}'and is_deleted ={is_deleted} {include_attempted_condition} group by error_name;"
                trigger_errors = await app.comm_db.execute_raw_select_query(query)
                app.logger.debug(f"get_campaign_summary.failure_count_data :: {failure_count}")
            except Exception as e:
                app.logger.error(f"get_campaign_summary.failure_count_data.exception {str(e)}")
                return await make_response(
                    json.dumps({"message": "failed", "output": str(e)}),
                    HTTPStatus.INTERNAL_SERVER_ERROR.value,
                )
            if not isinstance(trigger_errors, list) or isinstance(trigger_errors, str):
                return await make_response(
                    json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
                    HTTPStatus.INTERNAL_SERVER_ERROR.value,
                )
            failure_count = 0
            for error_dict in trigger_errors:
                failure_count += error_dict.get("count", 0)
    else:
        try:
            query = f"select error_name, count(*) as count from mc_failure where company_id = '{company_id}' and campaign_id = '{campaign_id}'and is_deleted ={is_deleted} group by error_name;"
            trigger_errors = await app.comm_db.execute_raw_select_query(query)
            app.logger.debug(f"get_campaign_summary.trigger_errors :: {trigger_errors}")
            if not trigger_errors and isinstance(trigger_errors, list):
                return await make_response(
                    json.dumps({"message": "failed", "output": "Campaigns summary details not found"}),
                    HTTPStatus.BAD_REQUEST.value,
                )
            elif not isinstance(trigger_errors, list):
                return await make_response(
                    json.dumps({"message": "failed", "output": "Failed to fetch campaigns summary details"}),
                    HTTPStatus.INTERNAL_SERVER_ERROR.value,
                )
            else:
                for error_dict in trigger_errors:
                    failure_count += error_dict.get("count", 0)
        except Exception as e:
            app.logger.error(f"get_campaign_summary.campaign_summary.exception {str(e)}")
            return await make_response(
                json.dumps({"message": "failed", "output": "Failed to fetch campaigns summary details"}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
    campaign_summary_dict = get_campaign_summary(
        campaign_export_output,
        channel,
        failed_count=failure_count,
        attempted_live=attempted_live,
        trigger_errors=trigger_errors,
        completion_summary=completion_summary,
    )
    if channel == "NA":
        campaign_summary_dict["attempted"] = failure_count
    app.logger.debug(f"campaign_summary.campaign_summary_dict: {campaign_summary_dict}")
    return await make_response(
        json.dumps({"message": "success", "output": campaign_summary_dict, "data": campaign_data}),
        HTTPStatus.OK.value,
    )


@bp.route("/update/campaign/status", methods=["POST"], endpoint="update_campaign_status")
@login_required
@verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_request(CampaignUpdate)
async def update_campaign_status(*args, data: CampaignUpdate, **kwargs):
    """
    update status of communication campaigns.
    """
    app.logger.info(f"app.routes.update_campaign")
    data = data.dict()
    company_id = data["company_id"]
    campaign_count_export = data.pop("campaign_count_export", [])
    campaign_export_output_map = {}
    is_deleted = data.get("is_deleted", False)
    for campaign_export_item in campaign_count_export:
        campaign_id = campaign_export_item["campaign_id"]
        campaign_export_output_map[campaign_id] = campaign_export_item
    campaign_ids = data.get("campaign_ids").split(",")
    campaign_id_condition = ""
    if len(campaign_ids) == 1:
        campaign_id_condition = f" and campaign_id = '{campaign_ids[0]}'"
    elif len(campaign_ids) > 1:
        campaign_id_condition = f" and campaign_id in {str(tuple(campaign_ids))}"
    data["campaign_export_output_map"] = campaign_export_output_map
    queue = f"{app.config['QUEUE_NAME']}_{QueueTypeChoices.campaign_update.value}"
    user = g.user
    data["user"] = user
    data["company"] = g.company
    data["request_id"] = request.headers.get("X-Request-Id", "")
    try:
        query = f"select company_id, data as comm_data, report_url, trigger_status, trigger_progress_count, delivery_status, delivery_progress_count, email_report_sent, sms_report_sent, campaign_id, channel, name, author, total_loans,created, latest_triggered_time, author_id, trigger_stop_count from campaigns where company_id='{company_id}' and is_deleted = {is_deleted} {campaign_id_condition} order by created DESC;"
        campaign_data = await app.campaign_db.execute_raw_select_query(query)
        app.logger.debug(f"update_campaign_status.campaign_data :: {campaign_data}")
        if isinstance(campaign_data, str):
            return await make_response(
                json.dumps(
                    {
                        "message": "failed",
                        "output": DB_ERROR_RESPONSE,
                    }
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
        if campaign_data == []:
            return await make_response(
                json.dumps(
                    {
                        "message": "success",
                        "output": f"Campaigns not found for company_id: {company_id}.",
                    }
                ),
                HTTPStatus.OK.value,
            )
        data["campaign_data"] = campaign_data
        data["queue"] = queue
        campaign_update.apply_async(queue=queue, kwargs=data)
        app.logger.info(f"update_campaign_status.campaign_update.company_id: {company_id}")
    except Exception as e:
        app.logger.error(f"update_campaign_status.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": "Failed to update campaign details"}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": f"Campaigns added to queue successfully.",
            }
        ),
        HTTPStatus.OK.value,
    )


@bp.route("/update/data", methods=["POST"], endpoint="update_data")
@login_required
@validate_request(UpdateBatchRecord)
async def update_data(*args, data: UpdateBatchRecord, **kwargs):
    app.logger.info(f"app.routes.update_data")
    data = data.dict()

    try:
        operation = "update"
        table = data.get("table")
        set_clause = data.get("set_clause")
        from_values = data.get("from_values")
        from_columns = data.get("from_columns")
        from_alias_name = data.get("from_alias_name")
        where_clause = data.get("where")
        query = create_query(
            table,
            set_clause,
            from_values,
            from_columns,
            from_alias_name,
            where_clause,
            operation,
        )
        app.logger.info(f"update_data.db.query {query}")
        result = await app.campaign_db.execute_raw_update_query(query)
        if not (result and isinstance(result, int)) or isinstance(result, str):
            app.logger.error(f"update_data.db.error {result}")
            return await make_response(
                json.dumps({"message": "failed", "output": f"Failed to update data"}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
    except Exception as e:
        app.logger.error(f"update_data.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": "Failed to update data"}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": f"Data updated successfully.",
            }
        ),
        HTTPStatus.OK.value,
    )


@bp.route("/campaign/count", methods=["POST"], endpoint="get_campaign_count")
@login_required
@validate_request(CampaignCount)
async def campaign_count(*args, data: CampaignCount, **kwargs):
    """
    Fetch success and failure count of a campaign
    """
    app.logger.info(f"app.routes.campaign_count")
    data = data.dict()
    campaign_id = data["campaign_id"]
    table = data["table"]
    is_deleted = data.get("is_deleted", False)
    try:
        query = f"select status, count(distinct(loan_id)), error_code from {table} where campaign_id='{campaign_id}' and is_deleted = {is_deleted} group by status, error_code;"
        campaigns_count_result = await app.campaign_db.execute_raw_select_query(query)
        app.logger.debug(f"campaign_count.result :: {campaigns_count_result}")
        if isinstance(campaigns_count_result, str):
            return await make_response(
                json.dumps(
                    {
                        "message": "failed",
                        "output": DB_ERROR_RESPONSE,
                    }
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
    except Exception as e:
        app.logger.error(f"campaign_count.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": "Failed to fetch campaign details"}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
    return await make_response(
        json.dumps({"message": "success", "output": campaigns_count_result}),
        HTTPStatus.OK.value,
    )


@bp.route("/report-download-queue", methods=["POST"])
@login_required
async def _report_download_queue(*args, **kwargs):
    app.logger.info(f"routes._report_download_queue")

    body = await request.get_json()

    queue = f"{app.config['QUEUE_NAME']}_litigation_report"
    kwargs["queue"] = queue

    user = g.user

    kwargs["user"] = user
    kwargs["token"] = user["authentication_token"]
    kwargs["role"] = user["role"]
    kwargs["author"] = user["email"]

    kwargs["request_id"] = request.headers.get("X-Request-Id")
    kwargs["company_id"] = body["company_id"]
    kwargs["report_name"] = body["data"]["report_name"]
    kwargs["data"] = body["data"]
    kwargs["batch_id"] = body["batch_id"]
    kwargs["company"] = g.company
    kwargs["request_id"] = request.headers.get("X-Request-Id")

    app.logger.debug(f"routes._report_download_queue :: {kwargs}")

    try:
        res = assign_report_download_queue.apply_async(queue=queue, kwargs=kwargs)
        app.logger.debug(f"routes.assign_report_download_queue.res :: {str(res)}")

    except Exception as e:
        app.logger.error(f"routes.assign_report_download_queue.exception :: {str(e)}, message: Task assign failed")

        return {"success": False, "message": "Task assign failed"}, 422

    return await make_response(
        json.dumps(
            {
                "success": True,
                "message": "Task assigned successfully",
                "data": kwargs["batch_id"],
            }
        ),
        200,
    )


################### Notice APIs ###################


# @bp.route("/notice_preview_queue", methods=["POST"])
# @login_required
# async def _notice_preview_queue(*args, **kwargs):
#     app.logger.info(f"routes._notice_preview_queue")

#     body = await request.get_json()

#     kwargs = {**kwargs, **body}

#     user = g.user

#     queue = f"{app.config['QUEUE_NAME']}_notice_preview"
#     kwargs["queue"] = queue

#     kwargs["user"] = g.user
#     kwargs["company"] = g.company

#     kwargs["author"] = user["email"]
#     kwargs["role"] = user["role"]
#     kwargs["token"] = request.headers.get("authenticationtoken")
#     kwargs["X-Request-Id"] = str(request.headers.get("X-Request-Id"))

#     kwargs["s3_link_uuid"] = kwargs["batch_id"]
#     # To track the generated pdf as we dont store it in the db
#     s3_link_uuid = kwargs["batch_id"]

#     kwargs["request_id"] = str(request.headers.get("X-Request-Id"))

#     (
#         local_batch_directory_path,
#         local_draft_file_path,
#         local_doc_directory_path,
#         local_pdf_directory_path,
#         local_qr_code_directory_path,
#         local_merged_pdf_directory_path,
#         local_merged_pdf_zip_file_path,
#     ) = get_directory_and_file_paths(**kwargs)

#     kwargs["local_batch_directory_path"] = local_batch_directory_path
#     kwargs["local_draft_file_path"] = local_draft_file_path
#     kwargs["local_doc_directory_path"] = local_doc_directory_path
#     kwargs["local_pdf_directory_path"] = local_pdf_directory_path
#     kwargs["local_qr_code_directory_path"] = local_qr_code_directory_path
#     kwargs["local_merged_pdf_directory_path"] = local_merged_pdf_directory_path
#     kwargs["local_merged_pdf_zip_file_path"] = local_merged_pdf_zip_file_path
#     kwargs["BUCKET_NAME"] = S3_BUCKET_NAME

#     draft_fields = get_draft_fields(**kwargs)

#     if isinstance(draft_fields, str):
#         app.logger.error(f"queue.routes.drafts_err : {draft_fields}")
#         return await make_response(
#             json.dumps(
#                 {
#                     "message": "failed",
#                     "output": f"Error while downloading draft from s3 : {draft_fields}",
#                     "data": kwargs["batch_id"],
#                 }
#             ),
#             400,
#         )

#     redis_instance = redis.Redis(host=REDIS["HOST"], port=REDIS["PORT"])
#     draft_fields_redis_key = f"notice_draft_{kwargs['batch_id']}"
#     redis_instance.setex(draft_fields_redis_key, 24 * 60 * 60, json.dumps(draft_fields))
#     kwargs["draft_fields_redis_key"] = draft_fields_redis_key

#     try:
#         res = assign_generate_notice_preview_queue.apply_async(queue=queue, kwargs=kwargs)
#     except Exception as e:
#         app.logger.error(f"routes._notice_preview_queue.exception : {str(e)}, message: Task assign failed")
#         return {"success": False, "message": "Task assign failed"}, 422

#     return await make_response(
#         json.dumps(
#             {
#                 "success": True,
#                 "message": "Task assigned successfully",
#                 "batch_id": kwargs["batch_id"],
#                 "s3_link": f"{S3_BUCKET_ENDPOINT}/preview_notice_links/{s3_link_uuid}.pdf",
#             }
#         ),
#         200,
#     )


# @bp.route("/notice_execution_status", methods=["GET"])
# @login_required
# async def notice_execution_status(*args, **kwargs):
#     columns = ["status", "response", "status_code", "loan_id"]
#     batch_id = request.args["batch_id"]
#     try:
#         notice_loans_data = await app.db.select(
#             table="notice_loans", columns=columns, where={"batch_id='%s'": batch_id, "is_deleted=%s": False}
#         )
#     except Exception as e:
#         app.logger.error(f"routes.notice_execution_status.exception :: {str(e)}")
#         return await make_response(
#             json.dumps(
#                 {
#                     "message": "FAIL",
#                     "output": "Can not get details for the given batch_id",
#                 }
#             ),
#             500,
#         )

#     return await make_response(json.dumps({"message": "SUCCESS", "output": notice_loans_data}), 200)


@bp.route("/campaign/filter", methods=["GET"], endpoint="campaign_filters")
@login_required
@verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_querystring(CampaignFilter)
async def get_campaign_filter(*args, query_args: CampaignFilter, **kwargs):
    """
    Fetch author and channel for campaign filter
    """
    app.logger.info(f"app.routes.get_campaign_filter")
    filter_data = query_args.dict()
    company_id = filter_data.get("company_id", None)
    is_deleted = filter_data.get("is_deleted", False)
    is_master_campaign_request = filter_data["is_master_campaign_request"]
    author_list = list()
    channel_list = list()
    try:
        if not is_master_campaign_request:
            channel_query = f"select distinct(channel) from campaigns where company_id='{company_id}' and master_campaign = False and parent_campaign_id is null and is_deleted = {is_deleted};"
            distinct_channel = await app.campaign_db.execute_raw_select_query(channel_query)
            if not isinstance(distinct_channel, list):
                return await make_response(
                    json.dumps({"message": "failed", "output": "failed to fetch filter details"}),
                    HTTPStatus.INTERNAL_SERVER_ERROR.value,
                )
            for channel in distinct_channel:
                if isinstance(channel.get("channel"), str):
                    channel_list.append(channel["channel"])
            author_query = f"select distinct(author) from campaigns where company_id='{company_id}' and master_campaign = False and parent_campaign_id is null and is_deleted = {is_deleted};"
        else:
            author_query = f"select distinct(author) from campaigns where company_id='{company_id}' and master_campaign = True and is_deleted = {is_deleted};"
        distinct_authors = await app.campaign_db.execute_raw_select_query(author_query)
        if not isinstance(distinct_authors, list):
            return await make_response(
                json.dumps({"message": "failed", "output": "failed to fetch filter details"}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
        for authors in distinct_authors:
            if isinstance(authors.get("author"), str):
                author_list.append(authors["author"])
        distinct_dict = {"author": author_list}
        if channel_list:
            distinct_dict["channel"] = channel_list
    except Exception as e:
        app.logger.error(f"queue-service.routes.get_filter_details exception :: {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": f"{str(e)}"}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

    return await make_response(
        json.dumps(
            {
                "message": "success",
                "output": "filter details sent successfully",
                "data": [distinct_dict],
            }
        ),
        HTTPStatus.OK.value,
    )


@bp.route("/update_batch_response", methods=["PATCH"], endpoint="update_batch_response")
@login_required
async def _batch_operations_update(*args, **kwargs):
    app.logger.info("app.routes._batch_operations_update")
    data = await request.get_json()

    values = {}

    try:
        if data.get("s3_error_report_excel_path"):
            values["s3_error_report_excel_path"] = data["s3_error_report_excel_path"]

        if data.get("s3_batch_report_excel_path"):
            values["s3_batch_report_excel_path"] = data["s3_batch_report_excel_path"]

        batch_id = data["batch_id"]
        where = {"batch_id='%s'": batch_id, "is_deleted=%s": False}
        table = "batch_operations"

        if values:
            await app.db.update(table=table, values=values, where=where)

    except Exception as e:
        app.logger.error("app.routes._batch_operations Exception: %s", e)
        return {"message": "failed"}, 500

    return {"message": "success"}


# @bp.route("/notice_batch_operations", methods=["GET"], endpoint="notice_batch_operations")
# @login_required
# async def _get_notice_batch_operations(*args, **kwargs):
#     app.logger.info("routes._get_notice_operations")

#     company_id = request.args["company_id"]
#     page_number = int(request.args.get("page_number", 1))
#     page_size = 13

#     offset = (page_number - 1) * page_size

#     columns = [
#         "batch_id",
#         "type",
#         "channel",
#         "created",
#         "updated",
#         "author",
#         "role",
#         "loan_data",
#         "data",
#         "total_loans",
#         "author_id",
#         "batch_name",
#         "notice_type",
#         "notice_mode",
#         "notice_draft_id",
#         "s3_error_report_excel_path",
#         "s3_batch_report_excel_path",
#         "(select count(1) from notice_loans where batch_id = batch_operations.batch_id and status = 'SUCCESS' and is_deleted = false) as success_count",
#         "(select count(1) from notice_loans where batch_id = batch_operations.batch_id and status = 'FAIL' and is_deleted = false) as  fail_count",
#     ]

#     order_by = "created desc"

#     tasks = []

#     try:
#         batch_operations_task = app.db.select(
#             table="batch_operations",
#             columns=columns,
#             where={"company_id='%s'": company_id, "type='%s'": "notice", "is_deleted=%s": False},
#             order_by=order_by,
#             limit=page_size,
#             offset=offset,
#         )
#         tasks.append(batch_operations_task)

#         total_count_task = app.db.select(
#             table="batch_operations",
#             columns=["count(1)"],
#             where={"company_id='%s'": company_id, "type='%s'": "notice", "is_deleted=%s": False},
#         )
#         tasks.append(total_count_task)
#         task_result = await asyncio.gather(*tasks)

#         notice_batch_operations_data = task_result[0]
#         total_notice_batch_operations_count = task_result[1][0]["count"]

#         result = {
#             "message": "success",
#             "data": {
#                 "notice_batch_operations_data": notice_batch_operations_data,
#                 "total_notice_batch_operations_count": total_notice_batch_operations_count,
#                 "s3_bucket_endpoint": S3_BUCKET_ENDPOINT,
#             },
#         }

#         return result

#     except Exception as e:
#         app.logger.error(f"routes._get_notice_bathc_operations Exception: {e}")
#         return {"message": "failed"}, 500


@bp.route("/campaign/errors", methods=["GET"], endpoint="campaign_errors")
@login_required
@validate_querystring(CampaignErrors)
async def campaign_errors(*args, query_args: CampaignErrors, **kwargs):
    app.logger.info(f"app.routes.campaign_errors")
    request_data = query_args.dict()
    company_id = request_data["company_id"]
    campaign_id = request_data["campaign_id"]
    channel = request_data["channel"]
    count = request_data["count"]
    app.logger.debug(f"app.routes.campaign_errors.request_data :: {request_data}")
    try:
        query = f"select total_loans, loan_data, helicarrier_trigger from campaigns where campaign_id= '{campaign_id}' and channel= '{channel}' and company_id= '{company_id}' and is_deleted = false;"
        campaign_data = await app.campaign_db.execute_raw_select_query(query)
        if not isinstance(campaign_data, list) or isinstance(campaign_data, str):
            return await make_response(
                json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
        elif not campaign_data:
            return await make_response(
                json.dumps({"message": "failed", "output": "invalid campaign_id provided"}),
                HTTPStatus.BAD_REQUEST.value,
            )
        error_response = await get_campaign_errors(
            campaign_id=campaign_id, company_id=company_id, channel=channel, campaign_data=campaign_data[0], count=count
        )
        return await make_response(
            json.dumps(
                {
                    "success": error_response["success"],
                    "message": error_response["message"],
                    "data": error_response.get("data", {}),
                }
            ),
            error_response["status_code"],
        )
    except Exception as e:
        app.logger.error(f"campaign_errors.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@bp.route("v1/campaign/errors", methods=["POST"], endpoint="campaign_errors_v1")
@login_required
@validate_request(CampaignErrorsV1)
async def campaign_errors_v1(*args, data: CampaignErrorsV1, **kwargs):
    app.logger.info(f"app.routes.campaign_errors")
    request_data = data.dict()
    company_id = request_data["company_id"]
    campaign_id = request_data["campaign_id"]
    channel = request_data["channel"]
    count = request_data["count"]
    campaign_errors = request_data["errors"]
    app.logger.debug(f"app.routes.campaign_errors.request_data :: {request_data}")
    try:
        query = f"select total_loans, loan_data, helicarrier_trigger from campaigns where campaign_id= '{campaign_id}' and channel= '{channel}' and company_id= '{company_id}' and is_deleted = false;"
        campaign_data = await app.campaign_db.execute_raw_select_query(query)
        if not isinstance(campaign_data, list) or isinstance(campaign_data, str):
            return await make_response(
                json.dumps({"message": "failed", "output": DB_ERROR_RESPONSE}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
        elif not campaign_data:
            return await make_response(
                json.dumps({"message": "failed", "output": "invalid campaign_id provided"}),
                HTTPStatus.BAD_REQUEST.value,
            )
        error_response = await get_campaign_errors(
            campaign_id=campaign_id,
            company_id=company_id,
            channel=channel,
            campaign_data=campaign_data[0],
            count=count,
            campaign_errors=campaign_errors,
        )
        return await make_response(
            json.dumps(
                {
                    "success": error_response["success"],
                    "message": error_response["message"],
                    "data": error_response.get("data", {}),
                }
            ),
            error_response["status_code"],
        )
    except Exception as e:
        app.logger.error(f"campaign_errors.exception {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@bp.route("/campaign/reattempt", methods=["POST"], endpoint="campaign_reattempt")
@login_required
@validate_request(CampaignReattempt)
async def campaign_reattempt(*args, data: CampaignReattempt, **kwargs):
    app.logger.info(f"app.routes.campaign_reattempt")
    request_data = data.dict()
    company_id = request_data["company_id"]
    campaign_id = request_data["campaign_id"]
    channel = request_data["channel"]
    reattempt_on = request_data["reattempt_on"]
    app.logger.debug(f"app.routes.campaign_reattempt.request_data :: {request_data}")
    retrigger_response = await retrigger_campaign(
        campaign_id=campaign_id, company_id=company_id, channel=channel, reattempt_on=reattempt_on
    )
    return await make_response(
        json.dumps(
            {
                "success": retrigger_response["success"],
                "message": retrigger_response["message"],
                "data": retrigger_response.get("data", {}),
            }
        ),
        retrigger_response["status_code"],
    )


@bp.route("/report", methods=["POST"], endpoint="campaign_report")
@login_required
@validate_request(CampaignExport)
async def _campaign_report(*args, **kwargs):
    try:
        app.logger.info("routes.campaign_report")
        data = await request.get_json()
        app.logger.debug(f"data_paylod:{data}")
        user = g.user
        author = user.get("email", None)
        if not author:
            return await make_response(
                json.dumps({"message": "failed", "output": f"No email id found on account."}),
                HTTPStatus.BAD_REQUEST.value,
            )
        campaign_id = data.get("campaign_id")
        company_id = data.get("company_id")
        channel = data.get("channel")
        payloads = []
        if channel == MASTER_CAMPAIGN_CHANNEL:
            campaign_column = ["campaign_id", "channel", "name", "current_delivery_status", "data"]
            campaign_where = {
                "company_id = '%s'": company_id,
                "parent_campaign_id = '%s'": campaign_id,
                "is_deleted = %s": False,
            }
            mc_campaign_data = await get_master_campaign_details(campaign_column, campaign_where)
            if not mc_campaign_data["success"] or not mc_campaign_data["data"]:
                return await make_response(
                    json.dumps({"message": "failed", "output": mc_campaign_data["message"]}),
                    mc_campaign_data["status_code"],
                )
            for mc_campaign in mc_campaign_data["data"]:
                app.logger.debug(f"routes.campaign_report.sub_campaign_data: {mc_campaign}")
                sub_campaign_metadata = json.loads(mc_campaign["data"])
                if not isinstance(sub_campaign_metadata, dict):
                    sub_campaign_metadata = json.loads(sub_campaign_metadata)
                payloads.append(
                    {
                        "company_id": company_id,
                        "campaign_id": mc_campaign["campaign_id"],
                        "channel": mc_campaign["channel"],
                        "name": mc_campaign["name"],
                        "delivery_status": mc_campaign["current_delivery_status"],
                        "template_name": sub_campaign_metadata.get("template_name"),
                    }
                )
        else:
            payloads.append(data)
        for payload in payloads:
            complete_campaign_data = await get_full_campaign_data(data=payload)
            campaign_data = complete_campaign_data.get("campaign_data")
            if campaign_data:
                campaign_data = campaign_data[0]
            app.logger.info(f"campaign_data:{campaign_data}")
            loan_ids = campaign_data.get("loan_data")
            if isinstance(loan_ids, str):
                loan_ids = json.loads(loan_ids)
            total_count = campaign_data.get("total_loans")
            campaign_metadata = campaign_data.get("data", {})
            if campaign_metadata and not isinstance(campaign_metadata, dict):
                campaign_metadata = json.loads(campaign_metadata)
                if not isinstance(campaign_metadata, dict):
                    campaign_metadata = json.loads(campaign_metadata)
            allocation_month = campaign_metadata.get("allocation_month")
            payload["allocation_month"] = allocation_month
            payload["triggered_time"] = campaign_data.get("created")
            app.logger.info(f"data_for_trigger_report:{payload}")
            response = await trigger_campaign_export(
                company_id=company_id,
                campaign_id=payload["campaign_id"],
                loan_ids=loan_ids,
                total_count=total_count,
                payload=payload,
                user_details=user,
                request_headers=dict(request.headers),
            )
            if not response.get("success"):
                return await make_response(
                    json.dumps(
                        {
                            "message": "failed",
                            "output": response.get("message", ""),
                        }
                    ),
                    HTTPStatus.BAD_REQUEST.value,
                )
        return await make_response(
            json.dumps(
                {
                    "message": "success",
                    "output": "Successfully triggered campaign report",
                }
            ),
            HTTPStatus.OK.value,
        )
    except Exception as e:
        app.logger.error(f"Error in campaign report api:{str(e)}")
        return await make_response(
            json.dumps(
                {
                    "message": "failed",
                    "output": f"{str(e)}",
                }
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@bp.route("/campaign_export_data", methods=["POST"], endpoint="campaign_export_data")
@login_required
async def _campaign_export_data(*args, **kwargs):
    app.logger.info("routes.campaign_export_data")
    result = []
    try:
        data = await request.get_json()
        app.logger.info(f"campaign_export_data")
        app.logger.info(
            f"_campaign_export_data.company_id:{data.get('company_id')},campaign_id:{data.get('campaign_id')},channel:{data.get('channel')}"
        )

        user = g.user
        author = user.get("email", None)
        if not author:
            return await make_response(
                json.dumps({"message": "failed", "output": f"No email id found on account."}),
                HTTPStatus.BAD_REQUEST.value,
            )
        data["author"] = author
        data["user"] = user
        data["company"] = g.company
        data["request_id"] = request.headers.get("X-Request-Id", "")
        channel_campaigns_columns = [
            "status",
            "response",
            "status_code",
            "loan_id",
            "created::VARCHAR",
        ]
        campaign_data = await get_full_campaign_data(
            data, channel_campaigns_columns=channel_campaigns_columns, get_channel_data=True
        )
        if data["channel"] != "NA":
            communication_export_data = await get_communication_details(data)
            if communication_export_data["error"]:
                return await make_response(
                    json.dumps(
                        {
                            "message": "success",
                            "output": communication_export_data["error"],
                            "data": communication_export_data["data"],
                        }
                    ),
                    communication_export_data["status_code"],
                )
            app.logger.info(f"communication_export_data.length:{len(communication_export_data['data'])}")
            result = get_campaign_report_data(data, communication_export_data["data"], campaign_data)
        else:
            mc_failure_response = await get_mc_failure_details(data)
            if mc_failure_response["status_code"] != HTTPStatus.OK.value:
                return await make_response(
                    json.dumps(
                        {
                            "message": mc_failure_response["message"],
                            "output": mc_failure_response["output"],
                            "data": mc_failure_response["data"],
                        }
                    ),
                    mc_failure_response["status_code"],
                )
            elif mc_failure_response["status_code"] == HTTPStatus.OK.value and not mc_failure_response["data"]:
                return await make_response(
                    json.dumps(
                        {
                            "message": mc_failure_response["message"],
                            "output": mc_failure_response["output"],
                            "data": mc_failure_response["data"],
                        }
                    ),
                    mc_failure_response["status_code"],
                )
            result = await get_mc_failure_campaign_report(mc_failure_response["data"], campaign_data)
        app.logger.info(f"_campaign_export_data.get_campaign_report_data.length:{len(result)}")
        return await make_response(
            json.dumps(
                {
                    "message": "success",
                    "output": "campaign data fetched successfully",
                    "data": result,
                }
            ),
            HTTPStatus.OK.value,
        )
    except Exception as e:
        app.logger.error(f"Error while getting campaign report data:{str(e)}")
        return await make_response(
            json.dumps(
                {
                    "message": "failure",
                    "output": "Failed to get campaign report data",
                    "data": result,
                }
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@bp.route("/campaign_report_activity", methods=["POST"], endpoint="campaign_report_activity")
@login_required
async def campaign_report_activity(*args, **kwargs):
    app.logger.info("app.communication.routes.process_export")
    request_data = await request.get_json()
    export_id = request.args.get("export_id")
    service_flag = request.args.get("service_flag")
    download_link = request_data.get("s3_link")
    failure_message = request_data.get("failure_message")

    app.logger.debug(f"campaign_report_activity.request_data:{request_data}")
    app.logger.debug(f"campaign_report_activity_link:{download_link}")
    app.logger.info(f"campaign_report_activity_link:{download_link}")
    company_trademark = g.company["trademark"]
    company_id = g.company["company_id"]
    try:
        response = await send_campaign_export_report(
            export_id=export_id,
            company_id=company_id,
            download_link=download_link,
            company_trademark=company_trademark,
            failure_message=failure_message,
            service_flag=service_flag,
        )
        app.logger.info(f"report_activity_response:{response}")
        if response["status_code"] == HTTPStatus.OK.value:
            return await make_response(
                json.dumps({"message": response["message"], "success": True}), HTTPStatus.OK.value
            )
        return await make_response(
            json.dumps({"message": response["message"], "success": False}), response["status_code"]
        )
    except Exception as e:
        app.logger.error(f"campaign_report_activity_error:{str(e)}")
        return await make_response(
            json.dumps({"message": "Failed to send export report", "success": False}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@bp.route("/campaign/cancel", methods=["POST"], endpoint="campaign_cancel")
@login_required
@verify_permission(submodules=CAMPAIGN_SUBMODULE)
@validate_request(CampaignCancel)
async def cancel_campaign(data: CampaignCancel):
    app.logger.info("app.routes.cancel_campaign")
    try:
        user = g.user
        user_id = user.get("user_id")
        data = data.dict()
        company_id = data["company_id"]
        campaign_id = data["campaign_id"]
        campaign_status_redis_key = f"campaign_status_{campaign_id}"
        update_data = {"is_stopped": True, "is_stopped_by": user_id}
        result = await app.campaign_db.update(
            table=CAMPAIGNS_TABLE,
            values=update_data,
            where={"company_id='%s'": company_id, "campaign_id='%s'": campaign_id},
        )
        if result and isinstance(result, int):
            await app.redis.delete_without_pattern(campaign_status_redis_key)
            return await make_response(
                json.dumps(
                    {
                        "message": "success",
                        "output": "Campaign stopped successfully",
                    }
                ),
                HTTPStatus.OK.value,
            )
        elif isinstance(result, int):
            return await make_response(
                json.dumps(
                    {
                        "message": "failed",
                        "output": "Invalid campaign id provided",
                    }
                ),
                HTTPStatus.BAD_REQUEST.value,
            )
        else:
            app.logger.error(f"app.routes.cancel_campaign db_response : {result}")
            return await make_response(
                json.dumps(
                    {
                        "message": "failed",
                        "output": "Failed to stop campaign",
                    }
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
    except Exception as e:
        app.logger.error(f"app.routes.cancel_campaign.exception : {str(e)}")
        return await make_response(
            json.dumps(
                {
                    "message": "failed",
                    "output": "Failed to stop campaign",
                }
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@bp.route("/campaign/status", methods=["GET"], endpoint="campaign_trigger_status")
@login_required
@validate_querystring(CampaignStatus)
async def get_campaign_status(query_args: CampaignStatus):
    app.logger.info(f"app.routes.get_campaign_status")
    try:
        query_args = query_args.dict()
        company_id = query_args["company_id"]
        campaign_id = query_args["campaign_id"]
        campaign_status_redis_key = f"campaign_status_{campaign_id}"
        result = await app.redis.get(key=campaign_status_redis_key)
        if result:
            return await make_response(
                json.dumps({"message": "success", "output": "Successfully fetched campaign status", "data": result}),
                HTTPStatus.OK.value,
            )
        columns = ["is_stopped"]
        where = {"company_id='%s'": company_id, "campaign_id='%s'": campaign_id}
        result = await app.campaign_db.select(
            table=CAMPAIGNS_TABLE, columns=columns, where=where, disable_read_replica=True
        )
        if result and isinstance(result, list):
            data = result[0]
            await app.redis.set(key=campaign_status_redis_key, value=data)
            return await make_response(
                json.dumps({"message": "success", "output": "Successfully fetched campaign status", "data": data}),
                HTTPStatus.OK.value,
            )
        elif isinstance(result, list):
            return await make_response(
                json.dumps({"message": "failed", "output": "Invalid campaign id provided", "data": {}}),
                HTTPStatus.BAD_REQUEST.value,
            )
        else:
            return await make_response(
                json.dumps({"message": "failed", "output": "Failed to fetch campaign status", "data": {}}),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
    except Exception as e:
        app.logger.error(f"app.routes.get_campaign_status.exception : {str(e)}")
        return await make_response(
            json.dumps({"message": "failed", "output": "Failed to fetch campaign status", "data": {}}),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
