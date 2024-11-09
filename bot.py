import discord
from discord.ext import commands
import yt_dlp as youtube_dl  # Usando yt-dlp em vez de youtube_dl
import os
from dotenv import load_dotenv
import asyncio

# Carrega o arquivo .env
load_dotenv()

# Obtém o token do .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Configura as intenções do bot
intents = discord.Intents.default()
intents.message_content = True  # Permissão para ler o conteúdo das mensagens

# Configura o bot com o prefixo '#' e as intenções definidas
bot = commands.Bot(command_prefix="#", intents=intents)

# Configuração do yt-dlp para baixar o áudio
yt_dl_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extractaudio': True,
    'audioformat': 'mp3',
}

# Fila de reprodução (armazenará URLs e títulos)
queue = []
current_track = None
current_voice_client = None

# Função para buscar o link de áudio ou realizar uma busca no YouTube e obter título
def download_audio(query):
    with youtube_dl.YoutubeDL(yt_dl_options) as ydl:
        # Se o query não é um URL, faz uma busca no YouTube
        if not query.startswith("http"):
            query = f"ytsearch:{query}"
        info = ydl.extract_info(query, download=False)
        # Pega o primeiro resultado se for uma busca
        if 'entries' in info:
            info = info['entries'][0]
        return info['url'], info['title']

# Carregar o Opus
if not discord.opus.is_loaded():
    discord.opus.load_opus('/opt/homebrew/lib/libopus.dylib')

# Função para tocar o próximo item da fila
async def play_next(ctx):
    global current_track, current_voice_client

    if queue:
        current_track = queue.pop(0)  # Define a próxima música como a atual
        audio_url = current_track['url']
        title = current_track['title']
        await ctx.send(f"Tocando agora: {title}")

        current_voice_client.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
    else:
        current_track = None
        await current_voice_client.disconnect()
        current_voice_client = None
        await ctx.send("A fila terminou e o bot saiu do canal.")

# Comando #play para adicionar música à fila e iniciar a reprodução se não estiver tocando
@bot.command(name='play')
async def play(ctx, *, query: str):
    global current_voice_client

    # Obtém o URL e o título da música
    audio_url, title = download_audio(query)

    # Adiciona a música à fila (salva o título e URL)
    queue.append({"title": title, "url": audio_url})
    await ctx.send(f"Adicionado à fila: {title}")

    # Conecta ao canal se não estiver conectado
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if not current_voice_client or not current_voice_client.is_connected():
            current_voice_client = await channel.connect()
        
        # Inicia a reprodução se não estiver tocando nada
        if not current_voice_client.is_playing() and not current_voice_client.is_paused():
            await play_next(ctx)
    else:
        await ctx.send("Entre em um canal de voz primeiro!")

# Comando #pause para pausar o áudio sem desconectar
@bot.command(name='pause')
async def pause(ctx):
    if current_voice_client and current_voice_client.is_playing():
        current_voice_client.pause()
        await ctx.send("Áudio pausado.")

# Comando #resume para retomar o áudio pausado
@bot.command(name='resume')
async def resume(ctx):
    if current_voice_client and current_voice_client.is_paused():
        current_voice_client.resume()
        await ctx.send("Retomando o áudio.")

# Comando #skip para pular a música atual
@bot.command(name='skip')
async def skip(ctx):
    if current_voice_client and current_voice_client.is_playing():
        current_voice_client.stop()  # Para a música atual, o after chamará play_next
        await ctx.send("Música pulada.")

# Comando #stop para parar o áudio, limpar a fila e desconectar o bot
@bot.command(name='stop')
async def stop(ctx):
    global queue, current_track, current_voice_client
    queue.clear()  # Limpa a fila
    current_track = None

    if current_voice_client and current_voice_client.is_playing():
        current_voice_client.stop()
    
    if current_voice_client:
        await current_voice_client.disconnect()
        current_voice_client = None

    await ctx.send("A reprodução foi parada e a fila foi limpa.")

# Comando #queue para exibir a música atual e as próximas músicas na fila
@bot.command(name='queue')
async def show_queue(ctx):
    if current_track or queue:
        # Exibe a música atual
        queue_message = f"**Tocando agora:** {current_track['title']}\n\n" if current_track else "Nenhuma música tocando no momento.\n\n"

        # Exibe as próximas músicas na fila
        if queue:
            next_tracks = "\n".join([f"{i + 1}. {item['title']}" for i, item in enumerate(queue)])
            queue_message += f"**Próximas na fila:**\n{next_tracks}"
        else:
            queue_message += "A fila está vazia."

        await ctx.send(queue_message)
    else:
        await ctx.send("A fila está vazia.")

# Comando #clear para limpar a fila sem interromper a música atual
@bot.command(name='clear')
async def clear_queue(ctx):
    global queue
    queue.clear()  # Limpa a fila
    await ctx.send("A fila foi limpa.")

# Executa o bot usando o token do .env
bot.run(TOKEN)