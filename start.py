import os
from disnake import Intents
from disnake.errors import ClientException
from dotenv import load_dotenv
from disnake.ext.commands import Bot, Context
from modules.ttsmodule import save_tts_file, LanguageCode
import secrets

load_dotenv()
gttsfile = os.getenv('gttsjsonfile')
gttsfile = os.path.abspath(__file__) + '/' + gttsfile
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gttsfile
del(gttsfile)

bot = Bot(command_prefix="'", help_command=None, Intents=Intents.all())

@bot.event
async def get_tts_message(ctx: Context):
    if ctx.author.bot == False and ctx.message.content[0] == "'":
        messagecontent = ctx.message.content
        messagelang = LanguageCode.english
        if messagecontent[1:8] == "english":
            messagecontent = messagecontent[9:]
        elif messagecontent[1:7] == "korean":
            messagecontent = messagecontent[8:]
            messagelang = LanguageCode.korean
        elif messagecontent[1:9] == "japanese":
            messagecontent = messagecontent[10:]
            messagelang = LanguageCode.japanese
        else:
            return

    try:
        voicechannel = ctx.author.voice.channel
    except AttributeError:
        await ctx.send("Can't find VoiceChannel, Do you join the voice channel?")
    else:
        try:
            voiceclient = await voicechannel.connect()
        except ClientException:
            voiceclient = ctx.voice_client
        name = f"output-{ctx.author.id}-{secrets.SystemRandom().randint(1, 10000)}.mp3"
        save_tts_file(messagecontent, name, messagelang)
        if voiceclient.is_playing is True:
            await ctx.send("tts currently playing")
        else:
            await voiceclient.play(name)