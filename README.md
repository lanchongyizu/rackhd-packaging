[![License](https://img.shields.io/badge/License-EPL%201.0-red.svg)](https://opensource.org/licenses/EPL-1.0)
[![Build Status](https://travis-ci.org/dellemc-symphony/credential-service-parent.svg?branch=master)](https://travis-ci.org/dellemc-symphony/credentia-service-parent)
[![Slack](http://community.codedellemc.com/badge.svg)](https://codecommunity.slack.com/messages/symphony)
[![Codecov](https://img.shields.io/codecov/c/github/dellemc-symphony/credential-service-parent.svg)](https://codecov.io/gh/dellemc-symphony/credential-service-parent)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/com.dell.cpsd/credential-service-parent/badge.svg)](https://maven-badges.herokuapp.com/maven-central/com.dell.cpsd/credential-service-parent)
[![Semver](http://img.shields.io/SemVer/2.0.0.png)](http://semver.org/spec/v2.0.0.html)

# thirdparty-rpm-generator

## Description
This respository contains the code to customize versions of the following third-party applications: Consul, Vault, RabbitMQ, PostgreSQL and RackHD. Each third-party application is deployed as a Docker image which is then packaged into an rpm.

## Documentation
You can find additional documentation for Project Symphony at [dellemc-symphony.readthedocs.io][documentation].

## Before you begin
### For Linux development
Verify that the latest versions of the following tools are installed:
* Docker community edition 
* rpm-build

### For Windows development
Windows development is not currently supported.

## Building
1. Navigate to the `thirdparty-rpm-generator` folder.
2. Run the following command to update the version of the rpms:

` ./unsupported/update-version-number`

3. Run the following command to build the rpms:

`./create_rpms`

The following rpms should be inside the `target/rpmbuild/RPMS/x86_64/ folder`:
* `dell-cpsd-consul-<version>.x86_64.rpm`
* `dell-cpsd-postgres-<version>.x86_64.rpm`
* `dell-cpsd-rabbitmq-<version>.x86_64.rpm`
* `dell-cpsd-vault-<version>.x86_64.rpm`
   
## Deploying
Run the following command to update the yum cache: 

`yum makecache fast`

Run the following command to install the rpm:

`yum localinstall ./target/rpmbuild/RPMS/x86_64/dell-cpsd-<rpm name>-<version>.x86_64.rpm`

## Community
Reach out to us on the Slack [#symphony][slack] channel. Request an invite at [{code}Community][codecommunity].

You can also join [Google Groups][googlegroups] and start a discussion.

[slack]: https://codecommunity.slack.com/messages/symphony
[googlegroups]: https://groups.google.com/forum/#!forum/dellemc-symphony
[codecommunity]: http://community.codedellemc.com/
[contributing]: http://dellemc-symphony.readthedocs.io/en/latest/contributingtosymphony.html
[github]: https://github.com/dellemc-symphony
[documentation]: https://dellemc-symphony.readthedocs.io/en/latest/
