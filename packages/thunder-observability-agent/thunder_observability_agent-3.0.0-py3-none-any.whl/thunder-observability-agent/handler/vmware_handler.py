#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
VMWare Handler to connect and publish the data.
To use, simply 'import VMWareHandler' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com); Vikas (vgautam@a10networks.com)'


import json
from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging

class VMWareHandler:
    
    _logger = Logging().get_logger("VMWareHandler")
    _credentials=None
    _thunder=None
    _token=None
    _url=None
        
    def __init__(self, thunder, token):
        self._thunder=thunder
        self._credentials =  Utils._vmware_credentials 
        self._token=token
 
    def token(self):
        _body = json.dumps({
                Constant._USERNAME: self._credentials.get(Constant._VMWARE_VROPS_USERNAME),
                Constant._PASSWORD: self._credentials.get(Constant._VMWARE_VROPS_PASSWORD)
        })
        _headers = {
            Constant._CONTENT_TYPE: Constant._APPLICATION_JSON,
            Constant._ACCEPT: Constant._APPLICATION_JSON 
        }
        response = Utils.rest_api((Constant._VMWARE_BASE_URL+"/auth/token/acquire").format(Utils._config.get(Constant._VMWARE_VROPS_HOST)), _headers, _body, Constant._POST, Constant._ERROR_VMWARE_AUTH_RESPONSE, self._thunder.get(Constant._IP))
        self._token = response.json()['token']
        return self._token
        
    def publish_metric(self, data):

        
        if(Utils.is_valid(data) and len(data) > 0):
            adaptor = "ThunderAdaptor"
            metric_data = {"stat-content": []}
            for metric in data:
                metric_dir = {
                    "statKey": self._thunder.get(Constant._NAMESPACE) +"|%s" % metric,
                    "timestamps": [Utils._datetime_epoc],
                    "data": [data[metric]]
                }
                metric_data['stat-content'].append(metric_dir)
            response = Utils.rest_api((Constant._VMWARE_BASE_URL+"/resources/{}/stats/adapterkinds/{}").format(Utils._config.get(Constant._VMWARE_VROPS_HOST), self._thunder.get(Constant._RESOURCE_ID), adaptor), Utils.get_headers(''.join(['vRealizeOpsToken ', self._token])), json.dumps(metric_data), Constant._POST, Constant._ERROR_VMWARE_VROPS_METRIC, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if (Utils.is_valid(response)):
                self._logger.info(Constant._SUCCESS_METRIC.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(data), data))
                return Constant._SUCCESS
        else:
            self._logger.info((Constant._SKIP_METRIC).format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper()))
        return None 
    
    def format(self, data): 
        if isinstance(data, str):
            data = json.loads(data)

        # replace key log-data with text
        # add meta data to search logs on vRLI UI
        for each_log in data:
            if 'log-data' not in each_log:
                pass
            else:
                each_log['text'] = each_log.pop('log-data')
            each_log['fields'] = [
                {
                    "name": "LOG_TYPE",
                    "content": Constant._SYSLOG
                },
                {
                    "name": "APPNAME",
                    "content": Constant._THUNDER
                },
                {
                    "name": "HOSTNAME",
                    "content": self._thunder.get(Constant._RESOURCE_ID)
                },
                {
                    "name": "IP",
                    "content": self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)
                },
                {
                    "name": "AGENT",
                    "content": Constant._TOA
                },
                {
                    "name": "JOBID",
                    "content": Utils._datetime_id
                },
                {
                    "name": "PRIORITY",
                    "content": Utils.priority(each_log['text'])
                },
                {
                    "name": "PARTITION",
                    "content": self._thunder.get(Constant._PARTITION).upper()
                }
            ]
            yield each_log

    def publish_log(self, data):
        if(len(data)>0):
            generator = self.format(data)
            logs = []
            for log in generator:
                logs.append(log)
            body = {
                "events": logs
            }
            body = json.dumps(body)   
            response = Utils.rest_api(Constant._VMWARE_VRLI_URL.format(Utils._config.get('vmware_vrli_host'), self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)), Utils.get_headers(None), body, Constant._POST, Constant._ERROR_VMWARE_VRLI_LOGS, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if (response):
                self._logger.info(Constant._SUCCESS_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(logs)))
                return Constant._SUCCESS
        else:
            self._logger.info(Constant._SKIP_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper()))
        return None