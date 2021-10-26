#!/usr/bin/env python3


"""Importing"""
# Importing Inbuilt Packages
from re import match
from helper.downloader.megaDL import MegaDL

# Importing Developer defined Module
from helper.downloader.urlDL import *


class Downloader:

    def __init__(self, update, url, bot):
        self.update = update
        self.url = url
        self.bot = bot
    
    @classmethod
    async def start(cls, update, url, bot):
        self = cls(update, url, bot)
        process_msg = await update.reply_text(BotMessage.processing_url, parse_mode = 'html')
        if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', url):
            await self.update.reply_text(BotMessage.youtube_url, parse_mode = 'html')
        elif 'mega.nz' in url:
            if ("folder" or "#F" or "#N") not in url:
                megadownOBJ = MegaDL(update, process_msg, bot, url)
                await megadownOBJ.start()
            else:
                await self.update.reply_text(BotMessage.megaFolder, parse_mode = 'html')
        else:   #Normal Url
            urldownOBJ = URLDL(update, process_msg, bot, url)
            await urldownOBJ.start()
            if urldownOBJ.filename:
                self.n_msg = urldownOBJ.n_msg
            self.filename = urldownOBJ.filename
            self.downloadFolder = urldownOBJ.Downloadfolder
        return self

    