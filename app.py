import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
import os  # Added to read Railway's port configuration

def generate_image(prompt):
    if not prompt.strip():
        raise gr.Error("Please type something first!")

    style_boost = ", ultra-clean, smooth surface, flawless texture, 3D render style, soft lighting, high resolution"
    final_prompt = prompt.strip() + style_boost
    
    encoded_prompt = urllib.parse.quote(final_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux"
    
    try:
        response = requests.get(url, timeout=40)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            raise gr.Error("The network is busy. Tap generate again!")
    except Exception as e:
        raise gr.Error(f"Connection failed: {str(e)}")

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🍌 Ultra-Smooth Image Bot")
    gr.Markdown("Type a prompt below to generate fast, clean, and smooth-surfaced images.")
    
    with gr.Row():
        user_prompt = gr.Textbox(label="What do you want to generate?", placeholder="e.g., a nano banana sitting on a glass table")
        generate_btn = gr.Button("Generate Image", variant="primary")
        
    output_image = gr.Image(label="Your Result")
    generate_btn.click(fn=generate_image, inputs=user_prompt, outputs=output_image)

# CRITICAL FOR RAILWAY: This tells the app to listen on the port Railway gives it
port = int(os.environ.get("PORT", 7860))
demo.launch(server_name="0.0.0.0", server_port=port)
