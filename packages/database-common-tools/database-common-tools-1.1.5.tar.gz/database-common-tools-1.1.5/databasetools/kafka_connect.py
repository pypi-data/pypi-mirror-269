# -*- coding: utf-8 -*-

from kafka import KafkaConsumer,TopicPartition


##################################################
# kafka function
##################################################

def kafka_consumer(topic, group, servers, offset):
    return KafkaConsumer(topic, group_id=group, bootstrap_servers=servers, auto_offset_reset=offset)

def kafka_consumer_no_offset(topic, group, servers):
    return KafkaConsumer(topic, group_id=group, bootstrap_servers=servers)

def kafka_consumer_no_offset_topic(group, servers):
    return KafkaConsumer(group_id=group, bootstrap_servers=servers)

def appoint_offset(csr, topic, _offset):
    # 创建 TopicPartition 对象，指定要操作的 topic 和 partition
    partitions = csr.partitions_for_topic(topic)
    # 遍历所有 partition
    for partition in partitions:
        # 创建 TopicPartition 对象，指定要操作的 topic 和 partition
        tp = TopicPartition(topic, partition)
        # 设置消费者的偏移量
        csr.assign([tp])
        csr.seek(tp, _offset)
