# !!!Declarer les variables pour eviter de repeter les chemins de fichier
mkdir -p ~/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/systems

cd ~/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/systems


wget -nc https://downloads.apache.org/kafka/4.3.1/kafka_2.13-4.3.1.tgz

tar -xzf kafka_2.13-4.3.1.tgz

mv kafka_2.13-4.3.1 kafka

ls kafka

./kafka/bin/kafka-topics.sh --version

# ./kafka/bin/kafka-storage.sh random-uuid # 8Ukmf5BBRs-ZO7moQSk4EA

./kafka/bin/kafka-storage.sh format --standalone -t 8Ukmf5BBRs-ZO7moQSk4EA -c ./kafka/config/server.properties

./kafka/bin/kafka-server-start.sh ./kafka/config/server.properties

sleep 5

./kafka/bin/kafka-topics.sh  --bootstrap-server localhost:9092 --delete --topic TelecomUsage 2>/dev/null || true
/kafka/bin/kafka-topics.sh  --bootstrap-server localhost:9092 --delete --topic __consumer_offsets 2>/dev/null || true
 

./kafka/bin/kafka-topics.sh --create --topic TelecomUsage --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

sleep 5

./kafka/bin/kafka-topics.sh  --bootstrap-server localhost:9092 --list
./kafka/bin/kafka-topics.sh --describe --topic TelecomUsage --bootstrap-server localhost:9092

# ./kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TelecomUsage --from-beginning

# ./kafka/bin/kafka-topics.sh  --bootstrap-server localhost:9092 --delete --topic TelecomUsage
# /kafka/bin/kafka-topics.sh  --bootstrap-server localhost:9092 --delete --topic __consumer_offsets
 