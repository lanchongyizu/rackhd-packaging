[![License](https://img.shields.io/badge/License-EPL%201.0-red.svg)](https://opensource.org/licenses/EPL-1.0)
[![Build Status](https://travis-ci.org/dellemc-symphony/credential-service-parent.svg?branch=master)](https://travis-ci.org/dellemc-symphony/credentia-service-parent)
[![Slack](http://img.shields.io/badge/slack-join%20the%20chat-00B9FF.svg?style=flat-square)](https://codecommunity.slack.com/messages/symphony)
[![Codecov](https://img.shields.io/codecov/c/github/dellemc-symphony/credential-service-parent.svg)](https://codecov.io/gh/dellemc-symphony/credential-service-parent)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/com.dell.cpsd/credential-service-parent/badge.svg)](https://maven-badges.herokuapp.com/maven-central/com.dell.cpsd/credential-service-parent)
[![Semver](http://img.shields.io/SemVer/2.0.0.png)](http://semver.org/spec/v2.0.0.html)

# thirdparty-rpm-generator

## Description
This respository contains the code to customize versions of RackHD. Each RackHD component is deployed as a Docker image which is then packaged into an rpm.

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
1. Navigate to the project home directory.
2. Run the following command to update the version of the rpms:

` ./unsupported/update-version-number`

3. Run the following command to build the rpms:

`./create_rpms`

The following rpms should be inside the `target/rpmbuild/RPMS/x86_64/ folder`:
* `dell-cpsd-rackhd-device-discovery-<version>.x86_64.rpm`
* `dell-cpsd-rackhd-files-<version>.x86_64.rpm`
* `dell-cpsd-rackhd-isc-dhcp-server-<version>.x86_64.rpm`
* `dell-cpsd-rackhd-all-<version>.x86_64.rpm`
and more rpms for each RackHD component.
   
## Deploying
Run the following command to update the yum cache: 

`yum makecache fast`

Run the following command to install the rpm:

For full RackHD install:
`yum localinstall ./target/rpmbuild/RPMS/x86_64/dell-cpsd-rackhd-all-<version>.x86_64.rpm`
Alternatively for individual rpm install:
`yum localinstall ./target/rpmbuild/RPMS/x86_64/dell-cpsd-rackhd-<rpm name>-<version>.x86_64.rpm`

For remote install using master repo:
`yum install dell-cpsd-rackhd-all`

## Community
Reach out to us on the Slack [#symphony][slack] channel. Request an invite at [{code}Community][codecommunity].

You can also join [Google Groups][googlegroups] and start a discussion.

[slack]: https://codecommunity.slack.com/messages/symphony
[googlegroups]: https://groups.google.com/forum/#!forum/dellemc-symphony
[codecommunity]: http://community.codedellemc.com/
[contributing]: http://dellemc-symphony.readthedocs.io/en/latest/contributingtosymphony.html
[github]: https://github.com/dellemc-symphony
[documentation]: https://dellemc-symphony.readthedocs.io/en/latest/
