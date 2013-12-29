from arrow import Arrow
import colors

import os
import json
import multiprocessing
import requests
import webbrowser
import time
import sys

from flask import Flask, request

instagram_api = 'https://api.instagram.com/v1'
client_id = 'c895de4e2dde4f32886ec383d6f39bd8'
redirect_uri = 'http://localhost:8642/'
config = {'client_id': client_id,
          'redirect_uri': redirect_uri}


class InstagramMedia(object):

    def __init__(self, media_json):
        self.username = media_json['user']['username']
        self.created_time = Arrow.utcfromtimestamp(media_json['created_time'])

    def __repr__(self):
        params = {'class_name': type(self).__name__,
                  'username': self.username,
                  'human_time': self.created_time.humanize()}
        return u'<%(class_name)s by @%(username)s created %(human_time)s>' % params

    def coloured(self):
        params = {'class_name': type(self).__name__,
                  'username': colors.red(self.username, bg='white'),
                  'human_time': self.created_time.humanize()}
        return u'<%(class_name)s by @%(username)s created %(human_time)s>' % params



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
def get_access_token(access_token):
    access_token_file = 'access_token.txt'
    with open(access_token_file, 'w') as f:
        f.write(access_token)
    return ('Your Instagram access token is now stored within %s. You can '
            'return to the shell now.' % os.path.abspath(access_token_file))


def get_access_token():
    access_token_file = './access_token.txt'
    try:
        with open(access_token_file, 'r') as f:
            access_token = f.readline()
    except IOError:
        handle_auth_flow()
    else:
        return access_token


def handle_auth_flow():
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


def get_latest_media_raw(access_token):
    try:
        with open('./latest_media.json', 'r') as f:
            latest_media = json.load(f)
    except IOError:
        user_feed_url = instagram_api + '/users/self/feed'
        params = {'access_token': access_token}
        latest_media_response = requests.get(user_feed_url, params=params)
        latest_media = latest_media_response.json()
        with open('./latest_media.json', 'w') as f:
            json.dump(latest_media, f)
    return latest_media['data']


def get_latest_media(access_token):
    return map(InstagramMedia, get_latest_media_raw(access_token))


if __name__ == '__main__':
    access_token = get_access_token()
    latest_media = get_latest_media(access_token)
    for media in latest_media:
        print media.coloured()
