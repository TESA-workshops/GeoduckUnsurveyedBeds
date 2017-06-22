from ADO import adoBaseClass as OpenDB
from numpy import ndarray,array
from DenCatInRegion import DenCatInRegion
from AllSurveyedRegion import AllSurveyedRegion



class DenCatAllRegion(ndarray):
  '''A numpy.array of density-classes occuring in the regions'''
  def __new__(self,ODB,Regions=None):
      
      if Regions==None:Regions=AllSurveyedRegion(ODB)
      if not isinstance(Regions,(list,ndarray)):return(DenCatAllRegion(ODB,Regions=[Regions]))
      result=list(map(lambda r: DenCatInRegion(ODB,r)    ,Regions))
 
      return(array(result))
        

if __name__ == "__main__":
  databasepath='H:\\QuotaCalcs\\data\\2014_Quotas.mdb'
  ODB=OpenDB(databasepath)
  test=DenCatAllRegion(ODB)

  print('\n type(test) ',type(test))
  print(test)
  print(len(test))
