import pickle
import json
from .models import ETAPrediction
from .db import SessionLocal
from pyspark.ml import PipelineModel
from .spark_session import spark
from pyspark.sql import Row

MODEL_VERSION = "v1"

# Charger modèle pré-entrainé

model = PipelineModel.load("ML/smart_logitrack_pipeline")



def predict_eta(features: dict) -> float:

    #  Convertir le dict en DataFrame Spark
    df = spark.createDataFrame([Row(**features)])

    #  Faire la prédiction avec ton modèle Spark
    pred_row = model.transform(df).select("prediction").first()
    pred = float(pred_row["prediction"])

    #  Sauvegarder la prédiction dans PostgreSQL
    db = SessionLocal()
    try:
        eta_record = ETAPrediction(
            features_json=json.dumps(features),
            estimated_duration=pred,
            model_version=MODEL_VERSION
        )
        db.add(eta_record)
        db.commit()
    finally:
        db.close()

    #  Retourner la prédiction
    return pred
