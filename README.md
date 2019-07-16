#  Azure VMWare Solution by Virtustream Extension

The Azure CLI extension for Azure VMWare Solution by Virtustream is an extension for Azure CLI 2.0.

## Install
``` sh
whl=azure_vmware_virtustream_cli_extension-0.2.0-py2.py3-none-any.whl
az extension add --source $whl -y
```

## Usage
``` sh
az vmware --help
az vmware privatecloud list -g $resourcegroup
```

## Uninstall
``` sh
az extension remove --name azure-vmware-virtustream-cli-extension
```

## Build
Update `VERSION` in `setup.py`.
```
python setup.py bdist_wheel
```

## AutoRest client code generation
The code in the `azext_vmware/vendored_sdks` subdirectory was generated using the [AutoRest CLI](http://azure.github.io/autorest/user/command-line-interface.html). It is a Node app that bootstraps a dotnet app. It generates code from the a Swagger 2 spec. Here is how the current code was generated:

``` ps
cp ../azure-rest-api-specs/specification/vmwarevirtustream/resource-manager/Microsoft.VMwareVirtustream/preview/2016-09-01-preview/vmwarevirtustream.json
docker run --rm -it -v ${PWD}:/src -w /src node:lts bash
```

``` sh
npm install -g autorest
apt-get update
apt-get install libunwind-dev -y
./autorest.sh
```