__author__ = 'atrimble'


def get_topic_string(topic, partition):
    return topic + "(" + partition + ")"


def get_topic(topic_partition):
    if '(' in topic_partition:
        return topic_partition.split("\\(")[0]
    return topic_partition


def get_partition(topic_partition):
    if '(' in topic_partition:
        spl = topic_partition.split("\\(")
        if spl.length > 1:
            return spl[1]

    return '.*'
