'''
# CDKTF prebuilt bindings for hashicorp/dns provider version 3.4.1

This repo builds and publishes the [Terraform dns provider](https://registry.terraform.io/providers/hashicorp/dns/3.4.1/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-dns](https://www.npmjs.com/package/@cdktf/provider-dns).

`npm install @cdktf/provider-dns`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-dns](https://pypi.org/project/cdktf-cdktf-provider-dns).

`pipenv install cdktf-cdktf-provider-dns`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Dns](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Dns).

`dotnet add package HashiCorp.Cdktf.Providers.Dns`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-dns](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-dns).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-dns</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-dns-go`](https://github.com/cdktf/cdktf-provider-dns-go) package.

`go get github.com/cdktf/cdktf-provider-dns-go/dns/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-dns-go/blob/main/dns/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-dns).

## Versioning

This project is explicitly not tracking the Terraform dns provider version 1:1. In fact, it always tracks `latest` of `~> 3.2` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform dns provider](https://registry.terraform.io/providers/hashicorp/dns/3.4.1)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

__all__ = [
    "a_record_set",
    "aaaa_record_set",
    "cname_record",
    "data_dns_a_record_set",
    "data_dns_aaaa_record_set",
    "data_dns_cname_record_set",
    "data_dns_mx_record_set",
    "data_dns_ns_record_set",
    "data_dns_ptr_record_set",
    "data_dns_srv_record_set",
    "data_dns_txt_record_set",
    "mx_record_set",
    "ns_record_set",
    "provider",
    "ptr_record",
    "srv_record_set",
    "txt_record_set",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import a_record_set
from . import aaaa_record_set
from . import cname_record
from . import data_dns_a_record_set
from . import data_dns_aaaa_record_set
from . import data_dns_cname_record_set
from . import data_dns_mx_record_set
from . import data_dns_ns_record_set
from . import data_dns_ptr_record_set
from . import data_dns_srv_record_set
from . import data_dns_txt_record_set
from . import mx_record_set
from . import ns_record_set
from . import provider
from . import ptr_record
from . import srv_record_set
from . import txt_record_set
