from os import getenv
import requests
from dotenv import load_dotenv
from functools import partial
import asyncio

load_dotenv()
key = getenv("STABLE_DIFFUSION_API_KEY")

class StableDiffusion:
    async def get_stable(prompt: str):
        response = await asyncio.get_running_loop().run_in_executor(None,
            partial(requests.post,f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "authorization": f"Bearer {key}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": prompt,
                "output_format": "jpeg",
                "model": "sd3-large-turbo",
            })
        )
        if response.status_code == 200:
            return response.content
        else:
            return