from pydantic import BaseModel, Field


class ORMModel(BaseModel):
    class ConfigDict:
        from_attributes = True


class CityOut(ORMModel):
    id: int
    name: str


class CityCreate(BaseModel):
    name: str


class EdgeCreate(BaseModel):
    from_city_id: int
    to_city_id: int
    distance: int


class ShortestPathResult(BaseModel):
    distance: int
    target_city: str = Field(alias='targetCity')


class ShortestPathOut(BaseModel):
    city: str
    result: ShortestPathResult
