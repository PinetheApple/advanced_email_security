import joblib
from fix_contents import separate_email, remove_css
from nltk.stem import WordNetLemmatizer


def classify_email(email) -> list:
    svm_model_p = joblib.load('../../trained_models/SVM_PhishTrain.joblib')
    svm_model_s = joblib.load('../../trained_models/SVM_Spam.joblib')
    naiveBayes_model_p = joblib.load(
        '../../trained_models/NB_PhishTrain.joblib')
    naiveBayes_model_s = joblib.load('../../trained_models/NB_Spam.joblib')
    logReg_model_p = joblib.load(
        '../../trained_models/logReg_PhishTrain.joblib')
    logReg_model_s = joblib.load('../../trained_models/logReg_Spam.joblib')
    vectorizer = joblib.load('../../trained_models/vectorizer.joblib')

    spam_models = [svm_model_s, naiveBayes_model_s, logReg_model_s]
    phishing_models = [svm_model_p, naiveBayes_model_p, logReg_model_p]

    email = remove_css(separate_email(email)[0])
    lemmatizer = WordNetLemmatizer()
    email = (" ").join([lemmatizer.lemmatize(
        word.lower(), pos='v') for word in email.split(" ")])
    pred_input = vectorizer.transform([email])

    spam_prediction = 0
    phishing_prediction = 0

    for model in spam_models:
        spam_prediction += model.predict(pred_input)[0]
    spam_prediction = 1 if spam_prediction > 1 else 0

    for model in phishing_models:
        phishing_prediction += model.predict(pred_input)[0]
    phishing_prediction = 1 if phishing_prediction > 1 else 0

    return [phishing_prediction, spam_prediction]
