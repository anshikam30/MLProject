import os, sys

from src.entity.artifact_entity import ClassificationMetricArtifact

from src.exception import NetworkSecurityException
from src.logger import logging

from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score


def get_classification_score(true, predicted) ->ClassificationMetricArtifact :
    try:
        
        f1 = f1_score(true, predicted)
        recall = recall_score(true, predicted)
        precision = precision_score(true, predicted)
        
        classification = ClassificationMetricArtifact(f1_score=f1, precision_score= precision, recall_score=recall)
        return classification
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    


from src.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

class NetworkModel:
    def __init__(self, preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)