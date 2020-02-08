import discord
import urllib.request
import json
import re
import os

#トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()

citycodes = {
    "土浦": '080020',
    "水戸": '080010',
    "札幌": '016010',
    "仙台": '040010',
    "東京": '130010',
    "横浜": '140010',
    "名古屋": '230010',
    "大阪": '270000',
    "広島": '340010',
    "福岡": '400010',
    "鹿児島": '460010',
    "那覇": '471010'
}

taio = "札幌、仙台、土浦、水戸、東京、横浜、名古屋、大阪、広島、福岡、鹿児島、那覇"

@client.event
async def on_ready():
  print("logged in as " + client.user.name)
  await client.change_presence(status=discord.Status.idle,activity=discord.Game(name='創成の女神'))


@client.event
async def on_message(message):
  if message.content == "対応都市":
     await message.channel.send(taio)

  if message.author != client.user:

    reg_res = re.compile(u"ノア、(.+)の天気は？").search(message.content)
    if reg_res:

      if reg_res.group(1) in citycodes.keys():

        citycode = citycodes[reg_res.group(1)]
        resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
        resp = json.loads(resp.decode('utf-8'))

        msg = resp['location']['city']
        msg += "の天気は、\n"
        for f in resp['forecasts']:
          msg += f['dateLabel'] + "が" + f['telop'] + "(" +  f['date'] + ")\n"
        msg += "です。\n\n```"
        msg += resp['description']['text'] + "```"

        await message.channel.send(message.author.mention + msg)

      else:
        await message.channel.send("そこの天気はわかりません...")

client.run(TOKEN)
