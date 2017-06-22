from ADO import adoBaseClass as OpenDB

def GetSurveyedRegions(ODB):
    '''Get all Regions with density estimates'''
    query ='SELECT DISTINCT [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion '
    query+=' FROM [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion] '
    query+='order by  [205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].QuotaCalcRegion ;'

    try:
      ODB.execute(query)
    except:
      print('/nGetSurveyedRegions 12')
      print(query)
      ODB.execute(query)
    result=ODB.GetVariable('QuotaCalcRegion')
    return(result)

if __name__ == "__main__":
  databasepath='H:\\QuotaCalcs\\data\\2014_Quotas.mdb'
  ODB=OpenDB(databasepath)
  test=GetSurveyedRegions(ODB)
  print('\ntest',test)
