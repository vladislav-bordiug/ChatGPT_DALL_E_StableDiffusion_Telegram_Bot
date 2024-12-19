import aiohttp

class StableDiffusion:
    def __init__(self, key: str):
        self.key = key

    async def get_stable(self, prompt: str):
        try:
            form_data = aiohttp.FormData()
            form_data.add_field("prompt", prompt, content_type='multipart/form-data')
            form_data.add_field("output_format", "jpeg", content_type='multipart/form-data')
            form_data.add_field("model", "sd3-large-turbo", content_type='multipart/form-data')

            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.stability.ai/v2beta/stable-image/generate/sd3',
                                        headers={
                                            "authorization": f"Bearer {self.key}",
                                            "accept": "image/*"
                                        },
                                        data=form_data) as response:
                    if response.status == 200:
                        photo = await response.read()
                        return photo
                    else:
                        return
        except:
            return