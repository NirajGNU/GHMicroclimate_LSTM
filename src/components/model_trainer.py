from tensorflow import keras
from keras import Sequential, layers, callbacks 
from keras.layers import Dense, LSTM, GRU, Dropout, Bidirectional, LayerNormalization

from src.exception import CustomException
from src.logger import logging

import os 
import sys

from src.utils import save_object

from dataclasses import dataclass

@dataclass

class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
    
class ModelTrainer:
    def __init__(self,config:ModelTrainerConfig):
        self.model_trainer_config = config
        
    def model_LSTM(X_train, y_train, lstm_units):
        model = Sequential()
        model.add(LSTM(units=lstm_units, return_sequences=True, input_shape=X_train.shape, y_train.shape))
        model.add(Dropout(0.001))
        # #Second Lstm layer
        model.add(LSTM(units=lstm_units))
        model.add(Dropout(.001))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer = 'adam')
        return model
    
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            models = {
                "LSTM": self.model_LSTM(X_train = X_train, y_train= y_train, lstm_units=64),
                # "Bidirection LSTM" : model_BiLSTM(),
                # "CNN LSTM" : model_CNNLSTM(),
                # "Attention LSTM": model_AttentionLSTM(),                 
            }
            
            
            
        
        except Exception as e:
            raise CustomException(e, sys)
        
    
