from unittest import TestCase

from ha_services.mqtt4homeassistant.components.switch import Switch
from ha_services.mqtt4homeassistant.data_classes import ComponentConfig, ComponentState
from ha_services.mqtt4homeassistant.device import MqttDevice


class SwitchTestCase(TestCase):
    def test_switch(self):
        switch = Switch(
            device=MqttDevice(name='My Device', uid='device1'),
            name='My Switch',
            uid='switch1',
        )
        self.assertEqual(
            switch.get_config(),
            ComponentConfig(
                topic='homeassistant/switch/device1/device1-switch1/config',
                payload={
                    'command_topic': 'homeassistant/switch/device1/device1-switch1/command',
                    'component': 'switch',
                    'device': {'identifiers': 'device1', 'name': 'My Device'},
                    'json_attributes_topic': 'homeassistant/switch/device1/device1-switch1/attributes',
                    'name': 'My Switch',
                    'payload_off': 'OFF',
                    'payload_on': 'ON',
                    'state_topic': 'homeassistant/switch/device1/device1-switch1/state',
                    'unique_id': 'device1-switch1',
                },
            ),
        )
        self.assertEqual(
            switch.get_state(),
            ComponentState(topic='homeassistant/switch/device1/device1-switch1/state', payload=None),
        )
        with self.assertRaises(AssertionError) as cm:
            switch.set_state('invalid_state')
        self.assertEqual(str(cm.exception), 'Invalid state: invalid_state')

        switch.set_state('ON')
        self.assertEqual(
            switch.get_state(),
            ComponentState(topic='homeassistant/switch/device1/device1-switch1/state', payload='ON'),
        )
