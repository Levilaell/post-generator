from requests.auth import HTTPBasicAuth
import io
from PIL import Image
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from config import stability_api

def generate_image_prompt(title, idea, description):
    return f"Create a high-quality image inspired by the idea '{idea}' and the description: '{description}'"

def generate_image(prompt):
    answers = stability_api.generate(
        prompt=prompt,
        steps=30,           # Aumentado para melhorar detalhes
        cfg_scale=8.0,      # Ajustado para melhor aderência ao prompt
        width=1000,    # Alterado para 1024
        height=1500, 
        samples=1,
        sampler=generation.SAMPLER_K_EULER  # Usando um sampler comum
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                print("A solicitação ativou os filtros de segurança da API e não pôde ser processada.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                return img
    return None
