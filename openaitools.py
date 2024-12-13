from os import getenv
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import List, Dict

load_dotenv()


class OpenAiTools:
    def __init__(self, token: str):
        self.client = AsyncOpenAI(
            api_key=token,
        )

    async def get_chatgpt(self, messages: List[Dict[str, str]]):
        try:
            response = await self.client.chat.completions.create(
                messages=messages,
                model="gpt-4o",
                max_tokens=16384,
                temperature=1,
            )

            return response.choices[0].message.content
        except:
            return

    async def get_dalle(self, prompt: str):
        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1,
            )

            return response.data[0].url
        except:
            return
