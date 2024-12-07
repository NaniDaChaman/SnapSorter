# Use the Confluent Kafka image
FROM apache/kafka

# Copy your custom server.properties file into the container
COPY /configuration_files/server.properties /opt/kafka/config/server.properties
COPY /configuration_files/consumer.properties /opt/kafka/config/consumer.properties
COPY /configuration_files/producer.properties /opt/kafka/config/producer.properties
COPY /configuration_files/zookeeper.properties /opt/kafka/config/zookeeper.properties

# Expose the default Kafka port
EXPOSE 9092
EXPOSE 2021
#RUN ./opt/kafka/bin/zookeeper-server-start.sh opt/kafka/config/zookeeper.properties
#RUN ./opt/kafka/bin/kafka-server-start.sh opt/kafka/config/server.properties


# Use the server.properties file when starting Kafka
#CMD ["./opt/kafka/bin/zookeeper-server-start.sh", "opt/kafka/config/zookeeper.properties"]