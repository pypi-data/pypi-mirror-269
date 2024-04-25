#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
AWS Handler to connect and publish teh data.
To use, simply 'import AWSHandler' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com); Pramod Nimbhore (pnimbhore@a10networks.com)'

import datetime
import boto3
from common.toa_constant import Constant
from common.toa_utils import Utils
from common.toa_logging import Logging

class AWSHandler:
    
    _logger = Logging().get_logger("AWSHandler")
    _config=None
    _credentials=None
    _temp=None
    _thunder=None
    _client=None
    _service=None
        
    def __init__(self, thunder, service):
        self._thunder = thunder 
        self._credentials =  Utils._aws_credentials 
        self._service= service
        self.init_client()
    
    def init_client(self):
        self._client = boto3.client(self._service, aws_access_key_id=self._credentials.get(Constant._AWS_ACCESS_KEY_ID),aws_secret_access_key=self._credentials.get(Constant._AWS_SECRET_ACCESS_KEY),region_name=Utils._aws_config.get(Constant._AWS_REGION))
             
    def publish_metric(self, data):
        if(Utils.is_valid(data) and len(data) > 0):
            ip = self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)
            dimension = "%s (%s)" % (self._thunder[Constant._RESOURCE_ID], ip)
            # create a metric_data list
            metric_data = []
            # add metric data to metric_data list
            for metric in data:
                metric_data.append(
                    {
                        'MetricName': self._thunder.get(Constant._NAMESPACE),
                        'Dimensions': [
                            {
                                'Name': metric,
                                'Value': dimension
                            },
                        ],
                        'Timestamp': Utils._datetime, 
                        'StatisticValues': {
                            'SampleCount': 1,
                            'Sum': data[metric],
                            'Minimum': 0,
                            'Maximum': 0
                        },
                        'Unit': 'Percent',
                        'StorageResolution': 60
                    })
            try:
                # send thunder metrics to cloudwatch
                response = self._client.put_metric_data(Namespace=self._thunder.get(Constant._NAMESPACE),
                                                           MetricData=metric_data)
                if(Utils.is_valid(response, response.get("ResponseMetadata"), response.get("ResponseMetadata").get("HTTPStatusCode")) and (response.get("ResponseMetadata").get("HTTPStatusCode")==200 or response.get("ResponseMetadata").get("HTTPStatusCode")==201)):
                    self._logger.info(Constant._SUCCESS_METRIC.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(data), data))
                    return Constant._SUCCESS
            except Exception as exp:
                self._logger.error((Constant._ERROR_AWS_CLOUDWATCH_METRICS).format(Constant._NAMESPACE, exp, data, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]"))
        else:
            self._logger.info((Constant._SKIP_METRIC).format(self._thunder.get(Constant._IP) , self._thunder.get(Constant._NAMESPACE).upper()))
        return None
    
    def publish_log(self, data):
        if(Utils.is_valid(data) and len(data) > 0):
            self.read()
            # get sequence token from temp file
            seq_token = self._temp.get("aws_nexttoken", " ")
            # get new log stream name
            log_stream_name, seq_token_status = self.stream()
            # get 13 digit timestamp
            timestamp = int(datetime.datetime.timestamp(Utils._datetime) * 1000)
            log_list = []
            #thunder_logs = eval(data)
    
            for log in data:
                log_list.append({'timestamp': timestamp, 'message': log["log-data"]}, )
            # create log event
            log_event = {'logGroupName': Utils._config.get(Constant._AWS_LOG_GROUP_NAME),
                         'logStreamName': log_stream_name, 'logEvents': log_list,
                         }
            if seq_token_status is not False:
                log_event['sequenceToken'] = seq_token
            try:
                # send logs to cloudwatch
                response = self._client.put_log_events(**log_event)
                # update config file
                self._temp["aws_nexttoken"] = response['nextSequenceToken']
                
                self._logger.info(Constant._SUCCESS_LOG.format(self._thunder.get(Constant._IP), self._thunder.get(Constant._NAMESPACE).upper(), len(data)))
                self.write()
                return Constant._SUCCESS
            except Exception as exp:
                self._logger.error((Constant._ERROR_AWS_CLOUDWATCH_LOGS).format(Utils._config.get(Constant._AWS_LOG_GROUP_NAME), exp, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]"))
        else:
            self._logger.info((Constant._SKIP_LOG).format(self._thunder.get(Constant._IP) , self._thunder.get(Constant._NAMESPACE).upper()))
        return None
    
    def read(self):
        self._temp = Utils.load_temp_storage(self._thunder.get(Constant._IP)+"-"+self._thunder.get(Constant._PARTITION))
    
    def write(self):
        Utils.write(self._temp, self._thunder.get(Constant._IP)+"-"+self._thunder.get(Constant._PARTITION))
    
    def stream(self):
        try:
            seq_token_status = True
            ip = self._thunder.get(Constant._PRIVATE_IP) if Utils.is_valid(self._thunder.get(Constant._PRIVATE_IP)) else self._thunder.get(Constant._IP)
            #TODO
            today = Utils._datetime
            date1 = today.strftime("%d/%m/%Y")
            log_stream_name = "%s/%s/%s"%(str(date1), ip, self._thunder.get(Constant._NAMESPACE))
            if log_stream_name == self._temp.get(self._thunder[Constant._PARTITION] + "_log_stream", "") == "":
                return log_stream_name, seq_token_status
            try:
                self._client.create_log_stream(
                    logGroupName=Utils._config.get(Constant._AWS_LOG_GROUP_NAME),
                    logStreamName=log_stream_name)
            except Exception:
                return log_stream_name, seq_token_status
            seq_token_status = False
            self._temp[self._thunder[Constant._PARTITION] + "_log_stream"] = log_stream_name
            return log_stream_name, seq_token_status
        except Exception as exp:
            self._logger.error((Constant._ERROR_AWS_LOGSTREAM).format(exp, self._thunder[Constant._IP]))
        return None

    def collect_thunders_from_autoscale(self):
        try:
            user_name = self._thunder.get(Constant._USERNAME, "admin")
            resource_id = self._thunder.get(Constant._RESOURCE_ID)
            thunder_password = self._thunder.get(Constant._PASSWORD)
            ec2 = boto3.resource(Constant._AWS_BOTO3_SERVICE_EC2)
            response = self._client.describe_auto_scaling_groups(AutoScalingGroupNames=[resource_id])
            groups = response.get("AutoScalingGroups")
            if len(groups) > 0:
                instances = (groups[0].get('Instances'))
                thunders = [
                    {Constant._IP: ec2.Instance(instance.get('InstanceId')).private_ip_address,
                    Constant._USERNAME: user_name, 
                    Constant._PASSWORD: thunder_password,
                    Constant._PARTITION: self._thunder.get(Constant._PARTITION, "SHARED"),
                    Constant._RESOURCE_ID: instance.get('InstanceId')} for instance in instances]
                
                if(Utils.is_valid(thunders) and len(thunders) >= 0):
                    return thunders
        except Exception as exp:
            self._logger.error((Constant._ERROR_AWS_AUTOSCALE_GROUP_LOGS).format(self._thunder.get(Constant._RESOURCE_ID), exp))
        return None
    
    