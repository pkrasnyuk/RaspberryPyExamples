from typing import Any
from unittest import TestCase
from unittest.mock import patch

from sensors.__main__ import main


class TestMain(TestCase):
    def test_main_base(self):
        """
        GIVEN: eval.__main__ class
        WHEN: mock add_command method and execute add_command method
        THEN: expected result returned
        """
        with patch.object(main, "add_command", return_value=None):
            self.assertIsNone(main.add_command(Any))

    @patch("sensors.__main__", return_value=None)
    def test_main(self, main):
        """
        GIVEN: sensors.__main__ class
        WHEN: check main method signature
        THEN: expected signature returned
        """
        self.assertIsNone(main())
