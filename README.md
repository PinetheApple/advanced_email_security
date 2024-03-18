# Advanced Email Security Project

## About

The project aims to develop a tool that can identify whether an email is malicious or not.
It is divided into three main components:

-   ML models for classifying the primary contents of the email
-   URL trust component to check links present in the email
-   Antivirus software to scan attachments - using ClamAV locally

The ML models are trained on three different datasets that contain spam/phishing emails/messages using Logistic Regression, Naive Bayes and SVM.
The url trust component uses a dataset of known malicious links to analyze links.

## Info for usage

Downloads datasets from the links provided in [sources.txt](./sources.txt) file. Save datasets to a separate folders under the parent 'datasets' folder. The datasets should be folders with the same names as in [sources.txt](./sources.txt) (or change the code to reflect the correct path).

Fix urls in spam.csv by removing extra spaces in them.
Search for the urls using the regex - `http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+`

For SVM Training - the value of C was selected by testing out different values to find the one that had the highest accuracy
