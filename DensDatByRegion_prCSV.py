'''2015-06-15 Force DenCat values from .mdb file to be integers
   2018-02-22 Variation on DensDatByRegion.
     Get the prime-densities
20220914 Read data from CSV file instead of MDB-table
'''
import csv
from numpy import ndarray,array


class DensDatByRegion_pr(ndarray):
  '''A numpy.array of density values'''
  def __new__(self,InFile205,InFile401,Region,DenCat=-1):

      file205 = open(InFile205, "r")
      data205 = list(csv.DictReader(file205, delimiter=","))
      for t in data205:
          if t['DenCat']=='':t['DenCat']=-1
      file401 = open(InFile401, "r")
      data401 = list(csv.DictReader(file401, delimiter=","))
      
      if Region:
          data205=[t for t in data205 if t['QuotaCalcRegion']==Region]
      else:
          data205=[t for t in data205 if (t['QuotaCalcRegion'])=='' or not(t['QuotaCalcRegion'])]
          
    
      if DenCat>-1:
        data205=[t for t in data205 if t['DenCat']==str(DenCat)]
      
      data=[]
      GIS_Code=[int(t['GIS_Code']) for t in data205]
      GIS_Code=list(set(GIS_Code))
      GIS_Code.sort()
      Dprime=[]
      for t in GIS_Code:
          Dprime+=[float(s['Dprime']) for s in data401 if int(s['GIS_Code'])==t]
      Dprime=list(set(Dprime))
      Dprime.sort()

      return(array(Dprime))
        

if __name__ == "__main__":
  InFile103="C:\\Analyses\\2023GduckQuotaCalcs\\data\\103-All_Beds_w_Area_MeanWt_DenCat_QRegion.csv"
  InFile205="C:\\Analyses\\2023GduckQuotaCalcs\\data\\205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion.csv"
  InFile401="C:\\Analyses\\2023GduckQuotaCalcs\\data\\401-Dprime_on_SurveyedBeds_w_QuotaCalcRegion.csv"
  OutFile="C:\\Analyses\\2023GduckQuotaCalcs\\data\\results.csv"
  Region='QCI'
  test1=DensDatByRegion_pr(InFile205,InFile401,Region,DenCat=-1)