from requests.auth import HTTPBasicAuth
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from ideas_generator import generate_blog_title, generate_related_ideas
from util import generate_blog_content
from wordpress import publish_to_wordpress

def generate_and_publish_blog(title):
    ideas_with_descriptions = generate_related_ideas(title)
    if not ideas_with_descriptions:
        print("Nenhuma ideia foi gerada.")
        return

    content, featured_image_id = generate_blog_content(title, ideas_with_descriptions, theme)
    publish_to_wordpress(title, content, featured_image_id)

def main(theme):
    blog_title = generate_blog_title(theme)
    if blog_title:
        generate_and_publish_blog(blog_title)
    else:
        print("Não foi possível gerar um título para o tema fornecido.")

if __name__ == "__main__":
    x = 1
    theme = "Home Decor"  

    for i in range(x):
        print(f"Execução {i+1} de {x}")
        main(theme)