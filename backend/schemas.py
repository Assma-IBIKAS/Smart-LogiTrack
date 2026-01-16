from pydantic import BaseModel

# Liste des colonnes attendues
categorical_cols = ["RatecodeID", "pickup_hour", "day_of_week"]
numerical_cols = ["trip_distance", "fare_amount", "tip_amount", "tolls_amount", "total_amount", "Airport_fee"]

class PredictRequest(BaseModel):
    RatecodeID: int
    pickup_hour: int
    day_of_week: int
    trip_distance: float
    fare_amount: float
    tip_amount: float
    tolls_amount: float
    total_amount: float
    Airport_fee: float