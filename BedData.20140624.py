from ADO import adoBaseClass as OpenDB
from DensDatByRegion import DensDatByRegion
from norm import norm
from LowHalfNormal import LowHalfNormal
from ProdDistributions import ProdDistributions

import gc
import pdb

class BedData:
    '''Density estimates as recorded in the Dom-database
       Called CBedData in previous implementation'''
    def __init__(self,ODB,OutMDB,Region=None,DenCat=-1,TableName="[103-All_Beds_w_Area_MeanWt_DenCat_QRegion].",\
                 QuantileUse=[.005,.025,.050,.125,.5,.875,.950,.975,.995]):
      '''BedData(ODB,QuotaCalcRegion=None,stat_area=None,sub_area=None,DenCat=-1)
      Reads data from the 103-All_Beds_w_Area_MeanWt_DenCat_QRegion table as conceived in the Dom-database

      ODB is a connection to an open Dom-database.  Other variables are based upon field-names'''
      self.ODB=ODB
      self.Region=Region
      self.DenCat=DenCat
      self.TableName=TableName
      self.QuantileUse=QuantileUse

      #Bed specific density estimates for the entire region.  combined density classes
      #DenCat indicates that all density-classes are to be used to calculate distributions
      self.DDBR=DensDatByRegion(self.ODB,self.Region,DenCat=-1)

      #Consider density-class of surveyed beds
      if self.DenCat>-1:self.DensDatByDenCat=DensDatByRegion(self.ODB,self.Region,DenCat=self.DenCat)
      else:self.DensDatByDenCat=self.DDBR

      #Read bed data (surveyed and unsurveyed)
      query=self.MakeQuery()
      try:
        self.ODB.execute(query)
      except:
          print('/nBedData 34')
          print(query)
          self.ODB.execute(query)
      self.ODB.DefineFieldNames()
      nfield=self.ODB.GetFieldCount()
      self.values=[]
      if(self.ODB.rs.EOF):return #no data in query
      self.ODB.rs.MoveFirst()
      gc.disable()
      gc.collect()
      p=list(map(lambda t:(t+.5)/200,range(200)))
      print('\n',self.Region,' ',self.DenCat)
      while not(self.ODB.rs.EOF):
          CurRec=ODB.Get()
          self.values+=[BedVal(ODB,CurRec,nfield,self.DensDatByDenCat,self.DDBR,QuantileUse=self.QuantileUse,p=p)]
          print(self.values[-1]['QuotaCalcRegion'],self.values[-1]['stat_area'],\
                self.values[-1]['sub_area'],self.values[-1]['gis_code'],self.values[-1]['description'])
          OutMDB.ADDTo_Results(self.values[-1])

      gc.collect()
      gc.enable()
       

    def MakeQuery(self):
      querySelect = "SELECT  "
      querySelect+=self.TableName+"counter, "
      querySelect+=self.TableName+"description, "
      querySelect+=self.TableName+"stat_area, "
      querySelect+=self.TableName+"sub_area, "
      querySelect+=self.TableName+"bed_code, "
      querySelect+='cstr('+self.TableName+"TextCode) as TextCode, "
      querySelect+=self.TableName+"gis_code, "
      querySelect+=self.TableName+"BedArea, "
      querySelect+=self.TableName+"BedAreaSE, "
      querySelect+=self.TableName+"MeanWt, "
      querySelect+=self.TableName+"MeanWtSE, "
      querySelect+=self.TableName+"MeanWtSource, "
      querySelect+=self.TableName+"QuotaCalcRegion, "
      querySelect+=self.TableName+"LicenceRegion, "
      querySelect+=self.TableName+"DenCat "

      queryFrom= " FROM "+self.TableName[:-1] +" "

      WhereString=[]
      if self.Region!=None:WhereString+=["("+self.TableName+"QuotaCalcRegion='"+self.Region+"')"]
      if self.DenCat!=-1:
          WhereString+=["("+self.TableName+"DenCat='"+str(self.DenCat)+"')"]
      else:
          WhereString+=["("+self.TableName+"DenCat is Null)"]
          
      queryWhere=''
      if len(WhereString)==1:queryWhere="Where"+WhereString[0]
      if len(WhereString)> 1:queryWhere="Where("+ (' and '.join(WhereString)) +')'

      queryOrder ="Order by "
      queryOrder+=self.TableName+"QuotaCalcRegion, "
      queryOrder+=self.TableName+"stat_area, "
      queryOrder+=self.TableName+"sub_area, "
      queryOrder+=self.TableName+"gis_code; "
      try:
        query=querySelect+queryFrom+queryWhere+queryOrder
      except:
          print('\nBedData 77')
          print('querySelect',querySelect)
          print('queryFrom',queryFrom)
          print('queryWhere',queryWhere)
          print('queryOrder',queryOrder)
          query=querySelect+queryFrom+queryWhere+queryOrder
      return(query)

class BedVal(dict):
  '''Class to contain information about individual beds'''
  def __new__(self,ODB, CurRec,nfield,DensDatByDenCat,DDBR,QuantileUse,n=100,p=None):
    self.n=n
    self.p=p
    if self.p==None:self.p=list(map(lambda t:(t+.5)/self.n,range(self.n)))
    CurValue={}
    #Values directly from Database
    for i in range(nfield):CurValue[ODB.Fname[i]]=CurRec[i]
            
    #Incorporate estimated abundance and confidence bounds into the dictionary
    SiteMean=CurValue['BedArea']*10000 #Convert bed-area from hectares to square metres
    SiteStDev=CurValue['BedAreaSE']*10000
    WeightMean=CurValue['MeanWt']/2.204622622 #Convert mean weight from pounds to kilos
    WeightStEr=CurValue['MeanWtSE']/2.204622622

    DistWeight=norm(         WeightMean,WeightStEr)
    DistArea  =LowHalfNormal(SiteMean  ,SiteStDev)
    DistWeightByArea=ProdDistributions(DistWeight,DistArea,p=self.p)


    BiomassDC=ProdDistributions(DistWeightByArea,DensDatByDenCat,p=self.p)#Based upon Density-class and region
    BiomassQR=ProdDistributions(DistWeightByArea,DDBR,p=self.p)#Based on Region only

    CurValue['CBBiomassDC']=BiomassDC.isf(QuantileUse)
    CurValue['CBBiomassQR']=BiomassQR.isf(QuantileUse)
    CurValue['n_DenCat']=len(DensDatByDenCat)
    CurValue['n_Region']=len(DDBR)
    return(CurValue)

        
              
if __name__ == "__main__":
  databasepath='h:\\QuotaCalcs\\data\\2014_Quotas.mdb'
  ODB=OpenDB(databasepath)
  from NewMDB import NewMDB
  OUTmdbName='h:\\QuotaCalcs\\data\\testGeorgiaStrait.mdb'
  OutMDB=NewMDB(OUTmdbName)
  test=BedData(ODB,OutMDB,Region='GeorgiaStrait',DenCat=-1)
  print('\ntest.MakeQuery()', test.MakeQuery() )
  print('\ndir(test)', dir(test) )
  print('len(test.values)', len(test.values) )
  print(' \ntest.values[0]', test.values[0])
  print(' \ntest.values[-1]', test.values[-1])
  #test.CalcResults()
