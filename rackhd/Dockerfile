FROM docker.io/rackhd/on-taskgraph:2.29.0

RUN echo 'deb http://linux.dell.com/repo/community/ubuntu wheezy openmanage' | tee -a /etc/apt/sources.list.d/linux.dell.com.sources.list
RUN gpg --keyserver hkp://pool.sks-keyservers.net:80 --recv-key 1285491434D8786F
RUN gpg -a --export 1285491434D8786F | apt-key add -
RUN apt-get update
RUN apt-get install -y srvadmin-idracadm7

# Pull in fix to allow Graph.Dell.Wsman.UpdateSystemComponents to set
# BiosBootSeq and HddSeq.
#
# NOTE: These are merged and will be in 2.30.0
#
# https://github.com/RackHD/on-taskgraph/pull/297/commits
# https://github.com/RackHD/on-tasks/pull/521/commits

COPY on-taskgraph-force-update-89395df.patch ./
RUN patch -p1 -d /RackHD/on-taskgraph < on-taskgraph-force-update-89395df.patch

COPY on-tasks-force-update-a851300.patch ./
RUN patch -p1 -d /RackHD/on-tasks < on-tasks-force-update-a851300.patch

# Pull in fix to properly format ipmi-user-list catalog data
#
# https://github.com/RackHD/on-tasks/pull/523

COPY on-tasks-ipmi-user-list-b16603c.patch ./
RUN patch -p1 -d /RackHD/on-tasks < on-tasks-ipmi-user-list-b16603c.patch

# Add ESXi installer option for clearing disk partitions
#
# https://github.com/RackHD/on-taskgraph/pull/309
# https://github.com/RackHD/on-tasks/pull/532

COPY on-taskgraph-esx-clearpart-6cb8a5a.patch ./
RUN patch -p1 -d /RackHD/on-taskgraph < on-taskgraph-esx-clearpart-6cb8a5a.patch

COPY on-tasks-esx-clearpart-a5ba0af.patch ./
RUN patch -p1 -d /RackHD/on-tasks < on-tasks-esx-clearpart-a5ba0af.patch


# Various fixes for UpdateSystemConfig after wsman refactor
#
# The wsman jobs were heavily refactored in 2.29.0 and the
# UpdateSystemComponents job broke.
#
# https://github.com/RackHD/on-tasks/pull/545

COPY on-tasks-fix-update-components-timeout-08fb7a.patch ./
RUN patch -p1 -d /RackHD/on-tasks < on-tasks-fix-update-components-timeout-08fb7a.patch
