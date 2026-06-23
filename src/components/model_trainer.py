
import sys,os
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

from src.exception import NetworkSecurityException
from src.logger import logging

from src.utils.main_utils.utils import save_object, load_object, load_numpy_array
from src.utils.ml_utils.utils import NetworkModel, get_classification_score

from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtfiact, DataTransformationArtifact
from src.constant.training_pipeline import TARGET_COLUMN

import mlflow

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try: 
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def evaluate_models(self,x_train, y_train, x_test, y_test, models, params) -> dict:
        try:
            report = {}
            for i in range(len(list(models))):
                model = list(models.values())[i]
                model_name = list(models.keys())[i]
                para = params[model_name]   
                
                gs = GridSearchCV(model,para,cv =3)
                gs.fit(x_train, y_train)
                
                model.set_params(**gs.best_params_)
                model.fit(x_train, y_train)
                

                y_test_pred = model.predict(x_test)
                test_model_score = accuracy_score(y_test, y_test_pred)
                
                report[model_name] = test_model_score
            return report 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision = classification_metric.precision_score
            recall = classification_metric.recall_score
            
            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.sklearn.log_model(model, "model")
         
    def train_model(self, x_train, y_train, x_test, y_test):
        
        models= {
            "RandomForest" : RandomForestClassifier(verbose=1),
            "DecisionTree" : DecisionTreeClassifier(),
            "LogisticRegression" : LogisticRegression(verbose=1),
            "SupportVector" : SVC(verbose=1),
            "AdaBoost" : AdaBoostClassifier(),
            "GradientBoosting" : GradientBoostingClassifier(verbose=1),
            "KNN" : KNeighborsClassifier()
        }
        params = {
            "RandomForest" : {
                # 'criterion' : ['gini', 'entropy', 'log_loss'],
                # 'max_features' : ['sqrt', 'log2', None],
                'n_estimators' : [8,16,32,64,128,256]
            },
            "DecisionTree" : {
                'criterion' : ['gini', 'entropy', 'log_loss'],
                # 'max_features' : ['sqrt', 'log2'],
                # 'splitter' : ['best','random']
            },
            "LogisticRegression" : {},
            "SupportVector" : {
                'kernel' : ['rbf','linear', 'poly', 'sigmoid'] 
            },
            "AdaBoost" : {
                'learning_rate' : [.1,.01,.5,.001],
                'n_estimators' : [8,16,32,64,128,256]
            },
            "GradientBoosting" :{
                'learning_rate' : [.1,.01,.5,.001],
                # 'criterion' : ['squared_error', 'friedman_mse'],
                # 'max_features' : ['sqrt', 'log2', None],
                # 'loss' : ['log_loss', 'exponential'],
                'n_estimators' : [8,16,32,64,128,256],
                'subsample' : [0.6,0.7,0.75, 0.8, 0.9]
            },
            "KNN" : {
                "n_neighbors": [3,5,7,9]
            }
        }
        model_report :dict = self.evaluate_models(x_train, y_train, x_test, y_test, models, params)
        
        sorted_report = sorted(
            model_report.items(),
            key=lambda x: x[1],
            reverse=True
        )

        best_model_name = sorted_report[0][0]
        best_model_score = sorted_report[0][1]
        
        best_model = models[best_model_name]
        logging.info(f"Best Model is {best_model}")
        
        y_test_pred = best_model.predict(x_test)
        y_train_pred = best_model.predict(x_train)
        classification_score_test = get_classification_score(true = y_test, predicted=y_test_pred)
        classification_score_train = get_classification_score(true = y_train, predicted=y_train_pred)
        
        ##Track mlflow
        self.track_mlflow(best_model, classification_score_train)
        self.track_mlflow(best_model, classification_score_test)
        preprocessor = load_object(path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.model_trainer_trained_file_path)
        os.makedirs(model_dir_path, exist_ok=True)
        
        network_model = NetworkModel(preprocessor=preprocessor, model= best_model)
        save_object(path=self.model_trainer_config.model_trainer_trained_file_path, obj=network_model)
        
        
        ##Model Trainer Artifact
        
        model_trainer_artifact = ModelTrainerArtfiact(trained_model_file_path=self.model_trainer_config.model_trainer_trained_file_path,
                             test_metric_artifact=classification_score_test,
                             trained_metric_artifact=classification_score_train )

        return model_trainer_artifact
    def initiate_model_trainer(self)-> ModelTrainerArtfiact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_npy_path
            test_file_path = self.data_transformation_artifact.transformed_test_npy_path
            
            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)
            
            x_train, x_test, y_train, y_test = train_arr[:, :-1], test_arr[:,:-1], train_arr[:,-1], test_arr[:,-1]
            
            model = self.train_model(x_train, y_train, x_test, y_test)
            return model
        except Exception as e:
            raise NetworkSecurityException(e,sys) 