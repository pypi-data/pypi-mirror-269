import sys
import unittest
from src.DLMSFirmwareUpdater import main


class TestType(unittest.TestCase):
    def test_Serial(self):
        sys.argv.extend(('-t', "Serial", "-p", "COM13", "-T", "1", '-s', "0000000000000000"))
        main.main()

    def test_File(self):
        sys.argv.extend(('-t', "File", "-p", "конфигурация GSM.csv"))
        main.main()
