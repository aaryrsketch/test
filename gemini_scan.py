import google.generativeai as genai
import streamlit as st
from datetime import date
from PIL import Image

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-flash-latest")

def analyze_waste_image(uploaded_file):
    image = Image.open(uploaded_file)
    today = date.today().strftime("%d/%m/%Y")

    prompt = f"""
    You are a waste segregation verification assistant.
    
    First, check if this image has a visible timestamp overlay burned onto it 
    (like from a GPS camera app). The timestamp must show today's date: {today}.
    
    If there is no timestamp overlay,
    or the date does not match {today},
    or if the image is unrelate to recycling or trash or waste,
    or the image contains trash but its not segrigated or ready for recycling....as in if in the image contains trash of different types
    like Wet waste, Dry waste, Hazardous waste, E-waste, Medical waste,
    or the trash is not contained in a bag,box or other container
    then respond with:
    INVALID: <reason>
    
    If the timestamp is valid, identify all waste categories visible in the image.
    Choose only from these categories: Wet waste, Dry waste, Hazardous waste, E-waste, Medical waste.
    
    Respond in this exact format:
    VALID
    CATEGORIES: <comma separated list>
    """

    response = model.generate_content([prompt, image])
    return parse_response(response.text)

def parse_response(text):
    text = text.strip()
    
    if text.startswith("INVALID"):
        reason = text.replace("INVALID:", "").strip()
        return {
            "valid": False,
            "reason": reason,
            "categories": []
        }
    
    if text.startswith("VALID"):
        lines = text.splitlines()
        categories = []
        for line in lines:
            if line.startswith("CATEGORIES:"):
                raw = line.replace("CATEGORIES:", "").strip()
                categories = [c.strip() for c in raw.split(",")]
        return {
            "valid": True,
            "reason": None,
            "categories": categories
        }
    
    return {
        "valid": False,
        "reason": "Unexpected response from Gemini",
        "categories": []
    }