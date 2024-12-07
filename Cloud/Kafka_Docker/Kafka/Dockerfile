FROM ubuntu:20.04

RUN apt-get -y update && apt-get install -y net-tools wget dnsutils iputils-ping iputils-tracepath iputils-arping iputils-clockdiff default-jdk python3
RUN apt-get install -y python3-dev python3-pip

RUN wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz
RUN zcat kafka_2.13-2.8.0.tgz | tar xpof -
#FROM apache/kafka


# Expose Kafka broker port
EXPOSE 9092

# Set environment variables for Kafka to work with Zookeeper
# ENV KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
# ENV KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
# ENV KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1

# # Start Kafka server
# CMD ["/etc/confluent/docker/run"]