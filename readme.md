# Astro

A simple astrology application with both a **Streamlit UI** and **REST API** interface.

## Project Structure
```bash
Astro Folder

├── astro_main.py # Main Streamlit application

├── api_server.py # REST API server

├── requirements.txt # Python dependencies

├── README.md # This file

└── config.yaml # Configuration file
```

## Quick Start

### Option 1: Streamlit UI (Recommended)

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```
2. **Run the Streamlit app:**

```bash
streamlit run astro_main.py
```

3. **Open in browser:**
```bash
Navigate to: http://localhost:8501
```
### Option 2: REST API
1. **Install additional dependencies:**
```bash
pip install flask
```
2. **Run the API server:**
```bash
python api_server.py
```
3. **Test the API:**
```bash
curl -X POST http://localhost:8000/generate-insight \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ritika",
    "birth_date": "1995-08-20",
    "birth_time": "14:30",
    "birth_place": "Jaipur, India",
    "language": "en"
  }'
```
