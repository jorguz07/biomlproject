#this module defines the data ingestion component:
# - loads data from source systems
# - performs minimal validation and filtering
# - integrates datasets
# - persists data for downstream processing

import sys
import os

#from pathlib import Path
#sys.path.append(str(Path(__file__).parent.parent))

from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

#class to store vars, to be used in data ingestion
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
        ''' Takes, stores, preprocess and merges original data sources. Does test-split, stores and returs resulting dfs '''
        logging.info( 'Entered the data ingestion component' )

        try: #where data is stored, could also be web
            drug_synergy_df=pd.read_csv('notebook/data/drug_synergy.csv')
            cell_lines_df=pd.read_csv('notebook/data/cell_lines.csv')
            drug_portfolio_df=pd.read_csv('notebook/data/drug_portfolio.csv', sep='\t')

            logging.info( 'Datasets loaded succsesfully' )

            #data was extracted from source, now we store it locally
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            drug_synergy_df.to_csv( self.ingestion_config.drug_synergy_data_path, index=False, header=True ) #uses attributes to def paths
            cell_lines_df.to_csv( self.ingestion_config.cell_lines_data_path, index=False, header=True )
            drug_portfolio_df.to_csv( self.ingestion_config.drug_portfolio_data_path, index=False, header=True )

            #minimal validation / filtering -----------------------------------------------------------------------------------------------
            drug_synergy_df = drug_synergy_df[drug_synergy_df.QA == 1] #quality filtering

            #feature selection
            drug_synergy_df = drug_synergy_df[['Cell line name', 'Compound A', 'Compound B', 'Max. conc. A', 'Max. conc. B', 'IC50 A', 'H A', 'Einf A', 'IC50 B', 'H B', 'Einf B', 'Synergy score']].drop_duplicates()
            cell_lines_df = cell_lines_df[['Cell line name', 'GDSC tissue descriptor 2', 'MSI', 'Growth properties']].drop_duplicates()
            drug_portfolio_df_A = drug_portfolio_df[['Challenge drug name', 'Putative target','Function', 'Pathway']].drop_duplicates()
            drug_portfolio_df_B = drug_portfolio_df[['Challenge drug name', 'Putative target','Function', 'Pathway']].drop_duplicates()

            #renaming cols
            drug_portfolio_df_A.columns = ['Compound A', 'Putative target A','Function A', 'Pathway A']
            drug_portfolio_df_B.columns = ['Compound B', 'Putative target B','Function B', 'Pathway B']

            #data integration 
            df = pd.merge(drug_synergy_df, cell_lines_df, on='Cell line name')
            df = pd.merge(df, drug_portfolio_df_A, on='Compound A')
            df = pd.merge(df, drug_portfolio_df_B, on='Compound B')

            logging.info(f'Merged dataset shape: {df.shape}')

            #-----------------------------------------------------------------------------------------------------------------------------

            #save combined dataset 
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
    obj.initiate_data_ingestion()
#this means, 'only run code if file executed directly' (not imported)
#avoids pipeline to run automatically if e.g. from src.data_ingestion import DataIngestion