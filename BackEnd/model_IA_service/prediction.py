import joblib
import numpy as np

# Cargar el modelo y definir los nombres de las características
model_path = "./RandomForest_BestModel_8827.joblib"
model = joblib.load(model_path)

feature_names = [
    "having_IP_Address", "URL_Length", "having_At_Symbol", "double_slash_redirecting",
    "Prefix_Suffix", "having_Sub_Domain", "Domain_registeration_length", "Favicon",
    "HTTPS_token", "Redirect", "popUpWidnow", "Iframe", "age_of_domain", "DNSRecord",
    "web_traffic", "Links_pointing_to_page"
]

# Diccionario para traducir las predicciones
prediction_labels = {
    1: "legitimate",
    -1: "malicious"
}

# Definir la función
def predict_from_features(features_json):
    """
    Realiza una predicción basado en un JSON de características.

    :param features_json: dict con los valores de las características
    :return: dict con la predicción traducida y la confianza
    """
    # Convertir el JSON en un vector ordenado
    test_data_vector = np.array([[features_json[feature] for feature in feature_names]])

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

# Prueba de la función
if __name__ == "__main__":
    # Ejemplo de datos de entrada
    test_data_json = {
        "having_IP_Address": -1,
        "URL_Length": 1,
        "having_At_Symbol": 1,
        "double_slash_redirecting": -1,
        "Prefix_Suffix": -1,
        "having_Sub_Domain": -1,
        "Domain_registeration_length": -1,
        "Favicon": 1,
        "HTTPS_token": -1,
        "Redirect": 0,
        "popUpWidnow": 1,
        "Iframe": 1,
        "age_of_domain": -1,
        "DNSRecord": -1,
        "web_traffic": -1,
        "Links_pointing_to_page": 1
    }

    # Llamar a la función
    result = predict_from_features(test_data_json)
    
    # Mostrar el resultado
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']}%")
