'''2015-06-15 Force DenCat values from .mdb file to be integers'''
from ADO import adoBaseClass as OpenDB
from numpy import ndarray,array


class DensDatByRegion(ndarray):
  '''A numpy.array of density values'''
  def __new__(self,ODB,Region,DenCat=-1,FieldType=int):
 
      query ='SELECT  [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].CurrentDensity '
      query+=' FROM [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion] '

      query+='Where( '
      if Region!=None:
        query+=   "([205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion='"
        query+=   Region +"')  "
      else:
        query+=   "([205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion is NULL)  "
    
      if DenCat>-1:
          query+= " and (  [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].DenCat= "
          query+=   str(DenCat)+')'
      query+=') ' #Close the where
      query+=  ';'
      
      try:
        ODB.execute(query)
      except:
          print('/nDensDatByRegion 25')
          print(query)
          ODB.execute(query)
      result=ODB.GetVariable('CurrentDensity')
      return(array(result))
        

if __name__ == "__main__":
  databasepath='q:\\analyses\\QuotaOptionCalculations\\20150612.bugcheck\\2016_Quotas.mdb'
  ODB=OpenDB(databasepath)
  test=DensDatByRegion(ODB,'GeorgiaStrait',DenCat=1)

  print('\n type(test) ',type(test))
  print(test)
  print(len(test))
  print(len(DensDatByRegion(ODB,'GeorgiaStrait',DenCat=1)    ))
  print(len(DensDatByRegion(ODB,'GeorgiaStrait',DenCat=2)    ))
  print(len(DensDatByRegion(ODB,'GeorgiaStrait',DenCat=3)    ))
  print(len(DensDatByRegion(ODB,'GeorgiaStrait',DenCat=-1)    ))
