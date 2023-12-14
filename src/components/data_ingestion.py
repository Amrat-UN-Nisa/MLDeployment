#Read the data from any source (local source).
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass# use to create the class variables.

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

# from src.components.model_trainer import ModelTrainerConfig
# from src.components.model_trainer import ModelTrainer
@dataclass
#Anything that are specific required for the input  we gave here
class DataIngestionConfig:
    #Directly define the class variable by the used of the decorators"dataclass".
    #Dataingestion know where to save the data
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")
#Inside thw class variable we used the  init() to define the variables     
class DataIngestion:
    def __init__(self):
        #initialized the three input
        self.ingestion_config=DataIngestionConfig()

    #read data from the DB
    def initiate_data_ingestion(self):
            logging.info("Entered the data ingestion method or component")
            try:
                df=pd.read_csv('D:/ML_deployment/notebook/data/stud.csv')
                logging.info('Read the dataset as dataframe')

                os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
                #save data on that path
                df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
                #index = False, means the index won't be included in the CSV file.
                #header = True, means the header with column names will be included in the CSV file.
                logging.info("Train test split initiated")
                train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

                train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

                test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

                logging.info("Inmgestion of the data iss completed")

                return(
                    self.ingestion_config.train_data_path,
                    self.ingestion_config.test_data_path

                )
            except Exception as e:
                raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    # obj.initiate_data_ingestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)
    # train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    # modeltrainer=ModelTrainer()
    # print(modeltrainer.initiate_model_trainer(train_arr,test_arr))