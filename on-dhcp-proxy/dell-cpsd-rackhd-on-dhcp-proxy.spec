#
# Copyright (c) 2017 Dell Inc. or its subsidiaries.  All Rights Reserved.
# Dell EMC Confidential/Proprietary Information
#

%define _source %_name-%_version.tgz

Summary: Dell Inc. RackHD ON DHCP PROXY
Name:    %_name
Version: %_version
Release: %_revision
Source:  %_source
License: Commercial
Vendor: Dell Inc.
Group: System Environment/Dell Inc. Applications
URL: http://www.dell.com
BuildArch: %(uname -m)
Requires: dell-cpsd-container-bootstrap

%description
Dell Inc. RackHD ON DHCP PROXY

%define  debug_package %{nil}

%prep
%setup -q

%build

%pre

getent group dell >/dev/null || /usr/sbin/groupadd -f -r dell
getent passwd rabbit >/dev/null || /usr/sbin/useradd -r -g dell -s /sbin/nologin -M rabbit
exit 0

%install

install -D on-dhcp-proxy.tar %{buildroot}/opt/dell/cpsd/rackhd/on-dhcp-proxy/image/on-dhcp-proxy.tar


%post

if [ $1 -eq 1 ];then
    RETVAL=0

    SERVICE_BASE=/opt/dell/cpsd/rackhd/on-dhcp-proxy

    echo "Installing Dell Inc. RackHD ON DHCP PROXY components"

    if [ ! -d "$SERVICE_BASE" ]; then
        echo "Could not find directory - [$SERVICE_BASE] does not exist."
        exit 1
    fi

    usermod -aG docker core

    docker load -i ${SERVICE_BASE}/image/on-dhcp-proxy.tar

    echo "Dell Inc. RackHD ON DHCP PROXY components install has completed successfully."

    exit 0
elif [ $1 -eq 2 ];then
    echo "Upgrade is not possible with this rpm"
    exit 1
else
    echo "Unexpected argument passed to RPM %post script: [$1]"
    exit 1
fi
exit 0

%preun

if [ $1 -eq 0 ];then
    SERVICE_BASE=/opt/dell/cpsd/rackhd/on-dhcp-proxy

    echo "Removing Dell Inc. ON DHCP PROXY components"
    echo "This will take a few minutes and several services will be restarted on the system. This is normal and please let the script run to completion"

    echo "Deleting the RackHD ON DHCP PROXY components for Dell Inc."
    /usr/bin/docker rmi $(docker images -q on-dhcp-proxy)

    echo "Dell Inc. RackHD ON DHCP PROXY components removal has completed successfully"
fi
exit 0

%files

%attr(0754,rabbit,dell) %dir /opt/dell/cpsd/rackhd/on-dhcp-proxy
%attr(0755,rabbit,dell) %dir /opt/dell/cpsd/rackhd/on-dhcp-proxy/image
%attr(0644,root,root) /opt/dell/cpsd/rackhd/on-dhcp-proxy/image/on-dhcp-proxy.tar