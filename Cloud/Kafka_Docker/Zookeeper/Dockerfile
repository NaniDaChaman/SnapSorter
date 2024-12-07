# Use the official Zookeeper image
FROM zookeeper:3.7.0

# Expose the default Zookeeper client port
EXPOSE 2181

# Start Zookeeper server
CMD ["/bin/bash", "-c", "zkServer.sh start-foreground"]