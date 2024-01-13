import joblib
from fix_contents import separate_email, remove_css
from extract_features import gen_feature_set
from nltk.stem import WordNetLemmatizer


def classify_email(email) -> int:
    svm_model_p = joblib.load('../../trained_models/SVM_PhishTrain.joblib')
    svm_model_sb = joblib.load('../../trained_models/SVM_SpamBase.joblib')
    svm_model_s = joblib.load('../../trained_models/SVM_Spam.joblib')
    naiveBayes_model_p = joblib.load(
        '../../trained_models/NB_PhishTrain.joblib')
    naiveBayes_model_sb = joblib.load(
        '../../trained_models/NB_SpamBase.joblib')
    naiveBayes_model_s = joblib.load('../../trained_models/NB_Spam.joblib')
    logReg_model_p = joblib.load(
        '../../trained_models/logReg_PhishTrain.joblib')
    logReg_model_sb = joblib.load(
        '../../trained_models/logReg_SpamBase.joblib')
    logReg_model_s = joblib.load('../../trained_models/logReg_Spam.joblib')
    vectorizer = joblib.load('../../trained_models/vectorizer.joblib')

    spamBase_models = [svm_model_sb, naiveBayes_model_sb, logReg_model_sb]
    nonSpamBase_models = [svm_model_p, svm_model_s, naiveBayes_model_p,
                          naiveBayes_model_s, logReg_model_p, logReg_model_s]

    pred_input1 = gen_feature_set(email).reshape(1, -1)
    email = remove_css(separate_email(email)[0])
    lemmatizer = WordNetLemmatizer()
    email = (" ").join([lemmatizer.lemmatize(
        word.lower(), pos='v') for word in email.split(" ")])
    pred_input2 = vectorizer.transform([email])

    prediction = 0
    for model in spamBase_models:
        prediction += model.predict(pred_input1)[0]

    for model in nonSpamBase_models:
        prediction += model.predict(pred_input2)[0]

    return 1 if prediction > 4 else 0
