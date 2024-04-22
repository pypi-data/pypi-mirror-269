# AWS Secure Bucket

[![GitHub](https://img.shields.io/github/license/gammarer/aws-secure-bucket?style=flat-square)](https://github.com/gammarer/aws-secure-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-secure-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-secure-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-secure-bucket?style=flat-square)](https://pypi.org/project/gammarer.aws-secure-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureBucket?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.SecureBucket/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-secure-bucket?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-secure-bucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarer/aws-secure-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarer/aws-secure-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarer/aws-secure-bucket?sort=semver&style=flat-square)](https://github.com/gammarer/aws-secure-bucket/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarer/aws-secure-bucket)](https://constructs.dev/packages/@gammarer/aws-secure-bucket)

This is a Simple S3 Secure Bucket.

* Bucket Access Control is Private
* Public Read Access is false
* Enforce SSL
* All Block public access
* Require encryption

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-bucket
# or
yarn add @gammarer/aws-secure-bucket
```

### Python

```shell
pip install gammarer.aws-secure-bucket
```

### C# / .Net

```shell
dotnet add package Gammarer.CDK.AWS.SecureBucket
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-secure-bucket</artifactId>
</dependency>
```

## Example

```python
import { SecureBucket } from '@gammarer/aws-secure-bucket';

const bucket = new SecureBucket(stack, 'SecureBucket', {
  bucketName: 'example-secure-bucket',
});
```
