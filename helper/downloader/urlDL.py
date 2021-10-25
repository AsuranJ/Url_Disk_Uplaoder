#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pySmartDL import SmartDL
from pyrogram.errors import exceptions

# Importing Common Files
from helper.importCommon import *

# Importing Inbuilt Packages
from time import sleep
from os import remove, makedirs
from random import randint
from uuid import uuid4


class URLDL:

    def __init__(self, update, process_msg, bot, url) -> None:
        self.update = update
        self.process_msg_id = process_msg.message_id
        self.bot = bot
        self.url = url
        self.Downloadfolder = f'{Config.DOWNLOAD_LOCATION}{str(uuid4())}'
        print(self.Downloadfolder)
        makedirs(self.Downloadfolder)

    async def start(self):

        len_file = await length_of_file(self.bot, self.url)
        self.userid = self.update.chat.id
        if len_file == 'Valid':
            msg = await self.bot.edit_message_text(self.userid, self.process_msg_id, BotMessage.starting_to_download, parse_mode = 'html')

            downObj = SmartDL(self.url, dest = self.Downloadfolder)
            downObj.start(blocking = False)
            while not downObj.isFinished():
                progress_bar = downObj.get_progress_bar().replace('#', '■').replace('-', '□')
                completed = downObj.get_dl_size(human=True)
                speed = downObj.get_speed(human=True)
                remaining = downObj.get_eta(human=True)
                percentage = int(downObj.get_progress()*100)
                try:
                    msg = await self.bot.edit_message_text(self.userid, msg.message_id, f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage} %\n✅Completed: {completed}\n🚀Speed: {speed}\n⌚️Remaining Time: {remaining}</b>", parse_mode = 'html')
                    sleep(2)
                except exceptions.bad_request_400.MessageNotModified:
                    pass
            try:
                filename = downObj.get_dest()
            except Exception as e:
                await self.bot.send_message(Config.OWNER_ID, line_number(fileName, e))
                await self.bot.edit_message_text(self.userid, msg.message_id, BotMessage.unsuccessful_upload, parse_mode = 'html')
            else:
                if downObj.isSuccessful():
                    n_msg = await self.bot.edit_message_text(self.userid, msg.message_id, BotMessage.uploading_msg, parse_mode = 'html')
                    self.n_msg, self.filename = n_msg, filename
                    return True
                else:
                    try:
                        remove(f'{self.Downloadfolder}{filename}')
                    except Exception as e:
                        await self.bot.send_message(Config.OWNER_ID, line_number(fileName, e))
                        await self.bot.delete_messages(self.userid, msg.id)
                        await self.bot.send_message(self.userid, BotMessage.unsuccessful_upload, parse_mode = 'html')
                    finally:
                        for e in downObj.get_errors():
                            await self.bot.send_message(Config.OWNER_ID, line_number(fileName, e))
        elif len_file == 'Not Valid':
            await self.bot.edit_message_text(self.userid, self.process_msg_id, BotMessage.unsuccessful_upload, parse_mode = 'html')
        else:
            await self.bot.edit_message_text(self.userid, self.process_msg_id, f'This filesize is **{len_file}mb**. {BotMessage.file_limit}', parse_mode = 'html')

        self.filename = None
        return
