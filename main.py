from flask import Flask, request, jsonify, render_template, redirect, url_for
import asyncio
from datetime import datetime
import requests
import os

# https://6687397b0bc7155dc016ffe0.mockapi.io/api/v1/top-spenders

def get_data():
    response = requests.get("https://6687397b0bc7155dc016ffe0.mockapi.io/api/v1/top-spenders")
    return response.json()


# def update_data(top_spenders, last_updated):
#     response = requests.put("https://6687397b0bc7155dc016ffe0.mockapi.io/api/v1/top-spenders/1",
#                             data={"spender-names": top_spenders, "last-updated": last_updated})
#     return response.json()

app = Flask(__name__)

data = []
last_updated = ""


@app.route("/")
def index():
    # convert %Y-%m-%d %H:%M:%S to 10 minutes ago
    global last_updated

    # if last_updated is empty, redirect to get-data
    if not last_updated:
        return redirect(url_for('get_latest_data'))

    print(last_updated)

    last_updated = datetime.strptime(str(last_updated), "%Y-%m-%d %H:%M:%S")
    min_ago = datetime.now() - last_updated
    min_ago = min_ago.total_seconds() / 60
    min_ago = round(min_ago)
    min_ago = f"{min_ago} minutes ago"

    super_heroes = [
        "Superman",
        "Captain America",
        "Hulk",
        "Spider-Man",
        "Batman",
        "Daredevil",
        "Wolverine",
        "Cyborg",
        "Aqua man",
        "Green Lantern"]

    return render_template('index.html', data=data, last_updated=min_ago, super_heroes=super_heroes)



@app.route("/get-data")
def get_latest_data():
    latest_data = get_data()
    print(latest_data)
    data.clear()
    data.extend(latest_data[0]["spender-names"])

    global last_updated
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return redirect(url_for('index'))


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, port=os.getenv("PORT", default=5000))