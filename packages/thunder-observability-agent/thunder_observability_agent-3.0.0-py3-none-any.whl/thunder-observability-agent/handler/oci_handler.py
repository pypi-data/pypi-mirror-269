#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT

"""
OCI Handler to connect and publish the data.
To use, simply 'import OCIHandler' and use it!
It also contains OCIClient class to inherit the 
Monitoring client.
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com); Khushi Vishnoi (Kvishnoi@a10networks.com)'

import json
import uuid
from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging
import oci
from oci.config import from_file
from oci.loggingingestion.models import PutLogsDetails, LogEntryBatch

class OCIClient(oci.monitoring.MonitoringClient):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.base_client.endpoint = self.base_client.endpoint.replace(
            "telemetry.", "telemetry-ingestion."
        )
        
        
class OCIHandler:
    _logger = Logging().get_logger("OCIHandler")
    _credentials = None
    _config = None
    _thunder = None

    def __init__(self, thunder):
        self._thunder = thunder
        self._credentials = Utils._oci_credentials 
        
    def publish_metric(self, data):
        try:
            auth = oci.config.from_file(file_location=self._credentials.get(Constant._OCI_API_KEY_PATH))
            monitoring_client = OCIClient(auth)
            metric_data = []
            ip = self._thunder.get(Constant._IP) if Utils.is_valid(self._thunder.get(Constant._IP)) else Constant._EMPTY
            namespace = self._thunder.get(Constant._NAMESPACE).upper() if Utils.is_valid(
                self._thunder.get(Constant._NAMESPACE)) else Constant._EMPTY
            if ip is None:
                ip = Constant._EMPTY
            for metric_name, metric_value in data.items():
                metric_data_details = oci.monitoring.models.MetricDataDetails(
                    namespace=Constant._OCI_METRIC_NAMESPACE,
                    compartment_id=Utils._config.get(Constant._OCI_COMPARTMENT_ID),
                    name=metric_name.replace('/','_').replace(' (','_').replace(')','').replace(' ','_'),
                    dimensions={
                                "IP": ip, 
                                "NAMESPACE": namespace
                                },
                    datapoints=[
                        oci.monitoring.models.Datapoint(
                            timestamp=Utils._datetime_utc_str,
                            value=metric_value,
                        )
                    ],
                    resource_group=Constant._OCI_METRIC_RESOURCE_GROUP,
                    metadata={
                                "APPNAME":Constant._THUNDER,
                                "HOSTNAME":self._thunder.get(Constant._RESOURCE_ID),
                                "IP":self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP),
                                "AGENT":Constant._TOA,
                                "JOBID":Utils._datetime_id,
                                "PARTITION":self._thunder.get(Constant._PARTITION).upper()
                              }
                )
                metric_data.append(metric_data_details)
            post_metric_data_response = monitoring_client.post_metric_data(
                post_metric_data_details=oci.monitoring.models.PostMetricDataDetails(
                    metric_data=metric_data
                ),
            )
            if Utils.is_valid(post_metric_data_response):
                self._logger.info(Constant._SUCCESS_METRIC.format(ip, namespace, len(data), data))
                return Constant._SUCCESS
            else:
                self._logger.info((Constant._SKIP_METRIC).format(ip, namespace))
            
        except oci.exceptions.ConfigFileNotFound as e:
            self._logger.error((Constant._ERROR_OCI_FILE_NOT_FOUND).format(self._credentials.get(Constant._OCI_API_KEY_PATH), e, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]"))
        except oci.exceptions.ServiceError as e:
            self._logger.error((Constant._ERROR_OCI_SERVICE_ERROR).format(e, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]"))
            
        return None
    
    def format(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        for log_data in data:
            yield oci.loggingingestion.models.LogEntry(
                    data=json.dumps({"MESSAGE":log_data.get('log-data', None), 
                                    "LOG_TYPE":Constant._SYSLOG,
                                    "APPNAME":Constant._THUNDER,
                                    "HOSTNAME":self._thunder.get(Constant._RESOURCE_ID),
                                    "IP":self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP),
                                    "AGENT":Constant._TOA,
                                    "JOBID":Utils._datetime_id,
                                    "PRIORITY":Utils.priority(log_data.get('log-data', None)),
                                    "PARTITION":self._thunder.get(Constant._PARTITION).upper()
                                 }),
                id=str(uuid.uuid4()),
                time=Utils._datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            )


    def publish_log(self, data):
        try:
            if len(data) > 0:
                generator = self.format(data)
                logs = list(generator)
                auth = from_file(file_location=self._credentials.get(Constant._OCI_API_KEY_PATH))
                loggingingestion_client = oci.loggingingestion.LoggingClient(auth)
                if logs:
                    put_logs_response = loggingingestion_client.put_logs(
                        log_id=Utils._config.get(Constant._OCI_LOG_ID),
                        put_logs_details=PutLogsDetails(
                            specversion="1.0",
                            log_entry_batches=[
                                LogEntryBatch(
                                    entries=logs,
                                    source=Constant._THUNDER,
                                    type=Constant._SYSLOG
                                )
                            ]
                        )
                    )
                    if put_logs_response:
                        self._logger.info(Constant._SUCCESS_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper() if self._thunder.get(Constant._NAMESPACE) else Constant._EMPTY, len(data)))
                        return Constant._SUCCESS
            else:
                self._logger.info(Constant._SKIP_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper() if self._thunder.get(Constant._NAMESPACE) else Constant._EMPTY))

        except oci.exceptions.ConfigFileNotFound as e:
            self._logger.error((Constant._ERROR_OCI_FILE_NOT_FOUND).format(self._credentials.get(Constant._OCI_API_KEY_PATH), e, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]"))
        except oci.exceptions.ServiceError as e:
            self._logger.error((Constant._ERROR_OCI_SERVICE_ERROR).format(e, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]"))
        return None
        