#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Data collection from thunder devices.
To use, simply 'import ThunderHandler' and use it!
"""
import asyncio
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

from common.toa_constant import Constant
from common.toa_utils import Utils
import json
import datetime
from common.toa_logging import Logging
import socket

class ThunderHandler:
    _logger = Logging().get_logger("ThunderHandler")
    _metric=None
    _date=None
    _thunder=None
    _token=None
    _url=None
    _headers=None
    _temp=None
    _callback=None
      
    def __init__(self, metric, date, thunder, token, callback):
        self._metric=metric
        self._thunder=thunder
        self._date=date
        self._url=Constant._THUNDER_BASE_URL.format(self._thunder.get(Constant._IP))
        self._token = token
        self._headers= Utils.get_headers(token)
        self._callback=callback
    
    def signout(self):
        try:
            return asyncio.run(self.async_logout())
        except Exception:
            return self.sync_logout()
    
    async def async_logout(self):
        response = Utils.rest_api(self._url +"/logoff" , Utils.get_headers(self._token), {}, Constant._GET, Constant._ERROR_THUNDER_LOGOFF_RESPONSE, self._thunder.get(Constant._IP))
        if(Utils.is_valid(response)):
            return Constant._SUCCESS
        return None 
    
    def sync_logout(self):
        response = Utils.rest_api(self._url +"/logoff" , Utils.get_headers(self._token), {}, Constant._GET, Constant._ERROR_THUNDER_LOGOFF_RESPONSE, self._thunder.get(Constant._IP))
        if(Utils.is_valid(response)):
            return Constant._SUCCESS
        return None 
    
    
    def read(self):
        self._temp = Utils.load_temp_storage(self._thunder.get(Constant._IP) + "-" + self._thunder.get(Constant._PARTITION))
    
    def token(self):
       
        _body = json.dumps({
            Constant._CREDENTIALS: {
                Constant._USERNAME: self._thunder.get(Constant._USERNAME),
                Constant._PASSWORD: self._thunder.get(Constant._PASSWORD),
            }
        })
        _headers = {
            Constant._CONTENT_TYPE: Constant._APPLICATION_JSON
        }
        response = Utils.rest_api(self._url +"/auth" , _headers, _body, Constant._POST, Constant._ERROR_THUNDER_AUTH_RESPONSE, self._thunder.get(Constant._IP))
        if(Utils.is_valid(response)):
            self._token = f"A10 {response.json()['authresponse']['signature']}"
            self.internal()
            self.header()
        return self._token
    
    def dates(self):
        response = Utils.rest_api(self._url+"/clock/show/oper", self._headers, {}, Constant._GET, Constant._ERROR_THUNDER_CLOCK_NOT_FOUND, self._thunder.get(Constant._IP))
        thunder = json.loads(response.text)
        time = thunder.get("show").get("oper").get("time")
        date = thunder.get("show").get("oper").get("date")
        date_time_obj = datetime.datetime.strptime(date + time, "%b %d %Y%H:%M:%S")
        date_time_obj = date_time_obj.replace(second=0, microsecond=0)
        
        log_delay = int(Utils._main.get(Constant._LOG_DELAY_MIN))*60
        cron_delay= int(Utils._main.get(Constant._CRON_DELAY_MIN))*60
        start_delta = log_delay + cron_delay 
        
        log_start_time = date_time_obj - datetime.timedelta(seconds=int(start_delta))
        log_end_time = log_start_time + datetime.timedelta(seconds=int(cron_delay))
        
        mins = (log_end_time - log_start_time).total_seconds()/60
        times = []
        for i in range(0, int(mins), 1):
            next_time_delta=i*60
            fetch_time = log_start_time + datetime.timedelta(seconds=int(next_time_delta))
            times.append(fetch_time.strftime("%b %d %Y %H:%M"))
            
        return times
        
    def collect_log(self):
        
        response = Utils.rest_api(self._url+"/syslog/oper?log-data-search={}".format(self._date), Utils.get_headers(self._token), {}, Constant._GET, Constant._ERROR_THUNDER_CLOCK_NOT_FOUND, self._thunder.get(Constant._IP))
        if(Utils.is_valid(response.text) and response.status_code==200):
            response_data = json.loads(response.text)
            oper = response_data["syslog"]["oper"]
            return oper["system-log"]
        return None
    
    def header(self):
        self._headers = Utils.get_headers(self._token)
    
    def collect_metric_cps(self): 
        result = None
        try:
            response = Utils.rest_api(self._url+"/system/app-performance/stats", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_CPS_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                total_new_connection_per_sec = response.json()['app-performance']['stats']['total-new-conns-per-sec']
                result = {"Total New Connection (Sec)": total_new_connection_per_sec}
        
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None
            
    def collect_metric_cpu(self): 
        result = None
        try:
            response = Utils.rest_api(self._url+"/system-cpu/data-cpu/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_CPU_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:    
                cpu_usage_list = response.json()['data-cpu']['oper']['cpu-usage']
                total_cpu_usage = 0
                for cpu_usage in cpu_usage_list:
                    total_cpu_usage += cpu_usage['60-sec']
                result = {"CPU Usage Percentage (Data)": total_cpu_usage / len(cpu_usage_list)}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None
            
    def collect_metric_memory(self): 
        result = None
        try:
            response = Utils.rest_api(self._url+"/system/memory/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_MEMORY_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                memory_usage = response.json()['memory']['oper']['Usage']
                result = {"Memory Usage Percentage": float(memory_usage.rstrip("%"))}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None
            
    def collect_metric_disk(self): 
        result = None
        try:
            response = Utils.rest_api(self._url+"/system/hardware/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_DISK_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                disk_usage = response.json()['hardware']['oper']['disk-percentage']
                result =  {"Disk Usage Percentage": disk_usage}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None
            
    def collect_metric_throughput(self): 
        result = None
        try:
            response = Utils.rest_api(self._url+"/system/throughput/stats", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_THROUGHPUT_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                global_throughput = response.json()['throughput']['stats']['global-system-throughput-bits-per-sec']
                result =  {"Throughput Rate (Global/BPS)": global_throughput}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None

    def collect_metric_interface(self): 
        result = None
        try:
            count = 0
            response = Utils.rest_api(self._url+"/interface/available-eth-list/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_INTERFACES_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                json_data = response.json()
                interfaces_list = json_data["available-eth-list"]['oper'].get("if-list", [])
                if(interfaces_list is None):
                    return {"Interface Down Count (Data)": count}
                for i in interfaces_list:
                    state = (i['state'])
                    if state == 'UP':
                        pass
                    else:
                        count += 1
                result = {"Interface Down Count (Data)": count}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None

    def collect_metric_transaction(self): 
        result = None
        try:
            response = Utils.rest_api(self._url+"/system/app-performance/stats", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_TPS_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                transaction_per_sec = response.json()['app-performance']['stats']['l7-trans-per-sec']
                result = {"Transactions Rate (Sec)": transaction_per_sec}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None

    def collect_metric_server_down(self): 
        result = None
        try:
            count=0
            response = Utils.rest_api(self._url+"/slb/server", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_SERVER_DOWN_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                if(Utils.is_valid(response.text) and Utils.is_valid(response.json())):
                    server_list = response.json().get("server-list", [])
                    if server_list is None or server_list.__len__().__eq__(0):
                        return {"Server Down Count": count}
                    for server in server_list:
                        server_name = server['name']
                        response = Utils.rest_api(self._url+"/slb/server/"+server_name+"/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_SERVER_DOWN_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
                        server_down_status = response.json()['server']['oper']['state']
                        if server_down_status == "Down":
                            count += 1
                result =  {"Server Down Count": count}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None

    def collect_metric_server_down_per(self): 
        result = None
        try:
            server_down_count = 0
            total_server = 0
            server_down_percentage = 0
            response = Utils.rest_api(self._url+"/slb/server", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_SERVER_PER_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                if(Utils.is_valid(response.text) and Utils.is_valid(response.json())):
                    server_list = response.json().get("server-list", [])
                    if server_list is None or server_list.__len__().__eq__(0):
                        return {"Server Down Percentage": 0}
                    for server in server_list:
                        server_name = server['name']
                        response = Utils.rest_api(self._url+"/slb/server/"+server_name+"/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_SERVER_DOWN_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
                        total_server += 1
                        server_down_status = response.json()['server']['oper']['state']
                        if server_down_status == "Down":
                            server_down_count += 1
                    server_down_percentage = ((server_down_count / total_server) * 100)
                result =  {"Server Down Percentage": server_down_percentage}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None

    def collect_metric_ssl(self): 
        result = None
        try:
            response = Utils.rest_api(self._url+"/slb/ssl-stats/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_SSL_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                ssl_errors_count = response.json()['ssl-stats']['oper']['server-cert-errors']
                result = {"SSL Errors Count": ssl_errors_count}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None


    def collect_metric_server_error(self): 
        result = None
        try:
            total_error_count = 0
            response = Utils.rest_api(self._url+"/slb/http-proxy/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_SERVER_ERROR_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                total_proxy_list = response.json()['http-proxy']['oper']['http-proxy-cpu-list']
                for error_count in total_proxy_list:
                    total_error_count += error_count.get('response_4xx', 0)
                    total_error_count +=error_count.get('response_5xx', 0)
                result = {"Server Errors Count": total_error_count}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None


    def collect_metric_session(self): 
        result = None
        try:
            response = Utils.rest_api(self._url+"/system/session/stats", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_SESSION_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                total_session = response.json()['session']['stats']['total_curr_conn']
                result =  {"Total Session Count": total_session}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None


    def collect_metric_packet_rate(self): 
        result = None
        try:
            self.read()
            old_timestamp_formatted = self._temp.get(Constant._TEMP_LAST_PACKET_SENT_TIME, "")
            current_timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d, %H:%M:%S")
            current_timestamp_formatted = datetime.datetime.strptime(current_timestamp, "%Y-%m-%d, %H:%M:%S")
            last_packet_count = self._temp.get(Constant._TEMP_LAST_PACKET_COUNT, 0)
            response = Utils.rest_api(self._url+"/plat-cpu-packet/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_PACKET_RATE_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
            if(not Utils.is_valid(response)):
                result = None
            else:
                all_cpus=None
                if(Utils.is_valid(response)):
                    all_cpus = response.json()['plat-cpu-packet']['oper']['pkt-stats']
                
                current_packet_count = 0
                if(Utils.is_valid(all_cpus)):
                    for cpu in all_cpus:
                        current_packet_count += cpu["pkt-sent"]
    
                if old_timestamp_formatted != "":
                    old_timestamp = datetime.datetime.strptime(old_timestamp_formatted.replace(",", ", "), "%Y-%m-%d, %H:%M:%S")
                    time_interval = (current_timestamp_formatted - old_timestamp).total_seconds()
                    # packet get sent in last minute
                    if current_packet_count > last_packet_count:
                        packet_rate = (current_packet_count - last_packet_count) / time_interval
                        self._temp[Constant._TEMP_LAST_PACKET_SENT_TIME] = current_timestamp
                        self._temp[Constant._TEMP_LAST_PACKET_COUNT] = current_packet_count
    
                    # no packet get sent in last minute
                    elif current_packet_count == last_packet_count:
                        packet_rate = 0
                        self._temp[Constant._TEMP_LAST_PACKET_SENT_TIME] = current_timestamp
                    # vThunder reboot
                    else:
                        packet_rate = 0
                        self._temp[Constant._TEMP_LAST_PACKET_SENT_TIME] = current_timestamp
                        self._temp[Constant._TEMP_LAST_PACKET_COUNT] = current_packet_count
                # first time crone job run
                else:
                    packet_rate = 0
                    self._temp[Constant._TEMP_LAST_PACKET_SENT_TIME] = current_timestamp
                    self._temp[Constant._TEMP_LAST_PACKET_COUNT] = current_packet_count
    
                Utils.write(self._temp, self._thunder.get(Constant._IP)+"-"+self._thunder.get(Constant._PARTITION))
                result =  {"Packet Rate (Sec)": int(packet_rate)}
            return self.callback(result)
        except Exception as exp:
            self._logger.debug(exp)
            return None
        
    def collect_metric_packet_drop(self): 
            result = None
            try:
                self.read()
                old_timestamp = self._temp.get(Constant._TEMP_LAST_PACKET_DROPPED_SENT_TIME, "")
                current_timestamp1 = datetime.datetime.utcnow().strftime("%Y-%m-%d, %H:%M:%S")
                current_timestamp = datetime.datetime.strptime(current_timestamp1, "%Y-%m-%d, %H:%M:%S")
                
                response = Utils.rest_api(self._url+"/plat-cpu-packet/oper", self._headers, {}, Constant._GET, Constant._ERROR_METRIC_PACKET_DROP_NOT_FOUND, self._thunder.get(Constant._IP) + " [" +self._thunder.get(Constant._NAMESPACE)+"]")
                if(not Utils.is_valid(response)):
                    result = None
                else:
                    all_cpus=None
                    last_packet_dropped = 0
                    if(Utils.is_valid(response)):
                        last_packet_dropped = self._temp.get(Constant._TEMP_LAST_PACKET_DROPPED_COUNT, 0)
                        all_cpus = response.json()['plat-cpu-packet']['oper']['pkt-stats']
                    
                    current_packet_dropped = 0
                    if(Utils.is_valid(all_cpus)):
                        for cpu in all_cpus:
                            current_packet_dropped += cpu["pkt-drop"]
        
                    if old_timestamp != "":
                        old_timestamp = old_timestamp.replace(",", ", ")
                        old_timestamp = datetime.datetime.strptime(old_timestamp,
                                                                   "%Y-%m-%d, %H:%M:%S")
                        time_interval = (current_timestamp - old_timestamp).total_seconds()
                        # packet get dropped in last minute
                        if current_packet_dropped > last_packet_dropped:
                            packet_dropped = (current_packet_dropped -
                                              last_packet_dropped) / time_interval
                            self._temp[Constant._TEMP_LAST_PACKET_DROPPED_SENT_TIME] = current_timestamp1
                            self._temp[Constant._TEMP_LAST_PACKET_DROPPED_COUNT] = current_packet_dropped
        
                        # no packet get dropped in last minute
                        elif current_packet_dropped == last_packet_dropped:
                            packet_dropped = 0
                            self._temp[Constant._TEMP_LAST_PACKET_DROPPED_SENT_TIME] = current_timestamp1
                        # vThunder reboot
                        else:
                            packet_dropped = 0
                            self._temp[Constant._TEMP_LAST_PACKET_DROPPED_SENT_TIME] = current_timestamp1
                            self._temp[Constant._TEMP_LAST_PACKET_DROPPED_COUNT] = current_packet_dropped
                    # first time crone job run
                    else:
                        packet_dropped = 0
                        self._temp[Constant._TEMP_LAST_PACKET_DROPPED_SENT_TIME] = current_timestamp1
                        self._temp[Constant._TEMP_LAST_PACKET_DROPPED_COUNT] = current_packet_dropped
        
                    Utils.write(self._temp, self._thunder.get(Constant._IP)+"-"+self._thunder.get(Constant._PARTITION))
                    result = {"Packet Drop Rate (Sec)": int(packet_dropped)}
                return self.callback(result)
         
            except Exception as exp:
                self._logger.debug(exp)
                return None
                                               
    def collect_metric(self):
        
        if(self._metric == Constant._AWS_CPS or self._metric == Constant._AZURE_CPS or self._metric == Constant._VMWARE_CPS or self._metric == Constant._PUSH_GATEWAY_CPS or self._metric == Constant._ES_CPS or self._metric == Constant._SPLUNK_CPS or self._metric == Constant._GCP_CPS or self._metric == Constant._OCI_CPS):
            return self.collect_metric_cps()
        
        elif(self._metric == Constant._AWS_CPU or self._metric == Constant._AZURE_CPU or self._metric == Constant._VMWARE_CPU or self._metric == Constant._PUSH_GATEWAY_CPU or self._metric == Constant._ES_CPU or self._metric == Constant._SPLUNK_CPU or self._metric == Constant._GCP_CPU or self._metric == Constant._OCI_CPU): 
            return self.collect_metric_cpu()
            
        elif(self._metric == Constant._AWS_MEMORY or self._metric == Constant._AZURE_MEMORY or self._metric == Constant._VMWARE_MEMORY or self._metric == Constant._PUSH_GATEWAY_MEMORY or self._metric == Constant._ES_MEMORY or self._metric == Constant._SPLUNK_MEMORY or self._metric == Constant._GCP_MEMORY or self._metric == Constant._OCI_MEMORY):
            return self.collect_metric_memory()
        
        elif(self._metric == Constant._AWS_DISK or self._metric == Constant._AZURE_DISK or self._metric == Constant._VMWARE_DISK or self._metric == Constant._PUSH_GATEWAY_DISK or self._metric == Constant._ES_DISK or self._metric == Constant._SPLUNK_DISK or self._metric == Constant._GCP_DISK or self._metric == Constant._OCI_DISK):
            return self.collect_metric_disk()
        
        elif(self._metric == Constant._AWS_THROUGHPUT or self._metric == Constant._AZURE_THROUGHPUT or self._metric == Constant._VMWARE_THROUGHPUT or self._metric == Constant._PUSH_GATEWAY_THROUGHPUT or self._metric == Constant._ES_THROUGHPUT or self._metric == Constant._SPLUNK_THROUGHPUT or self._metric == Constant._GCP_THROUGHPUT or self._metric == Constant._OCI_THROUGHPUT):
            return self.collect_metric_throughput()
        
        elif(self._metric == Constant._AWS_INTERFACES or self._metric == Constant._AZURE_INTERFACES or self._metric == Constant._VMWARE_INTERFACES or self._metric == Constant._PUSH_GATEWAY_INTERFACES or self._metric == Constant._ES_INTERFACES or self._metric == Constant._SPLUNK_INTERFACES or self._metric == Constant._GCP_INTERFACES or self._metric == Constant._OCI_INTERFACES):
            return self.collect_metric_interface()
        
        elif(self._metric == Constant._AWS_TPS or self._metric == Constant._AZURE_TPS or self._metric == Constant._VMWARE_TPS or self._metric == Constant._PUSH_GATEWAY_TPS or self._metric == Constant._ES_TPS or self._metric == Constant._SPLUNK_TPS or self._metric == Constant._GCP_TPS or self._metric == Constant._OCI_TPS):
            return self.collect_metric_transaction()
        
        elif(self._metric == Constant._AWS_SERVER_DOWN_COUNT or self._metric == Constant._AZURE_SERVER_DOWN_COUNT or self._metric == Constant._VMWARE_SERVER_DOWN_COUNT or self._metric == Constant._PUSH_GATEWAY_SERVER_DOWN_COUNT or self._metric == Constant._ES_SERVER_DOWN_COUNT or self._metric == Constant._SPLUNK_SERVER_DOWN_COUNT or self._metric == Constant._GCP_SERVER_DOWN_COUNT or self._metric == Constant._OCI_SERVER_DOWN_COUNT):
            return self.collect_metric_server_down()
            
        elif(self._metric == Constant._AWS_SERVER_DOWN_PERCENTAGE or self._metric == Constant._AZURE_SERVER_DOWN_PERCENTAGE or self._metric == Constant._VMWARE_SERVER_DOWN_PERCENTAGE or self._metric == Constant._PUSH_GATEWAY_SERVER_DOWN_PERCENTAGE or self._metric == Constant._ES_SERVER_DOWN_PERCENTAGE or self._metric == Constant._SPLUNK_SERVER_DOWN_PERCENTAGE or self._metric == Constant._GCP_SERVER_DOWN_PERCENTAGE or self._metric == Constant._OCI_SERVER_DOWN_PERCENTAGE):
            return self.collect_metric_server_down_per()

        elif(self._metric == Constant._AWS_SSL_CERT or self._metric == Constant._AZURE_SSL_CERT  or self._metric == Constant._VMWARE_SSL_CERT or self._metric == Constant._PUSH_GATEWAY_SSL_CERT or self._metric == Constant._ES_SSL_CERT or self._metric == Constant._SPLUNK_SSL_CERT or self._metric == Constant._GCP_SSL_CERT or self._metric == Constant._OCI_SSL_CERT):
            return self.collect_metric_ssl()
        
        elif(self._metric == Constant._AWS_SERVER_ERROR or self._metric == Constant._AZURE_SERVER_ERROR or self._metric == Constant._VMWARE_SERVER_ERROR or self._metric == Constant._PUSH_GATEWAY_SERVER_ERROR or self._metric == Constant._ES_SERVER_ERROR or self._metric == Constant._SPLUNK_SERVER_ERROR or self._metric == Constant._GCP_SERVER_ERROR or self._metric == Constant._OCI_SERVER_ERROR):
            return self.collect_metric_server_error()
            
        elif(self._metric == Constant._AWS_SESSION or self._metric == Constant._AZURE_SESSION or self._metric == Constant._VMWARE_SESSION or self._metric == Constant._PUSH_GATEWAY_SESSION or self._metric == Constant._ES_SESSION or self._metric == Constant._SPLUNK_SESSION or self._metric == Constant._GCP_SESSION or self._metric == Constant._OCI_SESSION):
            return self.collect_metric_session()
            
        elif(self._metric == Constant._AWS_PACKET_RATE or self._metric == Constant._AZURE_PACKET_RATE or self._metric == Constant._VMWARE_PACKET_RATE or self._metric == Constant._PUSH_GATEWAY_PACKET_RATE or self._metric == Constant._ES_PACKET_RATE or self._metric == Constant._SPLUNK_PACKET_RATE or self._metric == Constant._GCP_PACKET_RATE or self._metric == Constant._OCI_PACKET_RATE):
            return self.collect_metric_packet_rate()
            
        elif(self._metric == Constant._AWS_PACKET_DROP or self._metric == Constant._AZURE_PACKET_DROP or self._metric == Constant._VMWARE_PACKET_DROP or self._metric == Constant._PUSH_GATEWAY_PACKET_DROP or self._metric == Constant._ES_PACKET_DROP or self._metric == Constant._SPLUNK_PACKET_DROP or self._metric == Constant._GCP_PACKET_DROP or self._metric == Constant._OCI_PACKET_DROP):
            return self.collect_metric_packet_drop()

    def partitions(self):
        try:
            response = Utils.rest_api(self._url+"/partition", self._headers, {}, Constant._GET, Constant._ERROR_PARTITION_NOT_FOUND, self._thunder.get(Constant._IP))
            if(not Utils.is_valid(response)): 
                return None
            else:
                if(Utils.is_valid(response.text) and Utils.is_valid(response.json()['partition-list'])):
                    partitions = response.json()['partition-list']
                    return [partition.get(Constant._PARTITION_NAME, None) for partition in partitions] 
        except Exception as exp:
            self._logger.debug(exp)
        return None
        
    def activate(self):
        if(self._thunder.get(Constant._PARTITION)==Constant._SHARED):
            body = json.dumps({ "active-partition": { "shared": 1}})
        else:
            body = json.dumps({ "active-partition": { "curr_part_name": self._thunder.get(Constant._PARTITION)}})
        
        try:
            response = Utils.rest_api(self._url+"/active-partition", self._headers, body, Constant._POST, Constant._ERROR_PARTITION, self._thunder.get(Constant._IP))
            if(not Utils.is_valid(response)): 
                return None
            else:
                return Constant._SUCCESS
        except Exception as exp:
            self._logger.debug(exp)
        return None
    
    def activemode(self):
        try:
            response = Utils.rest_api(self._url+"/vrrp-a/vrid/oper", self._headers, {}, Constant._GET, Constant._ERROR_PARTITION_NOT_FOUND, self._thunder.get(Constant._IP))
            if(not Utils.is_valid(response)): 
                return True
            else:
                if(Utils.is_valid(response.text) and Utils.is_valid(response.json()['vrid-list']) and Utils.is_valid(response.json()['vrid-list'][0]) and Utils.is_valid(response.json()['vrid-list'][0]['oper'])):
                    state = response.json()['vrid-list'][0]['oper']['state']
                    if(state == "vrrp-a not enabled"):
                        return True
                    else:
                        return response.json()['vrid-list'][0]['oper']['state']=='Active' 
        except Exception as exp:
            self._logger.debug(exp)
        return None
    
        

    def callback(self, result):
        if(Utils.is_valid(self._callback)):
            return self._callback(result)
        else:
            return result
    
    def internal(self):
        if(self._thunder.get(Constant._IP) =="127.0.0.1"):
            response = Utils.rest_api(self._url +"/interface/management/oper" , Utils.get_headers(self._token), {}, Constant._GET, Constant._ERROR_THUNDER_MANG_IP_NOT_FOUND, self._thunder.get(Constant._IP))
            if(Utils.is_valid(response)):
                json_responce = json.loads(response.text).get("management") 
                self._thunder[Constant._PRIVATE_IP] =  json_responce.get("oper", {}).get("ipv4-addr")
                if(Utils._active_log_provider == Constant._AZURE_LOG or Utils._active_metric_provider == Constant._VMWARE_METRIC):
                    pass
                else:
                    self._thunder[Constant._RESOURCE_ID] = socket.gethostname()    
                    
            else:
                self._thunder[Constant._PRIVATE_IP] = None
        else:
            self._thunder[Constant._PRIVATE_IP] = None                