import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import urllib.parse

def generate_image(prompt):
    if not prompt.strip():
        raise gr.Error("Please type something first!")

    # Automatically injecting style attributes for that flawless nano-banana texture
    style_boost = ", ultra-clean, smooth surface, flawless texture, 3D clay style, soft lighting, high resolution"
    final_prompt = prompt.strip() + style_boost
    
    # Encode the text safely so the web address can read it
    encoded_prompt = urllib.parse.quote(final_prompt)
    
    # Connecting to the open-source image engine
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux"
    
    try:
        response = requests.get(url, timeout=40)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            raise gr.Error("The network is a bit busy. Please try clicking generate again!")
    except Exception as e:
        raise gr.Error(f"Connection failed: {str(e)}")

# Setting up the visual application interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🍌 Ultra-Smooth Image Bot")
    gr.Markdown("Type your prompt. The bot automatically boosts it for a clean, fast, and smooth surface finish.")
    
    with gr.Row():
        user_prompt = gr.Textbox(label="What do you want to generate?", placeholder="e.g., a nano banana sitting on a glass table")
        generate_btn = gr.Button("Generate Image", variant="primary")
        
    output_image = gr.Image(label="Your Result")
    
    generate_btn.click(fn=generate_image, inputs=user_prompt, outputs=output_image)

demo.launch()
