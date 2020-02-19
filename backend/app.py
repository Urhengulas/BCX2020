import json
import logging
from datetime import datetime, timedelta

import requests
import time
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, request
from flask_cors import CORS, cross_origin

from scheduler import schedule_task

# use loginpass to make OAuth connection simpler

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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
        time.sleep(0.025)
        changeStrangeLight("0", hex(i*21).lstrip("0x"))
        changeLight("2", hex(i*21).lstrip("0x"))
    # initIOPort("0")
    # initIOPort("2")
    # changeStrangeLight("0","FF")
    # changeLight("2","7F")
    return 'Hello, World!'


@app.route("/login")
def login():
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
@cross_origin()
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
    a = {"start_time": str(res)}
    print("a=", a)
    return a


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


def initIOPort(port):
    r = requests.post('http://192.168.1.1/TMG.htm', data="UDP_Packet=24.00.02.0F." + port +
                      ".00.0C.11.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20")


def changeLight(port, hexvalue):
    r = requests.post('http://192.168.1.1/TMG.htm', data="UDP_Packet=24.00.02.0B." + port + "." + hexvalue +
                      ".00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20")


def changeStrangeLight(port, hexvalue):
    r = requests.post('http://192.168.1.1/TMG.htm', data="UDP_Packet=24.00.02.0B." + port +
                      ".67.04.00.02.00.00."+hexvalue+".00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20")


def changeLight(hexvalue):
    requests.post(
        "http://192.168.1.1/TMG.htm",
        data=f"UDP_Packet=24.00.02.0B.0.{hexvalue}.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20"
    )
