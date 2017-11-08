#!/usr/bin/env bash
#
# Copyright © 2016 Dell Inc. or its subsidiaries. All Rights Reserved.
# VCE Confidential/Proprietary Information
#
source $(realpath $(dirname $0)/../)/lib/process_docker

SERVICE_BASE=/opt/dell/cpsd/rackhd/

echo "Removing Dell Inc. Consul components"
echo "This will take a few minutes and several services will be restarted on the system. This is normal and please let the script run to completion"

pushd ${SERVICE_BASE}/install

echo "Stopping Dell Inc. Consul components"
docker-compose down

echo "Deleting the Consul components for Dell Inc."
process_docker delete docker-compose.yml

popd

umount /opt/dell/cpsd/rackhd/iso/esxi/6.0
umount /opt/dell/cpsd/rackhd/iso/esxi/6.0-dell

sed -i '/\/opt\/dell\/cpsd\/rackhd/d' /etc/fstab

sed -i '/\/opt\/dell\/public/d' /etc/exports

echo "Cleaning up the ${SERVICE_BASE} directory"
rm -rf ${SERVICE_BASE}/

echo "Dell Inc. Consul components removal has completed successfully"
