# AWS Secure VPC Bucket

[![GitHub](https://img.shields.io/github/license/gammarer/aws-secure-vpc-bucket?style=flat-square)](https://github.com/gammarer/aws-secure-vpc-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-secure-vpc-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-secure-vpc-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-secure-vpc-bucket?style=flat-square)](https://pypi.org/project/gammarer.aws-secure-vpc-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureVpcBucket?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.SecureVpcBucket/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-secure-vpc-bucket?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-secure-vpc-bucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarer/aws-secure-vpc-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarer/aws-secure-vpc-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarer/aws-secure-vpc-bucket?sort=semver&style=flat-square)](https://github.com/gammarer/aws-secure-vpc-bucket/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarer/aws-secure-vpc-bucket)](https://constructs.dev/packages/@gammarer/aws-secure-vpc-bucket)

Access from specific VPC Endpoint only Bucket

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-vpc-bucket
# or
yarn add @gammarer/aws-secure-vpc-bucket
```

### Python

```shell
pip install gammarer.aws-secure-vpc-bucket
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.SecureVpcBucket
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-secure-vpc-bucket</artifactId>
</dependency>
```

## Example

```python
import { SecureSpecificVpcOnlyBucket } from '@gammarer/aws-secure-vpc-bucket';

new SecureVpcBucket(stack, 'SecureVpcBucket', {
  bucketName: 'example-origin-bucket',
  vpcEndpointId: 'vpce-0xxxxxxxxxxxxxxxx', // allready created vpc endpoint id
});
```

## License

This project is licensed under the Apache-2.0 License.
