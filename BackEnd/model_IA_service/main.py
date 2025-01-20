from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="Model IA Service")

# Cargar el modelo y definir los nombres de las características
model_path = "./RandomForest_BestModel_8827.joblib"
model = joblib.load(model_path)

# Diccionario para traducir las predicciones
prediction_labels = {
    1: "legitimate",
    -1: "malicious"
}

feature_names = [
    "having_IP_Address", "URL_Length", "having_At_Symbol", "double_slash_redirecting",
    "Prefix_Suffix", "having_Sub_Domain", "Domain_registeration_length", "Favicon",
    "HTTPS_token", "Redirect", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord",
    "web_traffic", "Links_pointing_to_page"
]

@app.get("/")
def read_root():
    return {"Hello": "Model IA Service"}

# Define el modelo para los datos de entrada
class Features(BaseModel):
    having_IP_Address: int
    URL_Length: int
    having_At_Symbol: int
    double_slash_redirecting: int
    Prefix_Suffix: int
    having_Sub_Domain: int
    Domain_registeration_length: int
    Favicon: int
    HTTPS_token: int
    Redirect: int
    popUpWidnow: int
    Iframe: int
    age_of_domain: int
    DNSRecord: int
    web_traffic: int
    Links_pointing_to_page: int

# Predict endpoint
@app.post("/predict")
def predict_from_features(features_json: Features):
    """
    Realiza una predicción basado en un JSON de características.

    :param features_json: dict con los valores de las características
    :return: dict con la predicción traducida y la confianza
    """
    # Convertir el JSON en un vector ordenado
    # test_data_vector = np.array([[features_json.dict()[feature] for feature in feature_names]])
    # Crear un DataFrame con los nombres de las características
    test_data_vector = pd.DataFrame([features_json.dict()], columns=feature_names)


    # Hacer la predicción
    prediction = model.predict(test_data_vector)[0]  # Extraer la clase predicha del array
    probabilities = model.predict_proba(test_data_vector)
    confidence = int(round(np.max(probabilities, axis=1)[0] * 100))  # Convertir confianza a porcentaje entero

    # Traducir la predicción
    translated_prediction = prediction_labels.get(prediction, "Unknown")

    # Devolver resultados
    return {
        "prediction": translated_prediction,
        "confidence": confidence
    }