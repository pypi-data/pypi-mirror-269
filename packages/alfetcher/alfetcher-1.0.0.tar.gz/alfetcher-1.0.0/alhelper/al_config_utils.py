import os, webbrowser, platform, requests, gevent, gc
from flask import Flask, request, redirect
from gevent.pywsgi import WSGIServer
from urllib.parse import parse_qs
from .utils import utils_save_json

# Paths
script_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_path, 'config', 'config.json')

is_ssh = 'SSH_CONNECTION' in os.environ
is_displayless = 'DISPLAY' not in os.environ
is_linux = platform.system() == 'Linux'
headless_config = False
if is_linux:
    if is_ssh or is_displayless:
        headless_config = True
 
def setup_webserver():
    app = Flask(__name__)

    # Enable CORS for all routes
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response

    @app.route('/access_token') #Listen for token webhook
    def receive_token():
        def make_request(code):
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            json = {
                'grant_type': 'authorization_code',
                'client_id': global_id,
                'client_secret': global_secret,
                'redirect_uri': 'http://localhost:8888/access_token',
                'code': f'{code}'
            }
            response = requests.post('https://anilist.co/api/v2/oauth/token', json=json, headers=headers)
            return response.json()

        # Extracting query parameters from the request URL
        query = request.query_string.decode()
        params = parse_qs(query)

        # Extracting the 'code' parameter from the query
        code = params.get('code', [''])[0]

        # Do something with the code
        global access_token
        access_token = make_request(code)['access_token']
        http_server.stop()
        return redirect('https://anilist.co')
        
    def start_webserver():
        if headless_config:
           print('Open this URL in your browser: ', global_tooltip)
        else:
            print('Authentificate in the opened tab')
            webbrowser.open(global_tooltip, 0)
        http_server.serve_forever()

    http_server = WSGIServer(('127.0.0.1', 8888), app, log=None)

    return start_webserver, http_server 
        
def config_setup(print_only = False):
    setup_function, _ = setup_webserver()  # Setup the server function here
    
    def gen_please(name, help):
        return f'Please input your {name} here ({help}):\n'
    
    def get_input(prompt, data_type = str):
        while True:
            user_input = input(prompt)
            try:
                converted_input = data_type(user_input)
                return converted_input
            except ValueError:
                print("Invalid input. Please enter a valid", data_type.__name__)     
    
    def generate_api_key(client_id, client_secret):
        global global_id
        global global_secret
        global global_tooltip
        global_id = client_id
        global_secret = client_secret
        global_tooltip = f"http://anilist.co/api/v2/oauth/authorize?client_id={client_id}&redirect_uri=http://localhost:8888/access_token&response_type=code" 
        setup_function()  # Start the server here
        user_token = access_token
        gevent.killall(
            [obj for obj in gc.get_objects() if isinstance(obj, gevent.Greenlet)]
        ) #kill all gevent greenlets to prevert interference
        return user_token    
    
    config_dict = {}
    print("ONLY THE USER TOKEN WILL BE SAVED!!!!")
    print("Please create a new API client")
    if headless_config:
        if is_displayless:
            print('The setup process cannot be continued on this machine')
            print('Please SSH into this machine, set the access key as an env variable or import the config directly')
        client_id = get_input(gen_please('Anilist API Client ID',"https://anilist.co/settings/developer"))
        client_secret = get_input(gen_please('Anilist API Client Secret',f"https://anilist.co/settings/client/{client_id}"))
    else:
        webbrowser.open('https://anilist.co/settings/developer', 0)
        client_id = get_input(gen_please('Anilist API Client ID',"Paste the Client ID"))    
        client_secret = get_input(gen_please('Anilist API Client Secret',"Paste the Client Secret"))
    config_dict['anilist_user_token'] = generate_api_key(client_id, client_secret)
    if not print_only:    
        utils_save_json(config_path, config_dict)
    return config_dict