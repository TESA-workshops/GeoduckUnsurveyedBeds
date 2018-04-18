'''
2018-02-22 New version to include calculations for biomass-prime
           To avoid calculating B-prime based on bed-categories, there are lines
           of code to delete or undelete.  Currently line# 36-41
2018-04-17
    Comment out all references to DensDatByDenCat_pr.  
    These values will not be used or calculated           
'''
from ADO import adoBaseClass as OpenDB
from DensDatByRegion import DensDatByRegion
from DensDatByRegion_pr import DensDatByRegion_pr
from norm import norm
from LowHalfNormal import LowHalfNormal
from ProdDistributions import ProdDistributions

import gc

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
      self.DDBR_pr=DensDatByRegion_pr(self.ODB,self.Region,DenCat=-1)

      #Consider density-class of surveyed beds
      if self.DenCat>-1:
          self.DensDatByDenCat   =DensDatByRegion(   self.ODB,self.Region,DenCat=self.DenCat)
          #self.DensDatByDenCat_pr=DensDatByRegion_pr(self.ODB,self.Region,DenCat=self.DenCat)
          
          #in case we don't want to show prime-results for specific density-categories
          #self.DensDatByDenCat_pr=[None  for t in self.DensDatByDenCat]
          
      else:
          self.DensDatByDenCat   =self.DDBR
          #self.DensDatByDenCat_pr=self.DDBR_pr

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
      print('\n BedData 50',self.Region,' ',self.DenCat)
      while not(self.ODB.rs.EOF):
          CurRec=ODB.Get()
          try:
             #exclude B-prime based on density-categories
             self.values+=[BedVal(ODB,CurRec,nfield,self.DensDatByDenCat,\
             #self.DensDatByDenCat_pr,\
                                  self.DDBR,self.DDBR_pr,QuantileUse=self.QuantileUse,p=p)]
          except:
             print()
             print('BedData 69')
             print('CurRec',CurRec)
             print('self.DensDatByDenCat',self.DensDatByDenCat)
             #print('self.DensDatByDenCat_pr',self.DensDatByDenCat_pr)
             print('self.DDBR',self.DDBR)
             print('self.DDBR_pr',self.DDBR_pr)
             self.values+=[BedVal(ODB,CurRec,nfield,self.DensDatByDenCat,\
                                  #self.DensDatByDenCat_pr,\
                                  self.DDBR,self.DDBR_pr,QuantileUse=self.QuantileUse,p=p)]
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
      else :WhereString+=["("+self.TableName+"QuotaCalcRegion is null)"]
      if self.DenCat!=-1:
          WhereString+=["("+self.TableName+"DenCat="+str(self.DenCat)+")"]
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
  #def __new__(self,ODB, CurRec,nfield,DensDatByDenCat,DensDatByDenCat_pr,DDBR,DDBR_pr,QuantileUse,n=100,p=None):
  def __new__(self,ODB, CurRec,nfield,DensDatByDenCat,DDBR,DDBR_pr,QuantileUse,n=100,p=None):
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

    #Biomass_pr_DC=ProdDistributions(DistWeightByArea,DensDatByDenCat_pr,p=self.p)#Based upon Density-class and region
    Biomass_pr_QR=ProdDistributions(DistWeightByArea,DDBR_pr,p=self.p)#Based on Region only

    CurValue['CBBiomassDC']   =BiomassDC.isf(QuantileUse)
    CurValue['CBBiomassQR']   =BiomassQR.isf(QuantileUse)
    #CurValue['CBBiomass_prDC']=Biomass_pr_DC.isf(QuantileUse)
    CurValue['CBBiomass_prQR']=Biomass_pr_QR.isf(QuantileUse)
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
