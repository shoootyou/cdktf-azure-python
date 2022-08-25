#!/usr/bin/env python
import os
from constructs import Construct
from cdktf import App, TerraformStack, RemoteBackend, NamedRemoteWorkspace
from cdktf_cdktf_provider_azurerm import AzurermProvider, AzurermProviderFeatures, ResourceGroup, StorageAccount


AzureClientID = os.environ['AzureClientID']
AzureTenantID = os.environ['AzureTenantID']
AzureSubscriptionID = os.environ['AzureSubscriptionID']
AzureClientSecret = os.environ['AzureClientSecret']


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

        gruporecursos = ResourceGroup(self,
                                      id_="central-rg",
                                      name="rg-temporal-001",
                                      location="eastus")

        StorageAccount(self,
                       id_="central-storage",
                       name="storagegprueba003423523",
                       location=gruporecursos.location,
                       resource_group_name=gruporecursos.name,
                       account_tier="Standard",
                       account_replication_type="LRS")


app = App()
stack = MyStack(app, "azure-python")
# RemoteBackend(stack,
#              hostname='app.terraform.io',
#              organization='orion-global',
#              workspaces=NamedRemoteWorkspace('azure-python')
#              )

app.synth()
