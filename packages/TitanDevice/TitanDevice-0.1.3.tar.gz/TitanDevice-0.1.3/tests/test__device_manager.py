import unittest

from titan._device_exception import DeviceNoFoundException
from titan._device_manager import _DeviceManager
from unittest.mock import patch, MagicMock


class _DeviceManagerTests(unittest.TestCase):
    @patch("titan._device_manager.adb")
    def test_get_all_devices(self, mock_adb):
        mock_device1 = MagicMock()
        mock_device1.info = {"model": "pixel3", "serial": "12"}
        mock_device2 = MagicMock()
        mock_device2.info = {"model": "nexus5", "serial": "23"}
        mock_adb.device_list.return_value = [mock_device1, mock_device2]

        devices = _DeviceManager.get_all_devices()
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0], {"model": "pixel3", "serial": "12"})
        self.assertEqual(devices[1], {"model": "nexus5", "serial": "23"})

        mock_adb.device_list.assert_called_once()


if __name__ == "__main__":
    unittest.main()
