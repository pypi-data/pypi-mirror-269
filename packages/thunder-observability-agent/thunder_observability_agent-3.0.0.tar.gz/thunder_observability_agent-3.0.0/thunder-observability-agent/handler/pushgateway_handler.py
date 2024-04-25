#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
PushGateway Handler to connect and publish the data.
To use, simply 'import PushGatewayHandler' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'
import json
from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging

class PushGatewayHandler: 
    
    _logger = Logging().get_logger("PushGatewayHandler")
    _credentials=None
    _thunder=None
    _token=None
        
    def __init__(self, thunder):
        self._thunder=thunder
        self._credentials =  Utils._pushgateway_credentials
        self._token = Utils.auth_token(self._credentials.get(Constant._USERNAME), self._credentials.get(Constant._PASSWORD))
        
    def publish_metric(self, data):

        if(Utils.is_valid(data) and len(data) > 0):
            metric_data = ""
            for metric, value in data.items():
                metric = metric.replace(' ', '_').lower()
                ls = metric.split('(')
                metric_data += ls[0] + '{NAMESPACE="' + self._thunder.get(Constant._NAMESPACE) + '"' + ', PARTITION="' + self._thunder.get(Constant._PARTITION).upper() + '"' + ', HOSTNAME="' + self._thunder.get(Constant._RESOURCE_ID) + '"' + ', APPNAME="' + Constant._THUNDER + '"' + ', AGENT="' + Constant._TOA + '"' + ', JOBID="' + Utils._datetime_id + '"' + ', IP="' + (self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)) + '"'
                if len(ls) > 1:
                    ls[1] =  ', UNIT="' + ls[1].replace(')', Constant._EMPTY) + '"'
                    metric_data += ls[1]
                metric_data += '}'
                metric_data += ' ' + str(value) + '\n'
            _headers = {
                Constant._AUTHORIZATION: self._token,
                Constant._CONTENT_TYPE: Constant._TEXT_XML
            }
            response = Utils.rest_api(Constant._PUSH_GATEWAY_URL.format(Utils._config.get(Constant._PUSH_GATEWAY_HOST)), _headers, metric_data, Constant._POST, Constant._ERROR_PUSH_GATEWAY_METRIC, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if (Utils.is_valid(response)):
                self._logger.info(Constant._SUCCESS_METRIC.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(data), data))
                return Constant._SUCCESS
        else:
            self._logger.info((Constant._SKIP_METRIC).format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper()))
        return None 

    def format(self, data): 
        if isinstance(data, str):
            data = json.loads(data)
            
        for each_log in data:
            message = Constant._EMPTY
            if 'log-data' in each_log:
                message = each_log.pop('log-data')
                
            each_log = 'thunder_logs{'
            
            if len(message) > 0: 
                message = message.replace('"', '`')
                each_log += 'MESSAGE="' + message + '", '
                
            each_log += 'TIMESTAMP="' + Utils._datetime_str + '", '
            each_log += 'LOG_TYPE="' + Constant._SYSLOG + '", '
            each_log += 'APPNAME="' + Constant._THUNDER + '", '
            each_log += 'NAMESPACE="' + self._thunder.get(Constant._NAMESPACE) + '", '
            each_log += 'HOSTNAME="' + self._thunder.get(Constant._RESOURCE_ID) + '", '
            each_log += 'IP="' + (self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)) + '", '
            each_log += 'AGENT="' + Constant._TOA + '", '
            each_log += 'JOBID="' + Utils._datetime_id + '", '
            each_log += 'PRIORITY="' + Utils.priority(message) + '", '
            each_log += 'PARTITION="' + self._thunder.get(Constant._PARTITION).upper() + '" }'
            
            yield each_log

    def publish_log(self, data):
        if(len(data)>0):
            generator = self.format(data)
            logs = Constant._EMPTY
            for log in generator:
                logs += log + " 1\n"
            
            _headers = {
                Constant._AUTHORIZATION: self._token,
                Constant._CONTENT_TYPE: Constant._TEXT_XML
            }

            response = Utils.rest_api(Constant._PUSH_GATEWAY_URL.format(Utils._config.get(Constant._PUSH_GATEWAY_HOST)), _headers, logs, Constant._POST, Constant._ERROR_PUSH_GATEWAY_LOGS, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if (response):
                self._logger.info(Constant._SUCCESS_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(data)))
                return Constant._SUCCESS
        else:
            self._logger.info(Constant._SKIP_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper()))
        return None