import streamlit as st
import json
from datetime import datetime, date, time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import hashlib
import random
from enum import Enum
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain

import yaml
import os
import re

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

os.environ['GROQ_API_KEY'] = config['groq_api_key']

def generate_horoscope(name, zodiac):
    llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    )
    prompt_template = ChatPromptTemplate.from_template(config['prompt'])
    chain = LLMChain(prompt=prompt_template, llm=llm)
    result = chain.invoke({
        "name": name,
        "zodiac": zodiac
    })


    raw_output=result['text']

    match = re.search(r"{.*}", raw_output, re.S)
    json_str = match.group(0).strip() if match else None

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
    
    return data

    

@dataclass
class BirthDetails:
    name: str
    birth_date: date
    birth_time: time
    birth_place: str

class Language(Enum):
    ENGLISH = "en"
    HINDI = "hi"

class ZodiacSign(Enum):
    ARIES = ("Aries", "मेष", (3, 21), (4, 19))
    TAURUS = ("Taurus", "वृषभ", (4, 20), (5, 20))
    GEMINI = ("Gemini", "मिथुन", (5, 21), (6, 20))
    CANCER = ("Cancer", "कर्क", (6, 21), (7, 22))
    LEO = ("Leo", "सिंह", (7, 23), (8, 22))
    VIRGO = ("Virgo", "कन्या", (8, 23), (9, 22))
    LIBRA = ("Libra", "तुला", (9, 23), (10, 22))
    SCORPIO = ("Scorpio", "वृश्चिक", (10, 23), (11, 21))
    SAGITTARIUS = ("Sagittarius", "धनु", (11, 22), (12, 21))
    CAPRICORN = ("Capricorn", "मकर", (12, 22), (1, 19))
    AQUARIUS = ("Aquarius", "कुम्भ", (1, 20), (2, 18))
    PISCES = ("Pisces", "मीन", (2, 19), (3, 20))
    
    def __init__(self, english, hindi, start_date, end_date):
        self.english = english
        self.hindi = hindi
        self.start_date = start_date
        self.end_date = end_date

class ZodiacCalculator:
    """Handles zodiac sign calculation from birth date"""
    
    @staticmethod
    def get_zodiac_sign(birth_date: date) -> ZodiacSign:
        month = birth_date.month
        day = birth_date.day
        
        for sign in ZodiacSign:
            start_month, start_day = sign.start_date
            end_month, end_day = sign.end_date
            
            if start_month == end_month:
                if month == start_month and start_day <= day <= end_day:
                    return sign
            else:  # Sign spans across months (like Capricorn)
                if ((month == start_month and day >= start_day) or 
                    (month == end_month and day <= end_day)):
                    return sign
        
        return ZodiacSign.CAPRICORN

