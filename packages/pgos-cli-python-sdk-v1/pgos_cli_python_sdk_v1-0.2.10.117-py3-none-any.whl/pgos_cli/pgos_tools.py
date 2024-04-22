# -*- coding=utf-8
# tool functions

import hashlib
import requests
import time
from datetime import datetime
import json

import pgos_cli.pgos_cmdline as pgos_cmdline
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def Pretty(dict):
    return json.dumps(dict, indent=4, ensure_ascii=False)



def HashDict(dick, extra):
    sorted_keys = sorted(dick.keys())
    plain_text = ''
    for key in sorted_keys:
        plain_text += str(dick[key])
    plain_text += extra
    cipher_text = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
    # print(plain_text)
    # print(cipher_text)
    return cipher_text


def HttpPost(req_url, req_body):
    s = json.dumps(req_body)
    LogT('<< --- call REST api --- >>')
    LogT('url: ' + req_url)
    LogT('req:', True)
    LogT(Pretty(req_body), True)
    r = requests.post(req_url, json = req_body, verify = False)

    rsp_body = {}
    try:
        rsp_body = json.loads(s = r.text)
        LogT('rsp:', True)
        LogT(Pretty(rsp_body), True)
    except:
        pass

    if len(rsp_body) == 0:
        rsp_body['errno'] = 40000
        rsp_body['errmsg'] = 'Server internal error. Contact PGOS team please.'
    return rsp_body

def ErrorMsg(msg):
    print('\n\033[1;37;41m%s\033[0m' % msg)

def WarnningMsg(msg):
    print('\n\033[1;33;41m%s\033[0m' % msg)
    
def LogT(text, verbose = False):
    if verbose and not pgos_cmdline.VerboseLog():
        return
    stamp = time.time()
    time_array = time.localtime(stamp)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S  ', time_array)
    print(time_str + text + '\n')
