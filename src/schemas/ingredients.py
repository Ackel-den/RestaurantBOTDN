from pydantic import BaseModel


class Ingredients(BaseModel):
    name: str
    weight: float
    measure: str
