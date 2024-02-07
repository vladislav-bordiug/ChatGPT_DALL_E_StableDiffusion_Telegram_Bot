import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from dotenv import load_dotenv

load_dotenv()
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
stability_api = client.StabilityInference(
    key=os.getenv("STABLE_DIFFUSION_API_KEY"),
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0",
)

PATH_TO_IMAGES = "images/"

def get_stable(prompt: str):

    answers = stability_api.generate(
        prompt=prompt,
        seed=0,
        steps=30,
        cfg_scale=7.0,
        width=512,
        height=512,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img_path = self.PATH_TO_IMAGES + str(artifact.seed)+ ".png"
                img.save(img_path)

                return img_path