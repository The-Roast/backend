'''Module defining all environment variables to use'''

import secrets
from typing import Any, Dict, List, Optional, Union
import os
from dotenv import load_dotenv, find_dotenv

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

load_dotenv(find_dotenv(".env"))

class ServerSettings(BaseSettings):

    '''Settings class compiling properties to use from environment variables'''

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @classmethod
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:

        '''Validation method for specifying domains that can use backend'''

        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @classmethod
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:

        '''Validation method for creating DB connection'''

        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    @classmethod
    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:

        '''Validation method for getting project name'''

        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/theroast/templates/build"
    EMAILS_ENABLED: bool = True
    EMAILS_FROM_EMAIL: Optional[str]
    EMAILS_FROM_NAME: Optional[str]

    @classmethod
    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:

        '''Validation method for deciding if emails are enabled'''

        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    class Config:

        '''Meta class for ServerSettings'''

        case_sensitive = True
        env_file = ".env"

class APISettings(BaseSettings):

    '''Settings class for defining all API settings (e.g. keys)'''

    NEWS_API_KEY: str = "0c28d76ea1d44bd9a016683b50895718"
    OPENAI_API_KEY: str = "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"
    COHERE_API_KEY: str = "tcy8zG96y7hA4Tk0W4VK4GK9OQkkBLdg7qNpS5MY"
    ANTHROPIC_API_KEY: str = "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"

    class Config:

        '''Meta class for APISettings'''

        case_sensitive = True
        env_file = ".env"

server_config = ServerSettings()
api_config = APISettings()