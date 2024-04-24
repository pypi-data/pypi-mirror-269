from pyPhases.test.TestCase import TestCase
from pyPhasesRecordloader import RecordLoader

from SleepHarmonizer.phases.Setup import Setup


class TestSetup(TestCase):
    phase = Setup()
    
    def testConfigValues(self):
        self.assertIn("RecordLoaderAlice", RecordLoader.recordLoaders)