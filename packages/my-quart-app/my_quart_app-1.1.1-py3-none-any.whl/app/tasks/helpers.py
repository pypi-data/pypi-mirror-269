import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import pickle
import os
import uuid


def get_required_headers_per_level(headers):
    logger.info("get_required_headers_per_level")

    loan_level_headers = []
    case_level_headers = []
    stage_level_headers = []
    reminder_level_headers = []
    advocate_level_headers = []

    for key, value in headers.items():
        level = value.get("level")
        if not level:
            pass
        elif level == "loan":
            loan_level_headers.append(key)
        elif level == "stage":
            stage_level_headers.append(key)
        elif level == "case":
            case_level_headers.append(key)
        elif level == "reminder":
            reminder_level_headers.append(key)
        elif level == "advocate":
            advocate_level_headers.append(key)

    # adding necessary keys - various ids in all dicts -
    for header_array in (
        loan_level_headers,
        case_level_headers,
        stage_level_headers,
        reminder_level_headers,
        advocate_level_headers,
    ):
        for key in [
            "id",
            "case_row_id",
            "loan_id",
            "case_id",
            "stage_code",
            "current_stage_code",
            "proceeding",
            "data",
        ]:
            if key not in header_array:
                header_array.append(key)

    # adding specific keys -
    stage_level_headers.append("case_details_under_approval")
    stage_level_headers.append("iteration")
    reminder_level_headers.append("reminder_start_date")
    reminder_level_headers.append("deadline_date")
    reminder_level_headers.append("date_of_default")
    reminder_level_headers.append("next_stage_code")
    advocate_level_headers.append("user_id")
    advocate_level_headers.append("profession")
    advocate_level_headers.append("iteration")

    return (loan_level_headers, case_level_headers, stage_level_headers, reminder_level_headers, advocate_level_headers)


class ChunkClass:
    file_list = []
    batch_id = None
    counter = -1
    extension = None
    base_path = None
    chunks_file_path = None
    excel_file_path = None
    zip_file_path = None

    def __init__(self, base_path, batch_id, extension) -> None:
        self.file_list = []
        self.batch_id = batch_id
        self.counter = 0
        self.extension = extension
        os.makedirs(base_path, exist_ok=True)

        self.base_path = os.path.join(base_path, batch_id)
        os.makedirs(self.base_path, exist_ok=True)

        self.excel_file_path = f"{os.path.join(self.base_path,'excel')}"
        os.makedirs(self.excel_file_path, exist_ok=True)

        self.zip_file_path = f"{os.path.join(self.base_path,'zip')}"
        os.makedirs(self.zip_file_path, exist_ok=True)

        self.chunks_file_path = f"{os.path.join(self.base_path,'chunks')}"
        os.makedirs(self.chunks_file_path, exist_ok=True)

    def load_data(self):
        logger.info("ChunkClass.load_data")
        filename = self.file_list[self.counter]
        filename = os.path.join(self.chunks_file_path, filename)
        try:
            with open(filename, "rb") as f:
                data_load = pickle.load(f)
                return data_load

        except Exception as e:
            logger.error(f"Exception while loading pickle file - : {str(e)}")
            raise e

    def save_data(self, data):
        logger.info("ChunkClass.save_data")
        if data is None or len(data) == 0:
            logger.debug(f"ChunkClass.save_data || file not saved - 0 data")
            return

        filename = f"{str(uuid.uuid4())}{self.extension}"
        logger.debug(f"ChunkClass.save_data || {filename} len : {len(data)}")
        self.counter += 1
        self.file_list.append(filename)
        filename = os.path.join(self.chunks_file_path, filename)
        try:
            with open(filename, "wb") as file:
                pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            logger.error(f"Exception while saving pickle file - : {str(e)}")
            raise e

    def pop_data(self):
        logger.info("ChunkClass.pop_data")
        if self.counter <= len(self.file_list):
            self.counter -= 1
            return self.load_data()
        logger.info("ChunkClass.pop_data failed because all files are loaded")
        return False

    def create_file_list(self):
        logger.info("ChunkClass.create_file_list")
        self.file_list = os.listdir(self.chunks_file_path)
        self.counter = len(self.file_list)
        logger.info(f"ChunkClass.create_file_list || {self.batch_id} || len of file_list : {len(self.file_list)}")


class LitigationReportRedisKeys:
    batch_count = None
    batch_kwargs = None
    callback_kwargs = None
    task_state = None
    batch_number = None
    headers = None

    def __init__(self, batch_id) -> None:
        self.batch_count = f"{batch_id}_loan_ids_batches"
        self.batch_kwargs = f"{batch_id}_batch_kwargs"
        self.callback_kwargs = f"{batch_id}_callback_kwargs"
        self.task_state = f"{batch_id}_report_state"
        self.headers = f"{batch_id}_headers"

    def set_batch_number_key(self, batch_number):
        self.batch_number = batch_number
        self.headers = f"{self.headers}_{self.batch_number}"
