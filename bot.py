import discord
from discord.ext import commands
from main import FusionBrainAPI  # API ile çalışırken güncel sınıfı kullanma
from config import TOKEN, API_KEY, SECRET_KEY
import os

# Bot başlatma
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} olarak giriş yaptı!')

@bot.command()
async def help(ctx):
    help_text = (
        "Merhaba! Görüntü üretmek için bir metin mesajı gönderin.\n"
        "Örnek: 'Bir dağın üzerinde gün batımı sahnesi.'"
    )
    await ctx.send(help_text)

@bot.command()
async def sing(ctx):
    sing_text = (
        """İzmir'in dağlarında çiçekler açar,
        Altın güneş orda sırmalar saçar
        Bozulmuş düşmanlar, hep yel gibi kaçar,
        Yaşa Mustafa Kemal Paşa yaşa;
        Adın yazılacak mücevher taşa.

        İzmir'in dağlarına bomba koydular,
        Türk'ün sancağını öne koydular.
        Şanlı zaferlerle düşmanı boğdular,
        Kader böyle imiş ey garip ana;
        Kanım feda olsun güzel vatana.

        İzmir'in dağlarında oturdum kaldım;
        Şehit olanları deftere yazdım,
        Öksüz yavruları bağrıma bastım,
        Kader böyle imiş ey garip ana;
        Kanım feda olsun güzel vatana.

        Peygamber kucağı şehitler yeri,
        Çalındı borular haydi ileri.
        Bozuldu çadırlar kalmayın geri,
        Yaşa Mustafa Kemal Paşa yaşa;
        Adın yazılacak mücevher taşa.

        Türk oğluyum ben ölmek isterim;
        Toprak diken olsa yatağım yerim;
        Allah'ından utansın dönenler geri;
        Yaşa Mustafa Kemal Paşa yaşa.
        Adın yazılacak mücevher taşa."""
    )
    await ctx.send(sing_text)
    

# Metin mesajı işleyici/handler
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    msg = await message.channel.send("Görüntünüz oluşturuluyor, lütfen bekleyin...")
  
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

    await message.channel.delete(msg)
    # Sending the image to the user
    with open(file_path, 'rb') as photo:
        await message.channel.send(file=discord.File(photo, "generated_image.png"))
        
    # Gönderildikten sonra görüntü siliniyor
    os.remove(file_path)

# Bot çalıştırılıyor
bot.run(TOKEN)