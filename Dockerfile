FROM centos:6
RUN ln -sf /usr/share/zoneinfo/Japan /etc/localtime

RUN yum install -y https://centos6.iuscommunity.org/ius-release.rpm
RUN yum install -y python36*

COPY src/* /nlp/

ENTRYPOINT python3.6 /nlp/test.py >> /nlp/log/log.txt
