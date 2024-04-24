from pydantic import BaseModel
from pydantic import Extra

from gwproto.utils import snake_to_camel


DEFAULT_WEB_SERVER_NAME = "default"


class WebServerGt(BaseModel):
    Name: str = DEFAULT_WEB_SERVER_NAME
    Host: str = "localhost"
    Port: int = 8080
    Enabled: bool = True
    Kwargs: dict = {}

    class Config:
        extra = Extra.allow
        alias_generator = snake_to_camel
        allow_population_by_field_name = True
