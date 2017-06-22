from ADO import adoBaseClass as OpenDB
from numpy import ndarray,array


class DensDatByRegion(ndarray):
  '''A numpy.array of density values'''
  def __new__(self,ODB,Region,DenCat=-1):
 
      query ='SELECT  [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].CurrentDensity '
      query+=' FROM [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion] '

      if (DenCat>-1) or (Region!=None):query+='Where( '
      if Region!=None:

        query+=   "([205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion='"
        query+=   Region +"')"

      if (DenCat>-1) and (Region!=None):query+=" and "
      if DenCat>-1:
        query+= "  (  [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].DenCat= "
        query+=   str(DenCat)+')'
      if (DenCat>-1) or (Region!=None):query+=') '
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
  databasepath='H:\\QuotaCalcs\\data\\2014_Quotas.mdb'
  ODB=OpenDB(databasepath)
  test=DensDatByRegion(ODB,'GeorgiaStrait',DenCat=1)

  print('\n type(test) ',type(test))
  print(test)
  print(len(test))
  print(len(DensDatByRegion(ODB,'GeorgiaStrait',DenCat=1)    ))
  print(len(DensDatByRegion(ODB,'GeorgiaStrait',DenCat=2)    ))
  print(len(DensDatByRegion(ODB,'GeorgiaStrait',DenCat=3)    ))
  print(len(DensDatByRegion(ODB,'GeorgiaStrait',DenCat=-1)    ))
