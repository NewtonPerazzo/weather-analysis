from app.exceptions.exceptions import CityInfoAlreadyExistsInDBException
from app.model.city_info_database_model import CityInfoDatabaseModel
from app.model.city_info_model import CityInfoModel
from app.repository.city_info_database_repository import CityInfoDatabaseRepository
from app.dependencies import get_connection_handler


class DatabaseCityInfo():
    def __init__(self):
        self._city_info_repository = CityInfoDatabaseRepository(
            connection_handler_factory=get_connection_handler,
        )

    def add_city_info(self, city: CityInfoModel, key: str) -> CityInfoDatabaseModel:        
        if self._city_info_repository.select_by_id(city_id=key):
            raise CityInfoAlreadyExistsInDBException(city=key)

        city_formated = city.id = key
        response = self._city_info_repository.insert(city=city_formated)
        return response

    def get_city_info_by_key(self, key: str) -> CityInfoDatabaseModel  | None:
        response = self._city_info_repository.select_by_id(city_id=key)
        return response