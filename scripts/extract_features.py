import re


# script to generate feature set to match that of spambase.data to predict inputs based on model trained on that dataset
def gen_feature_set(text) -> list:
    wf_dict = {"make": 0, "address": 0, "all": 0, "3d": 0, "our": 0, "over": 0, "remove": 0, "internet": 0, "order": 0, "mail": 0, "receive": 0, "will": 0, "people": 0, "report": 0, "addresses": 0, "free": 0, "business": 0, "email": 0, "you": 0, "credit": 0, "your": 0, "font": 0, "000": 0,
               "money": 0, "hp": 0, "hpl": 0, "george": 0, "650": 0, "lab": 0, "labs": 0, "telnet": 0, "857": 0, "data": 0, "415": 0, "85": 0, "technology": 0, "1999": 0, "parts": 0, "pm": 0, "direct": 0, "cs": 0, "meeting": 0, "original": 0, "project": 0, "re": 0, "edu": 0, "table": 0, "conference": 0}
    cf_dict = {";": 0, "\(": 0, "\[": 0,
               "!": 0, "$": 0, "#": 0}
    crl_average = crl_longest = crl_total = 0
    word_count = len(text.split(' '))
    char_count = len(re.sub(r'[ \n]', '', text))

    for word in wf_dict.keys():
        occurances = len(re.findall(fr'\b{word}\W*\b', text))
        wf_dict[word] = 100 * occurances / word_count

    for char in cf_dict.keys():
        occurances = len(re.findall(char, text))
        cf_dict[char] = 100 * occurances / char_count

    capitalized_words = re.findall(r'[A-Z]+', text)
    if (len(capitalized_words) > 0):
        crl_total = sum(len(word) for word in capitalized_words)
        crl_average = crl_total / \
            len(capitalized_words) if len(capitalized_words) > 0 else 0
        crl_longest = max([len(word) for word in capitalized_words])

    return [val for val in wf_dict.values()] + [val for val in cf_dict.values()] + [crl_average, crl_longest, crl_total]
