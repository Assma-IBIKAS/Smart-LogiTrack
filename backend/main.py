from fastapi import FastAPI, Depends, HTTPException
from .auth import verify_token, create_access_token
from .utils import predict_eta
from .db import engine, SessionLocal
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel, conlist
from typing import Literal
from .schemas import PredictRequest

app = FastAPI(title="ETA API")

# === LOGIN ===
@app.post("/login")
def login(username: str, password: str):
    if username != "admin" or password != "admin123":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

# === PREDICTION ===
@app.post("/predict")
def predict(request: PredictRequest):
    # Convertir en dict pour passer à predict_eta
    features = request.dict()

    try:
        eta = predict_eta(features)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

    return {"estimated_duration": eta}

#   "RatecodeID": 1,
#   "pickup_hour": 10,
#   "day_of_week": 3,
#   "trip_distance": 2.5,
#   "fare_amount": 12.0,
#   "tip_amount": 2.0,
#   "tolls_amount": 0.0,
#   "total_amount": 14.0,
#   "Airport_fee": 0.0

# === ANALYTICS ===
@app.get("/analytics/avg-duration-by-hour")
def avg_duration_by_hour():
    db: Session = SessionLocal()
    sql = text("""
        WITH cte AS (
            SELECT pickup_hour, AVG(duration_minutes) AS avgduration
            FROM silver_data
            GROUP BY pickup_hour
        )
        SELECT * FROM cte ORDER BY pickup_hour
    """)
    result = db.execute(sql).fetchall()
    db.close()
    return [{"pickuphour": r[0], "avgduration": r[1]} for r in result]


@app.get("/analytics/payment-analysis")
def payment_analysis(user: str = Depends(verify_token)):
    db: Session = SessionLocal()
    sql = text("""
        SELECT payment_type,
               COUNT(*) AS total_trips,
               AVG(duration_minutes) AS avg_duration
        FROM silver_data
        GROUP BY payment_type
    """)
    result = db.execute(sql).fetchall()
    db.close()
    return [{"payment_type": r[0], "total_trips": r[1], "avg_duration": r[2]} for r in result]
