#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Splunk Handler to connect and publish the data.
To use, simply 'import SplunkHandler' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'
import json
from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging

class SplunkHandler:
    
    _logger = Logging().get_logger("SplunkHandler")
    _credentials=None
    _thunder=None
    
        
    def __init__(self, thunder):
        self._thunder=thunder
        self._credentials =  Utils._splunk_credentials 

    def publish_metric(self, data):
        namespace=Constant._EMPTY
        tempData = dict(data)
        if Utils.is_valid(tempData) and len(tempData) > 0:
            tempData["NAMESPACE"] = self._thunder.get(Constant._NAMESPACE)
            tempData["APPNAME"] = Constant._THUNDER
            tempData["AGENT"] = Constant._TOA
            tempData["JOBID"] = Utils._datetime_id
            tempData["HOSTNAME"]  = self._thunder.get(Constant._RESOURCE_ID)
            tempData["PARTITION"] = self._thunder.get(Constant._PARTITION).upper()
            tempData["IP"]        = self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)
            body = {
                "time": Utils._datetime_epoc,
                "event": tempData
            }
            token = "Splunk " + self._credentials.get(Constant._SPLUNK_TOKEN_METRICS)
            ip = self._thunder.get(Constant._IP) if Utils.is_valid(self._thunder.get(Constant._IP)) else Constant._EMPTY
            namespace = self._thunder.get(Constant._NAMESPACE).upper() if Utils.is_valid(self._thunder.get(Constant._NAMESPACE)) else Constant._EMPTY
            if ip is None:
                ip = Constant._EMPTY
            response = Utils.rest_api((Constant._SPLUNK_BASE_URL).format(Utils._config.get(Constant._SPLUNK_HOST)),{"Authorization":token},json.dumps(body),Constant._POST,Constant._ERROR_SPLUNK_METRIC,ip + " [" + namespace + "]")
            if Utils.is_valid(response):
                self._logger.info(Constant._SUCCESS_METRIC.format(self._thunder.get(Constant._IP),namespace,len(data),data))
                return Constant._SUCCESS
        else:
            self._logger.info((Constant._SKIP_METRIC).format(self._thunder.get(Constant._IP),namespace))
        return None
    

    def format(self, data): 
        if isinstance(data, str):
            data = json.loads(data)
        for each_log in data:
            if 'log-data' not in each_log:
                pass
            else:
                each_log['text'] = each_log.pop('log-data')
            each_log['LOG_TYPE']= Constant._SYSLOG
            each_log['APPNAME']= Constant._THUNDER
            each_log['HOSTNAME']= self._thunder.get(Constant._RESOURCE_ID)
            each_log['IP'] = self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)
            each_log['AGENT'] = Constant._TOA
            each_log['JOBID'] = Utils._datetime_id
            each_log['NAMESPACE'] = self._thunder.get(Constant._NAMESPACE)
            each_log['PRIORITY'] = Utils.priority(each_log['text'])
            each_log['TIME']= Utils._datetime_epoc
            each_log['PARTITION'] = self._thunder.get(Constant._PARTITION).upper()
            yield each_log



    def publish_log(self, data):
        if len(data) > 0:
            generator = self.format(data)
            logs = list(generator)
            if logs:
                body = {
                "event": logs
                }
                ip = self._thunder.get(Constant._IP)
                namespace = self._thunder.get(Constant._NAMESPACE)
                ip_namespace = f"{ip} [{namespace}]" if ip and namespace else Constant._EMPTY
                response = Utils.rest_api((Constant._SPLUNK_BASE_URL).format(Utils._config.get(Constant._SPLUNK_HOST)),Utils.get_headers((Constant._EMPTY).join(['Splunk ', self._credentials.get(Constant._SPLUNK_TOKEN_LOG)])),json.dumps(body),Constant._POST,Constant._ERROR_SPLUNK_LOG,ip_namespace)

                if response:
                    self._logger.info(Constant._SUCCESS_LOG.format(self._thunder.get(Constant._IP),self._thunder.get(Constant._NAMESPACE).upper() if self._thunder.get(Constant._NAMESPACE) else Constant._EMPTY,len(data)))
                    return Constant._SUCCESS
        else:
            self._logger.info(Constant._SKIP_LOG.format(self._thunder.get(Constant._IP),self._thunder.get(Constant._NAMESPACE).upper() if self._thunder.get(Constant._NAMESPACE) else Constant._EMPTY))

        return None