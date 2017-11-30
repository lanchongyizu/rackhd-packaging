#
# Copyright (c) 2017 Dell Inc. or its subsidiaries.  All Rights Reserved.
# Dell EMC Confidential/Proprietary Information
#

%define _source %_name-%_version.tgz

Summary: Dell Inc. RackHD
Name:    %_name
Version: %_version
Release: %_revision
Source:  %_source
License: Commercial
Vendor: Dell Inc.
Group: System Environment/Dell Inc. Applications
URL: http://www.dell.com
BuildArch: %(uname -m)

Requires: nfs-utils
Requires: dell-cpsd-container-bootstrap
Requires: dell-cpsd-rackhd-consul
Requires: dell-cpsd-rackhd-dell-chassis-inventory
Requires: dell-cpsd-rackhd-dell-powerthermal-monitoring
Requires: dell-cpsd-rackhd-dell-server-action
Requires: dell-cpsd-rackhd-dell-server-configuration-profile
Requires: dell-cpsd-rackhd-dell-server-firmwareupdate
Requires: dell-cpsd-rackhd-dell-server-inventory
Requires: dell-cpsd-rackhd-device-discovery
Requires: dell-cpsd-rackhd-files
Requires: dell-cpsd-rackhd-gateway
Requires: dell-cpsd-rackhd-isc-dhcp-server
Requires: dell-cpsd-rackhd-mongo
Requires: dell-cpsd-rackhd-on-dhcp-proxy
Requires: dell-cpsd-rackhd-on-http
Requires: dell-cpsd-rackhd-on-network
Requires: dell-cpsd-rackhd-on-syslog
Requires: dell-cpsd-rackhd-on-taskgraph
Requires: dell-cpsd-rackhd-on-tftp
Requires: dell-cpsd-rackhd-postgres
Requires: dell-cpsd-rackhd-rabbitmq
Requires: dell-cpsd-rackhd-swagger-aggregator
Requires: dell-cpsd-rackhd-virtualidentity
Requires: dell-cpsd-rackhd-virtualnetwork

%description
Dell Inc. RackHD

%define  debug_package %{nil}

%prep
%setup -q

%build

%pre

getent group dell >/dev/null || /usr/sbin/groupadd -f -r dell
getent passwd rackhd >/dev/null || /usr/sbin/useradd -r -g dell -s /sbin/nologin -M rackhd
exit 0

%install

mkdir -p %{buildroot}/opt/dell/cpsd/rackhd/files/mount/common
mkdir -p %{buildroot}/opt/dell/cpsd/rackhd/iso/esxi/6.0
mkdir -p %{buildroot}/opt/dell/cpsd/rackhd/iso/esxi/6.0-dell

# Create NFS share directories
mkdir -p %{buildroot}/opt/dell/public
mkdir -p %{buildroot}/opt/dell/public/write

install -d conf %{buildroot}/opt/dell/cpsd/rackhd/conf
(
    cd conf/
    tar cf - $(find . )
) | tar xvf - -C %{buildroot}/opt/dell/cpsd/rackhd/conf/

install -D install/.env %{buildroot}/opt/dell/cpsd/rackhd/install/.env
install -D install/docker-compose.yml %{buildroot}/opt/dell/cpsd/rackhd/install/docker-compose.yml
install -D secure.erase.overlay.cpio.gz %{buildroot}/opt/dell/cpsd/rackhd/files/mount/common/secure.erase.overlay.cpio.gz
install -D ESXi-3299935-vce-Quanta.iso %{buildroot}/opt/dell/cpsd/rackhd/iso/ESXi-3299935-vce-Quanta.iso
install -D VMware-VMvisor-Installer-6.0.0.update03-5224934.x86_64-Dell_Customized-A01.iso %{buildroot}/opt/dell/cpsd/rackhd/iso/VMware-VMvisor-Installer-6.0.0.update03-5224934.x86_64-Dell_Customized-A01.iso
install -D EMC_bootbank_scaleio-sdc-esx6.0_2.0-7058.0.vib %{buildroot}/opt/dell/cpsd/rackhd/iso/EMC_bootbank_scaleio-sdc-esx6.0_2.0-7058.0.vib


%post

