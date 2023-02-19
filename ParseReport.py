import csv
from typing import Dict, List


class ParseReport:

    def __init__(self, reportPath):
        file = open(reportPath, mode='r', encoding='utf-8-sig')
        self.csvFile = csv.DictReader(file)
        self.table: List[Dict[str, str]] = []
        self.descriptionOfReport = []  # list of description values i.e "gas"
        self.eeOfReport = []

    def generateRows(self):
        listOfTuples = []
        for row in self.csvFile:
            float_row: Dict[str, str] = {}
            for column in row:
                float_row[column] = row[column]
            self.table.append(float_row)
        for dict in self.table:
            listToTuple = []
            for x in dict.keys():
                listToTuple.append(dict[x])
            listOfTuples.append(tuple(listToTuple))
        return listOfTuples

    def getDescription(self):
        for dict in self.csvFile:
            self.descriptionOfReport.append(dict['description'])
        return self.descriptionOfReport

    def getEarnAndExp(self):
        for dict in self.csvFile:
            self.eeOfReport.append(dict['Earnings/Expenses'])
        return self.eeOfReport

    def getHeadings(self):
        return self.csvFile.fieldnames
