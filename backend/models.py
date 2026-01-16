from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ETAPrediction(Base):
    __tablename__ = "eta_predictions"

    id = Column(Integer, primary_key=True, index=True)
    features_json = Column(String)
    estimated_duration = Column(Float)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
