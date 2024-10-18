import dagshub
import mlflow
import argparse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, precision_score, recall_score, \
    f1_score
from sklearn.model_selection import train_test_split
import joblib

DAGSHUB_REPO_OWNER = "Brycenvn"
DAGSHUB_REPO = "MLOps-course"
# dagshub.auth.add_app_token('acb***2237')
dagshub.init(DAGSHUB_REPO, DAGSHUB_REPO_OWNER, )

# Consts
CLASS_LABEL = 'MachineLearning'
train_df_path = 'data/train.csv'
test_df_path = 'data/test.csv'

def get_or_create_experiment_id(name):
    exp = mlflow.get_experiment_by_name(name)
    if exp is None:
        exp_id = mlflow.create_experiment(name)
        return exp_id
    return exp.experiment_id


def feature_engineering(raw_df):
    df = raw_df.copy()
    df['CreationDate'] = pd.to_datetime(df['CreationDate'])
    df['CreationDate_Epoch'] = df['CreationDate'].astype('int64') // 10 ** 9
    df = df.drop(columns=['Id', 'Tags'])
    df['Title_Len'] = df.Title.str.len()
    df['Body_Len'] = df.Body.str.len()
    # Drop the correlated features
    df = df.drop(columns=['FavoriteCount'])
    df['Text'] = df['Title'].fillna('') + ' ' + df['Body'].fillna('')
    return df


def fit_tfidf(train_df, test_df):
    tfidf = TfidfVectorizer(max_features=25000)
    tfidf.fit(train_df['Text'])
    train_tfidf = tfidf.transform(train_df['Text'])
    test_tfidf = tfidf.transform(test_df['Text'])
    return train_tfidf, test_tfidf, tfidf


def fit_model(train_X, train_y, random_state=42):
    clf_tfidf = AdaBoostClassifier(random_state=random_state)    
    clf_tfidf.fit(train_X, train_y)
    return clf_tfidf


def eval_model(clf, X, y):
    y_proba = clf.predict_proba(X)[:, 1]
    y_pred = clf.predict(X)
    return {
        'roc_auc': roc_auc_score(y, y_proba),
        'average_precision': average_precision_score(y, y_proba),
        'accuracy': accuracy_score(y, y_pred),
        'precision': precision_score(y, y_pred),
        'recall': recall_score(y, y_pred),
        'f1': f1_score(y, y_pred),
    }


def split(random_state=42):
    print('Loading data...')
    df = pd.read_csv('data/CrossValidated-Questions.csv')
    df[CLASS_LABEL] = df['Tags'].str.contains('machine-learning').fillna(False)
    train_df, test_df = train_test_split(df, random_state=random_state, stratify=df[CLASS_LABEL])

    print('Saving split data...')
    train_df.to_csv(train_df_path)
    test_df.to_csv(test_df_path)


def train():
    print('Loading data...')
    train_df = pd.read_csv(train_df_path)
    test_df = pd.read_csv(test_df_path)

    print('Engineering features...')
    train_df = feature_engineering(train_df)
    test_df = feature_engineering(test_df)

    exp_id = get_or_create_experiment_id("tutorial-adaboost")

    with mlflow.start_run(experiment_id=exp_id):
        print('Fitting TFIDF...')
        train_tfidf, test_tfidf, tfidf = fit_tfidf(train_df, test_df)

        print('Saving TFIDF object...')
        joblib.dump(tfidf, 'outputs/tfidf.joblib')
        mlflow.log_params({f'tfidf__{k}': v for k, v in tfidf.get_params().items()})

        print('Training model...')
        train_y = train_df[CLASS_LABEL]
        model = fit_model(train_tfidf, train_y)

        print('Saving trained model...')
        joblib.dump(model, 'outputs/model.joblib')
        mlflow.log_param("model_class", type(model).__name__)
        mlflow.log_params({f'model__{k}': v for k, v in model.get_params().items()})

        print('Evaluating model...')
        train_metrics = eval_model(model, train_tfidf, train_y)
        print('Train metrics:')
        print(train_metrics)
        mlflow.log_metrics({f'train__{k}': v for k,v in train_metrics.items()})

        test_metrics = eval_model(model, test_tfidf, test_df[CLASS_LABEL])
        print('Test metrics:')
        print(test_metrics)
        mlflow.log_metrics({f'test__{k}': v for k,v in test_metrics.items()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Split or Train step:', dest='step')
    subparsers.required = True
    split_parser = subparsers.add_parser('split')
    split_parser.set_defaults(func=split)
    train_parser = subparsers.add_parser('train')
    train_parser.set_defaults(func=train)
    parser.parse_args().func()
