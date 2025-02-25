import os
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'framework\\infrastructure\\python\\'))
from AzureClient import AzureClient
from OEAModuleInstaller import OEAModuleInstaller
from AzureResourceProvisioner import AzureResourceProvisioner
from OEAFrameworkInstaller import OEAFrameworkInstaller
import logging
from datetime import datetime


# Info on logging in Azure python sdk: https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='setup_oea_log_{:%Y_%m_%d__%H_%M}.log'.format(datetime.now()), level=logging.DEBUG)
_logger = logging.getLogger('setup')
_logger.addHandler(logging.StreamHandler(sys.stdout))

# Enter these values before executing the script.
_tenant_id = "{AZURE TENANT ID}"
_subscription_id = "{AZURE SUBSCRIPTION ID}"
_oea_suffix = "{OEA SUFFIX}"
_location = "{LOCATION}"
_oea_version = "0.7"

# Instantiate AzureClient class to connect with Azure CLI using Python SDK
azure_client = AzureClient(_tenant_id, _subscription_id, _location)

# Instantiate AzureResourceProvisioner class to setup the required infrastructure in your Azure Tenant.
_logger.info('Setting up infrastructure in Azure Tenant.')
resource_provisioner = AzureResourceProvisioner(_tenant_id, _subscription_id, _oea_suffix, _location, _oea_version, _logger)
resource_provisioner.provision_resources()
_logger.info('Completed setting up infrastructure.')

# Instantiate OEAFrameworkInstaller class to install the Base OEA framework in your Synapse workspace.
_logger.info('Installing Base OEA Framework in Synapse workspace.')
oea_installer = OEAFrameworkInstaller(azure_client, resource_provisioner.storage_account, resource_provisioner.keyvault, resource_provisioner.synapse_workspace_name, 'framework/synapse', _logger)
oea_installer.install()
_logger.info('Successfully Installed Base OEA Framework.')

#Install Modules
_logger.info('Installing the Required modules in Azure Synapse workspace.')
module_installer = OEAModuleInstaller(resource_provisioner.synapse_workspace_name, _logger)
module_installer.install(azure_client)