# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SCmain.ui'
#
# Created: Mon Jul 22 09:00:28 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!
'''
2018-02-22 Write a copy of 401-Dprime_on_SurveyedBeds_w_QuotaCalcRegion to the output.
'''

from numpy.random import seed
from numpy import inf,iinfo,int16,sqrt,array
MinInt=iinfo(int16).min


from PyQt4.QtGui import QMainWindow, QDialog,QListWidgetItem
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtCore, QtGui


from QuotaCalcs import QuotaCalcsDialog
from AllSurveyedRegion import AllSurveyedRegion
from BedData import BedData

import sys,os
sys.path.append('D:\Coding\AnalysisPrograms2013\Fossil\working\common')
from CopyHeaders import OldHeaders 

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
        self.DoCalcs.clicked.connect(self.Calculations)
        self.QuitBttn.clicked.connect(self.QuitCalcs)
   

    def Calculations(self):
        
        #105 and 203-queries get copied to output as tables.
        self.CopyTables()

        ASR=AllSurveyedRegion(self.inMDB.ODB)
        for asr in ASR:
         CurBedData=BedData(self.inMDB.ODB,self.OUTmdb,Region=asr,DenCat=-1)
         CurBedData=BedData(self.inMDB.ODB,self.OUTmdb,Region=asr,DenCat=1)
         CurBedData=BedData(self.inMDB.ODB,self.OUTmdb,Region=asr,DenCat=2)
         CurBedData=BedData(self.inMDB.ODB,self.OUTmdb,Region=asr,DenCat=3)    
        print('\nCalculations are finished.  Click on the ''quit'' button.')
        
    def QuitCalcs(self):
        print ('\nBye Bye')
        os._exit(0)
        quit()
        sys.exit(app.exec_())

    def CopyTables(self):
        
        #write the 103-query to the output as a table 
        o103=OldHeaders(self.inMDB.MDBfile,TableName='103-All_Beds_w_Area_MeanWt_DenCat_QRegion' )
        o103.CreateHeadersTable(self.OUTmdb)
        o103.CopyRecordToNew(self.OUTmdb)
        
        
        #write the 205-query to the output as a table 
        o205=OldHeaders(self.inMDB.MDBfile,TableName='205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion' )
        o205.CreateHeadersTable(self.OUTmdb)
        o205.CopyRecordToNew(self.OUTmdb)
        
        
        #write 401-Dprime_on_SurveyedBeds_w_QuotaCalcRegion to the output as a table 
        o401=OldHeaders(self.inMDB.MDBfile,TableName='401-Dprime_on_SurveyedBeds_w_QuotaCalcRegion' )
        o401.CreateHeadersTable(self.OUTmdb)
        o401.CopyRecordToNew(self.OUTmdb)
 
  

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
