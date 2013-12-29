from os.path import abspath

from flask import Flask, request
import requests


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
    return ('Your Instagram access token is now '
            'stored within %s' % abspath(access_token_file))


if __name__ == '__main__':
    app.run(port=8642, debug=True)
    print 123456789
