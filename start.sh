ip addr add 10.10.28.1/16 dev eth0
ip route add default via 10.10.0.1

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
