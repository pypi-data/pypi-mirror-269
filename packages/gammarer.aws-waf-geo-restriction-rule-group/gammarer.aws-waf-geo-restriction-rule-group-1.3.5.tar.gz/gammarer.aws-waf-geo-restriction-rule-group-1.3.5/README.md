# AWS WAF(v2) GEO Restriction Rule Group

[![GitHub](https://img.shields.io/github/license/gammarer/aws-waf-geo-restriction-rule-group?style=flat-square)](https://github.com/gammarer/aws-waf-geo-restriction-rule-group/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-waf-geo-restriction-rule-group?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-waf-geo-restriction-rule-group)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-waf-geo-restriction-rule-group?style=flat-square)](https://pypi.org/project/gammarer.aws-waf-geo-restriction-rule-group/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.WafGeoRestrictionRuleGroup?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.WafGeoRestrictionRuleGroup/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-waf-geo-restriction-rule-group?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-waf-geo-restriction-rule-group/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarer/aws-waf-geo-restriction-rule-group/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarer/aws-waf-geo-restriction-rule-group/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarer/aws-waf-geo-restriction-rule-group?sort=semver&style=flat-square)](https://github.com/gammarer/aws-waf-geo-restriction-rule-group/releases)

[![View on Construct Hub](https://constructs.dev/badge?package=@gammarer/aws-waf-geo-restriction-rule-group)](https://constructs.dev/packages/@gammarer/aws-waf-geo-restriction-rule-group)

This is an AWS CDK Construct for Geo Restriction Rule Group on WAF V2

## Resources

This construct creating resource list.

* WAF V2 RuleGroup

## Install

### TypeScript

```shell
npm install @gammarer/aws-waf-geo-restriction-rule-group
# or
yarn add @gammarer/aws-waf-geo-restriction-rule-group
```

### Python

```shell
pip install gammarer.aws-waf-geo-restriction-rule-group
```

### C# / .Net

```shell
dotnet add package Gammarer.CDK.AWS.WafGeoRestrictionRuleGroup
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-waf-geo-restriction-rule-group</artifactId>
</dependency>
```

## Example

```python
import { WafGeoRestrictRuleGroup } from '@gammarer/aws-waf-geo-restriction-rule-group';

new WafGeoRestrictRuleGroup(stack, 'WafGeoRestrictRuleGroup', {
  scope: Scope.GLOBAL, // GLOBAL(CloudFront) or REIGONAL(Application Load Balancer (ALB), Amazon API Gateway REST API, an AWS AppSync GraphQL API, or an Amazon Cognito user pool)
  allowCountries: ['JP'], // alpha-2 country and region codes from the International Organization for Standardization (ISO) 3166 standard
});
```

## License

This project is licensed under the Apache-2.0 License.
