import openai
import re
import time
from requests.auth import HTTPBasicAuth
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

def extract_number_from_title(title):
    match = re.search(r'\d+', title)
    return int(match.group()) if match else 5

def clean_response_text(text, num_ideas):
    pattern = re.compile(r'Idea:\s*(.+?)\nDescription:\s*(.+?)(?=\nIdea:|\Z)', re.DOTALL)
    matches = pattern.findall(text)
    
    cleaned_ideas = []
    for match in matches:
        idea = match[0].strip()
        description = match[1].strip()
        if idea and description and len(description.split()) >= 45:
            cleaned_ideas.append({
                'idea': idea,
                'description': description
            })
    
    return cleaned_ideas

def generate_related_ideas(title):
    num_ideas = extract_number_from_title(title)
    attempt = 0
    max_attempts = 5
    
    while attempt < max_attempts:
        attempt += 1
        print(f"Tentativa {attempt} de {max_attempts}...")
        
        prompt = (
            f"Generate exactly {num_ideas} creative ideas based on the title '{title}'. "
            "Each idea should follow this exact format:\n"
            "Idea: [catchy phrase]\n"
            "Description: [detailed description with at least 45 words]\n\n"
            "For example:\n"
            "Idea: Use Mirrors Strategically\n"
            "Description: Mirrors are your best friend in a small apartment, reflecting light and creating the illusion of depth. Hang a large mirror opposite a window to amplify natural light and make the room feel larger. Consider mirrored furniture or decor accents to enhance this effect further.\n\n"
            "Generate exactly the requested number of ideas and descriptions, without omitting or adding extra ones."
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            ideas_text = response.choices[0].message['content'].strip()
            ideas_with_descriptions = clean_response_text(ideas_text, num_ideas)
            
            if len(ideas_with_descriptions) == num_ideas:
                return ideas_with_descriptions
            else:
                print(f"Erro: Gerou apenas {len(ideas_with_descriptions)} ideias. Tentando novamente...")
                time.sleep(2)
        
        except Exception as e:
            print("Erro ao gerar ideias:", e)
            return []
    
    print("Número de tentativas esgotado. Retornando resultados parciais.")
    return ideas_with_descriptions

def generate_blog_title(theme, attempt=1, max_attempts=2):
    prompt = (
        f"Given the theme '{theme}', generate a catchy blog title following the style of the examples below. "
        f"Ensure the title is no longer than 100 characters, including spaces and punctuation:\n\n"
        "3 Living Room Ideas That Will Make You Want to Redecorate Right Now (You Won't Believe #2!)\n"
        "3 Backyard Decor Hacks That Turn Your Outdoor Space into a Summer Oasis (Warning: #2 Is Magical!)\n"
        "3 Stunning Office Setups That'll Skyrocket Your Productivity (and Impress Your Boss!)\n\n"
        f"Please generate one blog title in this format for the theme '{theme}'."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        title = response.choices[0].message['content'].strip()

        if len(title) > 100:
            if attempt < max_attempts:
                print(f"O título gerado excede 100 caracteres. Tentativa {attempt} de {max_attempts}...")
                return generate_blog_title(theme, attempt + 1)
            else:
                return title

        print(title)
        return title
    
    except Exception as e:
        print("Erro ao gerar título:", e)
        return None

def generate_main_description(theme, title):
    prompt = (
        f"Generate a brief introductory description for a blog post titled '{title}' about '{theme}'. "
        "This description should engage the reader and provide context for the ideas that follow. "
        "Aim for 2-3 sentences."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        description = response.choices[0].message['content'].strip()
        return description
    except Exception as e:
        print("Erro ao gerar a descrição principal:", e)
        return ""
