'''
2018-02-22 New version to include calculations for biomass-prime
           To avoid calculating B-prime based on bed-categories, there are lines
           of code to delete or undelete.  Currently line# 36-41
2018-04-17
    Comment out all references to DensDatByDenCat_pr.  
    These values will not be used or calculated  
    
20220913
Read density-category from a CSV file
         
'''
from DensDatByRegionCSV import DensDatByRegion
from DensDatByRegion_prCSV import DensDatByRegion_pr
from norm import norm
from LowHalfNormal import LowHalfNormal
from ProdDistributions import ProdDistributions
from WriteResults import WriteResults

import csv

class BedData:
    '''Density estimates as recorded in the Dom-database
    Called CBedData in previous implementation'''
    #BedData(InFile103,InFile205,InFile401,OutFile,Region=None,DenCat=-1)
     #Reads data from the 103-All_Beds_w_Area_MeanWt_DenCat_QRegion table as conceived in the Dom-database
     #ODB is a connection to an open Dom-database.  Other variables are based upon field-names

    def __init__(self,InFile103,InFile205,InFile401,OutFile,Region=None,DenCat=-1, QuantileUse=[.005,.025,.050,.125,.5,.875,.950,.975,.995]):
          
          
          self.InFile103=InFile103
          self.InFile205=InFile205
          self.InFile401=InFile401
          self.Region=Region
          self.DenCat=DenCat
          self.QuantileUse=QuantileUse
    
          #Bed specific density estimates for the entire region.  combined density classes
          #DenCat indicates that all density-classes are to be used to calculate distributions
          self.DDBR=DensDatByRegion(self.InFile205,self.Region,DenCat=DenCat)
          self.DDBR_pr=DensDatByRegion_pr(InFile205,self.InFile401,self.Region,DenCat=DenCat)
    
          #Consider density-class of surveyed beds
          if self.DenCat>-1:
              self.DensDatByDenCat   =DensDatByRegion(   self.InFile205,self.Region,DenCat=self.DenCat)
              #self.DensDatByDenCat_pr=DensDatByRegion_pr(self.InFile103,self.Region,DenCat=self.DenCat)
              
              #in case we don't want to show prime-results for specific density-categories
              #self.DensDatByDenCat_pr=[None  for t in self.DensDatByDenCat]
              
          else:
              self.DensDatByDenCat   =self.DDBR
              #self.DensDatByDenCat_pr=self.DDBR_pr
    
          #Read bed data (surveyed and unsurveyed)
          CurBedData=self.ReadBedData()
          self.FieldNames=list(CurBedData[0].keys())
          self.nfield=len( self.FieldNames)
          
          
          p=list(map(lambda t:(t+.5)/200,range(200)))
          print('\n BedData 50',self.Region,' ',self.DenCat)
          
          self.values=[]
          for CurRec in CurBedData:
              try:
                 #exclude B-prime based on density-categories
                 self.values+=[BedVal(CurRec,self.DensDatByDenCat,self.DDBR,self.DDBR_pr,QuantileUse,self.DenCat,n=100)]
              except:
                 print()
                 print('BedData 69')
                 print('CurRec',CurRec)
                 print('self.DensDatByDenCat',self.DensDatByDenCat)
                 #print('self.DensDatByDenCat_pr',self.DensDatByDenCat_pr)
                 print('self.DDBR',self.DDBR)
                 print('self.DDBR_pr',self.DDBR_pr)
                 self.values+=[BedVal(CurRec,self.DensDatByDenCat,self.DDBR,self.DDBR_pr,QuantileUse,self.Dencat,n=100)]
          WriteResults(OutFile, self.values)

        
       
    def ReadBedData(self):
        file = open(self.InFile103, "r")
        data = list(csv.DictReader(file, delimiter=","))
        for t in data:
            if t['DenCat']=='':t['DenCat']='-1'
        if self.Region!=None:
            data=[t for t in data if t['QuotaCalcRegion']==self.Region]
        data=[t for t in data if t['DenCat']==str(self.DenCat)]
        for t in data:
            t['ï»¿counter']=int(t['ï»¿counter'])
            t['stat_area']=int(t['stat_area'])
            t['sub_area']=int(t['sub_area'])
            t['bed_code']=int(t['bed_code'])
            t['gis_code']=int(t['gis_code'])
            if t['DenCat']=='':t['DenCat']=-1
            t['DenCat']=int(t['DenCat'])
            
            t['BedArea']=float(t['BedArea'])
            t['BedAreaSE']=float(t['BedAreaSE'])
            t['MeanWt']=float(t['MeanWt'])
            t['MeanWtSE']=float(t['MeanWtSE'])
        return( data)


