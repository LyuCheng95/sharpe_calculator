import QFPandas as qp
from QFPandas import QFFrame 
frame = qp.read('data.csv')
qp.parseStringToList(frame, True)
companies = set(frame.col(1))
for company in companies:
    rows = frame.getRowIndiceContainingValue(company, 1)
    prices = list(map(lambda x: int(frame.valueAt(x, 3)), rows))
    returns = qp.calculateReturn(prices)
    sharpeRatio = qp.calculateSharpeRatio(returns)
    print(sharpeRatio)
