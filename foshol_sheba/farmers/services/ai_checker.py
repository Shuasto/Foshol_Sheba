import os
import json
from PIL import Image
import google.generativeai as genai


from django.conf import settings
from core.models import Disease

class AICheckerService:
    """
    A service to handle AI-based image analysis using Google's Gemini API.
    Make sure to add GEMINI_API_KEY to your .env file.
    """

    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing from Django settings.")
        genai.configure(api_key=self.api_key)

    def _construct_prompt(self) -> str:
        diseases = Disease.objects.all()
        disease_list = "\n".join([f"- {disease.name_en}" for disease in diseases])
        return f"""
        You are an expert agricultural scientist. Analyze the provided image of a crop leaf and identify the disease from the list of the diseases.

        **DISEASE LIST:**
        {disease_list}
        
        Return the result strictly in the following JSON format:
        {{
            "disease": "Name of the disease in English",
            "confidence_score": "Confidence score between 0 and 1",
            "description": "Description of the disease in short in Bangla"
        }}
        
        IMPORTANT RULES:
        1. Always output strictly in JSON format. Do not include any additional text, explanations, or formatting outside of the JSON structure.
        2. The 'description' field MUST be written in the Bengali language (Bangla). All other fields MUST be in English.
        3. If the image is completely dark, blurry, or does not show any identifiable crop leaf, set "disease" to "Unknown", "confidence_score" to 0.0, and "description" to a SHORT explanation in Bangla (e.g., "ছবিটি অস্পষ্ট বা অন্ধকার। অনুগ্রহ করে একটি পরিষ্কার ছবি দিন।").
        4. Keep your description field VERY SHORT, concise, and straight to the point (maximum 2 sentences).
        """
    
    def analyze_image(self, image_file) -> dict:
        """
        Takes a prompt and an image, invokes the AI model, 
        and returns a strict JSON structured output (disease, reason).
        """        
        # We use gemini-2.5-flash as it supports multimodal tasks securely
        # generation_config forces the model to return specifically formatted JSON
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        try:
            # Ensure the image is opened correctly via PIL
            img = Image.open(image_file)

            prompt = self._construct_prompt()
            
            # Call the AI model with the prompt and the image
            response = model.generate_content([prompt, img])
            
            # The model is forced to return JSON, which we parse into a Python dictionary
            result = json.loads(response.text)
            
            return {
                "status": "success",
                "data": result
            }
            
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "The AI responded with an invalid JSON format.",
                "raw_response": response.text if response else ""
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
