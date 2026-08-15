# 🛰️ Real-Time Satellite Population Intelligence

A real-time satellite observation processing and population estimation system built with **FastAPI, SQLite, Streamlit, and Random Forest**.

The system accepts satellite brightness observations, detects duplicate events, resolves conflicting observations using reliability information, identifies late events, records audit information, and provides AI-powered population estimates from satellite night-light features.

---

## 🚀 Project Overview

This project combines satellite night-light data with machine learning and a real-time API pipeline.

### Core workflow

```text
Satellite Observation
        │
        ▼
     FastAPI
        │
        ├── Event ID Generation
        │
        ├── Duplicate Detection
        │
        ├── SQLite Storage
        │
        ├── Late Event Detection
        │
        ├── Conflict Resolution
        │
        └── Audit Logging
        │
        ▼
 Resolved Observation
        │
        ▼
Population Prediction
        │
        ▼
 Random Forest Model
        │
        ▼
Estimated Population
```

The project also includes a **Streamlit dashboard** for city exploration, satellite observation ingestion, population prediction, and dataset analytics.

---

## ✨ Features

### 📡 Real-Time Satellite Observation Ingestion

The FastAPI backend provides an `/ingest` endpoint that accepts:

- Satellite source ID
- Observation timestamp
- City ID
- Brightness value
- Reliability score

Each observation receives a deterministic SHA-256 event ID.

### 🔁 Duplicate Detection

The system checks the generated `event_id` before storing an observation.

If the same event is submitted again, the API returns:

```json
{
  "status": "duplicate",
  "message": "Observation already processed"
}
```

This prevents the same observation from being processed multiple times.

### ⚔️ Conflict Resolution

When multiple satellite observations exist for the same city and timestamp, the conflict engine evaluates the observations and resolves the winning observation using the system's reliability-based resolution logic.

### ⏱️ Late Event Detection

The ingestion pipeline checks whether an incoming observation is late relative to the observations already processed for that city.

The API exposes this through:

```json
"late_event": true
```

or:

```json
"late_event": false
```

### 🧾 Audit Logging

Important processing decisions are recorded in the SQLite audit log, including:

- Event ID
- City
- Event timestamp
- Action
- Decision
- Reason
- Input data
- Output data

This provides traceability for observation processing.

### 🤖 AI Population Prediction

The project uses a trained **Random Forest** model to estimate population from satellite night-light features.

The prediction pipeline uses seven features:

1. `average_masked_mean`
2. `average_masked_max`
3. `average_masked_min`
4. `average_masked_stdDev`
5. `Brightness_Range`
6. `Brightness_Ratio`
7. `Brightness_Product`

### 📊 Interactive Streamlit Dashboard

The dashboard provides:

- Dashboard overview
- City Explorer
- Population AI
- Live Satellite Ingestion
- Satellite Analytics
- Brightness visualizations
- Population prediction interface
- API status information

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Backend API | FastAPI |
| API Server | Uvicorn |
| Data Validation | Pydantic |
| Database | SQLite |
| Machine Learning | Scikit-learn |
| ML Algorithm | Random Forest |
| Data Processing | Pandas, NumPy |
| Frontend / Dashboard | Streamlit |
| Testing | Pytest |
| API Testing | HTTPX / FastAPI TestClient |
| Model Serialization | Joblib |
| Satellite Data | NASA VIIRS night-light dataset |

---

## 📁 Project Structure

```text
myonsite_assignment/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── storage.py
│   ├── conflict_engine.py
│   ├── audit.py
│   └── prediction.py
│
├── data/
│   ├── satellite.db
│   ├── Indian_City_NightLights.csv
│   └── city_population.csv
│
├── models/
│   ├── population_model.pkl
│   └── model_metrics.json
│
├── scripts/
│   └── train_model.py
│
├── tests/
│   ├── test_audit.py
│   ├── test_conflict.py
│   ├── test_ingest.py
│   ├── test_late_event.py
│   └── test_prediction.py
│
├── streamlit_app.py
└── requirements.txt
```

---

## 📊 Dataset

The project uses the following data files:

### `Indian_City_NightLights.csv`

Contains city-level satellite night-light information, including:

- City
- Latitude
- Longitude
- Population
- Average masked maximum
- Average masked mean
- Average masked minimum
- Average masked standard deviation

### `city_population.csv`

Contains city population information with:

- City
- Population

The Streamlit dashboard uses the night-light dataset for city exploration and analytics.

---

## 🤖 Machine Learning

The population estimation model is stored at:

```text
models/population_model.pkl
```

Model-related metrics are stored at:

```text
models/model_metrics.json
```

The model is trained using the script:

```text
scripts/train_model.py
```

### Feature engineering

Additional brightness features are derived from the satellite measurements:

