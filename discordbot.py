import discord 
import os
from discord.ext import tasks
from datetime import datetime
import random
import re
import asyncio
import sys
from func import diceroll

class ScheduleTime:
  def __init__(self, weekday, hourTime, minutesTime):
    self.Weekday = weekday
    self.HourTime = hourTime
    self.MinutesTime = minutesTime

  def edit_Weekday(self, weekday):
    self.Weekday = weekday
    pass

  def edit_HourTime(self, hourTime):
    self.HourTime = hourTime
    pass

  def edit_MinutesTime(self, minutesTime):
    self.MinutesTime = minutesTime
    pass

  def edit_AllValue(self, weekday, hourTime, minutesTime):
    self.edit_Weekday(int(weekday))
    self.edit_HourTime(int(hourTime))
    self.edit_MinutesTime(int(minutesTime))
    pass

  def is_match(firstValue, secondValue):
    if firstValue.Weekday != secondValue.Weekday :
      return False
    if firstValue.HourTime != secondValue.HourTime :
      return False
    if firstValue.MinutesTime != secondValue.MinutesTime :
      return False
    return True

#トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

#チャンネルID
CHANNEL_ID = 613341065365291010  #top
CHANNEL_ID2 = 613346606347190274 #testlog
CHANNEL_ID3 = 624496341124513793 #omikuji
CHANNEL_ID4 = 613346909154836517 #ID取得

lot_channel_id = 643070878652825601 #ここにコマンドを送るチャンネルID
lot_result_channel_id1 = 613346390092939275 #class-saxony
lot_result_channel_id2 = 613346614085419040 #class-crimean
lot_result_channel_id3 = 613346718624251944 #class-rusviet
lot_result_channel_id4 = 613346798383267841 #class-nordic

master_owner_id = 459936557432963103 or 436078064292855818

# 接続に必要なオブジェクトを生成
client = discord.Client()
DebugId = '654949655947247616'                      # コマンドなどを入力するチャンネル
DefaultId = '613346909154836517'                    # 呟くチャンネル
StartTime = ScheduleTime(0,10,0)  # 集計開始
EndTime = ScheduleTime(2,23,59)   # 集計おわり
week = ['月','火','水','木','金','土','日']
commandList = {
  '/help':0,
  '/start':3,
  '/end':3,
  '/check':1
}
part = 0
isStartSended = False
isEndSended = False

@asyncio.coroutine
def SendMsg(Channel, msg):
  print('reply = '+ msg)
  if msg != '':
    yield from client.send_message(Channel, msg)
  pass

@asyncio.coroutine
async def check_for_reminder():
  while  True:
    await asyncio.sleep(3)
    now = datetime.now()
    currentTime = ScheduleTime(now.weekday(), now.hour, now.minute)

    if ScheduleTime.is_match(StartTime, currentTime):
      global isStartSended
      global part
      if not isStartSended:
        part = 0
        StartText = '今週の活動は、{}月{}日です。\n参加する方は、リアクションをお願いします。\n投票は{}曜日に無慈悲に締め切ります。'.format(datetime.now().month, datetime.now().day + 4, week[int(EndTime.Weekday)])
        await SendMsg(DefaultChannel, StartText)
        isStartSended = True
    else:
      isStartSended = False

    if ScheduleTime.is_match(EndTime, currentTime):
      global isEndSended
      if not isEndSended:
        global part
        EndText = '今週の参加登録を締め切りました。参加人数は{}人です！！'.format(part)
        await SendMsg(DefaultChannel, EndText)
        isEndSended = True
    else:
      isEndSended = False

