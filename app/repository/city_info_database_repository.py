from datetime import datetime
import json
from typing import Callable

from app.entity.city_info_database_entity import CityInfoDatabaseEntity
from app.model.city_info_database_model import CityInfoDatabaseModel
from app.model.city_info_model import CityInfoModel
from config.db_connection import DBConnectionHandler
from sqlalchemy.exc import SQLAlchemyError


class CityInfoDatabaseRepository():
    def __init__(
        self,
        connection_handler_factory: Callable[[], DBConnectionHandler],
    ) -> None:
        self.__connection_handler_factory = connection_handler_factory

    def select_by_id(
        self,  
        city_id: str,
    ) -> CityInfoDatabaseModel | None:
        with self.__connection_handler_factory() as db:
            try:
                city = db.session.query(CityInfoDatabaseEntity)\
                    .filter(CityInfoDatabaseEntity.id == city_id)\
                    .first()
                return CityInfoDatabaseModel.model_validate(city) if city else None
            except SQLAlchemyError as error:
                db.session.rollback()
                raise

    def insert(
        self,  
        city: CityInfoModel,
    ) -> CityInfoDatabaseModel:
        with self.__connection_handler_factory() as db:
            try:
                city_dict = json.loads(CityInfoModel.model_dump_json(city))
                city_entity = CityInfoDatabaseEntity(**city_dict)
                db.session.add(city_entity)
                db.session.commit()
                db.session.refresh(city_entity)
                return CityInfoDatabaseModel.model_validate(city_entity)
            except SQLAlchemyError as error:
                db.session.rollback()
                raise

    def delete_city_info_expired(
        self,
        date: datetime
    ) -> bool:
        with self.__connection_handler_factory() as db:
            try:
                deleted = db.session.query(CityInfoDatabaseEntity)\
                    .filter(CityInfoDatabaseEntity.expires_at < date)\
                    .delete()
                db.session.commit()
                return bool(deleted)
            except SQLAlchemyError as error:
                db.session.rollback()
                raise