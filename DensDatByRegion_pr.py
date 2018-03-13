'''2015-06-15 Force DenCat values from .mdb file to be integers
   2018-02-22 Variation on DensDatByRegion.
     Get the prime-densities
'''
from ADO import adoBaseClass as OpenDB
from numpy import ndarray,array


class DensDatByRegion_pr(ndarray):
  '''A numpy.array of density values'''
  def __new__(self,ODB,Region,DenCat=-1,FieldType=int):
 
      query ='SELECT [401-Dprime_on_SurveyedBeds_w_QuotaCalcRegion].Dprime '
      query+=' FROM [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion]  '
      query+=  ' INNER JOIN [401-Dprime_on_SurveyedBeds_w_QuotaCalcRegion] ON  '
      query+=       ' [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].GIS_Code =  '
      query+=       ' [401-Dprime_on_SurveyedBeds_w_QuotaCalcRegion].GIS_Code '

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
      result=ODB.GetVariable('Dprime')
      return(array(result))
        

if __name__ == "__main__":
  databasepath='D:\\Coding\\GeoduckQuotaCalcs\\TestOutput\\2019TestData.accdb'
  ODB=OpenDB(databasepath)
  test=DensDatByRegion_pr(ODB,'GeorgiaStrait',DenCat=1)

  print('\n type(test) ',type(test))
  print(test)
  print(len(test))
  print(len(DensDatByRegion_pr(ODB,'Area12',DenCat=1)    ))
  print(len(DensDatByRegion_pr(ODB,'Area12',DenCat=2)    ))
  print(len(DensDatByRegion_pr(ODB,'Area12',DenCat=3)    ))
  print(len(DensDatByRegion_pr(ODB,'Area12',DenCat=-1)    ))
  
  print()
  i=1
  print(i)
  print(DensDatByRegion_pr(ODB,'Area12',DenCat=i) )
  i=2
  print(i)
  print(DensDatByRegion_pr(ODB,'Area12',DenCat=i) )
  i=3
  print(i)
  print(DensDatByRegion_pr(ODB,'Area12',DenCat=i) )
  i=-1
  print(i)
  print(DensDatByRegion_pr(ODB,'Area12',DenCat=i) )
