'''2015-06-15 Force DenCat values from .mdb file to be integers
20220914 Read data from CSV file instead of MDB-table
'''
import csv
from numpy import ndarray,array


class DensDatByRegion(ndarray):
  '''A numpy.array of density values'''
  def __new__(self,InFile205,Region,DenCat=-1,FieldType=int):
 
      
      file = open(InFile205, "r")
      data = list(csv.DictReader(file, delimiter=","))
      for t in data:
          if t['DenCat']=='':t['DenCat']=-1
      
      if Region:
          data=[t for t in data if t['QuotaCalcRegion']==Region]
          
      if not(Region):
            data=[t for t in data if not(t['QuotaCalcRegion'])]
      if DenCat>-1:
            data=[t for t in data if t['DenCat']==str(DenCat)]
          
      
      result=[float(t['CurrentDensity']) for t in data]  
      return(array(result))
        
