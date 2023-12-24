import requests
from Dickscord import Style
import os
from concurrent.futures import ThreadPoolExecutor
from pystyle import *
import json
import time

os.system(f"mode con: cols=170 lines=30"); os.system("title Bypass Promo Checker")

class DickcordExtension:
    def __init__(self):
        self.cookie = None

    def get_cookies(self):
        response = requests.get("https://discord.com")
        self.cookie = response.cookies.get_dict()
        self.cookie['locale'] = "us"

    def cookies(self):
        if self.cookie is None:
            print("(!): Couldn't Fetch Cookies.")
        return self.cookie

    def cookies_head(self):
        cookies_dict = self.cookies()
        return "; ".join([f"{key}={value}" for key, value in cookies_dict.items()])


class DPS:
    def __init__(self, promo_codes_file, config_file="config.json"):
        self.promo_codes_file = promo_codes_file
        self.dickcord_extension = DickcordExtension()
        self.config_file = config_file
        self.discord_token = self.load()

    def extract(self, promo_link):
        parts = promo_link.split("/partner-promotions/")
        promo_id = parts[1].split("/")[0]
        message = parts[1].split("/")[1]
        return promo_id, message
    
    def load(self):
        with open(self.config_file, "r") as config_file:
            config_data = json.load(config_file)
            return config_data.get("token")

    def send(self, promo_id, jwt_token):
        self.dickcord_extension.get_cookies()
        cookies_header = self.dickcord_extension.cookies_head()
        url = f"https://discord.com/api/v9/entitlements/partner-promotions/{promo_id}"
        headers = {
            "Authorization": self.discord_token,
            "Access-Control-Allow-Origin": "https://discord.com",
            "cookie": cookies_header,
            "Content-Type": "application/json",
            "Origin": "https://discord.com"
        }
        data = {"jwt": jwt_token}
        response = requests.post(url, headers=headers, json=data)
        return response.status_code

    def check(self, promo_code):
        promo_id, message = self.extract(promo_code)
        status_code = self.send(promo_id, message)

        if status_code == 200:
            Style.print(f"(+): VALID https://discord.com/billing/partner-promotions/{promo_id}/{message[:60]}***")
            with open("output/valid.txt", 'a')as x: x.write(f"https://discord.com/billing/partner-promotions/{promo_id}/{message}")
        else:
            Style.print(f"(-): INVALID https://discord.com/billing/partner-promotions/{promo_id}/{message[:60]}***")
            with open("output/invalid.txt", 'a')as x: x.write(f"https://discord.com/billing/partner-promotions/{promo_id}/{message}")

    def _process_(self):
        with ThreadPoolExecutor() as executor:
            with open(self.promo_codes_file, "r") as file:
                promo_codes = file.readlines()

            executor.map(self.check, promo_codes)

if __name__ == "__main__":
    os.system('cls')
    print("")
    dsn = '''
     ▄▄▄▄ ▓██   ██▓ ██▓███   ▄▄▄        ██████   ██████ 
    ▓█████▄▒██  ██▒▓██░  ██▒▒████▄    ▒██    ▒ ▒██    ▒ 
    ▒██▒ ▄██▒██ ██░▓██░ ██▓▒▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄   
    ▒██░█▀  ░ ▐██▓░▒██▄█▓▒ ▒░██▄▄▄▄██   ▒   ██▒  ▒   ██▒
    ░▓█  ▀█▓░ ██▒▓░▒██▒ ░  ░ ▓█   ▓██▒▒██████▒▒▒██████▒▒
    ░▒▓███▀▒ ██▒▒▒ ▒▓▒░ ░  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
    ▒░▒   ░▓██ ░▒░ ░▒ ░       ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒  ░ ░
     ░    ░▒ ▒ ░░  ░░         ░   ▒   ░  ░  ░  ░  ░  ░  
     ░     ░ ░                    ░  ░      ░        ░  
          ░░ ░ '''
    print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(dsn)))
    print("")
    Style.input("(#): Press Enter to start.\n")
    DPS("data/promos.txt")._process_()

    Style.input("\n(#): Finished Checking Promos.")