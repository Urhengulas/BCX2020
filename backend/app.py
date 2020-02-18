from flask import Flask, redirect
import requests
from authlib.integrations.flask_client import OAuth
import json
# use loginpass to make OAuth connection simpler

app = Flask(__name__)
app.secret_key = '!secret'
oauth = OAuth(app)

oauth.register(
    name='minion-production',
    client_id='4289A8B8A67A243408F3166280BB7EC4AEE1090C6C867ECA38B531A6FA863DE0',
    client_secret='A556DD7D0AA6AF00B56EDC2C2AD46626B03EC94FDDEB364CCB2AE4384CC95965',
    access_token_url='https://api.home-connect.com/security/oauth/token',
    access_token_params=None,
    authorize_url='https://api.home-connect.com/security/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'CoffeeMaker-Control IdentifyAppliance CoffeeMaker-Monitor CoffeeMaker-Settings'},
    
)

homeConnect = oauth.create_client('minion-production')

@app.route('/')
def hello_world():
    for i in range(13, -13, -1):
        i = abs(i)
        changeLight(hex(i*21).lstrip("0x"))
    return 'Hello, World!'

@app.route('/login')
def login():
    print('Hello, World!')
    redirect_uri ="http://localhost:5000/authorize"
    return homeConnect.authorize_redirect(redirect_uri)
    

@app.route('/authorize')
def authorize():
    token = homeConnect.authorize_access_token()
    
    #r = homeConnect.get('https://simulator.home-connect.com/api/homeappliances')
    status = homeConnect.get("https://api.home-connect.com/api/homeappliances/SIEMENS-TI9575X1DE-68A40E357F21/status")
    availablePrograms = homeConnect.get('https://api.home-connect.com/api/homeappliances/SIEMENS-TI9575X1DE-68A40E357F21/programs/available')
    print(status.content)
    selectedProgram()
    


    # do something with the token and profile
    return redirect('/')

def makeCoffee():
    makeCoffee = homeConnect.put('https://api.home-connect.com/api/homeappliances/SIEMENS-TI9575X1DE-68A40E357F21/programs/active', json={"data":{
        "key":"ConsumerProducts.CoffeeMaker.Program.Beverage.Espresso",
        "options":[
            {
                "key":"ConsumerProducts.CoffeeMaker.Option.BeanAmount",
                "value":"ConsumerProducts.CoffeeMaker.EnumType.BeanAmount.Mild"
            },
            {
                "key":"ConsumerProducts.CoffeeMaker.Option.FillQuantity",
                "value":35,
                "unit":"ml"
            }
        ]
    }})
    print(makeCoffee.content)
    return

def selectedProgram():
    selectedProgram = homeConnect.get("https://api.home-connect.com/api/homeappliances/SIEMENS-TI9575X1DE-68A40E357F21/programs/selected")
    print(selectedProgram.content)
    return

def initIOPort():
    r = requests.post('http://192.168.1.1/TMG.htm', data ="UDP_Packet=24.00.02.0F.0.00.0C.11.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20")


def changeLight(hexvalue):
    r = requests.post('http://192.168.1.1/TMG.htm', data ="UDP_Packet=24.00.02.0B.0."+hexvalue+".00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.20.20")

