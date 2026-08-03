class OpenMeteoIntegration():
    def __init__(
            self, 
            open_meteo_url: str, 
            open_meteo_forecast_url: str,
            open_meteo_archive_url: str
        ):
        self.open_meteo_url = open_meteo_url
        self.open_meteo_forecast_url = open_meteo_forecast_url
        self.open_meteo_archive_url = open_meteo_archive_url
        self.open_meteo_search_city_uri = '/v1/search'
        self.open_meteo_forecast_uri = '/v1/forecast'
        self.open_meteo_archive_uri = '/v1/archive'
