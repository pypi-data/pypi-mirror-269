import time
import traceback
from quart import Quart, g, request, make_response
from . import settings
from .cg_celery import make_celery
import json
from cg_database import Postgres
import cg_logger as logger
from cg_redis import RedisCache
from . import routes
from .utils import BadEnvException, VerifyEnv
from elasticapm.contrib.quart import ElasticAPM
from quart_schema import QuartSchema, RequestSchemaValidationError
from pydantic.error_wrappers import ValidationError

app = Quart(__name__)
app.config.from_object(settings)
QuartSchema(
    app,
    redoc_ui_path=f"{settings.BASE_ROUTE}/redocs",
    swagger_ui_path=f"{settings.BASE_ROUTE}/docs",
    openapi_path=f"{settings.BASE_ROUTE}/openapi.json",
    version="1.0.0",
    title="Queue Service API Documentation",
)
celery = make_celery(app=app)


@app.before_serving
async def _init():
    logger.init()
    apm = ElasticAPM(app)
    app.logger.info("logger initialized")

    verify_envs = VerifyEnv().verify()
    if verify_envs[0] is True:
        app.logger.info("Queue config variables verified")
    else:
        app.logger.error("QUEUE CONFIGS NOT VERIFIED %s", str(verify_envs[1]))
        error = "unable to verify these queue configs " + str(verify_envs[1])
        raise BadEnvException(message=error)

    await _init_db()
    app.logger.info("db initialized")

    await _init_redis()
    app.logger.info("redis initialized")

    _register_blueprints()
    app.logger.info("routes registered")
    return


@app.before_request
def _before_request():
    g.request_id = logger.get_request_id()
    g.request_start_time = time.time_ns()
    return


@app.after_request
def _after_request(response):
    response = _add_global_headers(response)
    return logger.print_access_log(response)


@app.errorhandler(400)
async def _bad_request(exception):
    body = await request.body
    app.logger.error("%s, request.args: %s, request.body: %s", exception, dict(request.args), body)

    return {"message": "unable to process the request due to invalid syntax"}, 400


@app.errorhandler(404)
def _route_not_found(exception):
    app.logger.error("%s, route: '%s'", exception, request.url)

    return {"message": "requested route not found"}, 404


@app.errorhandler(408)
def _resource_request_timed_out(exception):
    app.logger.error(
        "resource request timed out, traceback: %s",
        traceback.extract_tb(exception.__traceback__),
    )

    return {"message": "resource request timed out"}, 408


@app.errorhandler(405)
def _resource_request_method_not_allowed(exception):
    app.logger.error(
        "resource request method not allowed, traceback: %s",
        traceback.extract_tb(exception.__traceback__),
    )

    return {"message": "Method not allowed"}, 405


@app.errorhandler(Exception)
def _unhandled_exception(exception):
    app.logger.error(
        "server._unhandled_exception: %s, traceback: %s",
        exception,
        traceback.extract_tb(exception.__traceback__),
    )
    return {"message": f"Error occurred {exception}"}, 500


@app.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(error):
    if isinstance((error.validation_error), (ValidationError)):
        error = json.loads(error.validation_error.json())
        if error[0]["type"] == "value_error":
            error = error[0]["msg"]
            return await make_response(
                json.dumps(
                    {
                        "message": "failed",
                        "output": "invalid payload keys",
                        "data": {"errors": [{"error": error}]},
                    }
                ),
                400,
            )
        else:
            loc = error[0]["loc"]
            if "__root__" in loc:
                loc.remove("__root__")
            return await make_response(
                json.dumps(
                    {
                        "message": "failed",
                        "output": "invalid payload keys",
                        "data": {"errors": [{"error": error[0]["msg"], "key": error[0]["loc"]}]},
                    }
                ),
                400,
            )
    elif str(error.validation_error) == "type object argument after ** must be a mapping, not NoneType":
        return await make_response(
            json.dumps(
                {
                    "message": "failed",
                    "output": "Empty request body",
                }
            ),
            400,
        )
    else:
        error = str(error.validation_error)
        return await make_response(
            json.dumps(
                {
                    "message": "failed",
                    "output": str(error.replace("__init__() ", "")),
                }
            ),
            400,
        )


def _add_global_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1;mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["X-Request-ID"] = str(g.request_id)
    return response


async def _init_db():
    db_conf = app.config.get("POSTGRES")
    app.db = Postgres(
        database=db_conf["NAME"],
        host=db_conf["HOST"],
        port=db_conf["PORT"],
        user=db_conf["USER"],
        password=db_conf["PASSWORD"],
        enable_read_replica=db_conf["ENABLE_DB_READ_REPLICA"],
        read_replica_host=db_conf["READ_REPLICA_DB_HOST"],
        read_replica_port=db_conf["READ_REPLICA_DB_PORT"],
    )
    await app.db.connect()
    app.logger.info(f"DB initialized")

    campaign_db_conf = app.config.get("CAMPAIGN_POSTGRES")
    app.campaign_db = Postgres(
        database=campaign_db_conf["NAME"],
        host=campaign_db_conf["HOST"],
        port=campaign_db_conf["PORT"],
        user=campaign_db_conf["USER"],
        password=campaign_db_conf["PASSWORD"],
        enable_read_replica=campaign_db_conf["ENABLE_DB_READ_REPLICA"],
        read_replica_host=campaign_db_conf["READ_REPLICA_DB_HOST"],
        read_replica_port=campaign_db_conf["READ_REPLICA_DB_PORT"],
    )
    await app.campaign_db.connect()
    app.logger.info(f"campaign db initialized")

    recovery_db_conf = app.config.get("RECOVERY_POSTGRES")
    app.recovery_db = Postgres(
        database=recovery_db_conf["NAME"],
        host=recovery_db_conf["HOST"],
        port=recovery_db_conf["PORT"],
        user=recovery_db_conf["USER"],
        password=recovery_db_conf["PASSWORD"],
        enable_read_replica=recovery_db_conf["ENABLE_DB_READ_REPLICA"],
        read_replica_host=recovery_db_conf["READ_REPLICA_DB_HOST"],
        read_replica_port=recovery_db_conf["READ_REPLICA_DB_PORT"],
    )
    await app.recovery_db.connect()
    app.logger.info(f"recovery db initialized")

    comm_db_conf = app.config.get("COMM_POSTGRES")
    app.logger.info(f"comm_db_conf:{comm_db_conf}")
    app.comm_db = Postgres(
        database=comm_db_conf["NAME"],
        host=comm_db_conf["HOST"],
        port=comm_db_conf["PORT"],
        user=comm_db_conf["USER"],
        password=comm_db_conf["PASSWORD"],
        enable_read_replica=comm_db_conf["ENABLE_DB_READ_REPLICA"],
        read_replica_host=comm_db_conf["READ_REPLICA_DB_HOST"],
        read_replica_port=comm_db_conf["READ_REPLICA_DB_PORT"],
    )
    await app.comm_db.connect()
    app.logger.info("communication db initialized")
    return


async def _init_redis():
    app.redis = RedisCache(f"""{app.config.get("APP_NAME")}_{app.config.get("ENV")}""")
    redis_config = app.config.get("REDIS")
    if not redis_config:
        raise Exception("REDIS config not found")
    await app.redis.connect(host=redis_config["HOST"], port=redis_config["PORT"])


def _register_blueprints():
    app.register_blueprint(routes.bp)
