import csv
from numpy import ndarray


class AllSurveyedRegion(list):
  '''A numpy.array of density values'''
  def __new__(self,FileName="C:\\Analyses\\2023GduckQuotaCalcs\\data\\205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion.csv",FieldName='QuotaCalcRegion'):
 
    
    file = open(FileName, "r")
    data = list(csv.DictReader(file, delimiter=","))
    for t in data:
        if t['DenCat']=='':t['DenCat']=-1
    result=[t[FieldName] for t in data] 
    result=list(set(result))
    result.sort()
    print(type(result),type(result[0]), result)
    return(result)
        

if __name__ == "__main__":
  FileName='C:\\Analyses\\2023GduckQuotaCalcs\\data\\205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion.csv'
  FieldName='QuotaCalcRegion'
  test=AllSurveyedRegion(FileName=FileName, FieldName=FieldName)

  for t in test:print(t)
