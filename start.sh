start  zookeeper & kafka :

 /root/kafka/zookeeper/bin/zkServer.sh start
/root/kafka/kafka/bin/kafka-server-start.sh /root/kafka/kafka/config/server.properties


start bro:
vim /usr/local/bro/etc/node.cfg

host改成自己的ip

cd /usr/local/bro/bin

./broctl

deploy
start

测试收消息
/root/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic bro --from-beginning
