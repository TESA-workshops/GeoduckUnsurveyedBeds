from ADO import adoBaseClass as OpenDB

'''GetTpye(ODB,TableName="[103-All_Beds_w_Area_MeanWt_DenCat_QRegion].",FieldName="DenCat")
    Returns the data-type for DenCat-field in the [103-All_Beds_w_Area_MeanWt_DenCat_QRegion] table.
    
    '''
    
def ReadDenCatType(ODB,TableName="[103-All_Beds_w_Area_MeanWt_DenCat_QRegion].",FieldName="DenCat"):
    
    FieldDesignate= TableName+TableName       
    query ='SELECT First('
    query+=FieldDesignate
    query+=") AS FirstValue "
    
    query+="FROM "
    query+=TableName[:-1]
    query+=' '
    query+='HAVING ( '
    query+=FieldDesignate
    query+='( is Not Null );'
    ODB.execute(query)
    
    DummyVal=ODB.GetVariable(FirstValue)
    result=type(DummyVal)
    return(result)
        
class DenCatType():
    '''Class with globally accessible values indicating the datatype for DenCat'''
    def __init__(self, ODB,TableNames= ['[103-All_Beds_w_Area_MeanWt_DenCat_QRegion].','[205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion].']):    
        
        TN=TableNames
        if isinstance(TN,str):
            TN=[TN]
        global DCT
        DCT={}
        for tn in TN:
            DCT[tn]=ReadDenCatType(ODB,TableName=tn,FieldName="DenCat")
        
if __name__ == "__main__":
  databasepath='q:\\analyses\\QuotaOptionCalculations\\20150612.bugcheck\\2016_Quotas.mdb'
  ODB=OpenDB(databasepath)   
  dummy=DenCatType(ODB)
  print (DCT)