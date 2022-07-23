"""
Creator: Ivanovitch Silva
Date: 30 Jan. 2022
Implement a machine pipeline component that
incorporate preprocessing and train stages.
"""
import argparse
import logging
import os

import yaml
import tempfile
import mlflow
from mlflow.models import infer_signature
from sklearn.impute import SimpleImputer

import pandas as pd
import matplotlib.pyplot as plt
import wandb
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import plot_tree

# configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(message)s",
                    datefmt='%d-%m-%Y %H:%M:%S')

# reference for a logging obj
logger = logging.getLogger()


#Custom Transformer that extracts columns passed as argument to its constructor 
class FeatureSelector( BaseEstimator, TransformerMixin ):
    #Class Constructor 
    def __init__( self, feature_names ):
        self.feature_names = feature_names 
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        return X[ self.feature_names ]
        
# Handling categorical features 
class CategoricalTransformer( BaseEstimator, TransformerMixin ):
    # Class constructor method that takes one boolean as its argument
    def __init__(self, new_features=True, colnames=None):
        self.new_features = new_features
        self.colnames = colnames

    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 

    def get_feature_names(self):
        return self.colnames.tolist()

    # Transformer method we wrote for this transformer 
    def transform(self, X , y = None):
        df = pd.DataFrame(X,columns=self.colnames)

        # customize feature?
        # how can I identify this one? EDA!!!!
        #if self.new_features: 

        ## TODO
        
        # update column names
        self.colnames = df.columns      

        return df

# transform numerical features
class NumericalTransformer( BaseEstimator, TransformerMixin ):
    # Class constructor method that takes a model parameter as its argument
    # model 0: minmax
    # model 1: standard
    # model 2: without scaler
    def __init__(self, model = 0, colnames=None):
        self.model = model
        self.colnames = colnames

    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self

    # return columns names after transformation
    def get_feature_names(self):
        return self.colnames 

    #Transformer method we wrote for this transformer 
    def transform(self, X , y = None ):
        df = pd.DataFrame(X,columns=self.colnames)

        # update columns name
        self.colnames = df.columns.tolist()

        # minmax
        if self.model == 0: 
            scaler = MinMaxScaler()
            # transform data
            df = scaler.fit_transform(df)
        elif self.model == 1:
            scaler = StandardScaler()
            # transform data
            df = scaler.fit_transform(df)
        else:
            df = df.values

        return df

