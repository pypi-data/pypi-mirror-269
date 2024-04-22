from .packages import *
# saving and loading the models
from joblib import load as loadModel
from joblib import dump as saveModel
# models
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
# metrics
from sklearn.metrics import classification_report as classificationReport
from sklearn.metrics import accuracy_score as accuracyScore
# train_test_split
from .datasets import TabularDataLoader
from .datasets import trainTestSplit
from .datasets import Pipeline
# handle errors and warnings
import warnings

class Trainer:
    def __init__(self, data_loader=None, model=None):
        self.model = model
        self.data_loader = data_loader
    
    def train(self):
        if self.data_loader is None:
            print('No data_loader was provided')
            return

        self.X_train, self.X_test, self.y_train, self.y_test = trainTestSplit(
        self.data_loader.data.drop(self.data_loader.outcome, axis=1), 
        self.data_loader.data[self.data_loader.outcome],
        test_size=0.2, random_state=42
        )

        self.preprocessor = self.data_loader.createPreprocessor()

        pipeline = Pipeline(steps=[('preprocessor', self.preprocessor), ('model', self.model)])
        pipeline.fit(self.X_train, self.y_train)
        self.model = pipeline
        return self.model

    def evaluate(self):
        if self.data_loader is None:
            print('No data_loader was provided')
            return
            
        accuracy = self.model.score(self.X_test, self.y_test)
        return accuracy

    def predict(self, X):
        if self.model is None:
            print("No model specified for prediction.")
            return

        if X is None:
            print("No data available for prediction.")
            return

        # transformed_X = self.preprocessor.transform(X)
        predictions = self.model.predict(X)
        return predictions

    def report(self):
        if self.data_loader is None:
            print('No data_loader was provided')
            return
            
        y_true = self.y_test
        y_pred = self.model.predict(self.X_test)
        report = classificationReport(
            y_true, y_pred, 
            zero_division=1, output_dict=True
            )
        # convert report to data frame
        report = pd.DataFrame(report).transpose()
        return report

    def save(self, path:str='model.di'):
        if self.model is None:
            print('No model was provided')
            return

        saveModel(self.model, path)