if [ $1 -eq 1 ];then
    RETVAL=0

    SERVICE_BASE=/opt/dell/cpsd/rackhd

    echo "Installing Dell Inc. RackHD components"

    if [ ! -d "$SERVICE_BASE" ]; then
        echo "Could not find directory - [$SERVICE_BASE] does not exist."
        exit 1
    fi

    usermod -aG docker rackhd

    # Set up NFS shares
    if ! grep -q /opt/dell/public /etc/exports; then
        echo "Configuring and enabling NFS"
        echo "/opt/dell/public        *(rw,sync,no_subtree_check)" >> /etc/exports

        systemctl enable nfs
        systemctl start nfs
    fi

    if ! grep -q /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell /etc/fstab; then
        echo "Mounting ESXi images"
        echo "/opt/dell/cpsd/rackhd/iso/VMware-VMvisor-Installer-6.0.0.update03-5224934.x86_64-Dell_Customized-A01.iso /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell iso9660 loop 0 0" >> /etc/fstab
        echo "/opt/dell/cpsd/rackhd/iso/ESXi-3299935-vce-Quanta.iso /opt/dell/cpsd/rackhd/iso/esxi/6.0 iso9660 loop 0 0" >> /etc/fstab

        mount /opt/dell/cpsd/rackhd/iso/esxi/6.0
        mount /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell
    fi

    export HOST_IP=$(ip addr show ens33 | grep -w inet | awk -F ' ' '{print $2}' | cut -d/ -f1)
    (
        echo "Staring docker containers"
        cd ${SERVICE_BASE}/install
        docker-compose up -d
    )

    (
        echo "Configuring SMI Services"
        cd ${SERVICE_BASE}/conf/smi
        ./set_config.sh

        #setup the first user
        x=0
        retry_limit=60
        until curl -sk -w "%{http_code}\\n" -X POST -H Content-Type:application/json http://localhost:32080/api/current/users -d '{"username": "admin", "password": "admin123", "role": "Administrator"}' -o /dev/null | grep 201
        do
            sleep 2
            x=$(( $x + 1 ))
            if [ $x -eq $retry_limit ]
            then
                echo "ERROR: Failed to create RackHD admin user."
                exit 1
            fi
        done
    )

    echo "Dell Inc. RackHD components install has completed successfully."

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
    SERVICE_BASE=/opt/dell/cpsd/rackhd

    echo "Removing Dell Inc. RackHD components"
    echo "This will take a few minutes and several services will be restarted on the system. This is normal and please let the script run to completion"

    echo "Deleting the RackHD RackHD components for Dell Inc."

    umount /opt/dell/cpsd/rackhd/iso/esxi/6.0
    umount /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell

    sed -i '/\/opt\/dell\/cpsd\/rackhd/d' /etc/fstab

    sed -i '/\/opt\/dell\/public/d' /etc/exports

    echo "Dell Inc. RackHD RackHD components removal has completed successfully"
fi
exit 0

%files

%attr(0755,rackhd,dell) %dir /opt/dell/public
%attr(0777,rackhd,dell) %dir /opt/dell/public/write
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/install
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/conf
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/files/
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/files/mount/
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/files/mount/common
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/iso
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/iso/esxi
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/iso/esxi/6.0
%attr(0754,rackhd,dell) %dir /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell

%attr(0755,root,root) /opt/dell/cpsd/rackhd/install/.env
%attr(0644,root,root) /opt/dell/cpsd/rackhd/install/docker-compose.yml
%attr(0644,root,root) /opt/dell/cpsd/rackhd/files/mount/common/secure.erase.overlay.cpio.gz
%attr(0644,root,root) /opt/dell/cpsd/rackhd/iso/ESXi-3299935-vce-Quanta.iso
%attr(0644,root,root) /opt/dell/cpsd/rackhd/iso/VMware-VMvisor-Installer-6.0.0.update03-5224934.x86_64-Dell_Customized-A01.iso
%attr(0644,root,root) /opt/dell/cpsd/rackhd/iso/EMC_bootbank_scaleio-sdc-esx6.0_2.0-7058.0.vib

%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/dhcp/config/dhcpd.conf
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/dhcp/defaults/isc-dhcp-server
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/monorail/config.json
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/monorail/smiConfig.json
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/monorail/static/http/index.html
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/smi/device-discovery.yml
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/smi/gateway.yml
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/smi/set_config.sh
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/smi/set_rackhd_smi_config.sh
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/smi/swagger-aggregator.yml
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/smi/virtualidentity.yml
%attr(0755,root,root) /opt/dell/cpsd/rackhd/conf/smi/virtualnetwork.yml
