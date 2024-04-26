"""
cg_celery.py
Usage: Celery
"""
import logging

from celery import Celery

from logging import Filter
from cg_logger import CustomFormatter
from app.settings import DTMF_RATE_LIMIT, CELERY_VISIBILITY_SETTINGS_ENABLED, CELERY_VISIBILITY_TIMEOUT

LOGGER_CONFIGURATION = (
    '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", '
    '"path": "%(pathname)s", "function": "%(funcName)s", "line":"%(lineno)d", '
    '"request_id": "%(request_id)s", "message": "%(message)s", "json_message": %(json_message)s}'
)


class QueueLogFilter(Filter):
    def filter(self, record):
        # from celery import current_task as celery_task
        # if celery_task == None:
        #     return False
        # print(f"current_task :: {celery_task}")
        # print(f"current_task.dir :: {dir(celery_task)}")
        # print(f"current_task.request :: {celery_task.request}")
        # print(f"current_task.Request :: {celery_task.Request}")

        if record.module in (
            "connection",
            "tasks",
            "report",
            "execution",
            "delegator",
            "callback",
            "service",
        ):
            return True
        return False


def make_celery(app):
    """
    Make celery instance to register tasks and executes them.
    """
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    if CELERY_VISIBILITY_SETTINGS_ENABLED:
        celery.conf.BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": CELERY_VISIBILITY_TIMEOUT}
        print(f"\n CUSTOM CELERY SETTINGS || celery_visibility_timeout : {CELERY_VISIBILITY_TIMEOUT} \n")
    logger = logging.getLogger()
    sh = logging.StreamHandler()

    formatter = CustomFormatter(LOGGER_CONFIGURATION, None, "%", False)
    sh.setFormatter(formatter)
    sh.addFilter(QueueLogFilter())

    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    celery.autodiscover_tasks(
        [
            "app.tasks.result_tasks",
            "app.tasks.communication_result",
            "app.tasks.tasks",
            "app.tasks.delegator",
            "app.tasks.execution",
            "app.tasks.report",
        ],
        force=True,
    )
    celery.control.rate_limit("indiapost_tracking", "40/s")
    celery.control.rate_limit("communication", "100/s")
    celery.control.rate_limit("communication_dtmf_ivr", DTMF_RATE_LIMIT)
    celery.control.rate_limit("add_ecourt_case", "2/s")
    celery.control.rate_limit("update_ecourt_case", "2/s")
    celery.control.rate_limit("fetch_ecourt_case_orders", "2/s")
    celery.control.rate_limit("lat_long_conversion", "2/s")
    celery.worker_prefetch_multiplier = 1
    return celery
