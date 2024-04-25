#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
GCP Handler to connect and publish the data.
To use, simply 'import GCPHandler' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com); Khushi Vishnoi (Kvishnoi@a10networks.com)'
import json
from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class GCPHandler:

    _logger = Logging().get_logger("GCPHandler")
    _credentials=None
    _config=None
    _thunder=None
    _token=None

    def __init__(self, thunder, token):
        self._thunder=thunder
        self._credentials =  Utils._gcp_credentials 
        self._token=token

    def token(self):
        json_keyfile_path = self._credentials.get(Constant._GCP_SERVICE_KEY_PATH)
        scopes = [Constant._GCP_SCOPE_URL]
        try:
            credentials = service_account.Credentials.from_service_account_file(
                json_keyfile_path, scopes=scopes
            )
        except FileNotFoundError as e:
            self._logger.error((Constant._ERROR_GCP_TOKEN_NOT_CREATED).format(json_keyfile_path, e, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]"))
        
        if credentials.valid and not credentials.expired:
            self._token = credentials.token
            return self._token

        credentials.refresh(Request())
        self._token = credentials.token
        return self._token

    
    def publish_metric(self, data):
        project_id = self._credentials.get(Constant._GCP_PROJECT_ID)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}"
        }
        ip = self._thunder.get(Constant._IP) if Utils.is_valid(self._thunder.get(Constant._IP)) else Constant._EMPTY
        namespace = self._thunder.get(Constant._NAMESPACE).upper() if Utils.is_valid(
            self._thunder.get(Constant._NAMESPACE)) else Constant._EMPTY
        if ip is None:
            ip = Constant._EMPTY
        metric_entries = []
        input_timestamp = Utils._datetime
        input_datetime = input_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"
        
        for metric_name, metric_value in data.items():
            modified_string = metric_name.replace(" ", "-")
            request_body_metric = {
                "displayName": metric_name,
                "valueType": "DOUBLE",
                "unit": "1",  
                "metricKind": "GAUGE",
                "type": "custom.googleapis.com/{}/{}".format(project_id, modified_string)
            }
            custom_metric_body = json.dumps(request_body_metric)
            Utils.rest_api(Constant._GCP_CUSTOM_METRIC_URL.format(project_id), headers, custom_metric_body,Constant._POST, Constant._ERROR_GCP_METRIC,ip + " [" + namespace + "]")
            labels = {
                    "APPNAME":Constant._THUNDER,
                    "HOSTNAME":self._thunder.get(Constant._RESOURCE_ID),
                    "IP":self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP),
                    "AGENT":Constant._TOA,
                    "JOBID":Utils._datetime_id,
                    "PARTITION":self._thunder.get(Constant._PARTITION).upper()
            }
            time_series_entry = {
                "metric": {
                    "type": "custom.googleapis.com/{}/{}".format(project_id, modified_string),
                    "labels": labels
                },
                "points": [
                    {
                        "value": {
                            "doubleValue": metric_value
                        },
                        "interval": {
                            "endTime": input_datetime
                        }
                    }
                ]
            }
            metric_entries.append(time_series_entry)

        body = {"timeSeries": metric_entries}
        response = Utils.rest_api(Constant._GCP_TIME_SERIES_URL.format(project_id), headers, json.dumps(body),Constant._POST, Constant._ERROR_GCP_METRIC,ip + " [" + namespace + "]")
        if Utils.is_valid(response):
            self._logger.info(Constant._SUCCESS_METRIC.format(ip, namespace, len(data), data))
            return Constant._SUCCESS
        else:
            self._logger.info((Constant._SKIP_METRIC).format(ip, namespace))
            return None

    def format(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        for each_log in data:
            if 'log-data' not in each_log:
                pass
            else:
                each_log['textPayload'] = each_log['log-data']
                each_log.pop('log-data', None)  # Remove the 'log-data' key
                each_log['severity'] = Utils.priority(each_log['textPayload'])
            each_log['labels'] ={
                    "LOG_TYPE":Constant._SYSLOG,
                    "APPNAME":Constant._THUNDER,
                    "HOSTNAME":self._thunder.get(Constant._RESOURCE_ID),
                    "IP":self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP),
                    "AGENT":Constant._TOA,
                    "JOBID":Utils._datetime_id,
                    "PARTITION":self._thunder.get(Constant._PARTITION).upper()
            }
            yield each_log

    def publish_log(self,data):
        if len(data)>0:
            generator = self.format(data)
            logs = list(generator)
            logName = "projects/"+self._credentials.get(Constant._GCP_PROJECT_ID)+"/logs/"+Constant._GCP_LOG_NAME
            if logs:
                body={
                "logName":logName,
                "resource":{
                    "type":"global"
                },
                "entries": logs
                }
                ip = self._thunder.get(Constant._IP)
                namespace = self._thunder.get(Constant._NAMESPACE)
                ip_namespace = f"{ip} [{namespace}]" if ip and namespace else Constant._EMPTY
                headers ={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._token}"
                }
                response = Utils.rest_api(Constant._GCP_LOG_URL, headers, json.dumps(body),Constant._POST,Constant._ERROR_GCP_LOG,ip_namespace)
                if response:
                    self._logger.info(Constant._SUCCESS_LOG.format(self._thunder.get(Constant._IP),self._thunder.get(Constant._NAMESPACE).upper() if self._thunder.get(Constant._NAMESPACE) else Constant._EMPTY,len(data)))
                    return Constant._SUCCESS

        else:
            self._logger.info(Constant._SKIP_LOG.format(self._thunder.get(Constant._IP),self._thunder.get(Constant._NAMESPACE).upper() if self._thunder.get(Constant._NAMESPACE) else Constant._EMPTY))

        return None
    
