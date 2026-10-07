import csv

class CSVDataManager:
    def __init__(self):
        pass

    def readDataFromFile(self, fileName):
        with open(fileName, "r") as file:
            csvDict = csv.DictReader(file)

            raw = []
            for row in csvDict:
                raw.append(row)

        return raw