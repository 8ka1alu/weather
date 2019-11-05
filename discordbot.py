import discord 
import os
from discord.ext import tasks
from datetime import datetime
import random
import re
import asyncio

#トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

#チャンネルID
CHANNEL_ID = 613341065365291010  #top
CHANNEL_ID2 = 613346606347190274 #testlog
CHANNEL_ID3 = 624496341124513793 #omikuji
CHANNEL_ID4 = 613346909154836517 #ID取得

# 接続に必要なオブジェクトを生成
client = discord.Client()

#起動メッセージ
@client.event
async def on_ready():
    print('Hello World,リマインドbotプログラム「project-remain」、起動しました')
    channel = client.get_channel(CHANNEL_ID2)
    await channel.purge()
    await channel.send('BOT再起動しました。')   

@client.event
async def on_message(message):
    """メッセージを処理"""
    if message.author.bot:  # ボットのメッセージをハネる
        return
    
#おみくじ
    if message.content == "おみくじ":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢は！",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[運勢] ", value=random.choice(('大吉', '中吉', '小吉', '吉', '半吉', '末吉', '末小吉', '凶', '小凶', '半凶', '末凶', '大凶')), inline=False)
        await client.get_channel(CHANNEL_ID3).send(embed=embed)
     
#運勢
    if message.content == '運勢':
        prob = random.random()
    
        if prob < 0.3:
            await client.get_channel(CHANNEL_ID3).send('凶です……外出を控えることをオススメします(  ･᷄ὢ･᷅  )')
        
        elif prob < 0.65:
            await client.get_channel(CHANNEL_ID3).send('吉です！何かいい事があるかもですね！')
        
        elif prob < 0.71:
            await client.get_channel(CHANNEL_ID3).send('末吉……どれくらい運がいいんでしょうね？•́ω•̀)?')
        
        elif prob < 0.76:
            await client.get_channel(CHANNEL_ID3).send('半吉は吉の半分、つまり運がいいのです！')
        
        elif prob < 0.80:
            await client.get_channel(CHANNEL_ID3).send('小吉ですね！ちょっと優しくされるかも？')
        
        elif prob < 0.83:
            await client.get_channel(CHANNEL_ID3).send('吉の中で1番当たっても微妙に感じられる……つまり末吉なのです( ´･ω･`)')
       
        elif prob <= 1.0:
            await client.get_channel(CHANNEL_ID3).send('おめでとうございます！大吉ですよ！(๑>∀<๑)♥')   
            
#年月日
    if all(s in message.content for s in['何日？']):
        date = datetime.now()
        await message.channel.send(f'今日は{date.year}年{date.month}月{date.day}日です！')    
    if all(s in message.content for s in ['何時？']):
        date = datetime.now()
        await message.channel.send(f'今は{date.hour}時{date.minute}分{date.second}秒だよ！')

    if client.user in message.mentions: # 話しかけられたかの判定
        reply = f'{message.author.mention} 呼んだ？' # 返信メッセージの作成
        await message.channel.send(reply) # 返信メッセージを送信
    
@client.event
async def on_member_join(member):
    await client.get_channel(CHANNEL_ID4).send(member.id)     


# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '09:00':
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('９：００です！おはようございます！今日も一日頑張りましょう！')  
    elif now == '23:00':
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('２３：００です！おやすみなさい！以降のメンションはお控え下さい。') 
#ループ処理実行
loop.start()

client.run(TOKEN)

#リリナ
#反抗期
