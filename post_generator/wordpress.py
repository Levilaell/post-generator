import requests
from requests.auth import HTTPBasicAuth
import io
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from config import wordpress_app_password, wordpress_media_url, wordpress_url, wordpress_user

def upload_image_to_wordpress(image, image_name):
    # Converte a imagem para PNG e salva em bytes para upload
    image_buffer = io.BytesIO()
    image.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    files = {
        'file': (f"{image_name}.png", image_buffer, 'image/png')
    }

    try:
        response = requests.post(
            wordpress_media_url,
            auth=HTTPBasicAuth(wordpress_user, wordpress_app_password),
            files=files
        )

        if response.status_code == 201:
            response_data = response.json()
            image_url = response_data.get("source_url")
            image_id = response_data.get("id")  # Obtém o ID da imagem
            return image_url, image_id  # Retorna a URL e o ID
        else:
            print("Erro ao carregar a imagem no WordPress:", response.status_code)
            print("Resposta completa:", response.text)
            return None, None

    except Exception as e:
        print("Erro ao conectar com o WordPress:", e)
        return None, None

def publish_to_wordpress(title, content, featured_image_id):
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    data = {
        'title': title,
        'content': content,
        'status': 'publish'
    }

    if featured_image_id:
        data['featured_media'] = featured_image_id  # Define a imagem destacada
    
    try:
        response = requests.post(
            wordpress_url,
            headers=headers,
            auth=HTTPBasicAuth(wordpress_user, wordpress_app_password),
            json=data
        )
        
        if response.status_code == 201:
            print("Post publicado com sucesso no WordPress!")
            print("URL do post:", response.json().get("link"))
        else:
            print("Erro ao publicar no WordPress:", response.status_code, response.text)
    
    except Exception as e:
        print("Erro ao conectar com o WordPress:", e)
