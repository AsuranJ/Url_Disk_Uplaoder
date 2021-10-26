#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from mega import Mega

# Importing Common Files
from helper.importCommon import *

# Importing Inbuilt Packages
from subprocess import Popen, run
from uuid import uuid4
from os import makedirs


# Login Mega account
mega = Mega()
m = mega.login(Config.MEGA_EMAIL, Config.MEGA_PASS)


class MegaDL:

    def __init__(self, update, process_msg, bot, url):
        self.update = update
        self.process_msg_id = process_msg.message_id
        self.bot = bot
        self.url = url
        self.userid = self.update.chat.id
        self.Downloadfolder = f'{Config.DOWNLOAD_LOCATION}{str(uuid4())}'
        makedirs(self.Downloadfolder)

    async def __urlVerification(self):
        try:
            self.info = m.get_public_url_info(self.url)
            # self.info = m.get_public_url_info('https://mega.nz/file/8tJxRYjC#zaNRa7ziSV7YPmVwIsNllYqJ5iIQ0LsyGY1h8le04KI')
        except Exception as e:
            print(e)
            return
        else:
            len_file = self.info['size']
            if len_file > 419430400:   #File`s Size is more than Limit 
                await self.bot.edit_message_text(self.userid, self.process_msg_id, f'<b>This filesize is <i>{len_file}mb</i>. {BotMessage.file_limit}</b>', parse_mode = 'html')
                return
            return True

    async def start(self):
        if await self.__urlVerification():
            process = run(["megadl", self.url, "--path", self.Downloadfolder])
        return

