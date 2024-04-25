#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT

"""
Configure logging framework and logs asynchronously thread processes.
To use, simply 'import logging' and log away!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

import logging.config
from common.toa_constant import Constant 

class Logging:

    __instance__ = None 
    
    @staticmethod
    def get_logger(className):
        if Logging.__instance__ is None:
            for name in ['boto', 'urllib3', 's3transfer', 'boto3', 'botocore', 'nose']:
                logging.getLogger(name).setLevel(logging.CRITICAL)
            logging.config.fileConfig(fname=Constant._LOGGING_CONF_PATH)
            Logging.__instance__ = logging
        return Logging.__instance__.getLogger(className)