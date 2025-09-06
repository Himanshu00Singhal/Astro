Astro
├── astro_main.py          # Main Streamlit application
├── api_server.py          # REST API server
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── config.yaml           # Configuration file
----------------------------------------------------
Quick Start
----------------------------------------------------
Option 1: 

Streamlit UI (Recommended)

Install Dependencies:
pip install -r requirements.txt

Run the Streamlit App:
streamlit run astro_main.py

Open in Browser:
Navigate to http://localhost:8501
------------------------------------------------------
Option 2:
REST API

Install Additional Dependencies:
pip install flask

Run the API Server:
python api_server.py

Test the API:
curl -X POST http://localhost:8000/generate-insight \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ritika",
    "birth_date": "1995-08-20",
    "birth_time": "14:30",
    "birth_place": "Jaipur, India",
    "language": "en"
  }'