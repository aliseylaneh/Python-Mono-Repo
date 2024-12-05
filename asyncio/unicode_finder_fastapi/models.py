from pydantic import BaseModel


class CharName(BaseModel):
    char: str
    name: str
