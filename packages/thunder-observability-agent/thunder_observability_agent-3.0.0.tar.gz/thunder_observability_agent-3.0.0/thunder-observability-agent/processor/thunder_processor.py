#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Processing engine to process individual thunder.
To use, simply 'import ThunderProcessor' and use it!
"""
from processor.partition_processor import PartitionProcessor
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging
from handler.thunder_handler import ThunderHandler
from concurrent.futures import ThreadPoolExecutor

class ThunderProcessor:
    
    _logger = Logging().get_logger("ThunderProcessor") 
    
    def process(self, thunder):
        try:
            thunders = []
            count = 0
            partitions = self.partitions(thunder)
            if(thunder.get(Constant._PARTITION)=="*"):
                thunder[Constant._PARTITION]= Constant._SHARED
                thunder[Constant._NAMESPACE]= Constant._THUNDER+"-"+Constant._SHARED.upper()
                thunders.append(dict(thunder))
                
                if(Utils.is_valid(partitions) and len(partitions) > 0):
                    for partition in partitions:
                        if(count == Constant._PARTITION_LIMIT - 1):
                            break
                        thunder[Constant._PARTITION]=partition
                        thunder[Constant._NAMESPACE]= Constant._THUNDER+"-"+partition.upper()
                        thunders.append(dict(thunder))
                        count+=1
            else:
                partitions_upper = []
                if(Utils.is_valid(partitions)):
                    partitions_upper = [part.upper() for part in partitions]
                for partition in thunder.get(Constant._PARTITION):
                        if(count == Constant._PARTITION_LIMIT):
                            break
                        if(Utils.is_valid(partitions) and partition.strip().upper() in partitions_upper):
                            name = partitions[partitions_upper.index(partition.strip().upper())]
                            thunder[Constant._PARTITION]=name
                            thunder[Constant._NAMESPACE]= Constant._THUNDER+"-"+name.upper()
                            thunders.append(dict(thunder))
                            count+=1
                        elif(partition.strip().upper()==Constant._SHARED.upper()):
                            thunder[Constant._PARTITION]= Constant._SHARED
                            thunder[Constant._NAMESPACE]= Constant._THUNDER+"-"+Constant._SHARED.upper()
                            thunders.append(dict(thunder))
                        else:
                            self._logger.warn((Constant._WARN_PARTITION_NOT_FOUND).format(partition, thunder[Constant._IP])) 
                
                if(len(thunders)==0):
                    thunder[Constant._PARTITION]= Constant._SHARED
                    thunder[Constant._NAMESPACE]= Constant._THUNDER+"-"+Constant._SHARED.upper()
                    thunders.append(dict(thunder))                 
            
            thunder[Constant._PARTITION]= Constant._THUNDER
            thunder[Constant._NAMESPACE]= Constant._THUNDER
            thunders.append(dict(thunder))    
        
        
            with ThreadPoolExecutor(max_workers=int(Utils._main.get(Constant._THREADPOOL_MAX_WORKERS))) as executor:
                executor.map(PartitionProcessor().process, thunders)
        except Exception as exp:
            self._logger.debug(exp)
                     
    def partitions(self, thunder):
        handler = ThunderHandler(None, None, thunder, None, callback=None) 
        handler.token()
        if(not Utils.is_valid(handler._token)):
            return None

        partitions = handler.partitions()
        handler.signout()
        return partitions