def process_args(args):

    run = wandb.init(job_type="train")

    logger.info("Downloading and reading train artifact")
    local_path = run.use_artifact(args.train_data).file()
    df_train = pd.read_csv(local_path)

    # Spliting train.csv into train and validation dataset
    logger.info("Spliting data into train/val")
    # split-out train/validation and test dataset
    x_train, x_val, y_train, y_val = train_test_split(df_train.drop(labels=args.stratify,axis=1),
                                                    df_train[args.stratify],
                                                    test_size=args.val_size,
                                                    random_state=args.random_seed,
                                                    shuffle=True)
    
    logger.info("x train: {}".format(x_train.shape))
    logger.info("y train: {}".format(y_train.shape))
    logger.info("x val: {}".format(x_val.shape))
    logger.info("y val: {}".format(y_val.shape))

    logger.info("Removal Outliers")
    # temporary variable
    x = x_train.select_dtypes("number").copy()

    # identify outlier in the dataset
    lof = LocalOutlierFactor()
    outlier = lof.fit_predict(x)
    mask = outlier != -1

    logger.info("x_train shape [original]: {}".format(x_train.shape))
    logger.info("x_train shape [outlier removal]: {}".format(x_train.loc[mask,:].shape))

    # dataset without outlier, note this step could be done during the preprocesing stage
    x_train = x_train.loc[mask,:].copy()
    y_train = y_train[mask].copy()

    # Pipeline generation
    logger.info("Pipeline generation")

    # Get the configuration for the pipeline
    with open(args.model_config) as fp:
        model_config = yaml.safe_load(fp)
        
    # Add it to the W&B configuration so the values for the hyperparams
    # are tracked
    wandb.config.update(model_config)
    
    # Categrical features to pass down the categorical pipeline 
    categorical_features = x_train.select_dtypes("object").columns.to_list()

    # Numerical features to pass down the numerical pipeline 
    numerical_features = x_train.select_dtypes("number").columns.to_list()

    
    # Defining the steps in the categorical pipeline 
    categorical_pipeline = Pipeline(steps = [('cat_selector',FeatureSelector(categorical_features)),
                                             ('imputer_cat', SimpleImputer(strategy="most_frequent")),
                                             #('cat_transformer', #CategoricalTransformer(colnames=categorical_features)),
                                             #('cat_encoder','passthrough'
                                             ('cat_encoder',OneHotEncoder(sparse=False,drop="first"))
                                            ]
                                   )
    # Defining the steps in the numerical pipeline     
    numerical_pipeline = Pipeline(steps = [('num_selector', FeatureSelector(numerical_features)),
                                           ('imputer_num', SimpleImputer(strategy="median")),
                                           ('num_transformer', NumericalTransformer(model_config["numerical_pipe"]["model"],
                                                                                   colnames=numerical_features))
                                          ]
                                 )

    # Combining numerical and categorical piepline into one full big pipeline horizontally 
    # using FeatureUnion
    full_pipeline_preprocessing = FeatureUnion(transformer_list = [('cat_pipeline', categorical_pipeline),
                                                                   ('num_pipeline', numerical_pipeline)
                                                                  ]
                                              )
   
    
    # The full pipeline 
    pipe = Pipeline(steps = [('full_pipeline', full_pipeline_preprocessing),
                             ("regressor",DecisionTreeRegressor(**model_config["decision_tree"]))
                            ]
                   )

    # training 
    logger.info("Training")
    pipe.fit(x_train,y_train)

    # predict
    logger.info("Infering")
    predict = pipe.predict(x_val)
    
    # Evaluation Metrics
    logger.info("Evaluation metrics")
    
    # Metric: Mean Absolute Error
    mae = mean_absolute_error(y_val, predict)
    run.summary["MAE"] = mae
    
    # Metric: Root Mean Squared Error
    RMSE = mean_squared_error(y_val, predict, squared=False)
    run.summary["RMSE"] = RMSE
    
    # Metric: R2 Score
    r2score = r2_score(y_val, predict)
    run.summary["R2SCORE"] = r2score
    
    # Metric: renderize the tree
    # full pipeline
    features_full = pipe.named_steps['full_pipeline']

    # get columns names from categorial columns
    features_cat = features_full.get_params()["cat_pipeline"]
    features_cat = features_cat[2].get_feature_names_out().tolist()
    
    # get columns names from numerical columns
    features_num = features_full.get_params()["num_pipeline"][2].get_feature_names()
    
    # Export if required
    if args.export_artifact != "null":
        export_model(run, pipe, x_val, predict, args.export_artifact)

        
def export_model(run, pipe, x_val, val_pred, export_artifact):

    # Infer the signature of the model
    signature = infer_signature(x_val, val_pred)

    with tempfile.TemporaryDirectory() as temp_dir:

        export_path = os.path.join(temp_dir, "model_export")

        mlflow.sklearn.save_model(
            pipe, # our pipeline
            export_path, # Path to a directory for the produced package
            serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE,
            signature=signature, # input and output schema
            input_example=x_val.iloc[:2], # the first few examples
        )

        artifact = wandb.Artifact(
            export_artifact,
            type="model_export",
            description="Decision Tree pipeline export",
        )
        
        # NOTE that we use .add_dir and not .add_file
        # because the export directory contains several
        # files
        artifact.add_dir(export_path)

        run.log_artifact(artifact)

        # Make sure the artifact is uploaded before the temp dir
        # gets deleted
        artifact.wait()        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a Decision Tree",
        fromfile_prefix_chars="@",
    )
    
    parser.add_argument(
        "--train_data",
        type=str,
        help="Fully-qualified name for the training data artifact",
        required=True,
    )

    parser.add_argument(
        "--model_config",
        type=str,
        help="Path to a YML file containing the configuration for the random forest",
        required=True,
    )

    parser.add_argument(
        "--export_artifact",
        type=str,
        help="Name of the artifact for the exported model. Use 'null' for no export.",
        required=False,
        default="null",
    )

    parser.add_argument(
        "--random_seed",
        type=int,
        help="Seed for the random number generator.",
        required=False,
        default=42
    )

    parser.add_argument(
        "--val_size",
        type=float,
        help="Size for the validation set as a fraction of the training set",
        required=False,
        default=0.3
    )

    parser.add_argument(
        "--stratify",
        type=str,
        help="Name of a column to be used for stratified sampling. Default: 'null', i.e., no stratification",
        required=False,
        default="null",
    )

    ARGS = parser.parse_args()

    process_args(ARGS)

