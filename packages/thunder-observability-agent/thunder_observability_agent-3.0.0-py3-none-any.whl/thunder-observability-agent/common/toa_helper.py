#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Configure utility methods for toa framework.
To use, simply 'import Helper' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

from processor.thunder_processor import ThunderProcessor
from common.toa_logging import Logging 
from common.toa_constant import Constant 
from common.toa_utils import Utils
from handler.aws_handler import AWSHandler
from handler.azure_handler import AzureHandler
from concurrent.futures import ThreadPoolExecutor
class Helper:
    
    _logger = Logging().get_logger("Helper")
    
    def __init__(self):
        pass
    
    @staticmethod
    def init():
        try:
            Utils.load_properties()
            Utils.load_config()
            Utils.load_collect_provider() 
            Helper.load_autoscale_thunders()
            Utils.load_publish_provider()
            if(Utils.validate()):
                Helper.process()
        except Exception as exp:
            Utils._logger.debug(exp)
            return False
        
    @staticmethod
    def process():
        try:
            with ThreadPoolExecutor(max_workers=int(Utils._main.get(Constant._THREADPOOL_MAX_WORKERS))) as executor:
                executor.map(ThunderProcessor().process, Utils._thunders.get(Constant._THUNDERS))
        except Exception as exp:
            Utils._logger.debug(exp)

    @staticmethod
    def load_autoscale_thunders():
        if(Utils.is_valid(Utils._thunders)):
            if(Utils.is_valid(Utils._thunders.get(Constant._AUTOSCALE)) 
               and Utils._thunders.get(Constant._AUTOSCALE)==1 
               and Utils.is_valid(Utils._thunders.get(Constant._PROVIDER)) 
               and Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)) 
               and Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)[0]) 
               and Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._USERNAME), Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._PASSWORD), Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._RESOURCE_ID))):
                if(Utils._thunders.get(Constant._PROVIDER)==Constant._AWS):
                    if(not Utils.is_valid(Utils._aws_credentials)): 
                        Utils._aws_credentials =  Utils.load_configuration(Utils._main.get(Constant._AWS_CREDENTIALS_PATH), Utils._aws_credentials, Constant._ERROR_AWS_CREDENTIALS_NOT_FOUND, Constant._KEYVALUE) 
                    if(not Utils.is_valid(Utils._aws_config)): 
                        Utils._aws_config =  Utils.load_configuration(Utils._main.get(Constant._AWS_CONFIG_PATH), Utils._aws_config, Constant._ERROR_AWS_CONFIG_NOT_FOUND, Constant._KEYVALUE) 
                    
                    if(Utils.is_valid(Utils._aws_credentials) and Utils.is_valid(Utils._aws_config)): 
                        handler = AWSHandler(Utils._thunders.get(Constant._THUNDERS)[0], Constant._AWS_BOTO3_SERVICE_AUTOSCALING)
                        Utils._thunders[Constant._THUNDERS] = handler.collect_thunders_from_autoscale()
                    else:
                        if(not Utils.is_valid(Utils._aws_credentials)): 
                            Utils._logger.error(Constant._ERROR_AWS_CREDENTIALS_NOT_FOUND)
                        if(not Utils.is_valid(Utils._aws_config)): 
                            Utils._logger.error(Constant._ERROR_AWS_CONFIG_NOT_FOUND)
                             
                        Utils._azure_credentials = None
                        Utils._aws_config = None
                        Utils._thunders=None
                elif(Utils._thunders.get(Constant._PROVIDER)==Constant._AZURE):
                    if(not Utils.is_valid(Utils._azure_credentials)):
                        Utils._azure_credentials =  Utils.load_configuration(Utils._main.get(Constant._AZURE_CREDENTIALS_PATH), Utils._azure_credentials, Constant._ERROR_AZURE_CREDENTIALS_NOT_FOUND, Constant._KEYVALUE) 
                
                    if(Utils._azure_credentials and Utils.is_valid(Utils._azure_credentials.get(Constant._AZURE_CLIENT_ID))
                        and Utils.is_valid(Utils._azure_credentials.get(Constant._AZURE_SECRET_ID))
                        and Utils.is_valid(Utils._azure_credentials.get(Constant._AZURE_TENANT_ID))): 
                        handler = AzureHandler(Utils._thunders.get(Constant._THUNDERS)[0], None)
                        handler.token(Constant._AZURE_MANAGEMENT_RESOURCE)
                        Utils._thunders[Constant._THUNDERS] = handler.collect_thunders_from_autoscale()
                    else:
                        Utils._logger.error(Constant._ERROR_AZURE_CRED_AUTO_METRIC_NOT_FOUND) 
                        Utils._azure_credentials = None
                        Utils._thunders=None
                else:
                    Utils._logger.warn((Constant._ERROR_INVALID_THUNDER_AUTO).format(Utils._thunders.get(Constant._PROVIDER)))
                    Utils._thunders=None
            elif(Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)) and Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)[0]) and Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._IP), Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._USERNAME), Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._PASSWORD)) and Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._IP)=="127.0.0.1"):
                pass
            elif(Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)) and Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)[0]) and Utils.is_valid(Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._IP), Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._USERNAME), Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._PASSWORD), Utils._thunders.get(Constant._THUNDERS)[0].get(Constant._RESOURCE_ID))):
                pass
            else:
                Utils._thunders=None
                Utils._logger.warn(Constant._ERROR_INVALID_THUNDER_PARAMETERS)
                
            if(Utils.is_valid(Utils._thunders) and Utils.is_valid(Utils._thunders.get(Constant._THUNDERS))):
                Utils._logger.info(Constant._INFO_ACTIVE_THUNDERS_COUNT.format(str(len(Utils._thunders.get(Constant._THUNDERS))), [value['ip'] for value in Utils._thunders.get(Constant._THUNDERS)] ))
                
                for thunder in Utils._thunders.get(Constant._THUNDERS):
                    if(Utils.is_valid(thunder.get(Constant._PARTITION)) and not thunder.get(Constant._PARTITION)=="*"):
                        selected_partitions = set([part.strip().upper() for part in thunder.get(Constant._PARTITION).split(Constant._DELIMETER)])
                
                        if(Utils.is_valid(selected_partitions) and len(selected_partitions) > 0):
                            thunder[Constant._PARTITION] = selected_partitions
                            Utils._logger.info(Constant._INFO_ACTIVE_PARTITIONS_COUNT.format(thunder.get(Constant._IP), str(len(selected_partitions)), selected_partitions))
                        else:
                            thunder[Constant._PARTITION]= [Constant._SHARED]
                            Utils._logger.warn((Constant._WARN_ACTIVE_PARTITION_NOT_FOUND).format(thunder.get(Constant._IP)))
                            Utils._logger.info(Constant._INFO_ACTIVE_PARTITIONS_COUNT.format(thunder.get(Constant._IP), "1", Constant._SHARED.upper()))
                    elif(thunder.get(Constant._PARTITION)=="*"):
                        Utils._logger.info(Constant._INFO_ACTIVE_PARTITIONS_COUNT.format(thunder.get(Constant._IP), "1", "*"))
                    else:
                        thunder[Constant._PARTITION]= [Constant._SHARED]
                        Utils._logger.warn((Constant._WARN_ACTIVE_PARTITION_NOT_FOUND).format(thunder.get(Constant._IP)))
                        Utils._logger.info(Constant._INFO_ACTIVE_PARTITIONS_COUNT.format(thunder.get(Constant._IP), "1", Constant._SHARED.upper()))
                
            else:
                Utils._logger.info(Constant._INFO_ACTIVE_THUNDERS_COUNT.format(str(0),""))
                
    