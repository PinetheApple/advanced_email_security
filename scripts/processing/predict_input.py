# function to process input email/text and classify based on the model provided and dataset used
def classify_email(email, model, vectorizer=None) -> int:
    if vectorizer == None:  # no vectorizer for spambase data
        from extract_features import gen_feature_set
        prediction_input = gen_feature_set(email)

    else:
        from fix_contents import separate_email, remove_css
        from nltk.stem import WordNetLemmatizer

        lemmatizer = WordNetLemmatizer()
        email = separate_email(email)[0]
        email = remove_css(email)
        email = (" ").join([lemmatizer.lemmatize(
            word.lower(), pos='v') for word in email.split(" ")])
        prediction_input = vectorizer.transform([email])

    return model.predict(prediction_input)
