# Projet-Integrateur-5SDBS-Final
# Web Security Plugin Project

This repository contains a complete web security plugin designed to detect malicious websites using machine learning, feature extraction, and an orchestrated backend architecture. The project aims to integrate seamlessly into Chrome as a plugin, allowing users to test URLs for potential threats directly from their browser.

## **Project Overview**

The system consists of the following components:

### **Frontend**

- A simple web interface for testing URLs and interacting with the backend services.
- Designed to integrate with Chrome as a plugin.

### **Backend**

The backend is divided into multiple microservices, each deployed independently. The services communicate with each other via HTTP requests:

#### **1. Database Service (`db_service`)

- **Purpose**: Stores and retrieves information about URLs, including blacklists and reliability predictions.
- **Port**: `8010`
- **Main Endpoint**:
  - `GET /reliability/check/?url=<url>`: Check if a URL is in the database.
  - `POST /reliability/add/`: Add reliability data for a URL.

#### **2. Feature Extraction Service (********`feature_extraction_service`********\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*)**

- **Purpose**: Extracts various features from the URL for analysis (e.g., domain age, DNS records, external links).
- **Port**: Runs independently as required for feature processing.

#### **3. Machine Learning Service (********`model_IA_service`********\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*)**

- **Purpose**: Uses a pre-trained Random Forest model (`RandomForest_BestModel_8827.joblib`) to classify URLs as safe or malicious based on extracted features.
- **Port**: `8004`
- **Main Endpoint**:
  - `POST /predict/`: Accepts URL features and returns predictions.

#### **4. Orchestrator Service (********`orchestrator_service`********\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*)**

- **Purpose**: Coordinates requests between the feature extraction, machine learning, and database services.
- **Port**: `50000` (exposed for external requests in the INSA network).
- **Main Endpoint**:
  - `/start_orchestration/?l=<url>`: Orche

    strates the analysis pipeline for the given URL.

---

## **Directory Structure**

```plaintext
.
├── BackEnd
│   ├── db_service
│   ├── feature_extraction_service
│   ├── model_IA_service
│   └── orchestrator_service
├── FrontEnd
└── README.md
```

### **Backend Directory Details**

- **`db_service/`**: Contains the database logic and APIs.
- **`feature_extraction_service/`**: Scripts to extract features from URLs.
- **`model_IA_service/`**: Machine learning model and prediction logic.
- **`orchestrator_service/`**: Handles communication between services.

### **Frontend Directory Details**

- **`index.html`**: Main entry point for the plugin UI.
- **`script.js`**: Handles communication with backend APIs.
- **`manifest.json`**: Chrome plugin configuration.

---

## **Setup Instructions**

### **1. Building Docker Images**

Each service has its own `Dockerfile` to create its container image. Run the following commands from the respective service directories:

#### Database Service:

```bash
cd BackEnd/db_service
docker build -t microservice_db .
```

#### Feature Extraction Service:

```bash
cd BackEnd/feature_extraction_service
docker build -t feature_extraction_service .
```

#### Machine Learning Service:

```bash
cd BackEnd/model_IA_service
docker build -t microservice_ia .
```

#### Orchestrator Service:

```bash
cd BackEnd/orchestrator_service
docker build -t orchestrator_service .
```

### **2. Running Containers**

Start the containers for each microservice with their respective ports:

#### Database Service:

```bash
docker run -p 8010:8010 --name microservice_db_container microservice_db
```

#### Feature Extraction Service:

```bash
docker run -p 8002:8002 --name feature_extraction_service_container feature_extraction_service
```

#### Machine Learning Service:

```bash
docker run -p 8004:8004 --name microservice_ia_container microservice_ia
```

#### Orchestrator Service:

```bash
docker run -p 50000:50000 --name orchestrator_service_container orchestrator_service
```

---

## **Testing the Application**

### **Endpoints to Test**

#### **1. Orchestration Request**

Start the orchestration pipeline:

```bash
curl "http://192.168.37.69:50000/start_orchestration/?url=https://example.com"
```

#### **2. Database Service**

- **Check URL Reliability**:
  ```bash
  curl -X GET "http://192.168.37.14:8010/reliability/check/?url=https://example.com"
  ```
- **Add URL Reliability**:
  ```bash
  curl -X POST "http://192.168.37.14:8010/reliability/add/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "prediction": "safe", "confidence": 95}'
  ```

#### **3. Machine Learning Service**

Predict using the trained model:

```bash
curl -X POST "http://192.168.37.14:8004/predict" \
-H "Content-Type: application/json" \
-d '{"feature1": value1, "feature2": value2, ...}'
```

---

## **Deployment Notes**

1. Each microservice runs on its own **VM** or uses distinct ports for communication.
2. OpenStack and INSA TOULOUSE network only expose specific ports. It is possible to send HTTP requestes only to ports between 50000 and 50050. That’s why we exposed the orchestrator to this port, so the frontend can send the request.

---

## **Project contributors**
> - Cristian Martinez
> - Luz Vera
> - Emilie Greaker
> - Laura Cabanillas
> - Elisabeth Maton
> - Xuxin Zhu
## **University**: INSA TOULOUSE

---

## **Future Enhancements**

1. Integrate advanced machine learning models.
2. Enhance feature extraction with real-time DNS and WHOIS lookups.
3. Optimize service orchestration with Kubernetes.
