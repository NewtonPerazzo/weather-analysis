from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from types import TracebackType
from typing import Self

class DBConnectionHandler():
    def __init__(self, connection_string: str) -> None:
        self.__connection_string = connection_string
        self.__engine = self.__create_database_engine()
        self.session: Session | None = None

    def __create_database_engine(self) -> Engine:
        engine = create_engine(self.__connection_string)
        return engine
    
    def get_engine(self) -> Engine:
        return self.__engine
    
    def __enter__(self) -> Self:
        self.session = Session(self.__engine)
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.session is not None:
            self.session.close()
