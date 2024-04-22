# -*- coding=utf-8
# task to upload build

import os, sys
import traceback
import time
import json
from datetime import datetime
import platform

kCfgFileName = u'config.json'
gCfgContent = {}
gCustomCfgFile = u''

gConfigFilePath = u''

def createFolderFecursively(path):
    if not os.path.exists(path):
        createFolderFecursively(os.path.dirname(path))
        os.mkdir(path)

def getConfigFilePath():
    global gConfigFilePath
    global kCfgFileName
    if gConfigFilePath != u'':
        return gConfigFilePath
    
    current_platform = platform.system()
    if current_platform == "Darwin":
        gConfigFilePath = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'PGOSCLI', kCfgFileName)
    else:
        abspath = os.path.abspath(__file__)
        config_dir = os.path.dirname(abspath)

        if config_dir.endswith('pgos_cli'):
            config_dir = os.path.dirname(config_dir)
        if not config_dir.endswith('pgos_cli'):
            config_dir = os.path.join(config_dir, 'pgos_cli')
        gConfigFilePath = os.path.join(config_dir, kCfgFileName)

    print("gConfigFilePath:" + gConfigFilePath)
    config_dir = os.path.dirname(gConfigFilePath)
    if not os.path.exists(config_dir):
        print("gConfigFilePath not exists, create it.")
        createFolderFecursively(config_dir)
        
    return gConfigFilePath

def SetCustomCfgFile(p):
    global gCustomCfgFile
    gCustomCfgFile = p

def UpdateConfig(k, v):
    global gCfgContent
    # # path = os.path.join(os.path.dirname(os.path.abspath(__file__)), kCfgFileName
    # abspath = os.path.abspath(__file__)
    # print("[0] abspath:" + abspath)
    # dirname = os.path.dirname(abspath)
    # print("[1] dirname:" + dirname)
    # if dirname.endswith('pgos_cli'):
    #     dirname = os.path.dirname(dirname)
    # if not dirname.endswith('pgos_cli'):
    #     dirname = os.path.join(dirname, 'pgos_cli')
    # print("[2] dirname:" + dirname)
    
    # # make sure the config dir is exist[mac:pgos_cli/_internal]
    # if not os.path.exists(dirname):
    #     os.makedirs(dirname)

    # path = os.path.join(dirname, kCfgFileName)

    global gConfigFilePath
    path = getConfigFilePath()
    if not os.path.isfile(path):
        o = open(path, 'w')
        o.close()
    print("[3] path:" + path)
    
    f = open(path, 'r+', encoding='utf-8' )
    content = f.read()
    f.close()

    if len(content) > 0:
        try:
            gCfgContent = json.loads(content)
        except Exception as e:
            print(e)
    
    f = open(path, "w", encoding='utf-8' )
    gCfgContent[k] = v
    out = json.dumps(gCfgContent)
    f.write(out)
    f.close()

    print(u'configuration updated:')
    print(gCfgContent)

def GetConfig(k = u''):
    global gCfgContent
    global gCustomCfgFile

    if len(gCfgContent) == 0:
        # # path = os.path.join(os.path.dirname(os.path.abspath(__file__)), kCfgFileName)
        # # print('abspath: %s' % os.path.abspath(__file__))
        # # print('dirname: %s' % os.path.dirname(os.path.abspath(__file__)))
        # # print('path: %s' % path)
        # abspath = os.path.abspath(__file__)
        # print("[0] abspath:" + abspath)
        # dirname = os.path.dirname(abspath)
        # print("[1] dirname:" + dirname)

        # if dirname.endswith('pgos_cli'):
        #     dirname = os.path.dirname(dirname)
        # if not dirname.endswith('pgos_cli'):
        #     dirname = os.path.join(dirname, 'pgos_cli')
        # print("[2] dirname:" + dirname)

        # # make sure the config dir is exist[mac:pgos_cli/_internal]
        # if not os.path.exists(dirname):
        #     os.makedirs(dirname)

        # path = os.path.join(dirname, kCfgFileName)
        global gConfigFilePath
        path = getConfigFilePath()
        if len(gCustomCfgFile) != 0:
            path = gCustomCfgFile
        print(f'reading config from: {path}')

        if not os.path.isfile(path):
            o = open(path, 'w')
            o.close()
        f = open(path, 'r+', encoding='utf-8' )
        content = f.read()
        f.close()
        if len(content) > 0:
            try:
                gCfgContent = json.loads(content)
            except Exception as e:
                print(e)

    if k == u'':
        return gCfgContent
    if k in gCfgContent.keys():
        return gCfgContent[k]
    else:
        return u''

def GetTitleId():
    tr = GetConfig('title-region').split('_')
    return tr[1]