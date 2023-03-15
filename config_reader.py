from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):

    API_TOKEN: SecretStr
    DIR_PATH: SecretStr
    FILES: SecretStr

    class Config:

        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
