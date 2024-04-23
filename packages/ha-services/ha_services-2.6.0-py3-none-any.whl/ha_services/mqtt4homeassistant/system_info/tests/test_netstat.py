import json
from unittest import TestCase

from bx_py_utils.test_utils.snapshot import assert_snapshot

from ha_services.mqtt4homeassistant.device import MqttDevice
from ha_services.mqtt4homeassistant.mocks import HostSystemMock
from ha_services.mqtt4homeassistant.mocks.mqtt_client_mock import MqttClientMock
from ha_services.mqtt4homeassistant.system_info.netstat import NetStatSensor, NetStatSensors


class NetStatSensorsTestCase(TestCase):

    def test_happy_path(self):
        with HostSystemMock(), self.assertLogs('ha_services', level='DEBUG'):
            netstat_sensors = NetStatSensors(
                device=MqttDevice(name='foo', uid='bar'),
            )
            sensor = netstat_sensors.sensors['eth0']
            self.assertIsInstance(sensor, NetStatSensor)
            self.assertEqual(
                sensor.bytes_sent_sensor.get_state().topic,
                'homeassistant/sensor/bar/bar-eth0sent/state',
            )

            mqtt_client_mock = MqttClientMock()
            netstat_sensors.publish(mqtt_client_mock)
        topics = [message['topic'] for message in mqtt_client_mock.messages]
        self.assertEqual(
            topics,
            [
                'homeassistant/sensor/bar/bar-eth0sent/config',
                'homeassistant/sensor/bar/bar-eth0sent/state',
                'homeassistant/sensor/bar/bar-eth0sentrate/config',
                'homeassistant/sensor/bar/bar-eth0sentrate/state',
                'homeassistant/sensor/bar/bar-eth0received/config',
                'homeassistant/sensor/bar/bar-eth0received/state',
                'homeassistant/sensor/bar/bar-eth0receivedrate/config',
                'homeassistant/sensor/bar/bar-eth0receivedrate/state',
            ],
        )
        configs = [
            json.loads(message['payload']) for message in mqtt_client_mock.messages if '/config' in message['topic']
        ]
        assert_snapshot(got=configs)
