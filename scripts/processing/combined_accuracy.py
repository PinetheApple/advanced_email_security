'''script to find accuracy of voting based prediction combining all three models trained on the phishing dataset'''
import joblib
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import numpy as np
import pandas as pd
from fix_contents import separate_email, remove_css

def predict_input(x, models):
    prediction = 0
    for model in models:
        prediction += model.predict(x)
    return 1 if prediction > 1 else 0

def add_metrics(Y_true, Y_predicted, stats_dict):
    accuracy = accuracy_score(Y_true, Y_predicted)
    precision = precision_score(Y_true, Y_predicted)
    recall = recall_score(Y_true, Y_predicted)
    roc_auc = roc_auc_score(Y_true, Y_predicted)

    stats_dict['accuracy'].append(f'{accuracy:.2f}')
    stats_dict['precision'].append(f'{precision:.2f}')
    stats_dict['recall'].append(f'{recall:.2f}')
    stats_dict['roc_auc'].append(f'{roc_auc:.2f}')

def main():
    df = pd.read_csv('./datasets/phishing_emails_kaggle/Phishing_Email.csv')
    df.drop(columns=['Unnamed: 0'], inplace=True)
    df = df.dropna()
    df.columns = ["Content", "Category"]
    df["Category"] = df.Category.map({'Safe Email': 0, 'Phishing Email': 1})

    lemmatizer = WordNetLemmatizer()
    vectorizer = joblib.load('./trained_models/vectorizer.joblib')
    svm_model = joblib.load('./trained_models/SVM_PhishTrain.joblib')
    naiveBayes_model = joblib.load('./trained_models/NB_PhishTrain.joblib')
    logReg_model = joblib.load('./trained_models/logReg_PhishTrain.joblib')
    models = [svm_model, naiveBayes_model, logReg_model]

    stats_without_preprocessing = {'accuracy':[], 'precision':[], 'recall':[], 'roc_auc':[]}
    stats_with_preprocessing = {'accuracy':[], 'precision':[], 'recall':[], 'roc_auc':[]}

    for i in range(5):
        dataset = df.values
        np.random.shuffle(dataset)

        X = dataset[:, 0]
        Y = dataset[:, 1]
        Y = Y.astype('int32')
        X_transformed = vectorizer.transform(X)
        X_test = X_transformed[0:6000, :] # finding accuracy based on 6000 samples from the dataset
        Y_test = Y[0:6000]

        Y_predicted = np.array([ predict_input(x, models) for x in X_test ])
        add_metrics(Y_test, Y_predicted, stats_without_preprocessing)

        X = dataset[:, 0]
        Y = dataset[:, 1]
        Y = Y.astype('int32')
        for j in range(X.shape[0]):
            content = separate_email(X[j])[0]
            content = remove_css(content)
            X[j] = (" ").join([lemmatizer.lemmatize(word.lower(), pos='v')
                            for word in content.split(" ")])
        X_transformed = vectorizer.transform(X)
        X_test = X_transformed[0:6000, :]
        Y_test = Y[0:6000]

        Y_predicted = np.array([ predict_input(x, models) for x in X_test ])
        add_metrics(Y_test, Y_predicted, stats_with_preprocessing)

    print('No Preprocessing')
    for metric in stats_without_preprocessing:
        print(metric, stats_without_preprocessing[metric])
    print('With Preprocessing')
    for metric in stats_with_preprocessing:
        print(metric, stats_with_preprocessing[metric])

if __name__ == "__main__":
    main()