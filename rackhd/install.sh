#!/usr/bin/env bash
#
# Copyright (c) 2017 Dell Inc. or its subsidiaries.  All Rights Reserved.
# Dell EMC Confidential/Proprietary Information
#
source $(realpath $(dirname $0)/../)/lib/process_docker

RETVAL=0

SERVICE_BASE=/opt/dell/cpsd/rackhd/

echo "Installing Dell Inc. Consul components"

if [ ! -d "$SERVICE_BASE" ]; then
    echo "Could not find directory - [$SERVICE_BASE] does not exist."
    exit 1
fi

usermod -aG docker rackhd

# Set up NFS shares
if ! grep -q /opt/dell/public /etc/exports; then
    echo "/opt/dell/public        *(rw,sync,no_subtree_check)" >> /etc/exports

    systemctl enable nfs
    systemctl start nfs
fi

pushd ${SERVICE_BASE}/install
source ${SERVICE_BASE}/install/.env
process_docker load docker-compose.yml
popd

if ! grep -q /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell /etc/fstab; then
    echo "/opt/dell/cpsd/rackhd/iso/VMware-VMvisor-Installer-6.0.0.update03-5224934.x86_64-Dell_Customized-A01.iso /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell iso9660 loop 0 0" >> /etc/fstab
    echo "/opt/dell/cpsd/rackhd/iso/ESXi-3299935-vce-Quanta.iso /opt/dell/cpsd/rackhd/iso/esxi/6.0 iso9660 loop 0 0" >> /etc/fstab

    mount /opt/dell/cpsd/rackhd/iso/esxi/6.0
    mount /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell
fi

pushd ${SERVICE_BASE}/install
export HOST_IP=$(ip addr show ens33 | grep -w inet | awk -F ' ' '{print $2}' | cut -d/ -f1)
/usr/bin/docker-compose up -d
popd

pushd ${SERVICE_BASE}/conf/smi
./set_config.sh
popd


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

pushd ${SERVICE_BASE}/conf/smi
popd

echo "Dell Inc. Consul components install has completed successfully."
exit 0
