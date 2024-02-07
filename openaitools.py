from os import getenv
from dotenv import load_dotenv
from openai import OpenAI

class OpenAiTools:
    def __init__(self):
        load_dotenv()

        self.client = OpenAI(
            api_key=getenv("OPENAI_API_KEY"),
        )

    def get_chatgpt(self,question: str):
        prompt = question

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo",
                max_tokens=3000,
                temperature=1,
            )

            return response.choices[0].message.content
        except:
            return

    def get_dalle(self,prompt: str):
        try:
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="1024x1024",
                n=1,
            )
            return response.data[0].url
        except:
            return