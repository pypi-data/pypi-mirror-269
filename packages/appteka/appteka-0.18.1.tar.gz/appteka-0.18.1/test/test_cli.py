import unittest
from appteka.cli import ProgressMessages
from time import sleep


class Test_ProgressMessages(unittest.TestCase):

    def setUp(self):
        self.text = ""

    def test_touch(self):
        pms = ProgressMessages(output=self)
        pms.begin("proc")
        sleep(1)
        pms.end()

        self.assertTrue("proc ..." in self.text)
        self.assertTrue("ready" in self.text)
        self.assertTrue("sec]" in self.text)

    def write(self, text):
        self.text += text

    def flush(self):
        pass
