from openai import OpenAI
import os
from dotenv import load_dotenv

class DallE:
    def to_image(self, prompt):
        load_dotenv()

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        try:
            response = client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="1024x1024",
                n=1,
            )
            return response.data[0].url
        except:
            return
