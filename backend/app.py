import json
from datetime import datetime, timedelta
import requests
import time
import pandas as pd 
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect

# use loginpass to make OAuth connection simpler

app = Flask(__name__)
app.secret_key = "!secret"
oauth = OAuth(app)

data: pd.Series = pd.read_csv(
    "../data/renewData.csv",
    sep=";",
    parse_dates=["datelabel"],
    index_col="datelabel"
)

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
    initIOPort("0")
    initIOPort("2")
    
    # for i in range(-13, 13):
    #     i = 12-abs(i)
    #     time.sleep(0.025)
    #     changeStrangeLight("0",hex(i*21).lstrip("0x"))
    #     changeLight("2",hex(i*21).lstrip("0x"))
    
    changeStrangeLight("0","0")
    changeLight("2","0")
    runEnergyData(data,"2019-01-01 02:00:00","2019-01-01 23:00:00", 1)
    return 'Hello, World!'

@app.route("/login")
def login():
    redirect_uri ="http://localhost:5000/authorize"
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
    r = requests.post('http://192.168.1.1/TMG.htm', data ="UDP_Packet=24.00.02.0F." + port + ".00.0C.11.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20")


def changeLight(port, hexvalue):
    r = requests.post('http://192.168.1.1/TMG.htm', data ="UDP_Packet=24.00.02.0B." + port + "." + hexvalue + ".00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20")

def changeStrangeLight(port, hexvalue):
    r = requests.post('http://192.168.1.1/TMG.htm', data ="UDP_Packet=24.00.02.0B." + port + ".67.04.00.02.00.00."+hexvalue+".00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20")

def runEnergyData(data, start_date, job_start, job_length):
    print(data["2019-01-01 02:00:00"])

    start_date = datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S" )
    job_start = datetime.strptime(job_start,"%Y-%m-%d %H:%M:%S" )
    end_date = start_date + timedelta(days=3)
    delta = timedelta(hours=1)
    job_length = timedelta(hours= job_length)
    while start_date <= end_date:
        
        print(data[start_date.strftime("%Y-%m-%d %H:%M:%S")].values[0][0])
        changeLight("2", hex(int(data[start_date.strftime("%Y-%m-%d %H:%M:%S")].values[0][0]*2.5)).lstrip("0x"))
        if(start_date == job_start):
            print(start_date)
            changeStrangeLight("0","FF")
        if (start_date == job_start + job_length):
            print(start_date)
            changeStrangeLight("0","0")
        time.sleep(0.2)
        start_date += delta
    changeLight("2", "0")

