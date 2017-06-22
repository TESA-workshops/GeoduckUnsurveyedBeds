from ADO import adoBaseClass as OpenDB
from numpy import ndarray,array


class DenCatInRegion(ndarray):
  '''A numpy.array of density values'''
  def __new__(self,ODB,Region):
 
      query ='SELECT Distinct [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].DenCat '
      query+=' FROM [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion] '
      query+='Where( '
      query+=   "([205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion='"
      query+=   Region +"')"
     
      query+= " and "
      query+= "(  [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].DenCat Is Not Null)  "
      query+=') '
      query+='Order By [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].DenCat; '
      
      try:
        ODB.execute(query)
      except:
          print('/nDensDatByRegion 25')
          print(query)
          ODB.execute(query)
      result=ODB.GetVariable('DenCat')
      return(array(result,dtype=int))
        

if __name__ == "__main__":
  databasepath='H:\\QuotaCalcs\\data\\2014_Quotas.mdb'
  ODB=OpenDB(databasepath)
  test=DenCatInRegion(ODB,'Area12')

  print('\n type(test) ',type(test))
  print(test)
  print(len(test))
