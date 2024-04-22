# -*- coding=utf-8
# main file
import sys, os
import getopt
import logging
import codecs
import json
import time

import pgos_cli.pgos_cmdline as pgos_cmdline
import pgos_cli.pgos_cli_config as pgos_cli_config
import pgos_cli.pgos_asset_uploader as pgos_asset_uploader
import pgos_cli.pgos_tools as pgos_tools
import pgos_cli.pgos_backend_apis as pgos_backend_apis


# @brief pgos cli python module
class PgosCliClient(object):
    # @param titleRegion: title region id, could be obtained from https://pgos.intlgame.com/
    # @param secretKey: secret key, could be obtained from https://pgos.intlgame.com/
    def __init__(self, titleRegion = None, secretKey = None):
        self.SetTitleRegion(titleRegion)
        self.SetSecretKey(secretKey)
        pgos_cmdline.InitCmdline()

    def SetTitleRegion(self, title_region):
        if title_region != None:
            pgos_cli_config.UpdateConfig('title-region', title_region)

    def SetSecretKey(self, secret_key):
        if secret_key != None:
            pgos_cli_config.UpdateConfig('secret-key', secret_key)

    def GetConfig(self):
        return pgos_cli_config.GetConfig()

    # @brief get help informatin for pgos cli
    # @param helpTarget: command name that need help information, 
    #   leave it empty to get avaliable command list of pgos cli
    def Help(self, helpTarget = None):
        _command = None
        if helpTarget == None:
            _command = pgos_cmdline.Command(
                pgos_cmdline.kCmdHelp, 
                [ pgos_cmdline.StructDataOption(pgos_cmdline.kOptionLoadJson, {'help_command': 'pgos_cli'}) ])
        else:
            _command = pgos_cmdline.Command(
                pgos_cmdline.kCmdHelp, 
                [ pgos_cmdline.StructDataOption(pgos_cmdline.kOptionLoadJson, {'help_command': helpTarget}) ])
        _params = pgos_cmdline.MergeCommandParams(_command)

        return self.__MakePgosCliRequest(command= _command.command, params= _params)

    # @brief execute a command
    # @param command_name: the command to execute
    # @param cli_load_json: pgos cli loads all parameters in batches from a JSON file or JSON string provided.
    # @param cli_upload_files: a JSON string that lists resource files to upload, 
    #   such as game build, virtual server script package, and more.
    def ExecuteCommand(self, command_name = '', cli_load_json = '{}', cli_upload_files = '[]'):
        params_json = pgos_cmdline.ParseCliJsonString(cli_load_json)
        upload_files_json = pgos_cmdline.ParseCliJsonString(cli_upload_files)

        _command = pgos_cmdline.Command( 
            command_name,
            [ 
                pgos_cmdline.StructDataOption( pgos_cmdline.kOptionLoadJson, params_json ),
                pgos_cmdline.StructDataOption( pgos_cmdline.kOptionUploadFiles, upload_files_json )
            ] 
        )

        _command = pgos_asset_uploader.PrepareResourceToUpload(_command)
        _params = pgos_cmdline.MergeCommandParams(_command)
        return self.__MakePgosCliRequest(command= _command.command, params= _params)

    def __MakePgosCliRequest(self, command = '', params = {}):
        print('executing command: ' + str(command))
        # Make request, it's may be a [help request] or a [business request]
        global_host = True if command in pgos_cmdline.kGlobalHostCommands else False
        url = pgos_backend_apis.FormatApiUrl(pgos_cli_config.GetConfig('title-region'), 
            pgos_backend_apis.kApiGlobal if global_host else pgos_backend_apis.kApiBusiness ,
            global_host)
        rsp = pgos_backend_apis.MakeBusinessRequest(url, command, params)
        return rsp