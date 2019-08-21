#!/bin/sh -e
# swagger validation
# https://github.com/Azure/azure-rest-api-specs/blob/master/documentation/swagger-checklist.md#validation-tools-for-swagger-checklist
autorest --input-file=vmwarevirtustream.json --azure-validator --openapi-type=arm
oav validate-spec vmwarevirtustream.json -p
oav validate-example vmwarevirtustream.json -p
autorest --input-file=vmwarevirtustream.json --python --output-folder=azext_vmware --namespace=vendored_sdks --azure-arm=true --override-client-name=VirtustreamClient --use=@microsoft.azure/autorest.python@~3.0.56