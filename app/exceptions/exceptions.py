from datetime import date

class CityNotFoundException(Exception):
    """Exception raised when a city is not found."""

    def __init__(self, city_name: str):
        self.city_name = city_name
        self.message = f"City '{city_name}' not found."
        super().__init__(self.message)

class InvalidWeatherProviderResponseException(Exception):
    """Exception raised when the weather provider returns an invalid response."""

    def __init__(self, message: str = "Invalid response from weather provider."):
        self.message = message
        super().__init__(self.message)

class ForecastDateUnavailableException(Exception):
    """Exception raised when the forecast date is unavailable."""

    def __init__(self, date: date):
        self.message = f"Forecast date '{date}' is unavailable."
        super().__init__(self.message)

class CityInfoAlreadyExistsInDBException(Exception):
    """Exception raised when the city info request already exists in DB."""

    def __init__(self, city: str):
        self.message = f"City info '{city}' already exists in DB."
        super().__init__(self.message)