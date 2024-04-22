# AWS Secure CloudFront Origin Bucket (for CDK v2)

[![GitHub](https://img.shields.io/github/license/gammarer/aws-secure-cloudfront-origin-bucket?style=flat-square)](https://github.com/gammarer/aws-secure-cloudfront-origin-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-secure-cloudfront-origin-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-secure-cloudfront-origin-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-secure-cloudfront-origin-bucket?style=flat-square)](https://pypi.org/project/gammarer.aws-secure-cloudfront-origin-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureCloudFrontOriginBucket?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.ScureCloudFrontOriginBucket/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-secure-cloudfront-origin-bucket?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-secure-cloudfront-origin-bucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarer/aws-secure-cloudfront-origin-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarer/aws-secure-cloudfront-origin-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarer/aws-secure-cloudfront-origin-bucket?sort=semver&style=flat-square)](https://github.com/gammarer/aws-secure-cloudfront-origin-bucket/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarer/aws-secure-cloudfront-origin-bucket)](https://constructs.dev/packages/@gammarer/aws-secure-cloudfront-origin-bucket)

An AWS CDK construct library to create secure S3 buckets for CloudFront origin.

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-cloudfront-origin-bucket
# or
yarn add @gammarer/aws-secure-cloudfront-origin-bucket
# or
pnpm add @gammarer/aws-secure-cloudfront-origin-bucket
# or
bun add @gammarer/aws-secure-cloudfront-origin-bucket
```

### Python

```shell
pip install gammarer.aws-secure-cloudfront-origin-bucket
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.SecureCloudFrontOriginBucket
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-secure-cloudfront-origin-bucket</artifactId>
</dependency>
```

## Example

### for OAI(Origin Access Identity)

```python
import { SecureCloudFrontOriginBucket, SecureCloudFrontOriginType } from '@gammarer/aws-secure-cloudfront-origin-bucket';

const oai = new cloudfront.OriginAccessIdentity(stack, 'OriginAccessIdentity');

new SecureCloudFrontOriginBucket(stack, 'SecureCloudFrontOriginBucket', {
  bucketName: 'example-origin-bucket',
  cloudFrontOriginType: SecureCloudFrontOriginType.ORIGIN_ACCESS_IDENTITY,
  cloudFrontOriginAccessIdentityS3CanonicalUserId: oai.cloudFrontOriginAccessIdentityS3CanonicalUserId,
});
```

### for OAC(Origin Access Control)

```python
import { SecureCloudFrontOriginBucket, SecureCloudFrontOriginType } from '@gammarer/aws-secure-cloudfront-origin-bucket';

declare const distribution: cloudfront.Distribution;

new SecureCloudFrontOriginBucket(stack, 'SecureCloudFrontOriginBucket', {
  bucketName: 'example-origin-bucket',
  cloudFrontOriginType: SecureCloudFrontOriginType.ORIGIN_ACCESS_CONTROL,
  cloudFrontArn: `arn:aws:cloudfront::123456789:distribution/${distribution.distributionId}`,
});
```

## License

This project is licensed under the Apache-2.0 License.
