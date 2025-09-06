# this is api_server.py
from flask import Flask, request, jsonify
from datetime import datetime, date, time
import json
import yaml
import os
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from astro_main import AstrologicalService, BirthDetails, Language, generate_horoscope

# Load config for API key
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

os.environ['GROQ_API_KEY'] = config['groq_api_key']


app = Flask(__name__)
astro_service = AstrologicalService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Astrological Insight Generator"
    })

@app.route('/generate-insight', methods=['POST'])
def generate_insight():
    """Main API endpoint for generating insights"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'birth_date', 'birth_time', 'birth_place',"language"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        # Parse date and time
        birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        birth_time = datetime.strptime(data['birth_time'], '%H:%M').time()
        language = Language(data.get('language', 'en'))

        # Create birth details
        birth_details = BirthDetails(
            name=data['name'],
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=data['birth_place']
        )

        # Generate insight
        result = astro_service.generate_daily_insight(birth_details, language)
        
        if "error" in result:
            return jsonify(result), 500

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({
            "error": f"Invalid date/time format: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/generate-horoscope', methods=['POST'])
def api_generate_horoscope():
    """Standalone endpoint for generating horoscope"""
    try:
        data = request.get_json()
        
        if 'name' not in data or 'zodiac' not in data:
            return jsonify({
                "error": "Missing required fields: name and zodiac"
            }), 400

        result = generate_horoscope(data['name'], data['zodiac'])
        
        return jsonify({
            "name": data['name'],
            "zodiac": data['zodiac'],
            "horoscope_data": result['horoscope'],
            "generated_at": datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Error generating horoscope: {str(e)}"
        }), 500

@app.route('/zodiac-info/<sign>', methods=['GET'])
def get_zodiac_info(sign):
    """Get information about a specific zodiac sign"""
    try:
        from astro_main import ZodiacSign
        
        zodiac = None
        for z in ZodiacSign:
            if z.english.lower() == sign.lower():
                zodiac = z
                break
        
        if not zodiac:
            return jsonify({
                "error": f"Zodiac sign '{sign}' not found"
            }), 404

        traits = astro_service.insight_generator.zodiac_traits[zodiac]
        
        return jsonify({
            "sign": zodiac.english,
            "hindi_name": zodiac.hindi,
            "date_range": f"{zodiac.start_date[0]}/{zodiac.start_date[1]} - {zodiac.end_date[0]}/{zodiac.end_date[1]}",
            "traits": traits["traits"],
            "strengths": traits["strengths"],
            "challenges": traits["challenges"]
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Error fetching zodiac info: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, extra_files=[], exclude_patterns=["venv/*"])