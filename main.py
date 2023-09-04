import pandas
import requests
import json
import openai

data_frame = pandas.read_csv("SDW2023.csv")
user_ids = data_frame["UserID"].tolist()
openai_api_key = ""
with open("api_key.txt") as api_file:
    openai_api_key = api_file.readline()

sdw2023_api_url = "https://sdw-2023-prd.up.railway.app"

def get_user(id):
    response = requests.get(f"{sdw2023_api_url}/users/{id}")
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]

# print(json.dumps(users, indent=2))

openai.api_key = openai_api_key

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role" : "system",
                "content" : "Você é um especialista em marketing bancário."
            },
            {
                "role" : "user",
                "content" : f"Crie um mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
            }
        ]
    )

    return completion.choices[0].message.content.strip("\"")

for user in users:
    # news = generate_ai_news(user)
    news = f"Faça já o seu investimento, {user['name']}"
    user["news"].append({
        "icon" : "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description" : news
    })

def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return response.status_code == 200

for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated: {success}")
