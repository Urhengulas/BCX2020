import json
import logging
from datetime import datetime, timedelta

import requests
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, request

from scheduler import schedule_task

# use loginpass to make OAuth connection simpler

app = Flask(__name__)
app.secret_key = "!secret"
oauth = OAuth(app)

oauth.register(
    name="minion-production",
    client_id="4289A8B8A67A243408F3166280BB7EC4AEE1090C6C867ECA38B531A6FA863DE0",
    client_secret="A556DD7D0AA6AF00B56EDC2C2AD46626B03EC94FDDEB364CCB2AE4384CC95965",
    access_token_url="https://api.home-connect.com/security/oauth/token",
    access_token_params=None,
    authorize_url="https://api.home-connect.com/security/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={
        "scope": "CoffeeMaker-Control IdentifyAppliance CoffeeMaker-Monitor CoffeeMaker-Settings"},
)
homeConnect = oauth.create_client("minion-production")


@app.route("/")
def hello_world():
    for i in range(-13, 13):
        i = 12-abs(i)
        changeLight(hex(i*21).lstrip("0x"))
    return "Hello, World!"


@app.route("/login")
def login():
    print("Hello, World!")
    redirect_uri = "http://localhost:5000/authorize"
    return homeConnect.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    token = homeConnect.authorize_access_token()

    # r = homeConnect.get("https://simulator.home-connect.com/api/homeappliances")
    status = homeConnect.get(
        "https://api.home-connect.com/api/homeappliances/SIEMENS-TI9575X1DE-68A40E357F21/status"
    )
    availablePrograms = homeConnect.get(
        "https://api.home-connect.com/api/homeappliances/SIEMENS-TI9575X1DE-68A40E357F21/programs/available")
    print(status.content)
    selectedProgram()

    # do something with the token and profile
    return redirect("/")


@app.route("/schedule", methods=["POST"])
def schedule():
    """
    Schedule a given task.

    Request object
    {
        "earliest_start_time": datetime,
        "deadline": datetime,
        "prod_time_in_min": timedelta
    }
    """
    args: dict = request.json
    try:
        earliest_start_time = datetime.strptime(
            args["earliest_start_time"],
            "%Y-%m-%d %H:%M:%S"
        )
        deadline = datetime.strptime(
            args["deadline"],
            "%Y-%m-%d %H:%M:%S"
        )
        prod_time_in_min = timedelta(minutes=int(args["prod_time_in_min"]))
    except:
        return "Wrong arguments! Did you supply {earliest_start_time: string, deadline: string, prod_time_in_min: int } ?"

    res = schedule_task(
        earliest_start_time=earliest_start_time,
        deadline=deadline,
        prod_time=prod_time_in_min
    )
    return str(res)


def makeCoffee():
    makeCoffee = homeConnect.put(
        "https://api.home-connect.com/api/homeappliances/SIEMENS-TI9575X1DE-68A40E357F21/programs/active",
        json={
            "data": {
                "key": "ConsumerProducts.CoffeeMaker.Program.Beverage.Espresso",
                "options": [
                    {
                        "key": "ConsumerProducts.CoffeeMaker.Option.BeanAmount",
                        "value": "ConsumerProducts.CoffeeMaker.EnumType.BeanAmount.Mild"
                    },
                    {
                        "key": "ConsumerProducts.CoffeeMaker.Option.FillQuantity",
                        "value": 35,
                        "unit": "ml"
                    }
                ]
            }})
    print(makeCoffee.content)
    return


def selectedProgram():
    selectedProgram = homeConnect.get(
        "https://api.home-connect.com/api/homeappliances/SIEMENS-TI9575X1DE-68A40E357F21/programs/selected"
    )
    print(selectedProgram.content)
    return


def initIOPort():
    requests.post(
        "http://192.168.1.1/TMG.htm",
        data="UDP_Packet=24.00.02.0F.0.00.0C.11.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20"
    )


def changeLight(hexvalue):
    requests.post(
        "http://192.168.1.1/TMG.htm",
        data=f"UDP_Packet=24.00.02.0B.0.{hexvalue}.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20"
    )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d - %(module)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
