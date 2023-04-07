import openai
import os
import io
import warnings
from PIL import Image
from dotenv import load_dotenv

class TextToImg:

    def to_image(self, prompt):
        load_dotenv()

        openai.api_key = os.getenv("CHAT_GPT3_API_KEY")
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            return response['data'][0]['url']
        except openai.error.OpenAIError as e:
            print(e.http_status)
            print(e.error)
            return
