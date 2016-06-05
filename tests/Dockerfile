# - run sshd with builder user's public key
#   so that builder can ssh directly in as root
#
FROM centos:7

RUN yum -y install openssh-server initscripts
RUN /usr/sbin/sshd-keygen
RUN mkdir /root/.ssh
COPY ./tmp/id_dsa.pub /root/.ssh/authorized_keys
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
