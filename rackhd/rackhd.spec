#
# Copyright (c) 2017 Dell Inc. or its subsidiaries.  All Rights Reserved.
# Dell EMC Confidential/Proprietary Information
#
Summary: Dell Inc. RackHD 0.7.5
Name: dell-cpsd-rackhd
Version: %_version
Release: %_revision
License: Commercial
Vendor: Dell Inc.
Group: System Environment/Dell Inc. Applications
URL: http://www.dell.com
Requires: nfs-utils
Requires: dell-cpsd-container-bootstrap

%define _use_internal_dependency_generator 0
%define __find_requires %{nil}

%description
Dell Inc. RackHD 1.0.0


##############################################################################
# build
##############################################################################
%build

# Creates directory if it doesn't exist
# $1: Directory path
init_dir ()
{
    [ -d $1 ] || mkdir -p $1
}

##############################################################################
# check and create the common directories
##############################################################################
init_dir ${RPM_BUILD_ROOT}/usr/lib/systemd/system


##############################################################################
# check and create the root directory
##############################################################################
RPM_SOURCE_BASE_DIR=${RPM_SOURCE_DIR}/rackhd
SERVICE_BASE=${RPM_BUILD_ROOT}/opt/dell/cpsd/rackhd
init_dir ${SERVICE_BASE}/image
init_dir ${SERVICE_BASE}/lib
init_dir ${SERVICE_BASE}/install
init_dir ${SERVICE_BASE}/conf
init_dir ${SERVICE_BASE}/files


##############################################################################
# copy the image to the required directory
##############################################################################
cp -r ${RPM_SOURCE_DIR}/target/*.tar ${SERVICE_BASE}/image


##############################################################################
# copy the files to the install directory
##############################################################################
echo "rpm source dir ${RPM_SOURCE_DIR}"
echo "rpm source base dir ${RPM_SOURCE_BASE_DIR}"
echo "service build dir ${IMAGES_DIR}"
cp -f ${RPM_SOURCE_BASE_DIR}/install.sh ${SERVICE_BASE}/install
cp -f ${RPM_SOURCE_BASE_DIR}/remove.sh ${SERVICE_BASE}/install
cp -f ${RPM_SOURCE_BASE_DIR}/upgrade.sh ${SERVICE_BASE}/install
cp -f ${RPM_SOURCE_BASE_DIR}/docker-compose.yml ${SERVICE_BASE}/install/docker-compose.yml
cp -f ${RPM_SOURCE_BASE_DIR}/Dockerfile ${SERVICE_BASE}/install/Dockerfile
cp -f ${RPM_SOURCE_BASE_DIR}/lib/process_docker ${SERVICE_BASE}/lib/process_docker
cp -f ${RPM_SOURCE_BASE_DIR}/.env ${SERVICE_BASE}/install
cp -rf ${RPM_SOURCE_BASE_DIR}/conf/* ${SERVICE_BASE}/conf/
mkdir -p ${SERVICE_BASE}/files/mount/common
cp -f ${RPM_SOURCE_BASE_DIR}/secure.erase.overlay.cpio.gz ${SERVICE_BASE}/files/mount/common/secure.erase.overlay.cpio.gz
mkdir -p ${SERVICE_BASE}/iso/esxi/6.0
cp -f ${RPM_SOURCE_BASE_DIR}/ESXi-3299935-vce-Quanta.iso ${SERVICE_BASE}/iso/ESXi-3299935-vce-Quanta.iso
cp -f ${RPM_SOURCE_BASE_DIR}/VMware-VMvisor-Installer-6.0.0.update03-5224934.x86_64-Dell_Customized-A01.iso ${SERVICE_BASE}/iso/VMware-VMvisor-Installer-6.0.0.update03-5224934.x86_64-Dell_Customized-A01.iso
mkdir -p ${SERVICE_BASE}/iso/esxi/6.0-dell

# Create NFS share directories
mkdir -p ${RPM_BUILD_ROOT}/opt/dell/public
mkdir -p ${RPM_BUILD_ROOT}/opt/dell/public/write

# Adds ScaleIOsdc into nfs Directory
cp -f ${RPM_SOURCE_BASE_DIR}/EMC_bootbank_scaleio-sdc-esx6.0_2.0-7058.0.vib ${RPM_BUILD_ROOT}/opt/dell/cpsd/rackhd/iso/

##############################################################################
# pre
##############################################################################
%pre
getent group dell >/dev/null || /usr/sbin/groupadd -f -r dell
getent passwd rackhd >/dev/null || /usr/sbin/useradd -r -g dell -s /sbin/nologin -M rackhd
exit 0


##############################################################################
# post
##############################################################################
%post
if [ $1 -eq 1 ];then
    /opt/dell/cpsd/rackhd/install/install.sh
elif [ $1 -eq 2 ];then
    /opt/dell/cpsd/rackhd/install/upgrade.sh
else
    echo "Unexpected argument passed to RPM %post script: [$1]"
    exit 1
fi
exit 0


##############################################################################
# preun
##############################################################################
%preun
if [ $1 -eq 0 ];then
    /bin/sh /opt/dell/cpsd/rackhd/install/remove.sh
fi
exit 0

##############################################################################
# configure directory and file permissions
##############################################################################
%files

#%attr(644,root,root) /usr/lib/systemd/system/rackhd.service

%attr(0754,rackhd,dell) /opt/dell/cpsd/rackhd/
%attr(0754,rackhd,dell) /opt/dell/cpsd/rackhd/lib
%attr(0755,rackhd,dell) /opt/dell/cpsd/rackhd/image
%attr(0755,rackhd,dell) /opt/dell/cpsd/rackhd/install
%attr(0755,rackhd,dell) /opt/dell/cpsd/rackhd/files
%attr(0755,rackhd,dell) /opt/dell/cpsd/rackhd/conf

# NFS share location used by RackHD SMI workflows
%attr(0755,rackhd,dell) /opt/dell/public

# Publicly writeable share needed by SMI Export SCP workflows
%attr(0777,rackhd,dell) /opt/dell/public/write
