#!/usr/bin/env python
import os
from constructs import Construct
from cdktf import App, TerraformStack, RemoteBackend, NamedRemoteWorkspace
from cdktf_cdktf_provider_azurerm import AzurermProvider, AzurermProviderFeatures, ResourceGroup, StorageAccount


AzureClientID = os.environ['AzureClientID']
AzureTenantID = os.environ['AzureTenantID']
AzureSubscriptionID = os.environ['AzureSubscriptionID']
AzureClientSecret = os.environ['AzureClientSecret']
TerraformOrganization = os.environ['TerraformOrganization']
TerraformToken = os.environ['TerraformToken']


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        features = AzurermProviderFeatures()
        AzurermProvider(self,
                        id="Azure",
                        features=features,
                        client_id=AzureClientID,
                        client_secret=AzureClientSecret,
                        tenant_id=AzureTenantID,
                        subscription_id=AzureSubscriptionID
                        )

        rg_central_001 = ResourceGroup(self,
                                      id_="central-rg",
                                      name="rg-tempo-001",
                                      location="eastus")

        StorageAccount(self,
                       id_="central-storage",
                       name="stopythoncdktf0987123",
                       location=rg_central_001.location,
                       resource_group_name=rg_central_001.name,
                       account_tier="Standard",
                       account_replication_type="LRS")

        rg_shared_001 = ResourceGroup(self,
                                      id_="rg_shared_001",
                                      name="rg-shared-001",
                                      location="eastus")


app = App()
stack = MyStack(app, "azure-python")

RemoteBackend(stack,
              hostname='app.terraform.io',
              organization=TerraformOrganization,
              workspaces=NamedRemoteWorkspace('azure-python'),
              token=TerraformToken
              )

app.synth()
