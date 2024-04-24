################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Kalo Pake Ini Kode Minimal Cantumkan Credits . Gw Boleh Mikir Juga Anjing, Meski Liat Ultroid
"""
################################################################


import asyncio
from .class_log import LOGGER
from .database import ndB
from Mix import nlx
from random import randint
from os import execvp
from sys import executable
import wget
import random



async def autobot():
    LOGGER.info("MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather, Mohon Tunggu")
    gw = nlx.me
    name = gw.first_name + " Asisstant"
    if gw.username:
        username = gw.username + "_bot"
    else:
        username = "mix_" + (str(gw.id))[5:] + "_bot"
    bf = "@BotFather"
    await nlx.unblock_user(bf)
    await nlx.send_message(bf, "/start")
    await asyncio.sleep(1)
    await nlx.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, "Alright, a new bot.", limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone is None or "20 bots" in isdone:
        LOGGER.error(
            "Tolong buat Bot dari @BotFather dan tambahkan tokennya di BOT_TOKEN, sebagai env var dan mulai ulang saya."
        )
        import sys

        sys.exit(1)
    await nlx.send_message(bf, name)
    await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Good."):
        await nlx.send_message(bf, username)
    await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "mix_" + (str(gw.id))[6:] + str(ran) + "_bot"
        await nlx.send_message(bf, username)
        await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
         isdone = None
    token = None
    for k in isdone.split("HTTP API:"):
      token = k.split("\n")[1]
    if token:
        ndB.set_key("BOT_TOKEN", token)
        LOGGER.info(
            f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
        )
        await enable_inline(username)
    else:
        LOGGER.info(
            "Harap Hapus Beberapa bot Telegram Anda di @Botfather atau Setel Var BOT_TOKEN dengan token bot"
        )
        import sys
        sys.exit(1)
        
async def enable_inline(username):
    pp = random.choice(["https://telegra.ph//file/19b336da463a05d7d8f8c.jpg", "https://telegra.ph//file/2eaf853d09c319465a8f4.jpg", "https://telegra.ph//file/7d2e8f0ae636e2f6dc381.jpg"])
    bb = wget.download(pp)
    LOGGER.info(f"Menyesuaikan Bot Asisten di @BotFather")
    bf = "BotFather"
    await nlx.send_message(bf, "/setuserpic")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await nlx.send_photo(bf, bb)
    await asyncio.sleep(1)
    await nlx.send_message(bf, "/setabouttext")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"Mix-Userbot Asisten My Owner : @{nlx.me.first_name}")
    await asyncio.sleep(2)
    await nlx.send_message(bf, "/setdescription")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"Powerful Mix-Userbot Assistant\nMy Owner : @{nlx.me.first_name}\n\nPowered By ~ @KynanSupport")
    await asyncio.sleep(2)
    await nlx.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await nlx.send_message(bf, "Search")
    LOGGER.info("Customisation Done")
    execvp(executable, [executable, "-m", "Mix"])