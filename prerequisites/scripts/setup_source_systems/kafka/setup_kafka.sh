mkdir -p ~/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/systems

cd ~/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/systems


wget -nc https://downloads.apache.org/kafka/4.3.1/kafka_2.13-4.3.1.tgz

tar -xzf kafka_2.13-4.3.1.tgz

mv kafka_2.13-4.3.1 kafka

ls kafka

./kafka/bin/kafka-topics.sh --version

./kafka/bin/kafka-storage.sh random-uuid # 8Ukmf5BBRs-ZO7moQSk4EA

./kafka/bin/kafka-storage.sh format --standalone -t 8Ukmf5BBRs-ZO7moQSk4EA -c ./kafka/config/server.properties

./kafka/bin/kafka-server-start.sh ./kafka/config/server.properties

./kafka/bin/kafka-topics.sh  --bootstrap-server localhost:9092 --list

./kafka/bin/kafka-topics.sh --create --topic TelecomUsage --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

./kafka/bin/kafka-topics.sh  --bootstrap-server localhost:9092 --list

./kafka/bin/kafka-topics.sh --describe --topic TelecomUsage --bootstrap-server localhost:9092

# run the producer

#  then test with a consumer

./kafka/bin/kafka-console-consumer.sh  --bootstrap-server localhost:9092 --topic TelecomUsage --from-beginning


# ./kafka/bin/kafka-topics.sh --delete --topic TelecomUsage --bootstrap-server localhost:9092
