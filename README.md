# CDKTF Python Example 
[![vault enterprise](https://github.com/shoootyou/cdktf-azure-python/actions/workflows/github_action.yml/badge.svg)](https://github.com/shoootyou/cdktf-azure-python)

----

**Please note**: This example is for demonstration proposes only. This project uses the CDKTF Python library from Hashicorp and you can find the source code [here](https://github.com/hashicorp/terraform-cdk)

----

CDKTF allows you to deploy infrastructure using programming languages.

![terraform platform](https://github.com/hashicorp/terraform-cdk/raw/main/docs/terraform-platform.png)


In this case I use Python for the creation (in its most base form). In this case this is my setup:

### Environment

* Windows 11 x64 Enterprise
* VSCode

### Tools

| Tools  | Version          |
| ------ | ---------------- |
| Python | 3.7              |
| pip    | 22.2.2           |
| pipenv | 2022.8.19        |
| nodejs | 16.17.0          |
| npm    | 8.13.2           |
| cdktf  | 0.12.1           |
| git    | 2.37.2.windows.2 |

Internally, at pipenv level the project uses these modules (it's not necessary to install them manually):

| Module                       | Version    |
| ---------------------------- | ---------- |
| atomicwrites                 | ==1.4.1    |
| attrs                        | ==22.1.0   |
| cattrs                       | ==22.1.0   |
| cdktf                        | ==0.12.1   |
| cdktf-cdktf-provider-azurerm | ==2.0.10   |
| colorama                     | ==0.4.5    |
| constructs                   | ==10.1.86  |
| exceptiongroup               | ==1.0.0rc8 |
| iniconfig                    | ==1.1.1    |
| jsii                         | ==1.65.0   |
| packaging                    | ==21.3     |
| pluggy                       | ==1.0.0    |
| publication                  | ==0.0.3    |
| py                           | ==1.11.0   |
| pyparsing                    | ==3.0.9    |
| pytest                       | ==7.1.2    |
| python-dateutil              | ==2.8.2    |
| six                          | ==1.16.0   |
| tomli                        | ==2.0.1    |
| typeguard                    | ==2.13.3   |
| typing-extensions            | ==4.3.0    |

## Installation process

First at all you need to install nodejs and npm in your computer. Right now is necessary use npm for install cdktf (and this is not because Windows). You can compile the code by yourself but is different process, in this case use this command to install it:

```bash
    npm install --location=global cdktf-cli@latest
```

After that, you could check the if the installation was successful using this command:

```bash
    cdktf --version
```

After that, you need to clone the repository in your computer. You can use the command:

```bash
    git clone https://github.com/shoootyou/cdktf-azure-python.git
    cd cdktf-azure-python
```

If you want to run locally, you must run this command first. This command will install the dependencies:

```bash
    pipenv install
```

----

**Note** This project already has the module for azure, but in case you need another providers, you need to install them, and you can do it in two different ways:

```bash
     pipenv install cdktf-cdktf-provider-docker
```
or:

```bash
    cdktf provider add aws@~>4.0
```

----

## Checking the files

After you clone the repository, you will find a folder called `cdktf-azure-python` with the code. Inside, the principals files are:

```bash
    cdktf.json # Bootstrap for the project
    main.py # Here will be all the code
    Pipfile 
    Pipfile.lock # For pipenv to record & lock installed module versions & requirements.
```

## Checking the code

In the `main.py` file you can find the code for the deployment of the infrastructure.

```python
#!/usr/bin/env python
import os
from constructs import Construct
from cdktf import App, TerraformStack, RemoteBackend, NamedRemoteWorkspace

# Here you need import the provider for the infrastructure you want to deploy
from cdktf_cdktf_provider_azurerm import AzurermProvider, AzurermProviderFeatures, ResourceGroup, StorageAccount

# Always use environment values for the process, for Azure it's necessary use them for the authentication.
AzureClientID = os.environ['AzureClientID']
AzureTenantID = os.environ['AzureTenantID']
AzureSubscriptionID = os.environ['AzureSubscriptionID']
AzureClientSecret = os.environ['AzureClientSecret']
TerraformOrganization = os.environ['TerraformOrganization']
TerraformToken = os.environ['TerraformToken']


class MyStack(TerraformStack): # This is the priimary class for whole the process
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # Here you need to initialize the provider

        features = AzurermProviderFeatures()
        AzurermProvider(self,
                        id="Azure",
                        features=features,
                        client_id=AzureClientID,
                        client_secret=AzureClientSecret,
                        tenant_id=AzureTenantID,
                        subscription_id=AzureSubscriptionID
                        )

        # Each resource must be invocked in the constructor of the class and use "id_" for Terraform identification

        rg_central_001 = ResourceGroup(self,
                                      id_="central-rg",
                                      name="rg-tempo-001",
                                      location="eastus")

        # If you need, you could reference the resource in the constructor of the class if it was saved in a variable.

        StorageAccount(self,
                       id_="central-storage",
                       name="stopythoncdktf0987123",
                       location=rg_central_001.location,
                       resource_group_name=rg_central_001.name, # Here's the reference to the previous resource
                       account_tier="Standard",
                       account_replication_type="LRS")

         # You can repeat the same kind of resource but changing the "id_" and the variable for store it.

        rg_shared_001 = ResourceGroup(self,
                                      id_="rg_shared_001",
                                      name="rg-shared-001",
                                      location="eastus")


app = App()
stack = MyStack(app, "azure-python")

#----------------------------------------------------------------------------------------------------------------------
# Finally, this block is for terraform cloud registration, you need the orgazaition and the token for the operation and use remote state in Terraform Cloud.
# This is optional, if you don't use it, you can use local state.

RemoteBackend(stack,
              hostname='app.terraform.io',
              organization=TerraformOrganization,
              workspaces=NamedRemoteWorkspace('azure-python'),
              token=TerraformToken
              )

#-----------------------------------------------------------------------------------------------------------------------

app.synth()
```
## Deploying the infrastructure (locally)

The final step is to deploy the infrastructure. You can use the command (this command must be executed in the folder):

```bash
    cdktf deploy
```

Also, you can run `plan` and `destroy` actions as you use it with terraform binary. The commands are this:

```bash
    cdktf plan
    cdktf destroy # Use with precaution
```

## Deploying the infrastructure (Using GitHub Actions)

The project also have the GitHub Actions for deploy the infrastructure. Basically, the action prepare the environment installing the tools and the prerequisites for the deployment. Use two scenarios, one for test your code and the second for the deployment. In future releases will be added more scenarios.

```yaml
name: CDKTF Python Action

on:
  push:
    branches:
      - prod
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - prod

jobs:
  build_and_deploy_job:
    if: github.event_name == 'pull_request' && github.event.action != 'closed'
    runs-on: ubuntu-latest
    name: "Evaluate the pull request (Terraform plan)"
    steps:
      - name: Checkout the repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v1
        with:
          python-version: 3.7
      - name: Set up node
        uses: actions/setup-node@v3
        with:
          node-version: 16
      - name: Install pipenv
        run: |
          pip install pipenv
      - name: Install cdktf
        run: |
          npm install --location=global cdktf-cli@latest
      - name: Install dependencies
        run: |
          pipenv install
      - name: Execute plan
        env:
          AzureClientID: ${{ secrets.AzureClientID }}
          AzureTenantID: ${{ secrets.AzureTenantID }}
          AzureSubscriptionID: ${{ secrets.AzureSubscriptionID }}
          AzureClientSecret: ${{ secrets.AzureClientSecret }}
          TerraformOrganization: ${{ secrets.TerraformOrganization }}
          TerraformToken: ${{ secrets.TerraformToken }}
        run: |
          cdktf synth

  close_pull_request_job:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    name: "Deploy de infraestructure (Terraform apply)"
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v1
        with:
          python-version: 3.7
      - name: Set up node
        uses: actions/setup-node@v3
        with:
          node-version: 16
      - name: Install pipenv
        run: |
          pip install pipenv
      - name: Install cdktf
        run: |
          npm install --location=global cdktf-cli@latest
      - name: Install dependencies
        run: |
          pipenv install
      - name: Execute plan
        env:
          AzureClientID: ${{ secrets.AzureClientID }}
          AzureTenantID: ${{ secrets.AzureTenantID }}
          AzureSubscriptionID: ${{ secrets.AzureSubscriptionID }}
          AzureClientSecret: ${{ secrets.AzureClientSecret }}
          TerraformOrganization: ${{ secrets.TerraformOrganization }}
          TerraformToken: ${{ secrets.TerraformToken }}
        run: |
          cdktf deploy --auto-approve

```

## References

This project is based on this information:
* https://medium.com/@gurayy/creating-kubernetes-cluster-on-azure-with-terraform-and-python-using-cdk-for-terraform-8237ffa15092
* https://learn.hashicorp.com/tutorials/terraform/cdktf-install
* https://github.com/hashicorp/terraform-cdk