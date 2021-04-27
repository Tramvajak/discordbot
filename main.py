import discord
from discord.ext import commands
from config import settings
from discord.voice_client import VoiceClient
import hubwarframe
import youtube_dl
import os
import os.path, time, sched
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix= settings['prefix'])

@bot.event
async def on_ready():
    print('Logged in as')
    print("last modified: %s" % time.ctime(os.path.getmtime('main.py')))
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def info(ctx):
    #await ctx.message.delete()
    print(ctx.message)
    info = (
        f"{settings['prefix']}sortie - Получение информации о текущей вылазки"+
        f"\n{settings['prefix']}cambion - Деймос"+
        f"\n{settings['prefix']}trade - Баро"+
        f"\n{settings['prefix']}alert - Подарки от Лотос"+
        
        f"\n\n\nбудут еще команды, а сейчас нужно подождать"
    )
    embed=discord.Embed(title="Помощь", color=0xf27373)
    embed.add_field(name="Инфо", value=f"Префикс ( {settings['prefix']} ) - он нужен для обращения к боту.\nВремя показывает по МСК(+3)", inline=False)
    embed.add_field(name=f"Список команд:", value=str(info), inline=False)
    #embed.add_field(name="", value=f"", inline=False)
    embed.set_footer(text="Все информация берется с сайта hub.warframestat.us\n")
    await ctx.send(embed=embed)

