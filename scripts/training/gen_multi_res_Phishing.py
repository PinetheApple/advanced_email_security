'''script to generate accuracy results multiple times, shuffling the dataset for each iteration'''
import joblib
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import sys
sys.path.append('../')
from processing.fix_contents import separate_email, remove_css

no_pre = {'accuracy':[], 'precision':[], 'recall':[], 'roc_auc':[]}  # stores performance metrics for model without preprocessing dataset
preproc = {'accuracy':[], 'precision':[], 'recall':[], 'roc_auc':[]}  # stores metrics for model after preprocessing dataset

def add_metrics(Y_true, Y_predicted, pre=False):
    accuracy = str(accuracy_score(Y_true, Y_predicted))
    precision = str(precision_score(Y_true, Y_predicted))
    recall = str(recall_score(Y_true, Y_predicted))
    roc_auc = str(roc_auc_score(Y_true, Y_predicted))

    if(pre):
        preproc['accuracy'].append(accuracy[2:4]+'.'+accuracy[4:7])
        preproc['precision'].append(precision[2:4]+'.'+precision[4:7])
        preproc['recall'].append(recall[2:4]+'.'+recall[4:7])
        preproc['roc_auc'].append(roc_auc[2:4]+'.'+roc_auc[4:7])
    else:
        no_pre['accuracy'].append(accuracy[2:4]+'.'+accuracy[4:7])
        no_pre['precision'].append(precision[2:4]+'.'+precision[4:7])
        no_pre['recall'].append(recall[2:4]+'.'+recall[4:7])
        no_pre['roc_auc'].append(roc_auc[2:4]+'.'+roc_auc[4:7])

df = pd.read_csv('../../datasets/phishing_emails_kaggle/Phishing_Email.csv')
df.drop(columns=['Unnamed: 0'], inplace=True)
df = df.dropna()
df.columns = ["Content", "Category"]
df["Category"] = df.Category.map({'Safe Email': 0, 'Phishing Email': 1})

lemmatizer = WordNetLemmatizer()
vectorizer = joblib.load('../../trained_models/vectorizer.joblib')

for i in range(5):
    dataset = df.values
    np.random.shuffle(dataset)

    X = dataset[:, 0]
    Y = dataset[:, 1]
    Y = Y.astype('int32')
    X_transformed = vectorizer.transform(X)
    X_train = X_transformed[0:13000, :]
    Y_train = Y[0:13000]
    X_test = X_transformed[13000:, :]
    Y_test = Y[13000:]

    model = LogisticRegression(max_iter=900)
    model.fit(X_train, Y_train)
    Y_predicted = model.predict(X_test)
    add_metrics(Y_test, Y_predicted)

    X = dataset[:, 0]
    Y = dataset[:, 1]
    Y = Y.astype('int32')
    for j in range(X.shape[0]):
        content = separate_email(X[j])[0]
        content = remove_css(content)
        X[j] = (" ").join([lemmatizer.lemmatize(word.lower(), pos='v')
                           for word in content.split(" ")])
    X_transformed = vectorizer.transform(X)
    X_train = X_transformed[0:13000, :]
    Y_train = Y[0:13000]
    X_test = X_transformed[13000:, :]
    Y_test = Y[13000:]

    model = LogisticRegression(max_iter=900)

    model.fit(X_train, Y_train)
    Y_predicted = model.predict(X_test)
    add_metrics(Y_test, Y_predicted, True)

    print(i, ' completed')

print('No Preprocessing')
for metric in no_pre:
    print(metric, no_pre[metric])
print('With Preprocessing')
for metric in preproc:
    print(metric, preproc[metric])
