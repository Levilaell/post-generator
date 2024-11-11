from requests.auth import HTTPBasicAuth
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from ideas_generator import generate_main_description, generate_related_ideas
from image_generator import generate_image_prompt, generate_image
from wordpress import upload_image_to_wordpress, publish_to_wordpress

def generate_blog_content(title, ideas_with_descriptions, theme):
    main_description = generate_main_description(theme, title)
    meta_description = main_description[:155]
    content = f'<meta name="description" content="{meta_description}">\n'
    content = f"<p>{main_description}</p><br><br>\n\n"  # Insere a descrição principal antes das ideias
    
    featured_image_id = None
    for i, item in enumerate(ideas_with_descriptions, 1):
        idea = item['idea']
        description = item['description']
        image_prompt = generate_image_prompt(title, idea, description)
        image = generate_image(image_prompt)
        image_url = None
        image_id = None
        if image:
            image_url, image_id = upload_image_to_wordpress(image, f"{title.replace(' ', '_')}_{i}")
            if i == 1:
                featured_image_id = image_id

        content += f"<h2>{i}. {idea}</h2>\n"
        content += f"<p>{description}</p>\n"

        if image_url and image_id:
            alt_text = f"{idea} - {description[:50]}..."  # Texto alternativo para SEO
            content += f"<!-- wp:image {{\"id\":{image_id},\"sizeSlug\":\"full\"}} -->\n"
            content += f"<figure class=\"wp-block-image size-full\"><img src=\"{image_url}\" alt=\"{alt_text}\" class=\"wp-image-{image_id}\"/></figure>\n"
            content += f"<!-- /wp:image -->\n\n"

        content += "<br><br>\n"

    return content, featured_image_id

