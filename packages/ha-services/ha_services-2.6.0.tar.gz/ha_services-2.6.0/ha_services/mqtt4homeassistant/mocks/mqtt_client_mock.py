

class MqttClientMock:
    def __init__(self):
        self.messages = []

    def publish(self, **kwargs) -> None:
        self.messages.append(kwargs)
