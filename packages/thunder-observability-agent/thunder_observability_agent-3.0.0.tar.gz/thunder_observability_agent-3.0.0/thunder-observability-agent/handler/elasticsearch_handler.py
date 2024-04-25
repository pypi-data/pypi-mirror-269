#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
ElasticSearch Handler to connect and publish the data.
To use, simply 'import ElasticSearchHandler' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'
import json
from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging

class ElasticSearchHandler:
    
    _logger = Logging().get_logger("ElasticSearchHandler")
    _credentials=None
    _thunder=None
    _token=None
        
    def __init__(self, thunder):
        self._thunder=thunder
        self._credentials =  Utils._es_credentials
        self._token = Utils.auth_token(self._credentials.get(Constant._USERNAME), self._credentials.get(Constant._PASSWORD))
        
    def publish_metric(self, data):

        if(Utils.is_valid(data) and len(data) > 0):
            tempData = dict(data)
            metric_data = Constant._EMPTY
            tempData["NAMESPACE"] = self._thunder.get(Constant._NAMESPACE)
            tempData["APPNAME"] = Constant._THUNDER
            tempData["AGENT"] = Constant._TOA
            tempData["JOBID"] = Utils._datetime_id
            tempData["HOSTNAME"]  = self._thunder.get(Constant._RESOURCE_ID)
            tempData["PARTITION"] = self._thunder.get(Constant._PARTITION).upper()
            tempData["IP"]        = self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)
            tempData["TIMESTAMP"] = Utils._datetime_str
            metric_data += json.dumps({ 'index' : { '_index' : 'thunder-metrics'} }) + "\n"
            metric_data += json.dumps(tempData) + "\n"
            response = Utils.rest_api(Constant._ES_METRIC_URL.format(Utils._config.get(Constant._ES_HOST)), Utils.get_headers(self._token), metric_data, Constant._POST, Constant._ERROR_ES_METRIC, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
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
            if 'log-data' not in each_log:
                pass
            else:
                each_log['message'] = each_log.pop('log-data')
                each_log["TIMESTAMP"] = Utils._datetime_str
                each_log["LOG_TYPE"]  = Constant._SYSLOG
                each_log['NAMESPACE'] = self._thunder.get(Constant._NAMESPACE)
                each_log["APPNAME"]   = Constant._THUNDER
                each_log["HOSTNAME"]  = self._thunder.get(Constant._RESOURCE_ID)
                each_log["IP"]        = self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)
                each_log["AGENT"]     = Constant._TOA
                each_log["JOBID"]     = Utils._datetime_id
                each_log["PRIORITY"]  = Utils.priority(each_log['message'])
                each_log["PARTITION"] = self._thunder.get(Constant._PARTITION).upper()
            yield each_log

    def publish_log(self, data):
        
        if(len(data)>0):
            generator = self.format(data)
            logs = Constant._EMPTY
            for log in generator:
                logs += json.dumps({ 'index' : { '_index' : 'thunder-logs'} }) + "\n"
                logs += json.dumps(log) + "\n"
            
            response = Utils.rest_api(Constant._ES_LOG_URL.format(Utils._config.get(Constant._ES_HOST)), Utils.get_headers(self._token), logs, Constant._POST, Constant._ERROR_ES_LOGS, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if (response):
                self._logger.info(Constant._SUCCESS_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(data)))
                return Constant._SUCCESS
        else:
            self._logger.info(Constant._SKIP_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper()))
        return None