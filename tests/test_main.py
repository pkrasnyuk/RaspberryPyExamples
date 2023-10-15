from unittest import TestCase
from unittest.mock import patch

from sensors.__main__ import main
from sensors.data_processing.wheather_data_processing import WheatherDataProcessing
from sensors.helpers.app_handlers import AppHandlers
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.lcd_service import LCDService


class TestMain(TestCase):
    @patch("sensors.__main__", return_value=None)
    def test_main(self, main):
        """
        GIVEN: sensors.__main__ class
        WHEN: check main method signature
        THEN: expected signature returned
        """
        self.assertIsNone(main())

    def test_main_2(self):
        """
        GIVEN: sensors.__main__ class
        WHEN: execute main method
        THEN: expected result returned
        """
        with patch.object(WheatherDataProcessing, "processing", return_value=None):
            main(handlers=AppHandlers(), lcd_service=LCDService(), dht_sensor_service=DHTSensorService())
