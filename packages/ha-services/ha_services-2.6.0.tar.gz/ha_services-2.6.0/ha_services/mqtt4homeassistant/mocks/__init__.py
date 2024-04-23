from unittest.mock import patch

from bx_py_utils.test_utils.context_managers import MassContextManager

from ha_services.mqtt4homeassistant.components import get_origin_data
from ha_services.mqtt4homeassistant.mocks.psutil_mock import PsutilMock


class HostSystemMock(MassContextManager):
    def __init__(self):

        psutil_mock = PsutilMock()

        origin_data = get_origin_data()
        origin_data['name'] = 'ha-services-tests'
        origin_data['sw_version'] = '1.2.3'

        self.mocks = (
            patch('ha_services.mqtt4homeassistant.components.get_origin_data', return_value=origin_data),
            patch('ha_services.mqtt4homeassistant.device.socket.gethostname', return_value='TheHostName'),
            #
            patch('ha_services.mqtt4homeassistant.system_info.cpu.psutil', psutil_mock),
            patch('ha_services.mqtt4homeassistant.system_info.memory.psutil', psutil_mock),
            patch('ha_services.mqtt4homeassistant.system_info.temperatures.psutil', psutil_mock),
            patch('ha_services.mqtt4homeassistant.utilities.system_utils.psutil', psutil_mock),
        )
