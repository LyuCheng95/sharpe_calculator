import QFPandas as qp
from QFPandas import QFFrame 
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import math

qtCreatorFile = "SharpeRatioCalculator.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):        
        super().__init__()
        self.setupUi(self)
        self.pushButton_Calculate.clicked.connect(self.PB_C)
        
    def PB_C(self):
        frame = qp.read(self.file_name.text())
        qp.parseStringToList(frame, True)
        sharpeRatios = []
        for i in range(frame.col()):
            returns = frame.apply(qp.calculateReturn, col=i)
            sharpeRatios.append(qp.calculateSharpeRatio(returns))
        self.a_sr.setText(str(sharpeRatios[0]))
        self.b_sr.setText(str(sharpeRatios[1]))
        self.c_sr.setText(str(sharpeRatios[2]))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
