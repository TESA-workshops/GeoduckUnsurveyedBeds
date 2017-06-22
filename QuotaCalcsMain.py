# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SCmain.ui'
#
# Created: Mon Jul 22 09:00:28 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from numpy.random import seed
from numpy import inf,iinfo,int16,sqrt,array
MinInt=iinfo(int16).min
import pdb


from PyQt4.QtGui import QMainWindow, QDialog,QListWidgetItem
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtCore, QtGui


from QuotaCalcs import QuotaCalcsDialog
from AllSurveyedRegion import AllSurveyedRegion
from BedData import BedData

import sys,os
class QuotaCalcsMain(QMainWindow, QuotaCalcsDialog):

    def __init__(self,ODB,OUTmdb,parent = None):
        self.inMDB=ODB
        self.resultODB=OUTmdb
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.MakeConnect()
        
        self.OUTmdb=self.resultODB.ODB
        self.ODB=self.inMDB.ODB
        self.setFocus()

    def MakeConnect(self):
        #pdb.set_trace()
        self.DoCalcs.clicked.connect(self.Calculations)
        self.QuitBttn.clicked.connect(self.QuitCalcs)
   

    def Calculations(self):

        ASR=AllSurveyedRegion(self.inMDB.ODB)
        for asr in ASR:
         CurBedData=BedData(self.inMDB.ODB,self.OUTmdb,Region=asr,DenCat=-1)
         CurBedData=BedData(self.inMDB.ODB,self.OUTmdb,Region=asr,DenCat=1)
         CurBedData=BedData(self.inMDB.ODB,self.OUTmdb,Region=asr,DenCat=2)
         CurBedData=BedData(self.inMDB.ODB,self.OUTmdb,Region=asr,DenCat=3)            
        
    def QuitCalcs(self):
        print ('\nBye Bye')
        os._exit(0)
        quit()
        sys.exit(app.exec_())


  

if __name__ == "__main__":
    import sys
    from InputOutputMDB import dataODB,resultODB
    from NewMDB import NewMDB
    inMDB=dataODB(prompt="Select input database file",DefaultDirec="H:\QuotaCalcs\data", FileExt="Access Files (*.mdb *.accdb)")
    resultODB=resultODB(prompt="Select output database file",DefaultDirec="H:\QuotaCalcs\data", FileExt="Access Files (*.mdb *.accdb)")

    app = QtGui.QApplication(sys.argv)
    ui = QuotaCalcsMain(inMDB,resultODB)
    ui.show()
    sys.exit(app.exec_())
