from ADO import adoBaseClass as OpenDB

import pdb

class DensEstimates:
    '''Density estimates as recorded in the Dom-database
       Called CBedData in previous implementation'''
    def __init__(self,ODB,QuotaCalcRegion=None,stat_area=None,sub_area=None,DenCat=-1,TableName="[103-All_Beds_w_Area_MeanWt_DenCat_QRegion]."):
      '''DensEstimates(ODB,QuotaCalcRegion=None,stat_area=None,sub_area=None,DenCat=-1)
      Reads data from the 103-All_Beds_w_Area_MeanWt_DenCat_QRegion table as conceived in the Dom-database

      ODB is a connection to an open Dom-database.  Other variables are based upon field-names'''
      self.ODB=ODB
      self.QuotaCalcRegion=QuotaCalcRegion
      self.stat_area=stat_area
      self.sub_area=sub_area
      self.DenCat=DenCat
      self.TableName=TableName

      query=self.MakeQuery()
      try:
        self.ODB.execute(query)
      except:
          print('/nDensEstimates 21')
          print(query)
          self.ODB.execute(query)
      self.ODB.DefineFieldNames()
      nfield=self.ODB.GetFieldCount()
      self.values=[]
      if(self.ODB.rs.EOF):return #no data in query
      ODB.rs.MoveFirst()
      while not(self.ODB.rs.EOF):
          CurRec=ODB.Get()
          CurVal={}
          for i in range(nfield):CurVal[ODB.Fname[i]]=CurRec[i]
          self.values+=[CurVal]

    def MakeQuery(self):
      querySelect = "SELECT  "
      querySelect+=self.TableName+"counter, "
      querySelect+=self.TableName+"description, "
      querySelect+=self.TableName+"stat_area, "
      querySelect+=self.TableName+"sub_area, "
      querySelect+=self.TableName+"bed_code, "
      querySelect+=self.TableName+"TextCode, "
      querySelect+=self.TableName+"gis_code, "
      querySelect+=self.TableName+"BedArea, "
      querySelect+=self.TableName+"BedAreaSE, "
      querySelect+=self.TableName+"MeanWt, "
      querySelect+=self.TableName+"MeanWtSE, "
      querySelect+=self.TableName+"MeanWtSource, "
      querySelect+=self.TableName+"QuotaCalcRegion, "
      querySelect+=self.TableName+"LicenceRegion, "
      querySelect+=self.TableName+"DenCat "

      queryFrom= " FROM "+self.TableName[:-1] +" "

      WhereString=[]
      if self.QuotaCalcRegion!=None:WhereString+=["("+self.TableName+"QuotaCalcRegion='"+self.QuotaCalcRegion+"')"]
      if self.stat_area!=None:WhereString+=["("+self.TableName+"stat_area='"+str(self.stat_area)+"')"]
      if self.sub_area!=None:WhereString+=["("+self.TableName+"sub_area='"+str(self.sub_area)+"')"]
      if self.DenCat!=None:WhereString+=["("+self.TableName+"DenCat='"+str(self.DenCat)+"')"]

      queryWhere=''
      if len(queryWhere)==1:queryWhere="Where"+queryWhere[0]
      if len(queryWhere)> 1:queryWhere="Where("+ ' and '.join(queryWhere) +')'

      queryOrder ="Order by "
      queryOrder+=self.TableName+"QuotaCalcRegion, "
      queryOrder+=self.TableName+"stat_area, "
      queryOrder+=self.TableName+"sub_area, "
      queryOrder+=self.TableName+"DenCat; "
      try:
        query=querySelect+queryFrom+queryWhere+queryOrder
      except:
          print('\nDensEstimates 77')
          print('querySelect',querySelect)
          print('queryFrom',queryFrom)
          print('queryWhere',queryWhere)
          print('queryOrder',queryOrder)
          query=querySelect+queryFrom+queryWhere+queryOrder
      return(query)

class ReducedDensEstimates(DensEstimates):
    '''Similar to DensEstimates except that the dataset is reduced to a specific
    value for a specific field'''
    def __init__(self,oriDensEstimates,fieldname,fieldvalue):
      '''ReducedDensEstimates(oriDensEstimates,fieldname,value)'''
      self.ODB=oriDensEstimates.ODB
      self.QuotaCalcRegion=oriDensEstimates.QuotaCalcRegion
      self.stat_area=oriDensEstimates.stat_area
      self.sub_area=oriDensEstimates.sub_area
      self.DenCat=oriDensEstimates.DenCat
      self.TableName=oriDensEstimates.TableName

      #make a deep copy of the data-values
      temp=list(map(lambda x:x,oriDensEstimates.values))
      self.values=list(filter(lambda x:x[fieldname]==fieldvalue ,temp))

        
              
if __name__ == "__main__":
  databasepath='H:\\QuotaCalcs\\data\\2014_Quotas.mdb'
  ODB=OpenDB(databasepath)
  test=DensEstimates(ODB)
  print('type(test)', type(test) )
  print('dir(test)', dir(test) )
  print('len(test.values)', len(test.values) )
  print(' \ntest.values[0]', test.values[0])
  print(' \ntest.values[-1]', test.values[-1])

  test2= ReducedDensEstimates(test,'QuotaCalcRegion','WCVI')   
  print('\nlen(test.values)', len(test.values) )
  print(  'len(test2.values)', len(test2.values) )    
  print(' \ntest.values[0]', test.values[0])
  print(' \ntest.values[-1]', test.values[-1])
  print(' \ntest2.values[0]', test2.values[0])
  print(' \ntest2.values[-1]', test2.values[-1])          

