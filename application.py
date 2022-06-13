from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

#set API_KEY with 'export API_KEY=your_key
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

#include helper function for API call
def getCat(amount):
    #contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f'https://api.thecatapi.com/v1/images/search?limit={amount}&size=medium'
        headers = {'x-api-key': api_key}
        response = requests.get(url, headers = headers)
        response.raise_for_status()
    except requests.RequestException:
        return None

    #get url(s) of cat picture(s)
    try:
        cat_url = response.json()
        cat = []
        for elem in cat_url:
            cat.append(elem['url'])
        return cat

    except (KeyError, TypeError, ValueError):
        return None

@app.route('/')
def homepage():
    cat_url = getCat(1)
    return render_template("index.html", cat_url = cat_url)

@app.route('/cat')
def cat():
    amount = request.args.get("amount")
    print(amount)
    cat_url = getCat(amount)
    return render_template("cat.html", cat_url = cat_url)