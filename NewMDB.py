'''
2018-02-22 In the output, include fields related to biomass-prime.
           Convert values of -1 to NULL
2018-04-17
    Remove Fields corresponding to B-prime and density-categories
    Change field names corresponding to B-prime and regional densities
        BPrimeR95L, BPrimeR90L etc
'''

# for column types, see http://www.w3schools.com/ado/ado_datatypes.asp
from numpy import ndarray
import datetime
import os, sys
from win32com.client import Dispatch
from KeyValues import MinInt,KeyValues
import pdb

class NewMDB:
    def __init__(self,OUTmdbName,\
                 InitCounter=MinInt):

        if os.path.exists (OUTmdbName):os.remove (OUTmdbName)
        adox = Dispatch ("ADOX.Catalog")
        CONNECTION_STRING = "Provider=Microsoft.Jet.OLEDB.4.0; data Source=%s" % OUTmdbName
        try:
            adox.Create (CONNECTION_STRING)
        except:
            print('\nNewMDB 20,CONNECTION_STRING\n',CONNECTION_STRING)
            adox.Create (CONNECTION_STRING)
                  
 
        self.Tname='[12-Biomass_on_Unsurveyed_Beds]'       

        self.DB = Dispatch ('ADODB.Connection')
        self.DB.Open (CONNECTION_STRING)

        self.OUTmdbName=OUTmdbName
        self.Create_Results()

        self.Key=KeyValues(InitValue=InitCounter)


    def Create_Results(self):
        CreateStatement ='Create TABLE '+self.Tname+'('
        CreateStatement+='BedKey LONG,' #This was called 'counter' in previous version.
        CreateStatement+='description varchar,'
        CreateStatement+='stat_area INT, '
        CreateStatement+='sub_area INT, '
        CreateStatement+='bed_code INT, '
        CreateStatement+='TextCode varchar,'

        
        CreateStatement+='gis_code INT, '
        CreateStatement+='BedArea DOUBLE, '
        CreateStatement+='BedAreaSE DOUBLE, '
        CreateStatement+='MeanWt DOUBLE, '
        CreateStatement+='MeanWtSE DOUBLE, '
        CreateStatement+='MeanWtSource varchar,'
        
        CreateStatement+='DenCat INT, '
        CreateStatement+='QuotaCalcRegion varchar,'
        CreateStatement+='LicenceRegion varchar,'
        
        CreateStatement+='n_DenCat INT, '
        CreateStatement+='BiomDC99L DOUBLE, '
        CreateStatement+='BiomDC95L DOUBLE, '
        CreateStatement+='BiomDC90L DOUBLE, '
        CreateStatement+='BiomDC75L DOUBLE, '
        CreateStatement+='BiomDCMed DOUBLE, '
        CreateStatement+='BiomDC75H DOUBLE, '
        CreateStatement+='BiomDC90H DOUBLE, '
        CreateStatement+='BiomDC95H DOUBLE, '
        CreateStatement+='BiomDC99H DOUBLE, '
        
        CreateStatement+='n_Region INT, '
        CreateStatement+='BiomR99L DOUBLE, '
        CreateStatement+='BiomR95L DOUBLE, '
        CreateStatement+='BiomR90L DOUBLE, '
        CreateStatement+='BiomR75L DOUBLE, '
        CreateStatement+='BiomRMed DOUBLE, '
        CreateStatement+='BiomR75H DOUBLE, '
        CreateStatement+='BiomR90H DOUBLE, '
        CreateStatement+='BiomR95H DOUBLE, '
        CreateStatement+='BiomR99H DOUBLE, '
        
        #CreateStatement+='BprimeDC99L DOUBLE, '
        #CreateStatement+='BprimeDC95L DOUBLE, '
        #CreateStatement+='BprimeDC90L DOUBLE, '
        #CreateStatement+='BprimeDC75L DOUBLE, '
        #CreateStatement+='BprimeDCMed DOUBLE, '
        #CreateStatement+='BprimeDC75H DOUBLE, '
        #CreateStatement+='BprimeDC90H DOUBLE, '
        #CreateStatement+='BprimeDC95H DOUBLE, '
        #CreateStatement+='BprimeDC99H DOUBLE, '
        
        CreateStatement+='BprimeR99L DOUBLE, '
        CreateStatement+='BprimeR95L DOUBLE, '
        CreateStatement+='BprimeR90L DOUBLE, '
        CreateStatement+='BprimeR75L DOUBLE, '
        CreateStatement+='BprimeRMed DOUBLE, '
        CreateStatement+='BprimeR75H DOUBLE, '
        CreateStatement+='BprimeR90H DOUBLE, '
        CreateStatement+='BprimeR95H DOUBLE, '
        CreateStatement+='BprimeR99H DOUBLE, '
        
        CreateStatement+='YearCalc INT, '
        CreateStatement+='MontCalc INT, '
        CreateStatement+='DayCalc INT); '
        
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print ('\nNewMDB line 86\n',CreateStatement)
            self.DB.Execute(CreateStatement )            

    def ADDTo_Results(self, CurVal):
        ct=datetime.datetime.now()
        y,m,d=ct.year,ct.month,ct.day
       
        query ="insert INTO "+self.Tname+"("
        query+=     "BedKey, description, stat_area, sub_area, bed_code, TextCode, gis_code, "
        query+=     "BedArea, BedAreaSE, MeanWt, MeanWtSE, MeanWtSource,  "
        query+=     "DenCat, QuotaCalcRegion, LicenceRegion,  "
        query+=     "n_DenCat, BiomDC99L,     BiomDC95L,     BiomDC90L,     BiomDC75L,     BiomDCMed,     BiomDC75H,     BiomDC90H,    BiomDC95H,      BiomDC99H,  "
        #query+=               "BprimeDC99L, BprimeDC95L, BprimeDC90L, BprimeDC75L, BprimeDCMed, BprimeDC75H, BprimeDC90H, BprimeDC95H, BprimeDC99H,  "
        query+=     "n_Region, BiomR99L,     BiomR95L,     BiomR90L,     BiomR75L,     BiomRMed,     BiomR75H,     BiomR90H,     BiomR95H,     BiomR99H,  "
        query+=               "BprimeR99L, BprimeR95L, BprimeR90L, BprimeR75L, BprimeRMed, BprimeR75H, BprimeR90H, BprimeR95H, BprimeR99H,  "
        query+=     "YearCalc, MontCalc, DayCalc) "
        query+="Values("
        query+=str(self.Key.GetValue(IncrementFirst=True))
        
        #Quotes in description confuse things
        description=CurVal['description'].replace("'", "")
        query+=",'"+description+"'"
        
        query+=","+str(CurVal['stat_area'])
        query+=","+str(CurVal['sub_area'])
        
        query+=","+str(CurVal['bed_code'])
        query+=",'"+    CurVal['TextCode']+"'"
        query+=","+str(CurVal['gis_code'])
        query+=","+str(CurVal['BedArea'])
        query+=","+str(CurVal['BedAreaSE'])
        query+=","+str(CurVal['MeanWt'])
        query+=","+str(CurVal['MeanWtSE'])
        query+=",'"+CurVal['MeanWtSource']+"'"
        
        query+=","+str(CurVal['DenCat'])
        query+=",'"+CurVal['QuotaCalcRegion']+"'"
        query+=",'"+CurVal['LicenceRegion']+"'"
        try:
            query+=","+str(CurVal['n_DenCat'])
        except:
            pdb.set_trace()
            query+=","+str(CurVal['n_DenCat'])
        CBBiomassDC=CurVal['CBBiomassDC']
        query+=","+str(CBBiomassDC[0])
        query+=","+str(CBBiomassDC[1])
        query+=","+str(CBBiomassDC[2])
        query+=","+str(CBBiomassDC[3])
        query+=","+str(CBBiomassDC[4])
        query+=","+str(CBBiomassDC[5])
        query+=","+str(CBBiomassDC[6])
        query+=","+str(CBBiomassDC[7])
        query+=","+str(CBBiomassDC[8])
        #Don't want B-primes associated with density classes
        #CBBiomass_prDC=CurVal['CBBiomass_prDC']
        #query+=","+str(CBBiomass_prDC[0])
        #query+=","+str(CBBiomass_prDC[1])
        #query+=","+str(CBBiomass_prDC[2])
        #query+=","+str(CBBiomass_prDC[3])
        #query+=","+str(CBBiomass_prDC[4])
        #query+=","+str(CBBiomass_prDC[5])
        #query+=","+str(CBBiomass_prDC[6])
        #query+=","+str(CBBiomass_prDC[7])
        #query+=","+str(CBBiomass_prDC[8])
        
        query+=","+str(CurVal['n_Region'])
        CBBiomassQR=CurVal['CBBiomassQR']
        query+=","+str(CBBiomassQR[0])
        query+=","+str(CBBiomassQR[1])
        query+=","+str(CBBiomassQR[2])
        query+=","+str(CBBiomassQR[3])
        query+=","+str(CBBiomassQR[4])
        query+=","+str(CBBiomassQR[5])
        query+=","+str(CBBiomassQR[6])
        query+=","+str(CBBiomassQR[7])
        query+=","+str(CBBiomassQR[8])
        
        CBBiomass_prQR=CurVal['CBBiomass_prQR']
        query+=","+str(CBBiomass_prQR[0])
        query+=","+str(CBBiomass_prQR[1])
        query+=","+str(CBBiomass_prQR[2])
        query+=","+str(CBBiomass_prQR[3])
        query+=","+str(CBBiomass_prQR[4])
        query+=","+str(CBBiomass_prQR[5])
        query+=","+str(CBBiomass_prQR[6])
        query+=","+str(CBBiomass_prQR[7])
        query+=","+str(CBBiomass_prQR[8])
        
        query+=","+str(y)+","+str(m)+","+str(d)+");"
        query=query.replace('None','-32767')
        query=query.replace('-1,','NULL,')
        
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 145 query\n',query)
            self.DB.Execute(query)
 
   




        

