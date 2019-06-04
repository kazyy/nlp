FROM centos:6
RUN ln -sf /usr/share/zoneinfo/Japan /etc/localtime

RUN yum install -y https://centos6.iuscommunity.org/ius-release.rpm
RUN yum install -y python36*
RUN pip3.6 install --upgrade pip
RUN pip3.6 install requests
RUN pip3.6 install beautifulsoup4

COPY src/* /nlp/

ENTRYPOINT /bin/bash
