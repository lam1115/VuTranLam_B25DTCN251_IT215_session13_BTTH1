from pydantic import BaseModel, ConfigDict


class NewItems(BaseModel):
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float


class ItemResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    model_config = ConfigDict(from_attributes=True)


class ApiResponse(BaseModel):
    statusCode: int
    message: str
    error: str | None = None
    data: ItemResponse | None = None
    path: str
    timestamp: str


class ApiListResponse(BaseModel):
    statusCode: int
    message: str
    error: str | None = None
    data: list[ItemResponse]
    path: str
    timestamp: str
