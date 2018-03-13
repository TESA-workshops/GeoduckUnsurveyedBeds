from ADO import adoBaseClass as OpenDB
from numpy import ndarray,array


class AllSurveyedRegion(ndarray):
  '''A numpy.array of density values'''
  def __new__(self,ODB):
 
      query ='SELECT distinct [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion '
      query+=' FROM [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion] '
      query+=' order by  [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion ;'
            
      try:
        ODB.execute(query)
      except:
          print('/nAllSurveyedRegion 16')
          print('type(ODB) ',type(ODB))
          print(query)
          ODB.execute(query)
      result=ODB.GetVariable('QuotaCalcRegion')
      return(array(result))
        

if __name__ == "__main__":
  databasepath='H:\\QuotaCalcs\\data\\2014_Quotas.mdb'
  ODB=OpenDB(databasepath)
  test=AllSurveyedRegion(ODB)

  print('\n type(test) ',type(test))
  print(test)
  print(len(test))
