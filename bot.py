import discord
from discord.ext import commands
from main import FusionBrainAPI  # API ile çalışırken güncel sınıfı kullanma
from config import TOKEN, API_KEY, SECRET_KEY
import os

# Bot başlatma
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Metin mesajı işleyici/handler
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    prompt = message.content

    # FusionBrain API kullanılarak görüntü üretiliyor
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    
    # Görüntü üretmek için model alınıyor
    model_id = api.get_pipeline() # Pipeline ID’si alınıyor
    uuid = api.generate(prompt, model_id) # Görüntü üretiliyor
    images = api.check_generation(uuid)[0] # Üretim sonuçları alınıyor

    # Görüntüyü kaydetme
    file_path = "generated_image.jpg"
    api.save_image(images, file_path) # Görüntü diske kaydediliyor

    # Sending the image to the user
    with open(file_path, 'rb') as photo:
        await message.channel.send(file=discord.File(photo, "generated_image.jpg"))
        
    # Gönderildikten sonra görüntü siliniyor
    os.remove(file_path)

# Bot çalıştırılıyor
bot.run(TOKEN)