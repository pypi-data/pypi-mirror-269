import logging

from ha_services.mqtt4homeassistant.components import BaseComponent
from ha_services.mqtt4homeassistant.data_classes import ComponentConfig, ComponentState
from ha_services.mqtt4homeassistant.device import MqttDevice


logger = logging.getLogger(__name__)


class BinarySensor(BaseComponent):
    """
    MQTT Switch component for Home Assistant.
    https://www.home-assistant.io/integrations/binary_sensor.mqtt/

    """

    ON = 'ON'
    OFF = 'OFF'

    def __init__(
        self,
        *,
        device: MqttDevice,
        name: str,
        uid: str,
        component: str = 'binary_sensor',
        device_class: str | None = None,  # https://www.home-assistant.io/integrations/binary_sensor/#device-class
    ):
        super().__init__(device=device, name=name, uid=uid, component=component)

        self.device_class = device_class

        self.state2bool = {
            self.ON: True,
            self.OFF: False,
        }
        self.state = None

    @property
    def is_on(self) -> bool:
        if self.state is not None:
            return self.state2bool[self.state]

    def set_state(self, state: str):
        assert state in self.state2bool, f'Invalid state: {state}'
        self.state = state

    def get_state(self) -> ComponentState:
        # e.g.: {'topic': 'homeassistant/switch/My-device/My-BinarySensor/state', 'payload': 'ON'}
        return ComponentState(
            topic=f'{self.topic_prefix}/state',
            payload=self.state,
        )

    def get_config(self) -> ComponentConfig:
        return ComponentConfig(
            topic=f'{self.topic_prefix}/config',
            payload={
                'component': self.component,
                'device': self.device.get_mqtt_payload(),
                'device_class': self.device_class,  # e.g.: 'door', 'motion', etc...
                'name': self.name,
                'unique_id': self.uid,
                'payload_off': self.OFF,
                'payload_on': self.ON,
                'state_topic': f'{self.topic_prefix}/state',
                'json_attributes_topic': f'{self.topic_prefix}/attributes',
            },
        )
