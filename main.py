import asyncio
import aiohttp
import numpy
from os import system
from getpass import getpass
from colorama import init
from json import load
from sys import path, platform
from source import day_one, discord_webhook, resolve, spoof_title, unlock

path.insert(0, "/source")

if platform == "win32":
    global clear
    clear = "cls"
else:
    clear = "clear"

init(autoreset=True)

class Achievement_Unlocker():

    def __init__(self) -> None:
        self.token = ""
        self.xuid = ""
        self.gamertag = ""
        self.gamerscore = ""
        self.amount_to_add = 0
        self.total_amount = 0
        self.title_class = Title_Management()
        self.configs = self.title_class.collect_services()
        self.resolver = resolve.Resolve_Info()
        self.settings = Configuration_Settings()
        self.discord = discord_webhook.Discord_Webhook()
        self.spoofer = spoof_title.Title_Spoofer()
        self.unlocker = unlock.Unlock_Achievements()
        self.activity = day_one.Activity_Post()
        self.send_webhook, self.webhook_url, self.webhook_username, self.webhook_avatar_url, self.webhook_embed_thumbnail, self.send_post, self.post_text = self.settings.collect_config()
    

    async def get_token(self):
        self.token = getpass(" \x1b[1;37mauthorization token: \x1b[1;37m")


    async def main(self):
        print(" \x1b[1;37m[ welcome to \x1b[1;36mX1.AU \x1b[1;37m]")

        await self.get_token()
        await asyncio.sleep(2)

        print(" \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] collecting account information..")
        self.xuid, self.gamertag, self.gamerscore = await self.resolver.get_info(self.token)
        print(f" \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] XUID: \x1b[1;36m{self.xuid} \n \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] gamertag: \x1b[1;36m{self.gamertag} \n \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] current gamerscore: \x1b[1;36m{self.gamerscore} \x1b[1;37m")
        await asyncio.sleep(2)

        self.amount_to_add = int(input(f" \x1b[1;37m[\x1b[1;35m?\x1b[1;37m] how much gamerscore  would you like to add to \x1b[1;36m{self.gamertag} \x1b[1;37m(\x1b[1;36m?\x1b[1;37m): \x1b[1;37m"))
        self.total_amount = int(self.gamerscore) + self.amount_to_add

        await asyncio.sleep(1)
        self.configs = await self.title_class.find_title(self.configs)

        if self.send_webhook is True:
            await self.discord.webhook(self.webhook_url, self.webhook_username, self.webhook_avatar_url, self.webhook_embed_thumbnail, f"new thread for {self.gamertag}", f"**gamertag:** `{self.gamertag}`\n**xuid:** `{self.xuid}`\n**starting amount:** `{self.gamerscore}`\n\n**chosen amount to add:** `{self.amount_to_add}`")

        await self.start_process()
        
        await asyncio.sleep(1)

        if self.send_post is True:
            await self.activity.post_to_feed(self.token, self.post_text, self.xuid)

        _1, _2, gamerscore = await self.resolver.get_info(self.token)
        if self.send_webhook is True:
            await self.discord.webhook(self.webhook_url, self.webhook_username, self.webhook_avatar_url, self.webhook_embed_thumbnail, f"thread for {self.gamertag} finished", f"**gamertag:** `{self.gamertag}`\n**xuid:** `{self.xuid}`\n**starting amount:** `{self.gamerscore}`\n\n**chosen amount to add:** `{self.amount_to_add}`\n**finishing amount**: `{gamerscore}`")

        print(" \x1b[1;37m[\x1b[1;32m!\x1b[1;37m] process finished!                                        ")


    async def start_process(self):
        for title in self.configs:
            _1, _2, gamerscore = await self.resolver.get_info(self.token)

            if int(gamerscore) >= self.total_amount:
                break

            else:
                title_id, service_config = title.split(":")[0], title.split(":")[1]

                status = await self.spoofer.spoof_title_id(title_id, self.token, self.xuid)
                if status is True:
                    await self.unlocker.unlock(self.token, title_id, service_config, self.xuid)
                
            await asyncio.sleep(1.5)


class Title_Management():

    @staticmethod
    def collect_services():
        with open("title_data/services.json") as service_file:
            services = load(service_file)

        services = services["title_service_configurations"]  

        return services      

    @staticmethod
    async def find_title(title_list):
        start_from = input("\x1b[1;37m [\x1b[1;33m=\x1b[1;37m] start from title: \x1b[1;36m")
        a = numpy.array(title_list)
        found = False
        index = 0
        if start_from != "":
            for t in a:
                if t.find(str(start_from)) != -1:
                    print(f"\x1b[1;37m [\x1b[1;32m!\x1b[1;37m] found title! [\x1b[1;36m{start_from}\x1b[1;37m]")
                    found = True
                    break
                else:
                    a = numpy.delete(a, index)
                index + 1
            if found is True:
                return a
            else:
                print(f"\x1b[1;37m [\x1b[1;31m!\x1b[1;37m] could not find [\x1b[1;36m{start_from}\x1b[1;37m] \x1b[1;37mstarting from beginning...")
                return title_list
        else:
            return title_list
    


class Configuration_Settings():

    @staticmethod
    def collect_config():
        with open("configuration/config.json") as configuration_file:
            settings = load(configuration_file)

        send_webhook = settings["discord"][0]["Send_Webhook_Enabled"]  
        webhook_url = settings["discord"][0]["Webhook_URL"]
        webhook_username = settings["discord"][0]["Webhook_Username"]
        webhook_avatar_url = settings["discord"][0]["Webhook_Avatar_URL"]
        webhook_embed_thumbnail = settings["discord"][0]["Webhook_Embed_Thumbnail"]

        send_post = settings["xbox_feed"][0]["Send_Day_One_Post"]
        post_text = settings["xbox_feed"][0]["Post_Text"]

        return send_webhook, webhook_url, webhook_username, webhook_avatar_url, webhook_embed_thumbnail, send_post, post_text



if __name__ == "__main__":
    system(clear)
    unlocker = Achievement_Unlocker()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(unlocker.main())
