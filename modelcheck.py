import google.generativeai as genai
genai.configure(api_key="AIzaSyCRbmtG4ahFD9fa4V9Lj6JJ-ypXSmciocg")

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)