import QFPandas as qp
from QFPandas import QFFrame 
frame = qp.read('data.csv')
qp.parseStringToList(frame, True)
for i in range(frame.col()):
    returns = frame.apply(qp.calculateReturn, col=i)
    sharpeRatio = qp.calculateSharpeRatio(returns)
    print(sharpeRatio)
