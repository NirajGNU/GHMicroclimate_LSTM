import sys
import os

import numpy as np
import pandas as pd



from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass

class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    
class DataTransformation:
    
    def __init__(self, config : DataTransformationConfig):
        self.data_tranformation_config = config
        
    def get_data_transformer_object(self):
        
        try:
            numerical_columns = ["externalsolarradiation","outsidetemperature","outsidehumidity","windspeed","temperature_avg"]
            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
        
            logging.info("Data pipeline made to impute the missing data and scaling the required columns")
        
            preprocessor = ColumnTransformer([
                # Add your transformers here
            ("num_pipeline", numerical_pipeline, numerical_columns)
            ])
            
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")
            
            logging.info("Obtaining the preprocessor object")
            
            preprocessor_object = self.get_data_transformer_object()
            
            extra_column_name = ['geothermal1humidity','geothermal2humidity','geothermal3humidity','geothermal4humidity','geothermal_avg','temperature_avg','humidty123_avg','humidty4_avg']
            traget_column_name = "temperature_avg"
            numerical_column = ["externalsolarradiation","outsidetemperature","outsidehumidity","windspeed"]
            
            input_feature_train_df = train_df.drop(columns= extra_column_name,axis=1)
            target_feature_train_df = train_df[traget_column_name]
            
            input_feature_test_df = test_df.drop(columns=extra_column_name, axis=1)
            target_feature_test_df= test_df[traget_column_name]
            
            logging.info('Applying the preprocessing object on training dataf')
            
            input_feature_train_arr = preprocessor_object.fit_transform(input_feature_train_df)
            input_feature_test_arr= preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[
                input_feature_train_arr,
                np.arry(target_feature_train_df)
            ]
            
            test_arr =np.c_[
                input_feature_test_arr,
                np.arr[target_feature_test_df]
            ]
            # print(train_arr)
            # print(test_arr)
            logging.info("Save preprocessing object.")
            
            save_object(
                fiel_path = self.data_tranformation_config.preprocessor_obj_file_path, object= preprocessor_object
            )
            
            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)   
        
        
    
    
    

