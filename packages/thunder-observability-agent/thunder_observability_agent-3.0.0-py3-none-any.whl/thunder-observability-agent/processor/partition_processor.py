#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Processing engine to process partition information from thunder to configured provider.
To use, simply 'import PartitionProcessor' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging
from handler.thunder_handler import ThunderHandler
from concurrent.futures import ThreadPoolExecutor
from processor.log_processor import LogProcessor
from processor.metric_processor import MetricProcessor

class PartitionProcessor:
    
    _logger = Logging().get_logger("PartitionProcessor") 
    
    def process(self, thunder):
        handler = ThunderHandler(None, None, thunder, None, callback=None) 
        try:
            handler.token()
            if(not Utils.is_valid(handler._token)):
                return None
            
            thunders = [handler]
           
            with ThreadPoolExecutor(max_workers=int(Utils._main.get(Constant._THREADPOOL_MAX_WORKERS))) as executor:
                if(not handler._thunder.get(Constant._NAMESPACE)==Constant._THUNDER):
                    handler.activate()
                    if(handler.activemode()): 
                        executor.map(LogProcessor().process, thunders)
                        executor.map(MetricProcessor(metric=Utils._metrics, partition=Constant._L3V).process, thunders)
                    else:
                        Utils._logger.warn((Constant._WARN_STANDBY_PARTITION).format(handler._thunder.get(Constant._PARTITION), handler._thunder.get(Constant._IP)+"-"+handler._thunder.get(Constant._NAMESPACE))) 
    
                elif(handler._thunder.get(Constant._NAMESPACE)==Constant._THUNDER):
                    executor.map(MetricProcessor(metric=Utils._non_l4v_metrics, partition=Constant._NON_L3V).process, thunders) 
                    
        except Exception as exp:
            self._logger.debug(exp)
        handler.signout()
        