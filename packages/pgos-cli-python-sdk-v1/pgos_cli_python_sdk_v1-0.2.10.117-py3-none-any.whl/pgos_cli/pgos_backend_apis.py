# -*- coding=utf-8
# backend apis wrapper

import sys, os
import logging

import requests
import time
from datetime import datetime
import hashlib
import json

import pgos_cli.pgos_tools as pgos_tools
from pgos_cli.pgos_cmdline import GetApiProtocol, GetApiDomain
from pgos_cli.pgos_cli_config import *

# publish
kTestPrefix = 'apgz'

kApiUrlBase = "https://pgos.intlgame.com"
kEuffApiUrlBase = "https://euff.pgos.intlgame.com"

kApiHelp = '/help'
kApiLogin = '/userlogin/clilogin'
kApiBusiness = '/console/client/cmd'
kApiGlobal = '/index/client/cmd'

gCliVersion = '0.2.10' # [2024/01/26 yilungao]

gDicRegionToPrefix = {
    'dev': 'apgz',
    'test':'apgz',
    'd':'apgz',
    't':'apgz'
}

gTPrefix = {
    'test':'apgz',
    't':'apgz'
}

gDPrefix = {
    'dev': 'apgz',
    'd':'apgz',
}

gCnPrefix = {
    'apgz' : 1,
    'cnsh' : 1
}

gEvnType = {
    0: "Unknow",
    1: "d-", # dev
    2: "t-", # test
    3: ""    # publish
}

gMainHostUrl = {
    'd':'https://d-pgos.intlgame.cn',
    't':'https://t-pgos.intlgame.cn',
    'r':'https://pgos.intlgame.com'
}

def FormatApiUrl(title_region_id = '', api = '', global_host = False):
    local_code = title_region_id[: title_region_id.find('_')]
    
    protocol = GetApiProtocol()
    # core_domain = GetApiDomain()
    core_domain = ''
    suffix = ''
    prefix = ''
    evn = ''
    
    if local_code.startswith('t'):      # test evn
        evn = 't'
        core_domain = 't-pgos.intlgame'
        if local_code == 't':           # old rule's test evn
            prefix = 'apgz'
        else:                           # new rule's test evn
            prefix = local_code
        if prefix in gCnPrefix and not global_host:     # cn sub host
            suffix = 'cn'
        else:                           # main host or others
            suffix = 'com'
    elif local_code.startswith('d'):    # dev evn
        evn = 'd'
        core_domain = 'd-pgos.intlgame'
        if local_code == 'd':           # old rule's dev evn
            prefix = 'apgz'
        else:                           # new rule's dev evn
            prefix = local_code
        if prefix in gCnPrefix and not global_host:     # cn sub host
            suffix = 'cn'
        else:                           # main host or others
            suffix = 'com'
    else:                               # public evn
        evn = 'r'
        core_domain = 'pgos.intlgame'
        prefix = local_code
        if prefix in gCnPrefix and not global_host:     # cn sub host
            suffix = 'cn'
        else:                           # main host or others
            suffix = 'com'
            
    print('------')
    print(local_code)
    print(prefix)
    print(core_domain)
    print(suffix)
    print(api)


    api_url = ''
    if global_host:
        api_url = f'{gMainHostUrl[evn]}{api}'
    else:
        api_url = f'{protocol}{prefix}.{core_domain}.{suffix}{api}'
    return api_url
    
def SignToken(token):
    if token == '' or token == None:
        return ''
    hash = 5381;
    for char in token:
        hash += ((hash << 5) & 0x7fffffff) + ord(char);
    return hash & 0x7fffffff

def MakeLoginRequest():
    tr = GetConfig('title-region').split('_')
    sk = GetConfig('secret-key')

    title_id = tr[1]
    title_region_id = GetConfig('title-region')
    secret_id = sk[:sk.find('-')]
    t = int(time.time())
    secret_key = sk[sk.find('-') + 1:]
    plain_text = f'{title_id}{title_region_id}{secret_id}{t}{secret_key}'
    ticket = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
    url = FormatApiUrl(title_region_id, kApiLogin, True)

    post_body = {}
    post_body['title_id'] = title_id
    post_body['title_region_id'] = title_region_id
    post_body['t'] = t
    post_body['secret_id'] = secret_id
    post_body['ticket'] = ticket
    rsp_body = pgos_tools.HttpPost(url, post_body)

    try:
        if rsp_body['errno'] != 0:
            print('error when login to pgos backend, errmsg=%s' % rsp_body['errmsg'])
            sys.exit(-1)
        return rsp_body['data']['token']
    except Exception as e:
        print('error when parsing login rsp, e=%s' % str(e.args))

gBundledCommands = [
    'import-title-data-json-content'
]

def MakeBusinessRequest(url, command, params):
    webportaltoken = MakeLoginRequest()
    pgostoken = SignToken(webportaltoken)

    tr = GetConfig('title-region').split('_')
    title_id = tr[1]
    title_region_id = GetConfig('title-region')
    
    # some commands need bundle the params to a sub key
    post_body_params = {}
    if command in gBundledCommands:
        post_body_params['business_data'] = params
    else:
        post_body_params = params

    post_body_params['webportaltoken'] = webportaltoken
    post_body_params['pgostoken'] = pgostoken
    post_body_params['title_id'] = title_id
    post_body_params['title_region_id'] = title_region_id

    post_body = {}
    post_body['command'] = command
    post_body['params'] = post_body_params
    post_body['version'] = gCliVersion
    
    return pgos_tools.HttpPost(url, post_body)

def RequestCosSig(api, region, res_path, served_commend_name):
    root_path, file_name = os.path.split(res_path)
    url = FormatApiUrl(GetConfig('title-region'), kApiBusiness, False)

    tr = GetConfig('title-region').split('_')
    title_id = tr[1]
    title_region_id = GetConfig('title-region')
    
    webportaltoken = MakeLoginRequest()
    pgostoken = SignToken(webportaltoken)

    params = {}
    params['title_id'] = title_id
    params['title_region_id'] = title_region_id
    params['webportaltoken'] = webportaltoken
    params['pgostoken'] = pgostoken
    params['Region'] = region
    params['FileName'] = file_name
    params['CliCommand'] = served_commend_name

    post_body = {}
    post_body['command'] = api
    post_body['params'] = params
    post_body['version'] = gCliVersion


    rsp_body = pgos_tools.HttpPost(url, post_body)
    try:
        if rsp_body['errno'] != 0:
            print('error when request cos sig, errmsg=%s' % rsp_body['errmsg'])
            sys.exit(-1)
        return rsp_body['data']

    except Exception as e:
        print('error when parsing cos sig result, e=%s' % str(e.args))