def botCommand(command, contents):
  SendMsg =''
  if  command not in commandList:
    return 'そんなコマンドはないよ？ /help で確認してね'
  if len(contents) != commandList[command]:
    return '要素の数がおかしいよ？もう一度確認してね！'
  if command == '/start':
    StartTime.edit_AllValue(contents[0],contents[1],contents[2])
    SendMsg = '投票開始の時間を{}曜日の{}時{}分にセットしました。'.format(week[int(contents[0])],contents[1],contents[2])
  elif command == '/end':
    EndTime.edit_AllValue(contents[0],contents[1],contents[2])
    SendMsg = '投票終わりの時間を{}曜日の{}時{}分にセットしました。'.format(week[int(contents[0])],contents[1],contents[2])
  elif command == '/check':
    if contents[0] == 'start':
      SendMsg = '投票開始時間は、{}曜日{}時{}分に設定されています。'.format(week[int(StartTime.Weekday)],StartTime.HourTime,StartTime.MinutesTime)
    elif contents[0] == 'end':
      SendMsg = '投票終了時間は、{}曜日{}時{}分に設定されています。'.format(week[int(EndTime.Weekday)],EndTime.HourTime,EndTime.MinutesTime)
    elif contents[0] == 'people':
      global part
      SendMsg = '現在の参加人数は、{}人です。'.format(part)
    else:
      SendMsg = 'コマンドを確認してね！'
    pass
  else :
    SendMsg = 'コマンドを確認してね！'
  return SendMsg

#起動メッセージ
@client.event
async def on_ready():
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')
    print('Hello World,リマインドbotプログラム「project-RRN」、起動しました')
    channel = client.get_channel(CHANNEL_ID2)
    await channel.purge()
    await channel.send(client.user.name)  # ボットの名前
    await channel.send(client.user.id)  # ボットのID
    await channel.send(discord.__version__)  # discord.pyのバージョン
    await channel.send('------')
    await channel.send('BOT再起動しました。')   
    await client.change_presence(activity=discord.Game(name='ギルド専属ナビ'))
    global DebugChannel
    global DefaultChannel
    DebugChannel = client.get_channel(DebugId)
    DefaultChannel = client.get_channel(DefaultId)
    await SendMsg(DebugChannel, 'ログインしました')
    pass

@client.event
async def on_message(message):
    """メッセージを処理"""
    if message.content.startswith("BOT再起動"): #から始まるメッセージ 
        await asyncio.sleep(7200)
        channel = client.get_channel(CHANNEL_ID2)
        await channel.send(' 2時間たちました！') 

    if message.content.startswith("23"): 
        await message.channel.send('2時間たちました！') 
    if message.content == '/setup 00':
        if message.author.guild_permissions.administrator:
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await guild_members.add_roles(role0) 
    if message.content == '/resetup 00':
        if message.author.guild_permissions.administrator:
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await guild_members.remove_roles(role0) 

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

    if message.content == 'ダイス':
        suji=random.choice(('1', '2', '3', '4', '5', '6'))
        await message.delete()
        await message.channel.send(suji) 
 
    if message.content == 'ヘルプ':
        await message.channel.send('>>> **リリナのコマンド一覧** \n \n **何時？** \n ・今の時間を教えてくれます！(何時何分何秒) \n **何日？** \n ・何日か教えてくれます！(何月何日) \n **!dice XdY** \n Y面のダイスをX回振ります！ \n \n 以下のコマンドは <#624496341124513793> で使えます。 \n **おみくじ** \n ・おみくじが引けます！ \n **運勢** \n ・貴方の運勢は！') 

