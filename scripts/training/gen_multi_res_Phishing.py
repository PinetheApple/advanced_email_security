'''script to generate accuracy results multiple times, shuffling the dataset for each iteration'''
import joblib
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import sys
sys.path.append('../')
from processing.fix_contents import separate_email, remove_css

df = pd.read_csv('../../datasets/phishing_emails_kaggle/Phishing_Email.csv')
df.drop(columns=['Unnamed: 0'], inplace=True)
df = df.dropna()
df.columns = ["Content", "Category"]
df["Category"] = df.Category.map({'Safe Email': 0, 'Phishing Email': 1})

lemmatizer = WordNetLemmatizer()
vectorizer = joblib.load('../../trained_models/vectorizer.joblib')
no_pre = []  # stores accuracy for model without preprocessing dataset
preproc = []  # stores accuracy for model after preprocessing dataset
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
    score = str(accuracy_score(Y_test, Y_predicted))
    no_pre.append(float(score[2:4]+'.'+score[4:7]))

    X = dataset[:, 0]
    Y = dataset[:, 1]
    Y = Y.astype('int32')
    for i in range(X.shape[0]):
        content = separate_email(X[i])[0]
        content = remove_css(content)
        X[i] = (" ").join([lemmatizer.lemmatize(word.lower(), pos='v')
                           for word in content.split(" ")])
    X_transformed = vectorizer.transform(X)
    X_train = X_transformed[0:13000, :]
    Y_train = Y[0:13000]
    X_test = X_transformed[13000:, :]
    Y_test = Y[13000:]

    model = LogisticRegression(max_iter=900)

    model.fit(X_train, Y_train)
    Y_predicted = model.predict(X_test)
    score = str(accuracy_score(Y_test, Y_predicted))
    preproc.append(float(score[2:4]+'.'+score[4:7]))

print(no_pre)
print(preproc)
