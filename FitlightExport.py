from typing import List
from typing import Dict

class FitlightColumn(object):

    Columns = ['Run', 'Application', 'Sequence', 'Tag ID', 'Step', 'Response time', 'Light no', 'Info', 'Split time', 'Athlete name', 'Sequence name', 'Run date', 'csv_version_2']
    IdColumn1 = 'Run'
    IdColumn2 = 'Step'

    def __init__(self, row: Dict[str, str]):
        self.Cells = dict.fromkeys(self.Columns)
        for key in self.Cells.keys():
            if key in row:
                self.Cells[key] = row[key]
            else:
                self.Cells[key] = None

class FitlightOutputColumn(object):

    Columns = ['Run', 'Athlete name', 'Overall total', 'Section 1', 'Section 2', 'Section 3', 'Section 4', 'Section 5', 'Section 6', 'Section total']
    IdColumn = 'Run'

    def __init__(self, steps: List[FitlightColumn]):
        self.Cells = dict.fromkeys(self.Columns)
        self.setRun(steps)
        self.setAthleteName(steps)
        self.setOverallTotal(steps)
        self.setSections(steps)
        self.setSectionTotal(steps)
        return

    def setRun(self, steps: List[FitlightColumn]):
        for step in steps:
            self.Cells['Run'] = step.Cells['Run']
            return
        return

    def setAthleteName(self, steps: List[FitlightColumn]):
        for step in steps:
            self.Cells['Athlete name'] = step.Cells['Athlete name']
            return
        return
    
    def getAthleteName(self):
        return self.Cells['Athlete name']

    def setOverallTotal(self, steps: List[FitlightColumn]):
        maxStep = -1
        lastStep = FitlightColumn(dict())
        for step in steps:
            if int(step.Cells['Step']) > maxStep:
                lastStep = step
        self.Cells['Overall total'] = lastStep.Cells['Split time']
        return

    def setSections(self, steps: List[FitlightColumn]):
        for n in range(1, len(steps)):
            section = f'Section {n}'
            entry = self.getSection(steps, n)
            exit = self.getSection(steps, n+1)
            sectionTime = int(exit.Cells['Split time']) - int(entry.Cells['Split time'])
            self.Cells[section] = sectionTime
            
    def getSection(self, steps: List[FitlightColumn], stepNr: int):
        for step in steps:
            if int(step.Cells['Step']) == stepNr:
                return step
        return FitlightColumn(dict())

    def setSectionTotal(self, steps: List[FitlightColumn]):
        firstStep: FitlightColumn = None
        lastStep: FitlightColumn = None
        for step in steps:
            if firstStep == None or int(step.Cells['Step']) < int(firstStep.Cells['Step']):
                firstStep = step
            if lastStep == None or int(step.Cells['Step']) > int(lastStep.Cells['Step']):
                lastStep = step
        self.Cells['Section total'] = int(lastStep.Cells['Split time']) - int(firstStep.Cells['Split time'])

    def getSectionTotal(self):
        return int(self.Cells['Section total'])
