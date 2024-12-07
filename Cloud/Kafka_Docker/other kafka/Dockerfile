FROM ubuntu:20.04

#RUN apt-get update
#RUN apt-get upgrade -y
#RUN apt install curl -y
#RUN apt update
#RUN apt install default-jre -y
#RUN apt-get install -y python3-dev python3-pip
#RUN apt-get install -y kafka-python
#RUN curl https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz
#RUN zcat kafka_2.13-2.8.0.tgz | tar xpof -

#COPY kafka.tgz home/
#RUN tar -xvzf ~/home/kafka.tgz

RUN apt-get -y update && apt-get install -y net-tools wget dnsutils iputils-ping iputils-tracepath iputils-arping iputils-clockdiff default-jdk python3
RUN apt-get install -y python3-dev python3-pip
#RUN python3 -m pip install --upgrade pip

RUN wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz
RUN zcat kafka_2.13-2.8.0.tgz | tar xpof -

# COPY home/cc/server.properties /kafka_2.13-2.6.0/config/

# CMD /bin/bash

