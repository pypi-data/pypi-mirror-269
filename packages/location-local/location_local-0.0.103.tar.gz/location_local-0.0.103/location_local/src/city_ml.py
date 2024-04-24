from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger
from user_context_remote.user_context import UserContext

from .location_local_constants import LocationLocalConstants

logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)
user_context = UserContext()


class CityMl(GenericCRUDML):
    def __init__(self, is_test_data: bool = False):
        logger.start("start init CityMl")
        GenericCRUDML.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.CITY_TABLE_NAME,
            default_id_column_name=LocationLocalConstants.CITY_ML_ID_COLUMN_NAME,
            is_test_data=is_test_data)
        logger.end("end init CityMl")

    def insert(self, city_id: int, city: str, lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE,
               title_approved: bool = False, is_main: int = None):
        logger.start("start insert city_ml",
                     object={'city_id': city_id, 'city': city,
                             'lang_code': lang_code,
                             'title_approved': title_approved,
                             'is_main': is_main})
        LangCode.validate(lang_code)
        lang_code = lang_code or LangCode.detect_lang_code(city)
        city_ml_json = {
            key: value for key, value in {
                'city_id': city_id,
                'lang_code': lang_code.value,
                'is_main': is_main,
                'title': city,
                'title_approved': title_approved
            }.items() if value is not None
        }
        # TODO Shall we use CrudMl in all those case in this file?
        city_ml_id = GenericCRUDML.insert(
            self,
            table_name=LocationLocalConstants.CITY_ML_TABLE_NAME,
            data_json=city_ml_json)
        logger.end("end insert city_ml",
                   object={'city_ml_id': city_ml_id})

        return city_ml_id