#運勢
    if message.content == '運勢':
        prob = random.random()
    
        if prob < 0.3:
            await client.get_channel(CHANNEL_ID3).send('凶です……外出を控えることをオススメします')
        
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
        hensin = random.choice(('よんだ？', 'なにー？', 'たべちゃうぞー！', 'がおー！', 'よろしくね', '！？'))
        reply = f'{message.author.mention} さん' + hensin + '```\n 私の機能が分からなかったら「ヘルプ」と打ってね☆```' #返信メッセージの作成
        await message.channel.send(reply) # 返信メッセージを送信

    if message.content.startswith("赤"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.channel.id == lot_channel_id:
            role1 = discord.utils.get(message.guild.roles, name='class SAXONY')
            await message.author.add_roles(role1)
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await message.author.remove_roles(role0)
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention}さん! \n 「class-SAXONY」に参加しました。")
            await client.get_channel(lot_result_channel_id1).send(f'{message.author.mention} さんが参加しました！')
        if not message.channel.id == lot_channel_id:
            await message.delete()

    if message.content.startswith("黄"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.channel.id == lot_channel_id:
            role2 = discord.utils.get(message.guild.roles, name='class CRIMEAN')
            await message.author.add_roles(role2)
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await message.author.remove_roles(role0)
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention}さん！ \n 「class-CRIMEAN」に参加しました。")
            await client.get_channel(lot_result_channel_id2).send(f'{message.author.mention} さんが参加しました！')
        if not message.channel.id == lot_channel_id:
            await message.delete()

    if message.content.startswith("緑"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.channel.id == lot_channel_id:
            role3 = discord.utils.get(message.guild.roles, name='class RUSVIET')
            await message.author.add_roles(role3)
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await message.author.remove_roles(role0)
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention}さん! \n 「class-RUSVIET」に参加しました。")
            await client.get_channel(lot_result_channel_id3).send(f'{message.author.mention} さんが参加しました！')
        if not message.channel.id == lot_channel_id:
            await message.delete()

    if message.content.startswith("青"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.channel.id == lot_channel_id:
            role4 = discord.utils.get(message.guild.roles, name='class NORDIC')
            await message.author.add_roles(role4)
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await message.author.remove_roles(role0)
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention}さん! \n 「class NORDIC」に参加しました。")
            await client.get_channel(lot_result_channel_id4).send(f"{message.author.mention} さんが参加しました！")
        if not message.channel.id == lot_channel_id:
            await message.delete()

    if message.content.startswith("おはよ"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.author.id == master_owner_id:
            await message.channel.send('おはようございます！マスターさん！今日も一日頑張って下さい！') 
        if not message.author.id == master_owner_id:
            await message.channel.send(f"{message.author.mention} さん。おはようございます。") 

    if message.content.startswith("おやす"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.author.id == master_owner_id:
            await message.channel.send('おやすみなさい！マスターさん！今日も一日お疲れさまでした！') 
        if not message.author.id == master_owner_id:
            await message.channel.send(f"{message.author.mention} さん。おやすみなさい。") 

    if message.content.startswith("!dice"):
        # 入力された内容を受け取る
        say = message.content 

        # [!dice ]部分を消し、AdBのdで区切ってリスト化する
        order = say.strip('!dice ')
        cnt, mx = list(map(int, order.split('d'))) # さいころの個数と面数
        dice = diceroll(cnt, mx) # 和を計算する関数(後述)
        await message.channel.send(dice[cnt])
        del dice[cnt]

        # さいころの目の総和の内訳を表示する
        await message.channel.send(dice)

    if client.user == message.author:
        return
        contents = message.content.split(' ')
        bot_command = str(contents[0]).lower()
        contents = contents[1:]
        contents = [str(content) for content in contents]
        reply = botCommand(bot_command, contents)
        if message.channel.name == "bot":
            await SendMsg(message.channel, reply)
        pass

@client.event
async def on_reaction_add(reaction, user):
    global part
    if reaction.message.author == client.user:
        part += 1
        print('part = '+ str(part))
        await SendMsg(DefaultChannel, f'{user.mention} 参加登録しました。')


@client.event
async def on_reaction_remove(reaction, user):
    global part
    if reaction.message.author == client.user:
        part -= 1
        await SendMsg(DefaultChannel, f'{user.mention} 参加をキャンセルしました。')
    pass

loop = asyncio.get_event_loop()

try:
  asyncio.async(main_task())
  asyncio.async(check_for_reminder())
  loop.run_forever()
except:
  loop.run_until_complete(client.logout())
finally:
  loop.close()

@client.event
async def on_member_join(member):
    injoin = f'{member.mention} さん！いらっしゃい！ \n 私は <@511397857887125539> です！ \n 私について分からないことがありましたら、「ヘルプ」と打ってね☆'
    await client.get_channel(CHANNEL_ID4).send(member.name)
    await client.get_channel(CHANNEL_ID4).send(member.id)
    await client.get_channel(CHANNEL_ID).send(injoin)
                  
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
#
