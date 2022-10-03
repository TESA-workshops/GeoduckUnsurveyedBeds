'''
20220913
Read density-category from a CSV file
'''


import csv

'''GetTpye(ODB,TableName="[103-All_Beds_w_Area_MeanWt_DenCat_QRegion].",FieldName="DenCat")
    Returns the data-type for DenCat-field in the [103-All_Beds_w_Area_MeanWt_DenCat_QRegion] table.
    
    '''
    
def ReadDenCatType(FileName="C:\\Analyses\\2023GduckQuotaCalcs\\data\\103-All_Beds_w_Area_MeanWt_DenCat_QRegion.csv",FieldName="DenCat"):
    
    file = open(FileName, "r")
    data = list(csv.DictReader(file, delimiter=","))
    for t in data:
        if t['DenCat']=='':t['DenCat']=-1
    result=type(data[0][FieldName])
    return(result)
        
class DenCatType():
    '''Class with globally accessible values indicating the datatype for DenCat'''
    def __init__(self, FileName= [\
                                    "C:\\Analyses\\2023GduckQuotaCalcs\\data\\103-All_Beds_w_Area_MeanWt_DenCat_QRegion.csv",\
                                    "C:\\Analyses\\2023GduckQuotaCalcs\\data\\205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion.csv"]):    
        
        TN=FileName
        if isinstance(TN,str):
            TN=[TN]
        global DCT
        DCT={}
        for tn in TN:
            DCT[tn]=ReadDenCatType(FileName=tn,FieldName="DenCat")
        
if __name__ == "__main__":
  FileName="C:\\Analyses\\2023GduckQuotaCalcs\\data\\103-All_Beds_w_Area_MeanWt_DenCat_QRegion.csv"
  print(ReadDenCatType())
  DCT=DenCatType(FileName="C:\\Analyses\\2023GduckQuotaCalcs\\data\\103-All_Beds_w_Area_MeanWt_DenCat_QRegion.csv")
  print(DCT)
  
  DCType=DenCatType(FileName=[\
                                  "C:\\Analyses\\2023GduckQuotaCalcs\\data\\103-All_Beds_w_Area_MeanWt_DenCat_QRegion.csv",\
                                  "C:\\Analyses\\2023GduckQuotaCalcs\\data\\205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion.csv"])
  print(DCT)
  
  
  DCType=DenCatType(FileName=[\
                                  "C:\\Analyses\\2023GduckQuotaCalcs\\data\\103-All_Beds_w_Area_MeanWt_DenCat_QRegion.csv",\
                                  "C:\\Analyses\\2023GduckQuotaCalcs\\data\\205-CurrentDen_on_Surveyed_Beds_w_DenCat_QRegion.csv"])
  print(DCT)
  
  