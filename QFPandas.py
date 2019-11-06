def read(path):
    '''
    Read the content from the provided path.
    Create and return an instance of MyFrame.
    '''
    return QFFrame(open(path, 'r').read())

def parseStringToList(frame, hasHeaders=False):
    '''
    Create a 2D List from a string.
    e.g.:
        '1,2,3[/n]4,5,6[/n]7,8,9' will be converted to: 
        [['1','2','3'],['4','5','6'],['7','8','9']]
    '''
    recordList = frame.rawDataString.split('\n')
    for record in recordList:
        frame.dataList.append(record.split(','))
    if hasHeaders:
        frame.headers = frame.dataList.pop(0)

def calculateReturn(priceList):
    '''
    input: list of prices,
    formula: (current price - previous price) / previous price
    output: list of returns.
    '''
    returnList = []
    prev = float(priceList.pop(0))
    for price in priceList:
        returnList.append((float(price) - prev) / prev)
    return returnList
    
def calculateMean(nums):
    '''
    input: list of numbers,
    return: mean of the numbers.
    '''
    summation = sum(nums)
    count = len(nums)
    return summation/count

def calculateSD(nums):
    '''
    input: list of numbers,
    formula:
    return: standard deviation of the numbers.
    '''
    squareOfSumOfDiffFromMean = 0
    for num in nums:
        mean = calculateMean(nums)
        squareOfSumOfDiffFromMean += (num - mean) ** 2
    sd = (squareOfSumOfDiffFromMean / len(nums)) ** 0.5
    return sd 

def calculateSharpeRatio(returns, Rf=0.05):
    '''
    input: list of returns,
    formula: 
    return: sharpe ratio.
    '''
    productOfFactor = 1
    for value in returns:
        factor = value + 1
        productOfFactor = productOfFactor * factor
    effectiveRateOfReturn = (productOfFactor ** (1/len(returns)) ** 12) - 1
    adjustedSD = (len(returns)*calculateSD**2)**0.5
    riskPremium = effectiveRateOfReturn - Rf 
    sharpeRatio = riskPremium / adjustedSD
    return sharpeRatio

class QFFrame:
    rawDataString = ''
    dataList = []
    headers = []

    def __init__(self, constructionString):
        '''
        initiate a QFFrame instance
        '''
        self.rawDataString = constructionString
    
    def row(self):
        '''
        return num of rows
        '''
        return len(self.dataList) 

    def col(self):
        '''
        retrun num of cols
        '''
        return len(self.dataList[0])

    def getCol(self, col):
        '''
        get data of one column, return as list
        '''
        return [row[col] for row in self.dataList]
    
    def getRow(self, row):
        '''
        get data of one row, return as list
        '''
        return self.dataList[row]

    def valueAt(self, row, col):
        '''
        get data at a certian position
        '''
        return self.dataList[row][col]

    def getRowIndiceContainingValue(self, value, col=None):
        '''
        return the list of row indice containing the searching value,
        if column number is not None, this method will only compare data at the given column.
        '''
        resultList = []
        for i, row in enumerate(self.dataList):
            if col:
                if value == row[col]:
                    resultList.append(i)
            else:
                if value in row:
                    resultList.append(i)
        return resultList
    
    def apply(self, func, row=None, col=None):
        '''
        apply a function on a given row/col of data
        '''
        selectedData=[]
        if row:
            selectedData=self.getRow(row)
        else:
            selectedData=self.getCol(col)
        return func(selectedData)

    def __str__(self):
        return ','.join(str(item) for innerlist in self.dataList for item in innerlist)