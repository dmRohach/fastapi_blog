from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 8000
    database_url: str = 'sqlite:///./database.sqlite3'

    jwt_secret: str = 'HCKV_EPS8I2Q321QEmc-3L8nsQ3VS89NMrte7hnG2lM'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600


settings = Settings()