class BedVal(dict):
  '''Class to contain information about individual beds'''
  def __new__(self,CurBed,DensDatByDenCat,DDBR,DDBR_pr,QuantileUse,DenCat,n=100,p=None):
    self.n=n
    self.p=p
    if self.p==None:self.p=list(map(lambda t:(t+.5)/self.n,range(self.n)))
    CurValue={}
    #Values directly from Database
    for k in CurBed.keys():CurValue[k]=CurBed[k]
            
    #Incorporate estimated abundance and confidence bounds into the dictionary
    #print('CurBed 104\n',CurBed)
    SiteMean=float(CurBed['BedArea'])*10000 #Convert bed-area from hectares to square metres
    SiteStDev=float(CurBed['BedAreaSE'])*10000
    WeightMean=float(CurBed['MeanWt'])/2.204622622 #Convert mean weight from pounds to kilos
    WeightStEr=float(CurBed['MeanWtSE'])/2.204622622

    DistWeight=norm(         WeightMean,WeightStEr)
    DistArea  =LowHalfNormal(SiteMean  ,SiteStDev)
    DistWeightByArea=ProdDistributions(DistWeight,DistArea,p=self.p)


    BiomassDC=ProdDistributions(DistWeightByArea,DensDatByDenCat,p=self.p)#Based upon Density-class and region
    BiomassQR=ProdDistributions(DistWeightByArea,DDBR,p=self.p)#Based on Region only

    #Biomass_pr_DC=ProdDistributions(DistWeightByArea,DensDatByDenCat_pr,p=self.p)#Based upon Density-class and region
    Biomass_pr_QR=ProdDistributions(DistWeightByArea,DDBR_pr,p=self.p)#Based on Region only

    suffix=['99L','95L','90L','75L','Med','75H','90H','95H','99H']
    for i in range(len(QuantileUse)):
        CurValue['BiomDC'+suffix[i]]=BiomassDC.isf(QuantileUse[i])[0]
        CurValue['BiomR'+suffix[i]]=BiomassQR.isf(QuantileUse[i])[0]
        CurValue['BprimeR'+suffix[i]]=Biomass_pr_QR.isf(QuantileUse[i])[0]
        
    CurValue['n_DenCat']=len(DensDatByDenCat)
    CurValue['n_Region']=len(DDBR)
    
    CurValue['ï»¿counter']=int(CurValue['ï»¿counter'])
    CurValue['stat_area']=int(CurValue['stat_area'])
    CurValue['sub_area']=int(CurValue['sub_area'])
    CurValue['bed_code']=int(CurValue['bed_code'])
    CurValue['gis_code']=int(CurValue['gis_code'])
    CurValue['DenCat']=DenCat
    
    CurValue['BedArea']=float(CurValue['BedArea'])
    CurValue['BedAreaSE']=float(CurValue['BedAreaSE'])
    CurValue['MeanWt']=float(CurValue['MeanWt'])
    CurValue['MeanWtSE']=float(CurValue['MeanWtSE'])
    CurValue['BedArea']=float(CurValue['BedArea'])
    
    #print('BedDataCSV 127 CurValue.keys\n',CurValue.keys())
    return(CurValue)

        
              
if __name__ == "__main__":
  InFile103="C:\\Analyses\\2023GduckQuotaCalcs\\data\\103-All_Beds_w_Area_MeanWt_DenCat_QRegion.csv"
  InFile205="C:\\Analyses\\2023GduckQuotaCalcs\\data\\205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion.csv"
  InFile401="C:\\Analyses\\2023GduckQuotaCalcs\\data\\401-Dprime_on_SurveyedBeds_w_QuotaCalcRegion.csv"
  OutFile="C:\\Analyses\\2023GduckQuotaCalcs\\data\\12-Biomass_on_Unsurveyed_Beds.csv"
  OutFilem1="C:\\Analyses\\2023GduckQuotaCalcs\\data\\12-Biomass_on_Unsurveyed_Beds-1.csv"
  OutFile1="C:\\Analyses\\2023GduckQuotaCalcs\\data\\12-Biomass_on_Unsurveyed_Beds1.csv"
  OutFile2="C:\\Analyses\\2023GduckQuotaCalcs\\data\\12-Biomass_on_Unsurveyed_Beds2.csv"
  OutFile3="C:\\Analyses\\2023GduckQuotaCalcs\\data\\12-Biomass_on_Unsurveyed_Beds3.csv"
  
  
  
  ASR=[ 'Area12', 'Area23', 'Area23Closure', 'Area24', 'CentralCoast', 'GeorgiaStrait', 'Lund', 'QCI', 'Rupert', 'WCVI']
  result=[]
  for asr in ASR:
  #for asr in ['WCVI']:
      for DenCat in [-1,1,2,3]:
      #for DenCat in [-1]:
          try:
              test=BedData(InFile103,InFile205,InFile401,OutFilem1,Region=asr,DenCat=DenCat)
              result+=test.values
          except:
              print('BedDataCSV 181 ', asr, DenCat)
              dummy=True
  WriteResults(OutFile,result)