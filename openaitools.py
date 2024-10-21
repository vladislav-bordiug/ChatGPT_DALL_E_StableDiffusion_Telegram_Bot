from os import getenv
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import List, Dict

load_dotenv()

client = AsyncOpenAI(
    api_key=getenv("OPENAI_API_KEY"),
)

class OpenAiTools:
    async def get_chatgpt(messages: List[Dict[str, str]]):
        try:
            response = await client.chat.completions.create(
                messages=messages,
                model="gpt-4o",
                max_tokens=16384,
                temperature=1,
            )

            return response.choices[0].message.content
        except:
            return

    async def get_dalle(prompt: str):
        try:
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1,
            )

            return response.data[0].url
        except:
            return
