from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger
from user_context_remote.user_context import UserContext

from .location_local_constants import LocationLocalConstants

logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)
user_context = UserContext()


class StateMl(GenericCRUDML):
    def __init__(self, is_test_data: bool = False):
        logger.start("start init StateMl")
        GenericCRUDML.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.STATE_TABLE_NAME,
            default_id_column_name=LocationLocalConstants.STATE_ML_ID_COLUMN_NAME,
            is_test_data=is_test_data)
        logger.end("end init StateMl")

    def insert(self, state_id: int, state: str,
               lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE, title_approved: bool = False):
        logger.start("start insert state_ml",
                     object={'state_id': state_id,
                             'state': state,
                             'lang_code': lang_code,
                             'title_approved': title_approved})
        LangCode.validate(lang_code)
        lang_code = lang_code or LangCode.detect_lang_code(state)
        state_ml_json = {
            key: value for key, value in {
                'state_id': state_id,
                'lang_code': lang_code.value,
                'state_name': state,
                'state_name_approved': title_approved
            }.items() if value is not None
        }
        state_ml_id = GenericCRUDML.insert(
            self,
            table_name=LocationLocalConstants.STATE_ML_TABLE_NAME,
            data_json=state_ml_json)
        logger.end("end insert state_ml",
                   object={'state_ml_id': state_ml_id})

        return state_ml_id
