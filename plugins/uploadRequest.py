#!/usr/bin/env python3


"""Importing"""
# Importing Common Files
from helper.importCommon import *

# Importing Inbuilt Packages
from threading import Thread

# Importing Developer defined Module
from helper.downloader.downloader import Downloader
from helper.uploader import *


# Current File Name
fileName = 'uploadRequest'


# Some Global Variable
listThread = ['']
counter = 0



@Client.on_message(filters.private & filters.regex("^http(s)?:(.*)"))
async def upload_handler(bot, update):
    if await search_user_in_community(bot, update):
        async def task():
            a = Multitask(bot, update)
            await a.start()
        global counter
        counter += 1
        listThread.append(Thread(target = bot.loop.run(task)))
        listThread[counter].start()
    return

class Multitask:

    def __init__(self, bot, update):
        self.bot = bot
        self.update = update

    async def start(self, bot, update):
        url = update.text
        downloader = await Downloader.start(update, url, bot)
        filename = downloader.filename

        if filename:    #Sending file to user
            msg = downloader.n_msg
            message_id = update.message_id
            uploader = Upload(bot, update, msg, filename)
            await uploader.start()