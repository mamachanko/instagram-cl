import multiprocessing
import os
import sys
import time
import webbrowser


from flask import Flask, request


client_id = 'c895de4e2dde4f32886ec383d6f39bd8'
redirect_uri = 'http://localhost:8642/'
config = {'client_id': client_id,
          'redirect_uri': redirect_uri}


app = Flask(__name__)


@app.route('/', methods=['GET'])
def oauth_redirect():
    # shoutout to http://stackoverflow.com/a/7866932/213000
    return (
        '<script type="text/javascript">'
        'var access_token = window.location.href.split("access_token=")[1];'
        'window.location = "/" + access_token;'
        '</script>')


@app.route('/<access_token>/', methods=['GET'])
def get_access_token_from_response(access_token):
    access_token_file = 'access_token.txt'
    with open(access_token_file, 'w') as f:
        f.write(access_token)
    return ('Your Instagram access token is now stored within %s. You can '
            'return to the shell now.' % os.path.abspath(access_token_file))


def handle_oauth_flow():
    app_kwargs = {'port': 8642, 'debug': True}
    server = multiprocessing.Process(target=app.run, kwargs=app_kwargs)
    server.start()
    browser = webbrowser.get()
    instagram_auth_url = ('https://instagram.com/oauth/authorize/'
                          '?client_id=%(client_id)s&'
                          'redirect_uri=%(redirect_uri)s&'
                          'response_type=token' % config)
    browser.open_new_tab(instagram_auth_url)
    while True:
        if os.path.exists('./access_token.txt'):
            server.terminate()
            print 'restart please :)'
            sys.exit()
        time.sleep(1)


def get_access_token():
    access_token_file = './access_token.txt'
    try:
        with open(access_token_file, 'r') as f:
            access_token = f.readline()
    except IOError:
        from oauth_app import handle_oauth_flow
        handle_oauth_flow()
    else:
        return access_token
