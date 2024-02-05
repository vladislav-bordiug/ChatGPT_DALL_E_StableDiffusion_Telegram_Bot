from openai import OpenAI
import os
from dotenv import load_dotenv

class DallE:
    def to_image(self, prompt):
        load_dotenv()

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
