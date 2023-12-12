# program to read the spam.csv file as pandas.read_csv() doesnt work properly
import pandas as pd

def read_csv_file():
    data_file = open('../datasets/kaggle_email_spam/spam.csv',encoding = ('ISO-8859-1'))
    columns = ["Category","Content"]
    df = pd.DataFrame(columns=columns)

    i = 0
    for line in data_file:
        data_split = line.split(',',1)
        category = data_split[0].replace("\"","") # one oddity in the dataset -> ham""",
        content = data_split[1][:-4].strip("\"")
        if(content=="" or category==""):
            continue
        if i!=0:
            df.loc[i] = [category, content]
        i += 1
    
    return df