#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Processing engine to process metrics information from thunder to configured provider.
To use, simply 'import Metric' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

from common.toa_constant import Constant
from common.toa_utils import Utils
from concurrent.futures import ThreadPoolExecutor
from common.toa_logging import Logging
from handler.thunder_handler import ThunderHandler
from handler.aws_handler import AWSHandler
from handler.vmware_handler import VMWareHandler
from handler.azure_handler import AzureHandler
from handler.elasticsearch_handler import ElasticSearchHandler
from handler.pushgateway_handler import PushGatewayHandler 
from handler.splunk_handler import SplunkHandler
from handler.gcp_handler import GCPHandler
from handler.oci_handler import OCIHandler
import concurrent.futures
class LogProcessor:
    
    _logger = Logging().get_logger("LogProcessor")
    
    def process(self, thunder):
        if(Utils.is_valid(Utils._active_log_provider)):
            if Utils._active_log_provider==Constant._AWS_LOG:
                self.process_aws_log(thunder)
            elif Utils._active_log_provider==Constant._AZURE_LOG:
                self.process_azure_log(thunder)
            elif Utils._active_log_provider==Constant._VMWARE_LOG:
                self.process_vmware_log(thunder)
            elif Utils._active_log_provider==Constant._ES_LOG:
                self.process_es_log(thunder)
            elif Utils._active_log_provider==Constant._PUSH_GATEWAY_LOG:
                self.process_pushgateway_log(thunder)
            elif Utils._active_log_provider==Constant._SPLUNK_LOG:
                self.process_splunk_log(thunder)
            elif Utils._active_log_provider==Constant._GCP_LOG:
                self.process_gcp_log(thunder)
            elif Utils._active_log_provider==Constant._OCI_LOG:
                self.process_oci_log(thunder)
            
    def process_aws_log(self, thunder):
        logs = self.collect_log(thunder)
        if(Utils.is_valid(logs)):
            handler = AWSHandler(thunder._thunder, Constant._AWS_BOTO3_SERVICE_LOGS)  
            handler.publish_log(logs)
       
    def process_vmware_log(self, thunder): 
        logs = self.collect_log(thunder)
        if(Utils.is_valid(logs)):
            handler = VMWareHandler(thunder._thunder, None)
            handler.publish_log(logs) 
       
    def process_azure_log(self, thunder): 
        logs = self.collect_log(thunder)
        if(Utils.is_valid(logs)):
            handler = AzureHandler(thunder._thunder, None)
            handler.publish_log(logs)
    
    def process_es_log(self, thunder): 
        logs = self.collect_log(thunder)
        if(Utils.is_valid(logs)):
            handler = ElasticSearchHandler(thunder._thunder)
            handler.publish_log(logs)
            
    def process_pushgateway_log(self, thunder): 
        logs = self.collect_log(thunder)
        if(Utils.is_valid(logs)):
            handler = PushGatewayHandler(thunder._thunder)
            handler.publish_log(logs)
    
    def process_splunk_log(self,thunder):
        logs = self.collect_log(thunder)
        if(Utils.is_valid(logs)):
            handler = SplunkHandler(thunder._thunder)
            handler.publish_log(logs)
    
    def process_gcp_log(self, thunder): 
        logs = self.collect_log(thunder)
        if(Utils.is_valid(logs)):
            handler = GCPHandler(thunder._thunder, None)
            handler.token()
            handler.publish_log(logs)
    
    def process_oci_log(self,thunder):
        logs = self.collect_log(thunder)
        if(Utils.is_valid(logs)):
            handler = OCIHandler(thunder._thunder)
            handler.publish_log(logs)

    def collect_log(self, thunder): 
        logs_data = []
        dates = thunder.dates()
        
        thunders = [ThunderHandler(metric=None, date=date, thunder=thunder._thunder, token=thunder._token, callback=None) for date in dates]
        with ThreadPoolExecutor(max_workers=int(Utils._main.get(Constant._THREADPOOL_MAX_WORKERS))) as collect:
            futures_logs = [collect.submit(thunder.collect_log) for thunder in thunders]
            for future in concurrent.futures.as_completed(futures_logs):
                if future.result() is not None:
                    logs_data.extend(future.result())
                    
            #asyncio.run(thunder.signout())
            return Utils.unique_logdata(logs_data) 
    
    