class InsightGenerator:
    """Generates personalized astrological insights"""
    
    def __init__(self):
        self.zodiac_traits = {
            ZodiacSign.ARIES: {
                "traits": ["bold", "energetic", "pioneering", "impulsive"],
                "strengths": ["leadership", "courage", "enthusiasm"],
                "challenges": ["impatience", "aggression"]
            },
            ZodiacSign.TAURUS: {
                "traits": ["practical", "reliable", "patient", "stubborn"],
                "strengths": ["stability", "determination", "loyalty"],
                "challenges": ["inflexibility", "materialism"]
            },
            ZodiacSign.GEMINI: {
                "traits": ["adaptable", "curious", "communicative", "restless"],
                "strengths": ["versatility", "intelligence", "wit"],
                "challenges": ["inconsistency", "superficiality"]
            },
            ZodiacSign.CANCER: {
                "traits": ["nurturing", "emotional", "intuitive", "protective"],
                "strengths": ["empathy", "imagination", "loyalty"],
                "challenges": ["moodiness", "oversensitivity"]
            },
            ZodiacSign.LEO: {
                "traits": ["confident", "generous", "dramatic", "proud"],
                "strengths": ["leadership", "creativity", "warmth"],
                "challenges": ["arrogance", "attention-seeking"]
            },
            ZodiacSign.VIRGO: {
                "traits": ["analytical", "practical", "perfectionist", "helpful"],
                "strengths": ["attention to detail", "reliability", "service"],
                "challenges": ["overcritical", "worry"]
            },
            ZodiacSign.LIBRA: {
                "traits": ["diplomatic", "harmonious", "social", "indecisive"],
                "strengths": ["balance", "fairness", "charm"],
                "challenges": ["indecision", "people-pleasing"]
            },
            ZodiacSign.SCORPIO: {
                "traits": ["intense", "mysterious", "passionate", "determined"],
                "strengths": ["depth", "transformation", "intuition"],
                "challenges": ["jealousy", "secretiveness"]
            },
            ZodiacSign.SAGITTARIUS: {
                "traits": ["adventurous", "philosophical", "optimistic", "blunt"],
                "strengths": ["freedom", "wisdom", "honesty"],
                "challenges": ["restlessness", "tactlessness"]
            },
            ZodiacSign.CAPRICORN: {
                "traits": ["ambitious", "disciplined", "practical", "reserved"],
                "strengths": ["responsibility", "perseverance", "wisdom"],
                "challenges": ["pessimism", "rigidity"]
            },
            ZodiacSign.AQUARIUS: {
                "traits": ["innovative", "independent", "humanitarian", "detached"],
                "strengths": ["originality", "idealism", "friendship"],
                "challenges": ["aloofness", "unpredictability"]
            },
            ZodiacSign.PISCES: {
                "traits": ["compassionate", "artistic", "intuitive", "escapist"],
                "strengths": ["empathy", "creativity", "spirituality"],
                "challenges": ["oversensitivity", "confusion"]
            }
        }
        
        self.insight_templates = [
            "Your {trait} nature will guide you through today's challenges. Focus on {strength} and be mindful of {challenge}.",
            "Today's energy resonates with your {trait} spirit. Channel your {strength} while staying aware of potential {challenge}.",
            "As a {trait} soul, you'll find opportunities to showcase your {strength}. Watch out for tendencies toward {challenge}.",
            "The stars align with your {trait} essence today. Embrace your natural {strength} but guard against {challenge}.",
            "Your inherent {trait} qualities will shine bright. Let your {strength} lead the way while managing any {challenge}."
        ]
        
        self.hindi_insights = {
            "leadership": "नेतृत्व",
            "creativity": "रचनात्मकता", 
            "wisdom": "बुद्धिमत्ता",
            "patience": "धैर्य",
            "courage": "साहस"
        }

    def generate_insight(self, birth_details: BirthDetails, zodiac: ZodiacSign, 
                        language: Language = Language.ENGLISH) -> str:
        """Generate personalized insight based on birth details and zodiac"""
        
        traits = self.zodiac_traits[zodiac]
        
        name_hash = hashlib.md5(birth_details.name.encode()).hexdigest()
        time_factor = birth_details.birth_time.hour + birth_details.birth_time.minute
        
        random.seed(int(name_hash[:8], 16) + time_factor)
        
        trait = random.choice(traits["traits"])
        strength = random.choice(traits["strengths"])
        challenge = random.choice(traits["challenges"])
        template = random.choice(self.insight_templates)
        
        insight = template.format(trait=trait, strength=strength, challenge=challenge)
        
        hour = birth_details.birth_time.hour
        if 5 <= hour <= 11:
            insight += " Morning energy favors new beginnings."
        elif 12 <= hour <= 17:
            insight += " Afternoon brings clarity to decisions."
        elif 18 <= hour <= 22:
            insight += " Evening encourages reflection and planning."
        else:
            insight += " Night time enhances intuition and dreams."
        
        if language == Language.HINDI:
            insight = self._pseudo_translate_to_hindi(insight, zodiac)
            
        return insight
    
    def _pseudo_translate_to_hindi(self, insight: str, zodiac: ZodiacSign) -> str:
        """Pseudo Hindi translation - placeholder for real translation service"""
        hindi_templates = [
            f"आज आपका {zodiac.hindi} राशि का प्रभाव सकारात्मक होगा। नए अवसरों का लाभ उठाएं।",
            f"{zodiac.hindi} राशि वालों के लिए आज का दिन शुभ है। अपनी प्राकृतिक क्षमताओं का उपयोग करें।",
            f"आपके {zodiac.hindi} राशि के गुण आज चमकेंगे। धैर्य और समझदारी से काम लें।"
        ]
        return random.choice(hindi_templates)

