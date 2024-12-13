import requests
from functools import partial
import asyncio

class StableDiffusion:
    def __init__(self, key: str):
        self.key = key

    async def get_stable(self, prompt: str):
        response = await asyncio.get_running_loop().run_in_executor(None,
            partial(requests.post,f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "authorization": f"Bearer {self.key}",
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