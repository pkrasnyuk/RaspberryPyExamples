from typing import Any
from unittest import TestCase
from unittest.mock import patch
import sensors

from sensors.__main__ import main
from sensors.helpers.app_handlers import AppHandlers
from sensors.services.simple_sensors_service import SimpleSensorsService


class TestMain(TestCase):

    @patch("sensors.__main__", return_value=None)
    def test_main(self, main):
        """
        GIVEN: sensors.__main__ class
        WHEN: check main method signature
        THEN: expected signature returned
        """
        self.assertIsNone(main(handlers=Any, sensors_service_interface=Any))

    
    def test_main_2(self):
        """
        GIVEN: sensors.__main__ class
        WHEN: execute main method
        THEN: expected result returned
        """
        with patch.object(SimpleSensorsService, "get_humidity_and_temperature", return_value=None):
            main(handlers=AppHandlers(), sensors_service_interface=SimpleSensorsService())
