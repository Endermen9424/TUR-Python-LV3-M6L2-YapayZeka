import customtkinter as ctk
from config import API, SecretKey
from main import *

def generate_image():
    prompt = prompt_entry.get()
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API, SecretKey)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)[0]
    base64_string = files
    decoded_data = base64.b64decode(base64_string)
    with open("image.png", "wb") as f:
        f.write(base64.b64decode(decoded_data))

    image = ctk.CTkImage(light_image=Image.open("picture.png"), size=(500, 500))
    
    label = ctk.CTkLabel(app, text="", image=image)
    label.pack(pady=10)

app = ctk.CTk()
app.title("AI Image Generator")
app.geometry("400x600")

prompt_entry = ctk.CTkEntry(app, width=300, placeholder_text="Enter your prompt here")
prompt_entry.pack(pady=20)
generate_button = ctk.CTkButton(app, text="Generate Image", command=generate_image)
generate_button.pack(pady=10)
app.mainloop()
