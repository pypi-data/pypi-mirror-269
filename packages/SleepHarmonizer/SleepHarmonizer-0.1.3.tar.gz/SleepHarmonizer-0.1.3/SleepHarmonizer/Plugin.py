from pyPhases import Data, PluginAdapter, Project
from pyPhasesRecordloader import RecordLoader

from .phases.Export import Export
from .phases.LoadData import LoadData


class Plugin(PluginAdapter):
    def __init__(self, project: Project, options=None):
        super().__init__(project, options)

        dataDep =[
            Data("metadata", self.project, ["dataBase", "dataversion.minimalSamplingRate"]),
            Data("allDBRecordIds", self.project, ["metadata", "dataversion"]),
        ]

        loadData = LoadData(dataDep)
        project.addPhase(loadData)
        project.addPhase(Export([]))

        
    def initPlugin(self):
        RecordLoader.registerRecordLoader("RecordLoaderTest", "SleepHarmonizer.recordloaders")
        RecordLoader.registerRecordLoader("RecordLoaderDomino", "SleepHarmonizer.recordloaders")
        RecordLoader.registerRecordLoader("RecordLoaderAlice", "SleepHarmonizer.recordloaders")
