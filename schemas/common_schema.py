from pydantic import BaseSettings, BaseModel


class AuthInterfaceSchema(BaseModel):
    country_code: str
    client_id: str
    api_token: str
    provider: str
