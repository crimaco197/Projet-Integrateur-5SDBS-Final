from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="Model IA Service")

# Load trained model
model_path = "./RandomForest_BestModel_8827.joblib"
model = joblib.load(model_path)

# Diccionary to translate the predictions
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

# Defining the class which will be use as the input data
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
    Makes a prediction based on a JSON of features.

    :param features_json: dict with the feature values
    :return: dict with the translated prediction and confidence
    """
    # Create a DataFrame with the feature names
    test_data_vector = pd.DataFrame([features_json.dict()], columns=feature_names)


    # Make the prediction
    prediction = model.predict(test_data_vector)[0]  # Extract the predicted class from the array
    probabilities = model.predict_proba(test_data_vector)
    confidence = int(round(np.max(probabilities, axis=1)[0] * 100))  # Convert confidence to whole percentage

    # Translate prediction
    translated_prediction = prediction_labels.get(prediction, "Unknown")

    return {
        "prediction": translated_prediction,
        "confidence": confidence
    }