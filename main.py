from bardapi import Bard
import os

bard_secure_psid = ""
with open("api_key.txt") as api_file:
    bard_secure_psid = api_file.readline()

os.environ["_BARD_API_KEY"] = bard_secure_psid

bard_output = Bard().get_answer("Escolha um nome qualquer de pessoa")['content']
print(bard_output)