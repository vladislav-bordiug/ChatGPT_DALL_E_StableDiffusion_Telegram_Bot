from os import getenv, environ
from io import BytesIO
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from dotenv import load_dotenv

load_dotenv()
environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
stability_api = client.StabilityInference(
    key=getenv("STABLE_DIFFUSION_API_KEY"),
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0",
)

class StableDiffusion:
    def get_stable(prompt: str):

        answers = stability_api.generate(
            prompt=prompt,
            seed=0,
            steps=30,
            cfg_scale=7.0,
            width=1024,
            height=1024,
            samples=1,
            sampler=generation.SAMPLER_K_DPMPP_2M
        )

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    return
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(BytesIO(artifact.binary))
                    img_path = str(artifact.seed)+ ".png"
                    img.save(img_path)

                    return img_path