##############################
#Data Min Max Standardization#
##############################
from sklearn import preprocessing
import numpy as np
import pickle as pk
import pandas as pd 

class MinMaxStandard():
    
    def __init__(self,df,columns,target_pickle=None):
        
        #if only one column was supplied as a string
        if type(columns) == type("string"): columns = [columns]
            
        self.target_pickle = target_pickle
        for column in columns:
            self.scale(df,column)
        return None
    
    def scale(self,df,column):
        df[column] = preprocessing.scale(df[column])
        
        return None
        

        
    def save(self,df,target_pickle=None):
        if (target_pickle==None and self.target_pickle == None): raise ValueError("No file name was supplied")
        with open(self.target_pickle,'wb') as f:
            pk.dump(df,f)