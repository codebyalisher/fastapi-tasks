#Validation:in fastAPI, validation is done via Pydantic models, which automatically enforce data type, length, and value constraints.
class Item(BaseModel):
    name: str
    price: float

    @root_validator
    def check_price(cls, values):
        price = values.get("price")
        if price < 0:
            raise ValueError("Price must be positive")
        return values
