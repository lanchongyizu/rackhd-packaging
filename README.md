[![License](https://img.shields.io/badge/License-EPL%201.0-red.svg)](https://opensource.org/licenses/EPL-1.0)
[![Build Status](https://travis-ci.org/dellemc-symphony/credential-service-parent.svg?branch=master)](https://travis-ci.org/dellemc-symphony/credentia-service-parent)
[![Slack](http://img.shields.io/badge/slack-join%20the%20chat-00B9FF.svg?style=flat-square)](https://codecommunity.slack.com/messages/symphony)
[![Codecov](https://img.shields.io/codecov/c/github/dellemc-symphony/credential-service-parent.svg)](https://codecov.io/gh/dellemc-symphony/credential-service-parent)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/com.dell.cpsd/credential-service-parent/badge.svg)](https://maven-badges.herokuapp.com/maven-central/com.dell.cpsd/credential-service-parent)
[![Semver](http://img.shields.io/SemVer/2.0.0.png)](http://semver.org/spec/v2.0.0.html)

# rackhd-packaging

## Description
This respository contains the code to customize versions of RackHD. Each RackHD component is deployed as a Docker image and packaged as an rpm.

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
1. Navigate to the `project home` directory.
2. To update the version of the rpms, type:

` ./unsupported/update-version-number`

3. To build the rpms, type:

`./create_rpms`

4. Ensure that the master RackHD rpm and any RackHD component rpms are in the `target/rpmbuild/RPMS/x86_64/` folder.
For example:
* `dell-cpsd-rackhd-all-<version>.x86_64.rpm`
* `dell-cpsd-rackhd-device-discovery-<version>.x86_64.rpm`
* `dell-cpsd-rackhd-files-<version>.x86_64.rpm`
* `dell-cpsd-rackhd-isc-dhcp-server-<version>.x86_64.rpm`

   
## Deploying
To update the yum cache, type: 

`yum makecache fast`

To install all RackHD rpms, type:

`yum localinstall ./target/rpmbuild/RPMS/x86_64/dell-cpsd-rackhd-all-<version>.x86_64.rpm`

To install individual RackHD rpms, type:

`yum localinstall ./target/rpmbuild/RPMS/x86_64/dell-cpsd-rackhd-<rpm name>-<version>.x86_64.rpm`

To install all RackHD rpms using the master repository, type:

`yum install dell-cpsd-rackhd-all`

## Removing
To remove all RackHD components
`yum autoremove dell-cpsd-rackhd-all`

## Community
Reach out to us on the Slack [#symphony][slack] channel. Request an invite at [{code}Community][codecommunity].

You can also join [Google Groups][googlegroups] and start a discussion.

[slack]: https://codecommunity.slack.com/messages/symphony
[googlegroups]: https://groups.google.com/forum/#!forum/dellemc-symphony
[codecommunity]: http://community.codedellemc.com/
[contributing]: http://dellemc-symphony.readthedocs.io/en/latest/contributingtosymphony.html
[github]: https://github.com/dellemc-symphony
[documentation]: https://dellemc-symphony.readthedocs.io/en/latest/
