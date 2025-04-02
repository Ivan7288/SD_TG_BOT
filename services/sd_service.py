import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO
from deep_translator import GoogleTranslator

load_dotenv()


class StableDiffusionService:
    def __init__(self):
        self.sd_client = InferenceClient(
            token=os.getenv('HUGGINGFACE_TOKEN'),
            model="stabilityai/stable-diffusion-3-medium-diffusers"
        )
        self.translator = GoogleTranslator(source='ru', target='en')

    def translate_to_english(self, prompt: str) -> str:
        """
        Translate prompt from Russian to English using Google Translate
        """
        try:
            return self.translator.translate(prompt)
        except Exception as e:
            raise Exception(f"Error translating prompt: {str(e)}")

    def generate_image(self, prompt: str, output_path: str) -> str:
        """
        Generate an image using Hugging Face Hub API and save it to the specified path
        """
        try:
            # Translate prompt to English
            english_prompt = self.translate_to_english(prompt)
            print(f"Translated prompt: {english_prompt}")  # Debug line

            # Generate image using the client
            image = self.sd_client.text_to_image(english_prompt)

            # Convert bytes to image and save
            image.save(output_path)

            return output_path

        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")
