"""
Setup script to setup thunder observability agent
Create By: Vikas Gautam
"""

import os
import shutil
import compileall
from sys import platform
from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path

# check operating system and username
platform = "linux"

# compile all python files
source_code_path = "thunder-observability-agent"
compileall.compile_dir(source_code_path, force=True)

# package metadata
if platform == "win32" or platform == "win64":
    package_dir_loc = {"": ".\\"}
elif platform == "linux":
    package_dir_loc = {"": "./"}
else:
    package_dir_loc = {"": ""}


this_directory = Path(__file__).parent
readme = (this_directory / "README.md").read_text()

setup(
    name="thunder-observability-agent",
    version="3.0.0",
    description="A10 Thunder Observability Agent is a lightweight autonomous data processing engine that can be externally installed and configured for multiple A10 Thunder Instances to collect, process and publish performance metrics and logs into multiple monitoring dashboard.",
    keywords=["Python","A10Networks","Observability","Agent","Thunder","vThunder","cThunder","Thunder","AWS","Azure","Cloudwatch","VMware","Log","Insight","Application","App","Insight","Analytics","Dashboard","Monitoring","VROPS","VRLI","Operations","A10", "Splunk", "Prometheus", "PushGateway", "ElasticSearch", "ACOS", "A10","Google Cloud Platform (GCP)","Oracle Cloud Infrastructure (OCI)"],
    long_description=readme,
    long_description_content_type='text/markdown',
    Documentation="https://documentation.a10networks.com",
    Repository="https://github.com/a10networks/thunder-observability-agent/tree/release/v3.0.0",
    Changelog="https://github.com/a10networks/thunder-observability-agent/tree/release/v3.0.0/README.md",
    dependencies=[
      "crontab",
      "rsyslog"
      "requests>=2.27.1",
      "boto3>=1.23.10",
      "google-auth>=2.22.0",
      "oci>=2.121.1"
    ],
    # requires-python=">=3.6",
    url="https://github.com/a10networks/thunder-observability-agent",
    # authors=[{"name" == "Dinesh Kumar Lohia", "email" == "dlohia@a10networks.com"}],
    author="A10 Networks",
    author_email="support@a10networks.com",
    maintainer="A10 Networks",
    maintainer_email="support@a10networks.com",
    # maintainers = [{"name" == "Dinesh Kumar Lohia", "email" =="dlohia@a10networks.com"}],
    license="THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT.",
    packages=["thunder-observability-agent", "thunder-observability-agent.common",
              "thunder-observability-agent.handler", "thunder-observability-agent.processor", "thunder-observability-agent.config"],
    include_package_data=True,
    data_files=[("thunder-observability-agent", ["thunder-observability-agent/config.json",
                                                 "thunder-observability-agent/logging.conf",
                                                 "thunder-observability-agent/main.properties",
                                                 "thunder-observability-agent/init.sh"]),
                ("thunder-observability-agent/.tmp/config/.aws", ["thunder-observability-agent/config/.aws/config",
                                                                  "thunder-observability-agent/config/.aws/credentials"]),
                ("thunder-observability-agent/.tmp/config/.elasticsearch", ["thunder-observability-agent/config/.elasticsearch/credentials"]),
                ("thunder-observability-agent/.tmp/config/.gcp", ["thunder-observability-agent/config/.gcp/credentials"]),
                ("thunder-observability-agent/.tmp/config/.oci", ["thunder-observability-agent/config/.oci/credentials"]),
                ("thunder-observability-agent/.tmp/config/.pushgateway", ["thunder-observability-agent/config/.pushgateway/credentials"]),
                ("thunder-observability-agent/.tmp/config/.splunk", ["thunder-observability-agent/config/.splunk/credentials"]),
                ("thunder-observability-agent/.tmp/config/.azure", ["thunder-observability-agent/config/.azure/credentials"]),
                ("thunder-observability-agent/.tmp/config/.vmware", ["thunder-observability-agent/config/.vmware/credentials"]),
                ("thunder-observability-agent/.tmp/config/.thunder", ["thunder-observability-agent/config/.thunder/credentials"])
                ],
    package_dir=package_dir_loc,
    package_data={"thunder-observability-agent": ["*.py", "*.md", "*.txt", "pdf"],
                  "thunder-observability-agent.common": ["*.py"],
                  "thunder-observability-agent.handler": ["*.py"],
                  "thunder-observability-agent.processor": ["*.py"]},
    install_requires=["requests>=2.27.1", "boto3>=1.23.10",
      "google-auth>=2.22.0","oci>=2.121.1"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
        ]
)
