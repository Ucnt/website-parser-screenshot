#
# docker build -t website-parser . 
# docker run -v ~/website-parser/output:/opt/parser/output --rm -it website-parser google.com
#

FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install firefox 
RUN apt-get -y install openjdk-8-jdk 
RUN apt-get -y install python3 
RUN apt-get -y install python3-pip 
RUN apt-get -y install unzip
RUN pip3 install selenium browsermob-proxy

# Copy the folder
RUN mkdir /opt/parser
COPY . /opt/parser


ENTRYPOINT ["python3", "/opt/parser/parse_page.py"] 