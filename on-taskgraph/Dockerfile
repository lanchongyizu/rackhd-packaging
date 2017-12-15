ARG TAG
FROM docker.io/rackhd/on-taskgraph:${TAG}

RUN echo 'deb http://linux.dell.com/repo/community/ubuntu wheezy openmanage' | tee -a /etc/apt/sources.list.d/linux.dell.com.sources.list
RUN gpg --keyserver hkp://pool.sks-keyservers.net:80 --recv-key 1285491434D8786F
RUN gpg -a --export 1285491434D8786F | apt-key add -
RUN apt-get update
RUN apt-get install -y srvadmin-idracadm7

# Pull in fix to properly format ipmi-user-list catalog data
#
# https://github.com/RackHD/on-tasks/pull/523

COPY patches/on-tasks-ipmi-user-list-b16603c.patch ./
RUN patch -p1 -d /RackHD/on-tasks < on-tasks-ipmi-user-list-b16603c.patch

# Add ESXi installer option for clearing disk partitions
#
# https://github.com/RackHD/on-taskgraph/pull/309
# https://github.com/RackHD/on-tasks/pull/532

COPY patches/on-taskgraph-esx-clearpart-6cb8a5a.patch ./
RUN patch -p1 -d /RackHD/on-taskgraph < on-taskgraph-esx-clearpart-6cb8a5a.patch

COPY patches/on-tasks-esx-clearpart-a5ba0af.patch ./
RUN patch -p1 -d /RackHD/on-tasks < on-tasks-esx-clearpart-a5ba0af.patch

# Add RHEL installer options for adding packages and clearing partitions
#
# https://github.com/RackHD/on-taskgraph/pull/343
# https://github.com/RackHD/on-tasks/pull/568

COPY patches/on-taskgraph-dne-rhel-583e0f2.patch ./
RUN patch -p1 -d /RackHD/on-taskgraph < on-taskgraph-dne-rhel-583e0f2.patch

COPY patches/on-tasks-dne-rhel-19b89dd.patch ./
RUN patch -p1 -d /RackHD/on-tasks < on-tasks-dne-rhel-19b89dd.patch