```text
Brightness_Range   = maximum - minimum

Brightness_Ratio   = maximum / minimum

Brightness_Product = mean × maximum
```

These engineered features are supplied along with the original night-light statistics to the Random Forest model.

---

## 🔌 API Endpoints

### Root

```http
GET /
```

Returns an API status message.

Example:

```json
{
  "message": "Satellite Population Estimator API is running"
}
```

---

### Ingest Satellite Observation

```http
POST /ingest
```

Example request:

```json
{
  "source_id": "SATELLITE_UI_01",
  "timestamp": "2026-08-25T12:00:00",
  "city_id": "DELHI",
  "brightness_value": 150.0,
  "reliability_score": 0.90
}
```

Example successful response:

```json
{
  "status": "accepted",
  "message": "Observation stored and conflict resolved",
  "event_id": "...",
  "late_event": false,
  "resolved_observation": {
    "observation_id": 1,
    "source_id": "SATELLITE_UI_01",
    "city_id": "DELHI",
    "timestamp": "2026-08-25T12:00:00",
    "brightness_value": 150.0,
    "reliability_score": 0.9
  }
}
```

---

### Population Prediction

```http
POST /predict
```

Example request:

```json
{
  "average_masked_mean": 10.05,
  "average_masked_max": 56.14,
  "average_masked_min": 0.0,
  "average_masked_stdDev": 8.2,
  "Brightness_Range": 56.14,
  "Brightness_Ratio": 56140.0,
  "Brightness_Product": 563.207
}
```

The endpoint returns the model-generated population prediction.

---

## 🗄️ Database

The application uses SQLite:

```text
data/satellite.db
```

The database stores satellite observations and audit information.

The observation table contains fields such as:

```text
id
source_id
timestamp
city_id
brightness_value
reliability_score
event_id
created_at
received_at
```

The audit system records processing decisions for traceability.

---

## 🖥️ Running the Project

### 1. Create and activate the virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the FastAPI backend

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Start the Streamlit dashboard

Open a second terminal, activate the same virtual environment, and run:

```powershell
python -m streamlit run streamlit_app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

### 5. Run the tests

```powershell
python -m pytest -v
```

The project currently contains tests covering:

- Prediction
- Observation ingestion
- Duplicate handling
- Conflict resolution
- Late events
- Audit logging

---

## 🧪 Testing

The project uses Pytest for automated testing.

Test files:

```text
tests/
├── test_audit.py
├── test_conflict.py
├── test_ingest.py
├── test_late_event.py
└── test_prediction.py
```

The complete test suite has been verified successfully with:

```text
6 passed
```

---

## 📈 Dashboard Sections

### 🏠 Dashboard

Provides a high-level overview of:

- Number of cities
- Average brightness
- Maximum brightness
- Minimum brightness
- City selection
- Night-light intensity chart

### 🏙️ City Explorer

Allows users to select a city and inspect:

- Latitude
- Longitude
- Mean brightness
- Maximum brightness
- Minimum brightness
- Standard deviation

### 🤖 Population AI

Uses the selected city's satellite features and sends them to the FastAPI `/predict` endpoint to generate a population estimate.

### 📡 Live Ingestion

Allows a user to submit a satellite observation directly from the dashboard.

The UI displays:

- Processing status
- Event ID
- Winning satellite source
- Brightness
- Reliability
- Conflict-resolution result

### 📊 Analytics

Provides dataset-level statistics and visualizations for satellite night-light intensity.

---

## 🔐 Data Processing Flow

```text
1. Receive satellite observation
              ↓
2. Validate request with Pydantic
              ↓
3. Generate SHA-256 event ID
              ↓
4. Check duplicate event
              ↓
5. Detect late event
              ↓
6. Store observation in SQLite
              ↓
7. Resolve conflicting observations
              ↓
8. Create audit record
              ↓
9. Return processing result
```

---

## 🎯 Project Goals

The system demonstrates how satellite-derived night-light information can be combined with machine learning to support population estimation while also handling practical real-time data-processing concerns such as:

- Duplicate events
- Conflicting observations
- Late-arriving events
- Reliability-based resolution
- Auditability
- API-based processing
- Interactive analytics

---

## 🔮 Future Enhancements

Potential future improvements include:

- Live NASA satellite data ingestion
- Google Earth Engine integration
- Real-time event streaming with Kafka
- PostgreSQL deployment
- Authentication and role-based access
- Cloud deployment
- Advanced geospatial visualizations
- Historical population trend analysis
- Model retraining pipeline
- Monitoring and alerting
- Containerized deployment using Docker

---

## 👩‍💻 Project

**Real-Time Satellite Population Intelligence**

Built using:

**NASA VIIRS + Random Forest + FastAPI + SQLite + Streamlit**

#   m y O n s i t e _ a s s i g n m e n t  
 #   m y O n s i t e _ a s s i g n m e n t  
 