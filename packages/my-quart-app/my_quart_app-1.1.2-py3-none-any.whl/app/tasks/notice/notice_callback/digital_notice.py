# import shutil
# from celery import shared_task
# from app.settings import NOTICE_VOLUME_MOUNT_DIRECTORY
# import os
# import logging

# from app.tasks.notice.notice_callback.commons import delete_redis_keys

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# @shared_task(bind=True, name="generate_digital_notice_preview_callback")
# def generate_digital_notice_preview_callback(self, *args, **kwargs):
#     logger.info("generate_digital_notice_preview_callback")
#     logger.debug(f"generate_digital_notice_preview_callback.kwargs: {kwargs}")

#     volume_mount_directory = NOTICE_VOLUME_MOUNT_DIRECTORY
#     local_batch_directory_path = os.path.join(volume_mount_directory, "previews", kwargs["batch_id"])

#     shutil.rmtree(local_batch_directory_path, ignore_errors=True)
#     logger.debug(f"generate_digital_notice_preview_callback.dir_removal.info :{local_batch_directory_path} deleted")
#     delete_redis_keys(kwargs["batch_id"])

#     return True
