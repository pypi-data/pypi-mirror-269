#!/usr/bin/python3
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Configure and run thunder agent.
To use, simply 'import Toa' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'
import time
from common.toa_helper import Helper
from common.toa_logging import Logging
from common.toa_utils import Utils
from common.toa_constant import Constant

_logger = Logging().get_logger("main")

if __name__ == "__main__":
    
        _job_start_time = Utils._datetime
        _logger.info(Constant._INFO_JOB_ID.format(str(Utils._datetime_id)))
        _logger.info(Constant._INFO_JOB_START.format(str(_job_start_time)))

        Helper.init()

        _job_end_time = Utils.date_time_utc()
        _logger.info(Constant._INFO_JOB_TIME.format((_job_end_time - _job_start_time).total_seconds()))
        _logger.info(Constant._INFO_JOB_END.format(str(_job_end_time)))
        _logger.info(Constant._DOCS)
        _logger.info("##### TOA  ###### All Rights Reserved @A10 Networks Inc ##### TOA #####")
        