if __name__ == "__main__":


    from PyQt4 import QtGui
    from PyQt4.QtCore import *

    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    prompt="Select OutPut database file"
    DefaultDirec="H:\\AnalysisPrograms2013\\PyFunctions\\Geoduck\\SampleData"
    FileExt="Access Files (*.mdb *.accdb)"


    mdbfile = QtGui.QFileDialog.getSaveFileName(w, prompt,DefaultDirec,FileExt)
    testdb=NewMDB(mdbfile)
    testdb.ADDTo_Results_Header('SelectedSurveys',4,'Run comments',1000,756,3,100)

    SelectedSurveys,RunNumber,RunComments,\
                             NumberIterations,RandomSeed,MinDepth,MaxDepth


    testdb.ADDTo_ConfInterval(-3127,95,\
                           101,    102,\
                           103.,   104.4,\
                           105.,  106.9555555,\
                           107.00001, 108.3333)
    testdb.ADDTo_EstDens(200, 20,400,40)
    testdb.ADDTo_SurveyUsed('Location',1963)
    testdb.ADDTo_TranChar( 'Location',62,1962,12,3,10,100)
    testdb.ADDTo_Transect(1000,6,1001,2013,7,23,3.5,10.,\
                       65,13,100,6.5,13.8,\
                      False,'OmitTransectReason','TransectComments',1111)

    
    del testdb

    print('done NewMDB')
    ADDTo_Transect(self, TranCharKey,TransectNumber,HeaderKey,y,m,d,MinDepth,MaxDepth,\
                       TranLength,NumQuadrats,NumAnimals,Density,Biomass,\
                      OmitTransect,OmitTransectReason,TransectComments,GIS_Code)
