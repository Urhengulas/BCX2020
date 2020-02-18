from flask import Flask
from authlib.integrations.flask_client import OAuth
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
    client_kwargs={'scope': 'CoffeeMaker-Control'},
    
)

homeConnect = oauth.create_client('minion-production')

@app.route('/')
def hello_world():

    return 'Hello, World!'

@app.route('/login')
def login():
    homeConnect = oauth.create_client('minion-production')
    redirect_uri = 'https://example.com'
    return homeConnect.authorize_redirect(redirect_uri)
def authorize():
    github = oauth.create_client('github')
    token = oauth.github.authorize_access_token(request)
    resp = oauth.github.get('user')
    profile = resp.json()
    # do something with the token and profile
    return '...'