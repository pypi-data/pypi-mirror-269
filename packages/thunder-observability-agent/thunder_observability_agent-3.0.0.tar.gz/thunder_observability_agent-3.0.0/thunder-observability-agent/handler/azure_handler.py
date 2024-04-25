#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Azure Handler to connect and publish the data.
To use, simply 'import AzureHandler' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com); Sachin (spatil@a10networks.com)'

import hashlib
import hmac
import base64
import json
import socket
from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

class AzureHandler:

    _logger = Logging().get_logger("AzureHandler")
    _credentials=None
    _thunder=None
    _token=None
    _url=None
    _vm=None
 
    def __init__(self, thunder, token):
        self._thunder=thunder
        self._credentials=Utils._azure_credentials 
        self._token=token

    def token(self, resource):
        
        client_id = self._credentials.get(Constant._AZURE_CLIENT_ID)
        secret_id = self._credentials.get(Constant._AZURE_SECRET_ID)
        tenant_id = self._credentials.get(Constant._AZURE_TENANT_ID)

        _headers = {
            Constant._CONTENT_TYPE: Constant._APPLICATION_URLENCODED
        }
         
        _body = {'grant_type': 'client_credentials', 'client_id': f'{client_id}',
                   'client_secret': f'{secret_id}', 'resource': 
                       {resource}}
        
        response = Utils.rest_api(Constant._AZURE_OAUTH2_URL.format(tenant_id), _headers, _body, Constant._POST, Constant._ERROR_AZURE_AUTH_RESPONSE, self._thunder.get(Constant._IP))
        self._token = json.loads(response.text).get('access_token')
        return self._token

    def publish_metric(self, data):
        
        if (Utils.is_valid(data) and len(data.keys()) > 0):
            metric_name = data.__iter__().__next__()
            
            dimention = self._thunder.get(Constant._RESOURCE_ID, socket.gethostname())

            _body = json.dumps({
                "time": Utils._datetime_str,
                "data": {
                    "baseData": {
                        "metric": metric_name,
                        "namespace":self._thunder.get(Constant._NAMESPACE),
                        "dimNames": [
                            metric_name
                        ],
                        "series": [
                            {
                                "dimValues": [
                                    dimention
                                ],
                                "min": 0,
                                "max": 0,
                                "sum": data[metric_name],
                                "count": 1
                            }
                        ]
                    }
                }
            })
 
            response = Utils.rest_api(Constant._AZURE_METRICS_URL.format(self._credentials.get(Constant._AZURE_LOCATION), Utils._config.get(Constant._AZURE_METRIC_RESOURCE_ID)), Utils.get_headers(self._token), _body, Constant._POST, Constant._ERROR_AZURE_METRICS, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(Utils.is_valid(response)):
                return data
            else:
                return None
        else:
            return None
                
    def publish_log(self, data):
        if(not Utils.is_valid(data)):
            return None
        
        if(len(data)>0):
            generator = self.format(data)
            logs = []
            for log in generator:
                logs.append(log)
            def key(log):
                x_headers = 'x-ms-date:' + Utils._datetime_gmt_str
                customer_id = Utils._config.get(Constant._AZURE_LOG_WORKSPACE_ID)
                shared = self._credentials.get(Constant._AZURE_WORKSPACE_PRIMARY_KEY)
                string_to_hash = Constant._POST + "\n" + str(len(log)) + "\n" + \
                                 Constant._APPLICATION_JSON + "\n" + x_headers + "\n" + '/api/logs'
                bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
                decoded = base64.b64decode(shared)
                encoded_hash = base64.b64encode(
                    hmac.new(decoded, bytes_to_hash,
                             digestmod=hashlib.sha256).digest()).decode()
                return "SharedKey {}:{}".format(customer_id, encoded_hash)
        
            _headers = {
                Constant._CONTENT_TYPE: Constant._APPLICATION_JSON,
                Constant._AUTHORIZATION: key(json.dumps(data)),
                'Log-Type': "THUNDER_SYSLOG",
                'x-ms-date': Utils._datetime_gmt_str,
                'x-ms-AzureResourceId': self._thunder.get(Constant._RESOURCE_ID)
            }
            
            response = Utils.rest_api(Constant._AZURE_LOGS_URL.format(Utils._config.get(Constant._AZURE_LOG_WORKSPACE_ID)), _headers, json.dumps(data), Constant._POST, Constant._ERROR_AZURE_LOGS, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if (Utils.is_valid(response)):
                self._logger.info(Constant._SUCCESS_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(data)))
                return Constant._SUCCESS
        else:
            self._logger.info((Constant._SKIP_LOG).format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper()))
        return None
        
    
    def format(self, data): 
        if isinstance(data, str):
            data = json.loads(data)

        # replace key log-data with text
        # add meta data to search logs on vRLI UI
        for each_log in data:
            each_log["LOG_TYPE"] = Constant._SYSLOG
            each_log["APPNAME"] =  Constant._THUNDER
            each_log["HOSTNAME"] = self._thunder.get(Constant._RESOURCE_ID) 
            each_log["IP"] = self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)
            each_log["AGENT"] = Constant._TOA
            each_log["JOBID"] = Utils._datetime_id
            each_log["PRIORITY"] = Utils.priority(each_log['log-data'])
            each_log["PARTITION"] = self._thunder.get(Constant._PARTITION).upper()
            yield each_log
    
    def log(self, data):
        if(Utils.is_valid(data) and len(data)>0):
            self._logger.info(Constant._SUCCESS_METRIC.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(data), data))
            return Constant._SUCCESS 
        return None
    
    def collect_thunders_from_autoscale(self):
        
        headers = {Constant._AUTHORIZATION: "Bearer " + self._token}
        response = Utils.rest_api(Constant._AZURE_VIRTUALMACHINES_URL.format(self._thunder.get(Constant._RESOURCE_ID)), headers, {}, Constant._GET, Constant._ERROR_AZURE_LOGS, self._thunder.get(Constant._IP))
        vmss_obj = response.json()
        public_ip_list = []

        def get_azure_public_ip(vm):
            if(Utils.is_valid(vm.get("properties").get("networkProfile").get("networkInterfaces"), vm.get("properties").get("networkProfile").get("networkInterfaces")[0] )):
                interface_id = vm.get("properties").get("networkProfile").get("networkInterfaces")[0].get("id")
                response = Utils.rest_api(Constant._AZURE_BASE_URL.format(interface_id), headers, {}, Constant._GET, Constant._ERROR_AZURE_AUTOSCALE_THUNDERS, self._thunder.get(Constant._RESOURCE_ID))
                interface_obj = response.json()
                public_ip_id = interface_obj.get("properties").get("ipConfigurations")[0].get(
                    "properties").get("publicIPAddress").get("id")
                response = Utils.rest_api(Constant._AZURE_BASE_URL.format(public_ip_id), headers, {}, Constant._GET, Constant._ERROR_AZURE_AUTOSCALE_THUNDERS, self._thunder.get(Constant._RESOURCE_ID))
                public_obj = response.json()
                public_ip = public_obj.get("properties").get("ipAddress")
                return {
                          Constant._IP: public_ip, 
                          Constant._USERNAME: self._thunder.get(Constant._USERNAME, "admin"),
                          Constant._PASSWORD: self._thunder.get(Constant._PASSWORD), 
                          Constant._RESOURCE_ID: vm.get("id"),
                          Constant._PARTITION: self._thunder.get(Constant._PARTITION, "SHARED")
                    } 
            return None
           
        if vmss_obj.get("value"):
            with ThreadPoolExecutor(int(Utils._main.get(Constant._THREADPOOL_MAX_WORKERS))) as executor:
                futures_vm = {executor.submit(get_azure_public_ip, vm): vm for vm in
                              vmss_obj.get("value")}
                for future in concurrent.futures.as_completed(futures_vm):
                    if future.result() is not None:
                        public_ip_list.append(future.result())
                if(len(public_ip_list)>0):
                    return public_ip_list
                else:
                    return None
        else:
            return None