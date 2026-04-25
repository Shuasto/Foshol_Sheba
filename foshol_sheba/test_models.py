import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv('f:/Paid Project/Course Project/Shuasto Webapp/foshol_sheba/.env')
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("NO API KEY")
    exit()

genai.configure(api_key=api_key)
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
