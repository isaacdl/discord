import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
import asyncio
import pynput
from audio2text import *
from text2audio import *
from chat import *
from pynput import keyboard



    
def disconnect_after_playback(voice_client):
    def after_playback(error):
        if error:
            print(f"Error during playback: {error}")
        asyncio.run_coroutine_threadsafe(voice_client.disconnect(), bot.loop)

    return after_playback

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD = "El servidor de Esper"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
pressed_keys = []
keyboard_enabled = True
YOUR_VOICE_CHANNEL_ID = 1064981973644365977
YOUR_GUILD_ID = 1064981971773685870

# Variable para almacenar las teclas presionadas
pressed_keys = set()

# Función para detectar el atajo de teclado
def on_press(key):
    global keyboard_enabled, pressed_keys

    try:
        # Verificar si se presiona la tecla "ctrl" (izquierda o derecha)
        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            pressed_keys.add(key)

        # Verificar si también se presiona la tecla "g"
        if (
            keyboard.Key.ctrl_l in pressed_keys and
            keyboard.Key.ctrl_r in pressed_keys and
            keyboard.KeyCode.from_char('g') in pressed_keys
        ):
            keyboard_enabled = not keyboard_enabled
            print("Atajo de teclado activado" if keyboard_enabled else "Atajo de teclado desactivado")
            print("HOLA CARACOLA")
            

    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    global pressed_keys

    try:
        pressed_keys.remove(key)
    except KeyError:
        pass

    if key == keyboard.Key.esc:
        # Detener la escucha del teclado
        return False

# Escuchar eventos de teclado en segundo plano
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


# @bot.command()
# async def on_press(key):
#     global keyboard_enabled
#     global pressed_keys
#     try:
#         if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.KeyCode.from_char('g')):
#             pressed_keys.append(key)
#         if (
#             (keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys)
#             & (keyboard.KeyCode.from_char('g') in pressed_keys)
#         ):
#             print("Atajo de teclado activado" if keyboard_enabled else "Atajo de teclado desactivado")
#             keyboard_enabled = not keyboard_enabled
#         else:
#             pass
#     except Exception as e:
#         print(f"Error: {e}")

    
# @bot.command()
# async def on_release(key):
#     global pressed_keys
#     if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.KeyCode.from_char('g')):
#         # Detener la escucha del teclado
#         pressed_keys = []
#         return False

# # Escuchar eventos de teclado en segundo plano
# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()



@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    channel_dict = {}
    for channel in bot.get_all_channels():
        channel_dict[channel.name] = channel.id
    bot.channel_dict = channel_dict

