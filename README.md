#  Azure VMware Solution by Virtustream Extension

The Azure CLI extension for Azure VMware Solution by Virtustream is an extension for Azure CLI 2.0.

## Install
``` sh
az extension add --name vmware
```

Take a look at the [releases](https://github.com/virtustream/azure-vmware-virtustream-cli-extension/releases) page if you wish to install a specific version. It can be installed with `az extension add`, for example:
``` sh
az extension add -s https://github.com/virtustream/azure-vmware-virtustream-cli-extension/releases/download/0.5.5/vmware-0.5.5-py2.py3-none-any.whl -y

## Usage
``` sh
az vmware --help
az vmware private-cloud list
az vmware private-cloud create -g $resourcegroup -n $privatecloudname --location $location --cluster-size 3 --network-block 10.175.0.0/22
```
See [test_vmware_scenario.py](https://github.com/virtustream/azure-vmware-virtustream-cli-extension/blob/master/azext_vmware/tests/latest/test_vmware_scenario.py) for other examples.

## Uninstall
You can see if the extension is installed by running `az extension list`. You can remove the extension by running `az extension remove`.
``` sh
az extension remove --name vmware
```

## Build
Update `VERSION` in `setup.py`.
```
pipenv shell
python setup.py bdist_wheel
```

## AutoRest client code generation
The code in the `azext_vmware/vendored_sdks` subdirectory was generated using the [AutoRest CLI](http://azure.github.io/autorest/user/command-line-interface.html). It is a Node app that bootstraps a dotnet app. It generates code from the a Swagger 2 spec. Here is how the current code was generated:

``` ps
cp ../azure-rest-api-specs/specification/vmwarevirtustream/resource-manager/Microsoft.VMwareVirtustream/preview/2019-08-09-preview/vmwarevirtustream.json .
cp ../azure-rest-api-specs/specification/vmwarevirtustream/resource-manager/Microsoft.VMwareVirtustream/preview/2019-08-09-preview/examples/*.json examples/
docker run --rm -it -v ${PWD}:/src -w /src node:lts bash
```

``` sh
npm install -g autorest
npm install -g oav --unsafe-perm=true --allow-root
apt-get update
apt-get install libunwind-dev -y
./autorest.sh
```