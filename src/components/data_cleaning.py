import os
import sys
from src.exception import CustomException
from src.logger import logging

from src.components.data_transform  import DataTransformation
from src.components.data_transform import DataTransformationConfig

import pandas as pd
import numpy as np


from dataclasses import dataclass

@dataclass

class DataCleanConfig:
    cltrain_data_path: str = os.path.join('artifacts', 'cltrain.csv')
    cltest_data_path: str = os.path.join('artifacts', 'cltest.csv')


class DataClean:
    
    def __init__(self, config: DataCleanConfig):
        self.dataclean_config = config
        
    def initiate_data_clean(self, filename):
        logging.info ('Cleaning the ingest train and test data')
        
        try:
            clean_df = pd.read_csv(os.path.join('artifacts', filename))
            
            # Combine date and time column and made DateTime column as index
            clean_df['Datetime'] = clean_df['Date' ] + [' '] + clean_df['Time']
            clean_df = clean_df.drop('Date', axis=1)
            clean_df= clean_df.drop('Time', axis=1)
            clean_df['Datetime'] = pd.to_datetime(clean_df['Datetime'], format='%m/%d/%Y %H:%M:%S')
            clean_df= clean_df.set_index('Datetime')
            
            logging.info("DateTime conversion and indexing complete")
            
            all_col = list(clean_df)
            col_list = all_col[:]

            clean_df = clean_df[col_list]

            for col in col_list:
                clean_df[col] = pd.to_numeric(clean_df[col],errors='coerce')
                
            logging.info("Data Cleaning initiated and convert all column into numerical categories")
                
            if str(filename)=='trian.csv':
                clean_df.to_csv(self.dataclean_config.cltrain_data_path, index=True, header=True)
                return self.dataclean_config.cltrain_data_path
            else:
                clean_df.to_csv(self.dataclean_config.cltest_data_path, index=True, header=True)
                return self.dataclean_config.cltest_data_path
            
                
         
            
        except Exception as e:
            raise CustomException(e, sys)
    
if __name__ == '__main__':
    obj = DataClean(DataCleanConfig)
    cltrain_data = obj.initiate_data_clean('train.csv')
    cltest_data = obj.initiate_data_clean('test.csv')
    
    data_transformationobj = DataTransformation(DataTransformationConfig)
    data_transformationobj.initiate_data_transformation(cltrain_data,cltest_data)