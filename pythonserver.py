#!/usr/bin/env python
import codecs
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
#import authpython
import codecs
import json
import authpython

ip = '127.0.0.1'
port = 8000


'''
requests.put(url, data="
{
fleet_id: 000000,
new_settings: {}




")
'''

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        path = self.path  # path = 'http://127.0.0.1:8000/callback/?code=someString&state=someOtherString'

        params = parse.urlparse(path).query  # get params string
        self.handle_one_request()
        countflag = 0
        for param in params.split('&'):
            if param.startswith('code=') and countflag == 0:
                authorisetoken = param[5:]  # get everything after the 5th character: =
                pw = authpython.authorize(authorisetoken)
                print(pw['access_token'])


                #mp = authpython.refresh(pw['token_id'],pw['refresh_token'])

                #reader = codecs.getreader("utf-8")
                #jpw = json.load(reader(pw))
                #token_id_var = jpw["access_token"]
                #refresh_id_var = jpw["refresh_token"]
                #print(pw['token_id'])


                file_1_write = open("keys.key","w")
                file_1_write.write("%s %s" % (pw['access_token'],pw['refresh_token']))
                #file_1_write.write("%s %s" % (pw['token_id'],pw['refresh_id']))
                file_1_write.close()
                countflag = 1


        #print(mp)
                #print(mp)


                #reader = codecs.getreader("utf-8")
                #jpw = json.load(reader(pw))
                #print(pw.access_token)
                #authpython.verify(jpw['access_token'],jpw['token_type'])


        # Send response status code
        self.send_response(200)
        return


def run():
    redirect_uri = 'http://localhost:8000/callback/'
    client_id = '4d76436f1f6748b89e03ebe8d633dc3d'
    scope = 'esi-fleets.read_fleet.v1 esi-fleets.write_fleet.v1 esi-fittings.read_fittings.v1'
    state = ''

    parameters = '&'.join([
        'response_type=code',
        'redirect_uri=' + parse.quote(redirect_uri),
        'client_id=' + parse.quote(client_id),
        'scope=' + parse.quote(scope),
        'state=' + parse.quote(state),
    ])

    sso_url = 'https://login.eveonline.com/oauth/authorize?' + parameters



    #authorisetoken = 'BE3uIJnC8R0moL9eM8v-9_jMIWv719AGfzJWnJV8I-OXq0GX_pmr91JqbzH-QIqi0'
    #pw = authpython.authorize(authorisetoken)
    #print(pw)

    print('\nSSO Login URL: ' + sso_url)

    print('\nstarting server...')
    count = 1
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = (ip, port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    while count>0:
        httpd.handle_request()
        count = count - 1
        print("Request handled")

