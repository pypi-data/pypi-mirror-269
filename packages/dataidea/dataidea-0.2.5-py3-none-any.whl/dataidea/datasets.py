from .packages import *
from sklearn.model_selection import train_test_split as trainTestSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler


def loadDataset(name:str=None, inbuilt=True, file_type:str=None):
    '''
    Easily load datasets that are inbuit in DATAIDEA

    parameters:
    name: this is the name of the dataset, eg demo, fpl, music, titanic etc
    inbuilt: boolean to specify whether data is from DATAIDEA or custom data
    type: specifies the type of the dataset eg 'csv', 'excel' etc

    '''

    if inbuilt:
        package_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(package_dir, 'datasets', f'{name}.csv')
        return pd.read_csv(data_path)

    if file_type == None:
        raise TypeError('The file type was not specified')
    
    if file_type == 'csv':
        return pd.read_csv(name)
    
    if file_type == 'excel':
        return pd.read_excel(name)


def subsetData(data, columns=[]):
    subsetted_data = data[columns].copy()
    return subsetted_data

def createPreprocessor(numeric_features, categorical_features):
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    return preprocessor

def transformData(data, outcome, preprocessor):
    X_train, X_test, y_train, y_test = trainTestSplit(
        data.drop(outcome, axis=1), data[outcome],
        test_size=0.2, random_state=42
    )

    transformer = preprocessor.fit(X_train)
    transformed_X_train = transformer.transform(X_train)
    transformed_X_test = transformer.transform(X_test)

    if isinstance(transformed_X_train, sp.sparse.csr_matrix):
        transformed_X_train_dataframe = pd.DataFrame.sparse.from_spmatrix(transformed_X_train, columns=transformer.get_feature_names_out())
        transformed_X_test_dataframe = pd.DataFrame.sparse.from_spmatrix(transformed_X_test, columns=transformer.get_feature_names_out())
    else:
        transformed_X_train_dataframe = pd.DataFrame(data=transformed_X_train, columns=transformer.get_feature_names_out())
        transformed_X_test_dataframe = pd.DataFrame(data=transformed_X_test, columns=transformer.get_feature_names_out())

    return ((transformed_X_train_dataframe, transformed_X_test_dataframe, y_train, y_test), transformer)

def transformTable(table, preprocessor):
    transformer = preprocessor.fit(table)
    transformed_table = transformer.transform(table)
    return transformed_table, transformer


class TabularDataLoader:
    def __init__(
        self, data: pd.DataFrame = None, numeric_features: list = [],
        categorical_features: list = [], outcome: str = None
    ):
        self.data = data
        self.numeric_features = numeric_features
        self.categorical_features = categorical_features
        self.outcome = outcome

    def createPreprocessor(self):
        return createPreprocessor(self.numeric_features, self.categorical_features)

    def transform(self):
        transformer = self.createPreprocessor()
        return transformData(self.data, self.outcome, transformer)

    def transformTable(self):
        transformed_data = transformTable
        return transformed_data