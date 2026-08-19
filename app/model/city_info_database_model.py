from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.model.city_info_model import CityInfoModel


class CityInfoDatabaseModel(CityInfoModel):
    model_config = ConfigDict(from_attributes=True)
    
    created_at: datetime
    expires_at: datetime