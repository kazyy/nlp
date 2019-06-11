FROM centos:6
RUN ln -sf /usr/share/zoneinfo/Japan /etc/localtime

RUN yum install -y https://centos6.iuscommunity.org/ius-release.rpm
RUN yum install -y python36*
RUN pip3.6 install --upgrade pip
RUN pip3.6 install requests
RUN pip3.6 install beautifulsoup4
RUN pip3.6 install sklearn
RUN pip3.6 install nltk
RUN pip3.6 install gensim

COPY libs/* /nlp/libs/
VOLUME /usr/local/src
RUN yum install -y gcc-c++
RUN cd /nlp/libs/ && tar xf CRF++-0.58.tar.gz && cd CRF++-0.58 && ./configure && make install
RUN cd /nlp/libs/ && tar xf mecab-0.996.tar.gz && cd mecab-0.996 && ./configure --with-charset=utf8 && make install
RUN cd /nlp/libs/ && tar xf mecab-ipadic-2.7.0-20070801.tar.gz && cd mecab-ipadic-2.7.0-20070801 && ./configure --with-charset=utf-8 && make install
RUN rpm -ivh http://packages.groonga.org/centos/groonga-release-1.1.0-1.noarch.rpm
#RUN yum install -y mecab mecab-devel mecab-ipadic git make patch curl xz
RUN yum install -y git patch xz

RUN cd /usr/local/src/ && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -n -y
RUN cd /nlp/libs/ && tar xf cabocha-0.69.tar.bz2 && cd cabocha-0.69 && ./configure --with-charset=UTF8 && make install
RUN cd /nlp/libs/cabocha-0.69/python/ && python3.6 setup.py install

COPY src/* /nlp/src/

ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LANG=ja_JP.UTF8

ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT ["python3.6"]
#CMD ["/nlp/src/sample_07_08.py"]
