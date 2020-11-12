import requests
import bs4 as bs
import re

def get_text(url):
    try:
        response = requests.get(url);
    except:
        print("Couldn't get:", url)
        return ''
    if response.status_code != 200:
        return ''
    text = bs.BeautifulSoup(response.content, 'html.parser').text
    return text

def tokenize(text):
    text = text.strip('\n\r')
    tokens = re.split('\W+', text)
    token_list = []
    for i in tokens:
        if not i or len(i) > 20:
            continue
        token_list.append(i.lower())
    # tokens = []
    # for line in lines:
        # toks = line.split(' ')
        # for t in toks:
            # if not t:
                # continue
            # tokens.append(t)
    return token_list

def get_tokens(url):
    text = get_text(url)
    tokens = tokenize(text)
    return tokens

if __name__ == '__main__':
    links = open('./Links.txt', 'r').read().splitlines()
    print(get_tokens(links[0]))
