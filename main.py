from bardapi import Bard
import os
import requests

bard_secure_psid = ""
with open("api_key.txt") as api_file:
    bard_secure_psid = api_file.readline()

os.environ["_BARD_API_KEY"] = bard_secure_psid

session = requests.Session()
# https://github.com/dsdanielpark/Bard-API
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY"))

bard = Bard(session=session)

bard_output = bard.get_answer("Escolha um nome qualquer de pessoa")['content']
print(bard_output)

bard_output = bard.get_answer("Adicione um sobrenome e me diga o nome inteiro")['content']
print(bard_output)
