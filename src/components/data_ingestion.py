#this module defines the data ingestion component:
# - loads data from source
# - performs minimal validation and filtering
# - integrates datasets
# - train-test splits

import sys
import os

from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transform import DataTransformation
from src.components.data_transform import DataTransformationConfig

#class to hold vars, to be used in data ingestion
@dataclass #to avoid __init__ (mostly only for data containers!)
class DataIngestionConfig:
    drug_synergy_data_path: str=os.path.join('artifacts', 'drug_synergy.csv')
    cell_lines_data_path: str=os.path.join('artifacts', 'cell_lines.csv')
    drug_portfolio_data_path: str=os.path.join('artifacts', 'drug_portfolio.csv')

    interim_data_path: str = os.path.join('artifacts', 'interim.csv')
    train_data_path: str=os.path.join('artifacts', 'train.csv')
    test_data_path: str=os.path.join('artifacts', 'test.csv')

#class for data ingestion
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig() #creates instance of DataIngestionConfig class

    def initiate_data_ingestion(self):
        ''' Takes, stores, lightlty preprocess and merges original data. Train-test splits, stores and returs resulting dfs '''
        logging.info( 'Entered the data ingestion component' )

        try: 
            #extract data, could be web
            drug_synergy_df=pd.read_csv('notebook/data/drug_synergy.csv')
            cell_lines_df=pd.read_csv('notebook/data/cell_lines.csv')
            drug_portfolio_df=pd.read_csv('notebook/data/drug_portfolio.csv', sep='\t')

            logging.info( 'Datasets loaded succsesfully' )

            #store locally
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) #create folder
            
            drug_synergy_df.to_csv( self.ingestion_config.drug_synergy_data_path, index=False, header=True ) #uses held vars
            cell_lines_df.to_csv( self.ingestion_config.cell_lines_data_path, index=False, header=True )
            drug_portfolio_df.to_csv( self.ingestion_config.drug_portfolio_data_path, index=False, header=True )

            #minimal validation / filtering -----------------------------------------------------------------------------------------------
            drug_synergy_df = drug_synergy_df[drug_synergy_df.QA == 1] #quality filtering

            #feature selection
            drug_synergy_df = drug_synergy_df[['Cell line name', 'Compound A', 'Compound B', 'Max. conc. A', 'Max. conc. B', 'IC50 A', 'H A', 'Einf A', 'IC50 B', 'H B', 'Einf B', 'Synergy score']].drop_duplicates()
            cell_lines_df = cell_lines_df[['Cell line name', 'GDSC tissue descriptor 2', 'MSI', 'Growth properties']].drop_duplicates()
            drug_portfolio_df_A = drug_portfolio_df[['Challenge drug name', 'Putative target','Function', 'Pathway']].drop_duplicates()
            drug_portfolio_df_B = drug_portfolio_df[['Challenge drug name', 'Putative target','Function', 'Pathway']].drop_duplicates()

            #renaming
            drug_portfolio_df_A.columns = ['Compound A', 'Putative target A','Function A', 'Pathway A']
            drug_portfolio_df_B.columns = ['Compound B', 'Putative target B','Function B', 'Pathway B']

            #data integration 
            df = pd.merge(drug_synergy_df, cell_lines_df, on='Cell line name')
            df = pd.merge(df, drug_portfolio_df_A, on='Compound A')
            df = pd.merge(df, drug_portfolio_df_B, on='Compound B')

            logging.info(f'Merged dataset shape: {df.shape}')
            #-----------------------------------------------------------------------------------------------------------------------------

            #save dataset 
            df.to_csv( self.ingestion_config.interim_data_path, index=False ) 

            #train-test split
            os.makedirs( os.path.dirname( self.ingestion_config.train_data_path), exist_ok=True ) 
            os.makedirs( os.path.dirname( self.ingestion_config.test_data_path), exist_ok=True ) 
            
            logging.info( 'Train-test split initiated' )
            train_set, test_set = train_test_split( df, test_size=0.2, random_state=42 )
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info( 'Data ingestion is completed' )

            return( 
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys) #if something happens, use our custom exception
        
if __name__=='__main__':
    obj=DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation( train_data, test_data )
#every python files has a built in varaible __name__. If file ran directly, __name__ = '__main__', so the
#block runs. If the file is imported, __name__ ='src.components.data_ingestion' and the block doesn't run

#then, this block is for testing, as it only runs if we directly run it, not if its imported from somewhere