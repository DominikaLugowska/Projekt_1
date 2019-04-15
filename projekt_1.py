# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:31:59 2019

@author: lenovo
"""
import sys

from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, QApplication, QGridLayout, QColorDialog, QTextEdit, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

        
#funcja opisujaca równanie prostej z odcinka
def prosta(x1,y1,x2,y2):
    if x1==x2:
        return float("inf"), x1
    else:
        a = (y1-y2)/(x1-x2)
        b = y1 - a*x1
        return a, b

#wspolrzedne punktu przeciecia
def punktp(a1,a2,b1,b2):
    if a1==float("inf"):
        xp = b1
        yp = a2*b1 + b2
        return xp, yp
    elif a2==float("inf"):
        xp = b2
    else:
        xp = (b1-b2)/(a2-a1)
    yp = a1*xp + b1
    return xp, yp

#sprawdzenie czy dany punkt leży na odcinku czy poza w wersji zero-jedynkowej (nie/tak)
def czynalezy (xp,yp,x1,x2,y1,y2):
    if x1==x2: #jesli prosta jest pionowa, to sprawdzenie robimy na y-kach, a nie na x-ach, 
                #uzywajac tej samej funkcji z podstawionymi y zamiast x
        czynalezy(yp,0,y1,y2,0,1)
    elif x1>x2:
        if xp>x1 or xp<x2:
            return 0
        else:
            return 1 
    else:
        if xp>x2 or xp<x1:
            return 0
        else:
            return 1 
        
class AppWindow(QWidget): #appwindow dziedziczy po qwidget 
    
    def __init__ (self):
        super().__init__()
        self.title = "Projekt 1"
        self.initInterface()
        self.initWidgets()
        
    def initInterface(self):
        self.setWindowTitle(self.title) #tytuł
        self.setGeometry(100, 100, 600, 500) #rozmiar okna
        self.show() 
        
    
    def initWidgets(self):
        btn = QPushButton("Rysuj i znajdz przeciecie", self)
        btnCol = QPushButton("Zmien kolor", self)
        btnClear = QPushButton("Wyczysc dane", self)
        btnSave = QPushButton("Zapisz do pliku", self)
        xaLabel = QLabel("Xa", self)
        yaLabel = QLabel("Ya", self)
        xbLabel = QLabel("Xb", self)
        ybLabel = QLabel("Yb", self)
        xcLabel = QLabel("Xc", self)
        ycLabel = QLabel("Yc", self)
        xdLabel = QLabel("Xd", self)
        ydLabel = QLabel("Yd", self)
        xpLabel = QLabel("Xp", self)
        ypLabel = QLabel("Yp", self)
        consoleLabel = QLabel("Komunikaty programu:")
        self.xaEdit = QLineEdit()
        self.yaEdit = QLineEdit()
        self.xbEdit = QLineEdit()
        self.ybEdit = QLineEdit()
        self.xcEdit = QLineEdit()
        self.ycEdit = QLineEdit()
        self.xdEdit = QLineEdit()
        self.ydEdit = QLineEdit()
        self.xpEdit = QLineEdit()
        self.ypEdit = QLineEdit()
        self.xpEdit.setReadOnly(1)
        self.ypEdit.setReadOnly(1)
        self.console = QTextEdit('Witaj!')
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        
        
        #wyswietlanie
        grid = QGridLayout()
        grid.addWidget(xaLabel, 1, 0)
        grid.addWidget(self.xaEdit, 1, 1)
        grid.addWidget(yaLabel, 2, 0)
        grid.addWidget(self.yaEdit, 2, 1)
        grid.addWidget(xbLabel, 3, 0)
        grid.addWidget(self.xbEdit, 3, 1)
        grid.addWidget(ybLabel, 4, 0)
        grid.addWidget(self.ybEdit, 4, 1)
        grid.addWidget(xcLabel, 5, 0)
        grid.addWidget(self.xcEdit, 5, 1)
        grid.addWidget(ycLabel, 6, 0)
        grid.addWidget(self.ycEdit, 6, 1)
        grid.addWidget(xdLabel, 7, 0)
        grid.addWidget(self.xdEdit, 7, 1)
        grid.addWidget(ydLabel, 8, 0)
        grid.addWidget(self.ydEdit, 8, 1)
        grid.addWidget(xpLabel, 9, 0)
        grid.addWidget(self.xpEdit, 9, 1)
        grid.addWidget(ypLabel, 10, 0)
        grid.addWidget(self.ypEdit, 10, 1)
        grid.addWidget(btn, 11, 0, 1, 2)
        grid.addWidget(btnCol, 12, 0, 1, 2)
        grid.addWidget(btnClear, 13, 0, 1, 2)
        grid.addWidget(btnSave, 14, 0, 1, 2)
        grid.addWidget(consoleLabel, 15, 0,1,1)
        grid.addWidget(self.console, 16, 0, 1, 2)
        grid.addWidget(self.canvas, 1, 2, -1, -1)

        
        self.setLayout(grid)

        
        
        btn.clicked.connect(self.oblicz)
        btnCol.clicked.connect(self.zmienKolor)
        btnClear.clicked.connect(self.czysc)
        btnSave.clicked.connect(self.zapisz)
        
    def czysc(self):
        self.xaEdit.clear()
        self.yaEdit.clear()
        self.xbEdit.clear()
        self.ybEdit.clear()
        self.xcEdit.clear()
        self.ycEdit.clear()
        self.xdEdit.clear()
        self.ydEdit.clear()
        self.xpEdit.clear()
        self.ypEdit.clear()
        self.console.clear()
        self.figure.clear()
        self.canvas.draw()

    def zapisz(self):
        filename = QFileDialog.getSaveFileName()
        abcdp = open(filename, 'w')
        abcdp.write("|{:^15}|{:^15}|{:^15}|\n".format("Nazwa pkt", "X [m]", "Y [m]" ))
        abcdp.write("|{:^15}|{:^15}|{:^15}|\n".format("A",self.xaEdit.text(), self.yaEdit.text())) 
        abcdp.write("|{:^15}|{:^15}|{:^15}|\n".format("B",self.xbEdit.text(), self.ybEdit.text()))
        abcdp.write("|{:^15}|{:^15}|{:^15}|\n".format("C",self.xcEdit.text(), self.ycEdit.text()))
        abcdp.write("|{:^15}|{:^15}|{:^15}|\n".format("D",self.xdEdit.text(), self.ydEdit.text()))
        if self.xaEdit == None:
            abcdp.write("|{:^15}|{:^15}|{:^15}|\n".format("P","brak", "brak"))
        else:
            abcdp.write("|{:^15}|{:^15}|{:^15}|\n".format("P",self.xpEdit.text(), self.ypEdit.text()))
        self.console.append('Zapisano dane do pliku')
        abcdp.close()

                
    def zmienKolor(self):
        kolor = QColorDialog.getColor()
        if kolor.isValid():
            print(kolor.name())
            self.rysuj(kol=kolor.name())
        
        
    def sprawdzliczbe(self, element):
        if element.text().lstrip('-').replace('.','',1).isdigit():
            return float(element.text())
        else:
            return None
    
    def oblicz(self):
        self.rysuj()
    
    def rysuj(self, kol='red'):
        xa = self.sprawdzliczbe(self.xaEdit) #float(self.xEdit.text())
        ya = self.sprawdzliczbe(self.yaEdit) #float(self.yEdit.text())
        xb = self.sprawdzliczbe(self.xbEdit)
        yb = self.sprawdzliczbe(self.ybEdit)
        xc = self.sprawdzliczbe(self.xcEdit)
        yc = self.sprawdzliczbe(self.ycEdit)
        xd = self.sprawdzliczbe(self.xdEdit)
        yd = self.sprawdzliczbe(self.ydEdit)

        if None not in [xa, ya, xb, yb, xc, yc, xd, yd]:
              xa = float(self.xaEdit.text())
              ya = float(self.yaEdit.text())
              xb = float(self.xbEdit.text())
              yb = float(self.ybEdit.text())
              xc = float(self.xcEdit.text())
              yc = float(self.ycEdit.text())
              xd = float(self.xdEdit.text())
              yd = float(self.ydEdit.text())
        else:
            self.console.append('Proszę podać wszystkie dane')
#            print("Wpisz wszystkie dane")
            return
        
        a1, b1 = prosta(xa, ya, xb, yb)
        a2, b2 = prosta(xc, yc, xd, yd)
        
        #sprawdzenie położenia danego punktu przeciecia wzgledem odcinkow
        if a1!=a2:
            xp, yp = punktp(a1,a2,b1,b2)
            self.xpEdit.setText("{:.3f}".format(xp))
            self.ypEdit.setText("{:.3f}".format(yp))
            p_lezy_ab = czynalezy (xp, yp, xa, xb, ya, yb)
            p_lezy_cd = czynalezy (xp, yp, xc, xd, ya ,yb)
            if p_lezy_ab and p_lezy_cd:
                self.console.append("Rozwiazanie to przeciecie odcinkow")
            elif p_lezy_ab or p_lezy_cd:
                self.console.append("Rozwiazanie to przedluzenie jednego odcinka")
            else:
                self.console.append("Roziwazanie to przedluzenie dwoch odcinkow")
            self.console.append("W punkcie ({:5.3f}, {:5.3f})\n".format(xp, yp))
        else:
            self.xpEdit.clear()
            self.ypEdit.clear()
            if b1==b2:
                self.console.append("Odcinki sa wspolliniowe")
            else:
                self.console.append("Odcinki sa rownolegle")
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(xa, ya, color=kol, marker='o')
        ax.annotate("A ({:.3f}, {:.3f})".format(xa, ya), xy=[xa,ya], textcoords='data')
        ax.plot(xb, yb, color=kol, marker='o')
        ax.annotate("B ({:.3f}, {:.3f})".format(xb, yb), xy=[xb,yb], textcoords='data')
        ax.plot(xc, yc, color='green', marker='o')
        ax.annotate("C ({:.3f}, {:.3f})".format(xc, yc), xy=[xc,yc], textcoords='data')
        ax.plot(xd, yd, color='green', marker='o')
        ax.annotate("D ({:.3f}, {:.3f})".format(xd, yd), xy=[xd,yd], textcoords='data')
        if xp != None:
            ax.plot(xp, yp, color='black', marker='o')
            ax.annotate("P ({:.3f}, {:.3f})".format(xp, yp), xy=[xp,yp], textcoords='data')
        x_vals = np.arange(min([xa, xb, xc, xd])-1, max([xa, xb, xc, xd])+2)
        x_odc1 = np.arange(min([xa, xb]), max([xa, xb]), 0.0001)
        x_odc2 = np.arange(min([xc, xd]), max([xc, xd]), 0.0001)
        y_vals1 = b1 + a1 * x_vals
        y_vals2 = b2 + a2 * x_vals
        y_odc1 = b1 + a1 * x_odc1
        y_odc2 = b2 + a2 * x_odc2
        ax.plot(x_vals, y_vals1, '--', color = kol)
        ax.plot(x_vals, y_vals2, '--', color = "green")
        ax.plot(x_odc1, y_odc1, '-', color = kol)
        ax.plot(x_odc2, y_odc2, '-', color = "green")
        self.canvas.draw()
            
    #def wpisz(self):
    #    self.xEdit.setText("1")

    
def main(): # w funkcji main bd oczekiwać na nasze zdarzenia 
    app = QApplication(sys.argv)
    window = AppWindow()
    app.exec_()
    
if __name__ == '__main__':
    main()



