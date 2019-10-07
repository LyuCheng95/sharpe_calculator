
class MyFrame:
    rawDataString = ''
    dataList = []
    headers = []

    def read(self, path):
        self.rawDataString = open(path, 'r').read()

    def parseStringToList(self, hasHeaders=False):
        recordList = self.rawDataString.split('\n')
        for record in recordList:
            self.dataList.append(record.split(','))
        if hasHeaders:
            self.headers = self.dataList.pop(0)
    
    def groupRowByCol(self, col):
        colDict = {}
        for i, record in enumerate(self.dataList):
            if record[col] in colDict:
                colDict[record[col]].append(i)
            else:
                colDict[record[col]] = [i]
        return colDict
    
    def calculateReturn(self, colDict, computingCol):
        for value in colDict.values():
            # handle 1st row
            firstRecord = value[0]
            self.dataList[firstRecord].append(None)
            prevPrice = int(self.dataList[firstRecord][computingCol])
            for i in range(1, len(value)):
                returnValue = (int(self.dataList[value[i]][computingCol]) - int(prevPrice)) / prevPrice
                self.dataList[value[i]].append(returnValue)
                prevPrice = int(self.dataList[value[i]][computingCol])
    
    def calculateMean(self, colDict, computingCol):
        meanDict = {}
        for key, value in colDict.items():
            sum = 0
            for i in value:
                if self.dataList[i][computingCol]:
                    sum += self.dataList[i][computingCol]
            meanDict[key] = sum / (len(value)-1)
        return meanDict

    def calculateSD(self, colDict, meanDict, computingCol):
        sdDict = {}
        for key, value in colDict.items():
            sumOfDiffFromMean = 0
            for i in value:
                if self.dataList[i][computingCol]:
                    sumOfDiffFromMean += (int(self.dataList[i][computingCol]) - meanDict[key]) ** 2
            variance = sumOfDiffFromMean / (len(value) -1)
            sdDict[key] = variance ** 0.5
        return sdDict

    def calculateSharpeRatio(self, colDict, meanDict, sdDict, computingCol ,Rf=0.05):
        sharpeRatioDict = {}
        for key, value in colDict.items():
            productOfFactor = 1
            for i in value:
                currReturn = self.dataList[i][computingCol]
                if currReturn: 
                    factor = currReturn + 1
                    productOfFactor = productOfFactor * factor
            effectiveRateOfReturn = ((productOfFactor ** (1/(len(value)-1))) ** 12) - 1
            riskPremium = effectiveRateOfReturn - Rf 
            sharpeRatioDict[key] = riskPremium/(sdDict[key])    
        return sharpeRatioDict
            
frame = MyFrame()
frame.read(path='data.csv')
frame.parseStringToList(True)
stockDict = frame.groupRowByCol(1)
print('stockDict', stockDict)
frame.calculateReturn(stockDict, 3)
print('dataList', frame.dataList)
meanDict = frame.calculateMean(stockDict, 4)
print('meanDict', meanDict)
sdDict = frame.calculateSD(stockDict, meanDict, 4)
print('sdDict', sdDict)
sharpeRatioDict = frame.calculateSharpeRatio(stockDict, meanDict, sdDict, 4, Rf=0.05)
print('sharpeRatioDict', sharpeRatioDict)