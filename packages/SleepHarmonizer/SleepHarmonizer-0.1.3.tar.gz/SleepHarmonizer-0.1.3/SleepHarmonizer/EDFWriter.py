import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import List

import pyedflib
from pyPhases.util.Logger import classLogger
from pyPhasesRecordloader import Event, Signal


@classLogger
class EDFWriter:
    def __init__(self) -> None:
        self.patient = None

    def loadBaseAnnotationFile(self):
        self.xml = ET.parse(self.baseAnnotation)

    def writeRecord(
        self,
        recordName,
        signals: List[Signal],
        annotations: List[dict] = None,
        patient=None,
        startTime=None,
        lights=None,
        signalIsDigital=False,
    ):
        annotations = [] if annotations is None else annotations
        self.patient: dict = patient
        self.createFolderStructure(recordName)
        self.writeSignals(recordName, signals, startTime=startTime, signalIsDigital=signalIsDigital)
        self.loadBaseAnnotationFile()

        for annotation in annotations:
            self.writeAnnotation(annotation)

        if lights is not None:
            off, on = lights
            self.writeContentText(self.xml, ["Acquisition", "Sessions", "Session", "LightsOff"], off)

            if on is not None:
                self.writeContentText(self.xml, ["Acquisition", "Sessions", "Session", "LightsOn"], on)

        ET.register_namespace("", self.rmlNameSpace)
        self.saveAnnotation(self.getFilePath(recordName))

    def saveAnnotation(self, path, filename=""):
        self.xml.write(path + filename + ".rml")

    def createFolderStructure(self, recordName):
        p = Path(self.getFilePath(recordName))
        p.parent.mkdir(parents=True, exist_ok=True)

    def writeContentText(self, xml, subpath, value):
        el = self.getPath(xml, subpath)
        el.text = str(value)

    def writeAnnotation(self, annotation: dict):
        node = self.getPath(self.xml.getroot(), annotation.path)
        values = annotation.values

        for ev in values:
            attrib = annotation.addAttributes
            attrib[annotation.offsetAttribute] = str(ev.start)
            attrib[annotation.valueAttribute] = str(ev.name)
            if ev.duration > 0:
                attrib[annotation.durationAttribute] = str(ev.duration)
            newTag = ET.SubElement(node, annotation.tagName, attrib)
            for child in annotation.childs:
                for tagname, childAttributes in child.items():
                    ET.SubElement(newTag, tagname, childAttributes)

    def writeSignals(self, filePath, signals: List[Signal], events=[], startTime: datetime = None, signalIsDigital=False):
        # write an edf file
        signalCount = len(signals)
        writer = pyedflib.EdfWriter(filePath, signalCount)

        if self.patient is not None:
            writer.setPatientName(self.patient.name)
            writer.setGender(self.patient.gender)

        index = 0
        signalArray = []
        for index, signal in enumerate(signals):
            writer.setSignalHeader(
                index,
                {
                    "label": signal.name,
                    "dimension": signal.dimension,
                    "sample_rate": signal.frequency,
                    "physical_max": signal.physicalMax,
                    "physical_min": signal.physicalMin,
                    "digital_min": signal.digitalMin,
                    "digital_max": signal.digitalMax,
                    "transducer": signal.transducer,
                    "prefilter": signal.prefilter,
                },
            )
            signalArray.append(signal.signal)
            index += 1
        if startTime is not None:
            writer.setStartdatetime(startTime)

        if signalIsDigital:
            signalArray = [s.astype("int32") for s in signalArray]

        writer.writeSamples(signalArray, digital=signalIsDigital)

        for annotation in events:
            annotation = annotation.todict() if isinstance(annotation, Event) else annotation
            duration = 0 if annotation["duration"] is None else annotation["duration"]
            writer.writeAnnotation(annotation["start"], duration, annotation["name"])

        writer.close()