class CacheManager:
    """Simple caching system for insights"""
    
    def __init__(self):
        self.cache = {}
    
    def get_cache_key(self, birth_details: BirthDetails, language: Language) -> str:
        """Generate cache key based on user details and current date"""
        today = datetime.now().date()
        key_data = f"{birth_details.name}_{birth_details.birth_date}_{today}_{language.value}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get_cached_insight(self, cache_key: str) -> Optional[Dict]:
        """Retrieve cached insight"""
        return self.cache.get(cache_key)
    
    def cache_insight(self, cache_key: str, insight_data: Dict):
        """Store insight in cache"""
        self.cache[cache_key] = insight_data

class AstrologicalService:
    """Main service orchestrating all components"""
    
    def __init__(self):
        self.zodiac_calculator = ZodiacCalculator()
        self.insight_generator = InsightGenerator()
        self.cache_manager = CacheManager()
    
    def generate_daily_insight(self, birth_details: BirthDetails, 
                             language: Language = Language.ENGLISH) -> Dict:
        """Main method to generate personalized daily insight"""
        
        # Check cache first
        cache_key = self.cache_manager.get_cache_key(birth_details, language)
        cached_result = self.cache_manager.get_cached_insight(cache_key)
        
        if cached_result:
            return cached_result
        
        try:
            zodiac = self.zodiac_calculator.get_zodiac_sign(birth_details.birth_date)
            
            insight = self.insight_generator.generate_insight(
                birth_details, zodiac, language
            )
            horoscope = generate_horoscope(birth_details.name, zodiac)
            result = {
                "name": birth_details.name,
                "zodiac": zodiac.hindi if language == Language.HINDI else zodiac.english,
                "insight": insight,
                "language": language.value,
                "birth_place": birth_details.birth_place,
                "generated_at": datetime.now().isoformat(),
                "horoscope_by_llm": horoscope['horoscope']
            }
            
            self.cache_manager.cache_insight(cache_key, result)
            
            return result
            
        except Exception as e:
            return {
                "error": f"Failed to generate insight: {str(e)}",
                "name": birth_details.name
            }

def main():
    st.set_page_config(
        page_title="Astrological Insight Generator",
        page_icon="🔮",
        layout="wide"
    )
    
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #4A90E2;
        margin-bottom: 2rem;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .zodiac-badge {
        background: #FF6B6B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-header'>🔮 Astrological Insight Generator</h1>", 
                unsafe_allow_html=True)
    
    st.markdown("**Get personalized daily astrological insights based on your birth details**")
    
    if 'astro_service' not in st.session_state:
        st.session_state.astro_service = AstrologicalService()
    
    with st.form("birth_details_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", placeholder="Enter your name")
            birth_date = st.date_input("Birth Date", 
                                     value=date(1995, 8, 20),
                                     min_value=date(1900, 1, 1),
                                     max_value=date.today())
            
        with col2:
            birth_time = st.time_input("Birth Time", value=time(14, 30))
            birth_place = st.text_input("Birth Place", 
                                      placeholder="City, Country (e.g., Jaipur, India)")
        
        language = st.selectbox("Language", 
                               options=[Language.ENGLISH, Language.HINDI],
                               format_func=lambda x: "English" if x == Language.ENGLISH else "हिंदी")
        
        submitted = st.form_submit_button("Generate Insight", type="primary")
    
    if submitted:
        if not name or not birth_place:
            st.error("Please fill in all required fields.")
            return
        
        with st.spinner("Generating your personalized insight..."):
            birth_details = BirthDetails(
                name=name,
                birth_date=birth_date,
                birth_time=birth_time,
                birth_place=birth_place
            )
            
            result = st.session_state.astro_service.generate_daily_insight(
                birth_details, language
            )
        
        if "error" in result:
            st.error(result["error"])
        else:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="insight-box">
                    <h3>🌟 Daily Insight for {result['name']} by random shuffling of static traits</h3>
                    <p style="font-size: 1.1em; line-height: 1.6;">{result['insight']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="zodiac-badge">
                    ♈ Zodiac: {result['zodiac']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"📍 **Birth Place:** {result['birth_place']}")
                st.markdown(f"🗓️ **Birth Date:** {birth_date}")
                st.markdown(f"🕐 **Birth Time:** {birth_time}")
                st.markdown(f"🌐 **Language:** {'English' if language == Language.ENGLISH else 'हिंदी'}")
                st.markdown(f"🌐 **Horoscope By LLM:** {result['horoscope_by_llm']}")
    

if __name__ == "__main__":
    main()
