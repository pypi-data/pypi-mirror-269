import datetime
from unittest import TestCase

from ha_services.mqtt4homeassistant.utilities.system_utils import get_system_start_datetime, process_start_datetime


class SystemUtilsTestCase(TestCase):

    def test_get_system_start_datetime(self):
        start_dt = get_system_start_datetime()
        self.assertIsInstance(start_dt, datetime.datetime)

    def test_process_start_datetime(self):
        start_dt = process_start_datetime()
        self.assertIsInstance(start_dt, datetime.datetime)
