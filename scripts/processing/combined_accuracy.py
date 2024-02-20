'''script to find accuracy of voting based prediction combining all three models trained on the phishing dataset'''
import joblib
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import numpy as np
import pandas as pd
from fix_contents import separate_email, remove_css

def predict_input(x):
    prediction = 0
    for model in models:
        prediction += model.predict(x)
    return 1 if prediction > 1 else 0

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
svm_model = joblib.load('../../trained_models/SVM_PhishTrain.joblib')
naiveBayes_model = joblib.load('../../trained_models/NB_PhishTrain.joblib')
logReg_model = joblib.load('../../trained_models/logReg_PhishTrain.joblib')
models = [svm_model, naiveBayes_model, logReg_model]

no_pre = {'accuracy':[], 'precision':[], 'recall':[], 'roc_auc':[]}  # stores performance metrics for model without preprocessing dataset
preproc = {'accuracy':[], 'precision':[], 'recall':[], 'roc_auc':[]}  # stores metrics for model after preprocessing dataset

for i in range(5):
    dataset = df.values
    np.random.shuffle(dataset)

    X = dataset[:, 0]
    Y = dataset[:, 1]
    Y = Y.astype('int32')
    X_transformed = vectorizer.transform(X)
    X_test = X_transformed[0:6000, :] # finding accuracy based on 6000 samples from the dataset
    Y_test = Y[0:6000]

    Y_predicted = np.array([ predict_input(x) for x in X_test ])
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
    X_test = X_transformed[0:6000, :] # finding accuracy based on 6000 random samples from the dataset
    Y_test = Y[0:6000]

    Y_predicted = np.array([ predict_input(x) for x in X_test ])
    add_metrics(Y_test, Y_predicted, True)

    breakpoint()

print('No Preprocessing')
for metric in no_pre:
    print(metric, no_pre[metric])
print('With Preprocessing')
for metric in preproc:
    print(metric, preproc[metric])