@bot.event
async def on_message(message):
    # if message.author.id != bot.application_id:
    #     origin_text_channel = message.channel
    #     if is_command(message.content):
    #         if message.content.split(" ")[0] == "play":
    #             url = message.split(" ")[1]
    #             bot.audio_downloader.extract_info(url)
    #     else:
    #         if message.content.lower() == "hola":
    #             await origin_text_channel.send("Pa' ti mi cola")
    #         elif message.content.lower() == "general":
    #             channel_id = bot.channel_dict["General"]
    #             voice_channel = await bot.fetch_channel(channel_id)
    #             await origin_text_channel.send("Encendido y listo para el servicio.")
    #             return await voice_channel.connect()
    #         elif message.content.lower() == "sal":
    #             for voice_client in bot.voice_clients:
    #                 if (voice_client.guild == message.guild):
    #                     return await voice_client.disconnect()
    #             return await origin_text_channel.send("No estoy conectado a ningún canal de voz. Estás tan empanado como la Esclatusa.")
    # await bot.process_commands(message)
    if message.content.startswith('maia'):
            if message.author.voice:
                channel = message.author.voice.channel

                # Obtener el estado de voz del autor del mensaje
                voice_state = message.author.voice

                # Conectar al canal de voz del autor del mensaje
                vc = await voice_state.channel.connect()

                # Configurar la grabación de audio durante 5 segundos
                duration = 5  # Duración de la grabación en segundos
                sample_rate = 48000  # Tasa de muestreo de audio
                channels = 2  # Número de canales de audio (estéreo)

                # Iniciar la grabación de audio
                recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

                # Esperar durante la duración de la grabación
                await asyncio.sleep(duration)

                # Detener la grabación
                sd.stop()

                # Guardar la grabación en un archivo de audio
                sf.write(r'C:\Users\Isaac\Documents\Python Scripts\discord\recording.wav', recording, sample_rate)

                # Desconectar del canal de voz
                await vc.disconnect()       

                # Transcribir el audio a texto
                transcript = transcribe_audio(r'C:\Users\Isaac\Documents\Python Scripts\discord\recording.wav')

                # Escribir el texto en el canal de texto "toda-la-mierda-del-bot-aqui"
                # if transcript == "Maya pon la canción que me gusta":
                #     await message.channel.send("m!p https://www.youtube.com/watch?v=qObzgUfCl28")
                # else:
                #     await message.channel.send("No te he entendido nada hulio")

                entrada = transcript.split(" ")[2:]
                entrada = " ".join(entrada)
                if entrada == "la canción que me gusta":
                    voice_client = await message.author.voice.channel.connect()
                    voice_client.play(discord.FFmpegPCMAudio(r'C:\Users\Isaac\Documents\Python Scripts\discord\audios\ruby.mp3'))

    if message.content.startswith('gpt'):        
        if message.author.voice:
                # Obtener el canal de voz del autor del mensaje

                channel = message.author.voice.channel

                # Obtener el estado de voz del autor del mensaje
                voice_state = message.author.voice

                # Conectar al canal de voz del autor del mensaje
                vc = await voice_state.channel.connect()

                # Configurar la grabación de audio durante 5 segundos
                duration = 5  # Duración de la grabación en segundos
                sample_rate = 48000  # Tasa de muestreo de audio
                channels = 2  # Número de canales de audio (estéreo)

                # Iniciar la grabación de audio
                recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

                # Esperar durante la duración de la grabación
                await asyncio.sleep(duration)

                # Detener la grabación
                sd.stop()

                # Guardar la grabación en un archivo de audio
                sf.write(r'C:\Users\Isaac\Documents\Python Scripts\discord\recording.wav', recording, sample_rate)

                # Desconectar del canal de voz
                await vc.disconnect()       

                # Transcribir el audio a texto
                transcript = transcribe_audio(r'C:\Users\Isaac\Documents\Python Scripts\discord\recording.wav')

                # Responder utilizando chat-gpt3

                respuesta = generate_gpt3_response(transcript)
                respuestaaudio = text2audio(respuesta)
                voice_client = await message.author.voice.channel.connect()
                options = {
                'options': '-filter:a "atempo=1.5"',
                'executable': 'ffmpeg',
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            }

                future = asyncio.Future()
                voice_client.play(
                    discord.FFmpegPCMAudio(r'C:\Users\Isaac\Documents\Python Scripts\discord\text2audio.mp3', **options),
                    after=disconnect_after_playback(voice_client, future)
                )

                await future  # Esperar hasta que termine la reproducción
                await voice_client.disconnect()  # Desconectar después de la reproducción


    if message.channel.name != "musica":
        if message.clean_content.startswith('m!p'):
            await asyncio.sleep(2)
            await message.channel.send("Utiliza el puto canal de música, cojones.")
            await message.delete()
             # Expulsar al usuario 'Jockie Music#8158' del canal de voz
            username_to_find = "Jockie Music#8158"
            for member in message.guild.members:
                if str(member) == username_to_find:
                    if member.voice and member.voice.channel:
                        try:
                            await member.move_to(None)  # Move the member to None (null) voice channel
                        except discord.errors.Forbidden:
                            print("El bot no tiene permisos para expulsar usuarios del canal de voz.")
                        break  # Break the loop after finding and disconnecting the user
            # Esperar 5 segundos antes de eliminar los mensajes en el canal de texto
            await asyncio.sleep(8)
            
            # Obtiene los últimos mensajes del usuario 'Jockie Music#8158'
            messages = []
            async for msg in message.channel.history(limit=5):
                if msg.author == member:
                    messages.append(msg)

            await message.channel.delete_messages(messages)  
    if message.channel.name == "musica":
                if message.clean_content.startswith('Did you know you now get better audio'):
                    await message.delete()







@bot.command(name='suma')
async def sumar(ctx, num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    await ctx.send(num1 + num2)

@bot.command(name='troll')
async def troll(ctx):
    await ctx.send("m!p https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@bot.command(name='ruby')
async def troll(ctx):
    await ctx.send("m!p https://www.youtube.com/watch?v=qObzgUfCl28")





bot.run(TOKEN)