@bot.command()
async def sortie(ctx):
    #await ctx.message.delete()
    print(ctx.message)
    warf_json = hubwarframe.get_sortie_data()
    sortie1 = warf_json['variants'][0] # 1 миссия 
    sortie2 = warf_json['variants'][1]
    sortie3 = warf_json['variants'][2]
    embed=discord.Embed(title="Вылазка :earth_americas:", color=0xf27373)
    embed.add_field(name="Фракция", value=f"{warf_json['faction']}", inline=False)
    embed.add_field(name=f"1: {sortie1['node']}", value=f"Миссия: {sortie1['missionType']}\nМодификатор: {sortie1['modifier']}\n", inline=True)#{sortie1['modifierDescription']}
    embed.add_field(name=f"2: {sortie2['node']}", value=f"Миссия: {sortie2['missionType']}\nМодификатор: {sortie2['modifier']}\n", inline=True)
    embed.add_field(name=f"3: {sortie3['node']}", value=f"Миссия: {sortie3['missionType']}\nМодификатор: {sortie3['modifier']}\n", inline=True)
    embed.add_field(name="Окончание: ", value=f"{hubwarframe.date_convert_str(warf_json['expiry'])} ({warf_json['eta']})", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def cambion(ctx):
    #await ctx.message.delete()
    warf_json = hubwarframe.get_cambion_drift_status()
    datetime1 = datetime.now() - timedelta(hours=1)
    datetime2 = hubwarframe.date_convert_date(warf_json['expiry']) + timedelta(hours=3)
    date = datetime2 - datetime1
    text = 'Время начала: '+hubwarframe.date_convert_str(warf_json['activation']) 
    text += '\nВремя окончания: '+hubwarframe.date_convert_str(warf_json['expiry'])
    hour = date.seconds//3600
    minute = (date.seconds%3600)//60 
    if hour > 0: 
        text += f'\nОсталось: :{hour}h {minute}m'
    else: 
        text += f'\nОсталось: :{minute}m'
    if warf_json['active'] == 'fass':
        text += '\nСтадия: Фэз'
    else:
        text += '\nСтадия: Воум'
    embed=discord.Embed(title="Cambion Cycle Timer",description=text, color=0xf27373)
    
    await ctx.send(embed=embed)
    
@bot.command()
async def trade(ctx):
    #await ctx.message.delete()
    print(ctx.message)
    warf_json = hubwarframe.get_void_trade()
    if warf_json['active'] == False:
        embed=discord.Embed(title="Торговец из Бездны (Work in progress)",description=f"Прибудет на {warf_json['location']} через {warf_json['startString']}",color=0xf27373)#нужно дописать товары как только он прибудет
    else: 
        item = list(warf_json['inventory'])
        embed=discord.Embed(title="Торговец из Бездны (Work in progress)",description=f"Прибыл на {warf_json['location']}",color=0xf27373)
        for i in range(len(item)):
            embed.add_field(name=f"{item[i]['item']}", value=f"ducats: {item[i]['ducats']}\ncredits: {item[i]['credits']}\n", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def wave(ctx):
    print(ctx.message)
    warf_json = hubwarframe.get_nigthwave()
    print('===================\n'+str(warf_json['activeChallenges'][0]))
    chall = list(warf_json['activeChallenges'])
    pass
    #for i in range(len(warf_json['activeChallenges'])):
    #    chall[i] = warf_json['activeChallenges'][i]

    #embed=discord.Embed(title="Вылазка :earth_americas:", color=0xf27373)
    #embed.add_field(name="Фракция", value=f"{warf_json['faction']}", inline=False)
    #embed.add_field(name=f"1: {sortie1['node']}", value=f"Миссия: {sortie1['missionType']}\nМодификатор: {sortie1['modifier']}\n", inline=False)#{sortie1['modifierDescription']}
    #embed.add_field(name=f"2: {sortie2['node']}", value=f"Миссия: {sortie2['missionType']}\nМодификатор: {sortie2['modifier']}\n", inline=False)
    #embed.add_field(name=f"3: {sortie3['node']}", value=f"Миссия: {sortie3['missionType']}\nМодификатор: {sortie3['modifier']}\n", inline=False)
    #embed.add_field(name="Окончание: ", value=f"{hubwarframe.date_convert_str(warf_json['expiry'])} ({warf_json['eta']})", inline=False)
    #await ctx.send(embed=embed)

@bot.command()
async def alert(ctx):
    warf_json = hubwarframe.get_alerts()
    if warf_json['active'] == True:
        embed=discord.Embed(title=f"Подарки от Лотос :gift:", color=0xf27373)
        mission = list(warf_json)
        for i in range(len(mission)):
            embed.add_field(name=f"{mission[i]['mission']['node']}\n{mission[i]['mission']['type']}({mission[i]['mission']['faction']}) | Level: {mission[i]['mission']['minEnemyLevel']}-{mission[i]['mission']['maxEnemyLevel']}", 
            value=f"{mission[i]['mission']['reward']['asString']}\n{mission[i]['eta']}", inline=False)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"Подарков от Лотус сейчас нету :slight_frown:", color=0xf27373)

@bot.command()
async def debug(ctx):
    if ctx.author.id == 278759892289060864: #мой id
        embed=discord.Embed(title="Debug info:", color=0x002aff)
        embed.add_field(name="Channel id: ", value=f"{ctx.channel.id}", inline=False)
        #embed.add_field(name=f"1: {sortie1['node']}", value=f"Миссия: {sortie1['missionType']}\nМодификатор: {sortie1['modifier']}\n", inline=False)#{sortie1['modifierDescription']}
        #embed.add_field(name=f"2: {sortie2['node']}", value=f"Миссия: {sortie2['missionType']}\nМодификатор: {sortie2['modifier']}\n", inline=False)
        #embed.add_field(name=f"3: {sortie3['node']}", value=f"Миссия: {sortie3['missionType']}\nМодификатор: {sortie3['modifier']}\n", inline=False)
        #embed.add_field(name="Окончание: ", value=f"{hubwarframe.date_convert_str(warf_json['expiry'])} ({warf_json['eta']})", inline=False)
        await ctx.send(embed=embed)
    else: pass

"""
@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')
    

@bot.command()
async def play(ctx,url : str):
   # voiceChannel = ctx.message.author.voice.channel
   # voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    
   # if voice == None:
   #     await voiceChannel.connect()
#
    #ydl_opts = {
   #     'format': 'bestaudio/best',
   #     'postprocessors':[{
   #         'key': 'FFmpegExtractAudio',
   #         'preferredcodec': 'mp3',
   #         'proferredquality': '192',
  #      }],
  #  }
    
    voice_channel = ctx.message.author.voice.channel
    voice_client = await voice_channel.connect()
    player = await voice_client.create_ytdl_player(url)
    player.start()
    

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("not playing")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("not paused")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    voice.stop()


@bot.command()
async def vjoin(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    await ctx.message.author.voice.channel.connect()


@bot.command()
async def vleave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    await voice.disconnect()

#@bot.command()
#async def info(ctx):
#    print(ctx.message.author.voice.channel)

@bot.command(pass_context=True)
async def con(ctx,url : str):
    voiceChannel = discord.utils.get()
"""
#print(settings['token'])
bot.run(settings['token'])
