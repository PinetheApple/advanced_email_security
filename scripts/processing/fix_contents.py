import re


# function that returns the contents of the email separated from included links and addresses
def separate_email(text) -> list:
    text = re.sub(r'(\n)|(\s{2,})', ' ', text)
    email_regex = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
    email_addresses = re.findall(email_regex, text)
    text = re.sub(email_regex, " EMAIL_ADDRESS_HERE", text)
    link_regex1 = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    link_regex2 = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    invalid_regex = r"([A-z0-9]+\.{1,}[A-z0-9]+)|([A-z0-9]+\.{2,}[A-z0-9]+\.+[A-z0-9]+)"
    links = re.findall(link_regex1, text)
    text = re.sub(link_regex1, " URL_HERE", text)
    links2 = re.findall(link_regex2, text)
    links2 = [link for link in links2 if re.fullmatch(
        invalid_regex, link) == None]
    links = links + links2
    for link in links2:
        text = text.replace(link, " URL_HERE")
    return text, links, email_addresses


# function that removes css from the contents of the email for better training
def remove_css(text) -> str:
    css_regex = r'(\.|#)?[A-z]+(-[A-z]+)?\s?\{(\s?[A-z]+(-[A-z]+)?\s?:\s?#?\s?[0-9A-z]+(-[A-z]+)?\s?;?)+.*\}'
    text = re.sub(css_regex, "CSS_HERE", text)
    return text
