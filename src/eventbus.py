from pubsub import pub


def emit(topic: str, **data):
    return pub.sendMessage(topic, data)

def on(topic: str, callback):
    return pub.subscribe(callback, topic)