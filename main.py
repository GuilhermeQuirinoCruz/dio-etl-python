from bardapi import Bard
import pandas
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
bard.get_answer("Short, one-sentence answers, I'm in a hurry, no fluff, just the facts.")
review_options = ["Terrible", "Very Bad", "Bad", "Neutral", "Ok", "Good", "Very Good", "Excellent"]
bard.get_answer(f"I'm gonna give you a list of reviews, in the format: title: [title], review: [review], rating: [rating] and I want you to answer with one of the following representing how positive it is: {[review_options]}. If you can't decide, answer '---'. Keep a consistent style when answering")

def analyze_review(title, review, rating):
    formatted_review = f"title: [{title}], review: [{review}], rating: [{rating}]"
    bard_answer = bard.get_answer(formatted_review)['content']
    analysis = bard_answer.split("\n")[0]
    return analysis

LINE_LIMIT_CSV = 50
data_frame = pandas.read_csv("chatgpt_reviews.csv", nrows=LINE_LIMIT_CSV)
reviews = data_frame.to_dict()
analyzed_reviews = []

for i in range(LINE_LIMIT_CSV):
    title = reviews["title"][i]
    review_text = reviews["review"][i]
    rating = reviews["rating"][i]
    analysis = analyze_review(title, review_text, rating)

    analyzed_reviews.append([title, review_text, rating, analysis])

data_frame_analyzed = pandas.DataFrame(analyzed_reviews, columns=["original_title", "review", "rating", "analysis"])
data_frame_analyzed.to_csv("chatgpt_analyzed_reviews.csv", index=False)