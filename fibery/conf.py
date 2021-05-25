import json
import os

from pathlib import Path
from typing import Any
from typing import Dict

from pydantic import BaseSettings
from pydantic import SecretStr

from fibery.enums import FormatEnum


def json_config(settings: "Settings") -> Dict[str, Any]:
    encoding = settings.__config__.env_file_encoding
    config_file = os.getenv("FIBERY_CONFIG", f"{Path.home()}/.fibery/config.json")
    return json.loads(Path(config_file).read_text(encoding))


class MaskedSecretStr(SecretStr):
    @property
    def masked(self) -> str:
        value = self.get_secret_value()
        last_chars = 4
        if len(value) < 8:
            last_chars = int(len(value) / 2) or 1
        return f'{"*" * (len(value) - last_chars)}{value[-last_chars:]}'

    def __str__(self):
        return self.masked


class Settings(BaseSettings):
    workspace: str = None
    username: str = None
    password: MaskedSecretStr = None
    api_token: MaskedSecretStr = None
    login_url: str = "https://fibery.io/login"
    output_format: FormatEnum = FormatEnum.text

    class Config:
        env_prefix = "FIBERY_"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                json_config,
                env_settings,
                file_secret_settings,
            )


settings = Settings()
