##############################
#Data One Hot Encoder#
##############################
"""Warning ! LabelEncoder does not support handling unknown or NaN values when transform meethod is used.# Values should be removed before 
using this class

How to use: 

Object = Categorical(TrainDataFrame,Categorical_Columns)

TrainDataFrame will be updated automatically as DataFrame are mutable 

To transform data : 

Object.transformal_all(TestDataFrame)



"""

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd 
import numpy as np
import pickle as pk

class Categorical():
    
    def __init__(self,df=None,columns=None):
        self.mapping = dict()
        self.hot_encoders_dict = dict()
        self.label_encoders_dict = dict()
        self.columns_used = columns
        if ( type(df) == type(pd.DataFrame()) and columns != None):
            for column in columns:
                self.label_encode(df,column)


        elif (type(df) == type(pd.DataFrame()) and columns == None):
            raise ValueError("Error. You should supply both of columns and the data")
        else:
            pass
               
    def sort_dict(self,mapping):
        key_list = mapping.keys()
        key_list.sort()
        values = list()
        for key in key_list:
            values.append(mapping[key])
        return key_list,values


    def encode_column(self,df,column_name,feature_map=None):
        ohe = OneHotEncoder(handle_unknown="ignore")
        V = df[column_name].copy()
        V = ohe.fit_transform(V.reshape(-1,1)).toarray()
        self.hot_encoders_dict[column_name] = ohe
        active_features = ohe.active_features_
        if feature_map == None:
            feature_names = ohe.active_features_
        else:
            feature_names = list()
            keys,values = self.sort_dict(feature_map)
            for key in keys:
                feature_names.append(values[keys.index(key)])
                
        V = pd.DataFrame(V,columns = feature_names)
        df.drop(column_name,axis=1,inplace=True)
        for i in V.columns:
            df[i] = V[i]
        return df
        

    def Labelize(self,df,column_name):
        LE = LabelEncoder()
        X = df[column_name].copy()
        LE.fit(X)
        self.label_encoders_dict[column_name] = LE
        X = LE.transform(X)
        df[column_name] = X
        feature_mapping = dict()
        i = 0
        for cat in LE.classes_:
            feature_mapping[i] = cat
            i += 1     
        self.mapping[column_name] = feature_mapping
        return feature_mapping


    def label_encode(self,df,column_name):
        mapping = self.Labelize(df,column_name=column_name)
        self.encode_column(df,column_name=column_name,feature_map=mapping)
        return df

    
    def transform(self,df_test,column_name):
        """
        Transforms an input Matrix into formatted matrix based on OneHotEncoder and LabelEncoder that were fitted when object is created
        """
        X = df_test[column_name].copy() 
        X = self.label_encoders_dict[column_name].transform(X)
        df_test[column_name] = X 
        self.encode_column_transform(df_test,column_name=column_name,feature_map=self.mapping[column_name])


    def encode_column_transform(self,df,column_name,feature_map):

        V = df[column_name].copy()
        V = self.hot_encoders_dict[column_name].transform(V.reshape(-1,1)).toarray()
        active_features = self.hot_encoders_dict[column_name].active_features_
        feature_names = list()
        keys,values = self.sort_dict(feature_map)
        for key in keys:
            feature_names.append(values[keys.index(key)])
        V = pd.DataFrame(V,columns = feature_names)
        df.drop(column_name,axis=1,inplace=True)
        for i in V.columns:
            df[i] = V[i]
        return df

    def transformal_all(self,df_test):
        for column in self.columns_used:
            self.transform(df_test,column_name=column)
            
            
    def save_obj(self,df,file_name):
        with open(file_name,'wb') as f:
            pk.dump(df,f)
        
        