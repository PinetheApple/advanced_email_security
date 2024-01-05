# Advanced Email Security Project

Downloads datasets from the links provided in [sources.txt](./sources.txt) file. Save datasets to a separate folders under the parent 'datasets' folder. The datasets should be folders with the same names as in [sources.txt](./sources.txt) (or change the code to reflect the correct path).
Extract the [websites_list.csv.gz](./websites_list.csv.gz) file and place the extracted csv file in 'datasets>websites' folder.

fix urls in spam.csv by removing extra spaces in them (search for the urls using the regex - 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

For SVM Training - value of C was selected by testing out three C values to find one with highest accuracy (three out of 100, 500, 1000, 1250, 2000 based on size of dataset) (the three values had very similar accuracy scores)
