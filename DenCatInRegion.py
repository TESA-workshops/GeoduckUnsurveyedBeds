'''2015-06-15.  Within the query, force DenCat to be an integer'''



from ADO import adoBaseClass as OpenDB
from numpy import ndarray,array


class DenCatInRegion(ndarray):
  '''A numpy.array of density values'''
  def __new__(self,ODB,Region):
 
      query ='SELECT Distinct cint([205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].DenCat) as DenCat '
      query+=' FROM [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion] '
      query+='Where( '
      query+=   "([205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion='"
      query+=   Region +"')"
     
      query+= " and "
      query+= "(  [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].DenCat Is Not Null)  "
      query+=') '
      query+='Order By cint([205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].DenCat); '
      
      try:
        ODB.execute(query)
      except:
          print('/nDensDatByRegion 25')
          print(query)
          ODB.execute(query)
      result=ODB.GetVariable('DenCat')
      return(array(result,dtype=int))
        

if __name__ == "__main__":
  databasepath='q:\\analyses\\QuotaOptionCalculations\\20150612.bugcheck\\2016_Quotas.mdb'
  ODB=OpenDB(databasepath)
  test=DenCatInRegion(ODB,'Area12')

  print('\n type(test) ',type(test))
  print('\n type(test[0]) ',type(test[0]))
  print(test)
  print(len(test))
