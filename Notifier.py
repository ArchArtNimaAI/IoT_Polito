class Notifier:
    def notify(self, topic, payload):
        print("[Notifier] Received a message on topic %s: %s" % (topic, payload))
