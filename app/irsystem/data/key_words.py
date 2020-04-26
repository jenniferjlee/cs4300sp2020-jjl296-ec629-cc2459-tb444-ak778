import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
import re
import os
import json

data_file_name = "final_data1.json"

def save_json_file(name, input_data):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, name)
    with open(file_path, 'w') as f:
        f.write(json.dumps(input_data, ensure_ascii=False,indent=2))

def tokenize(text, stem_words = True):
    """Returns a tuple containing 
        a list of words that make up the text
        and the number of total words (not including stop words).
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Arguments
    =========
    text: String
    stem_words: boolean
    
    Returns
    =======
    Tuple of a list and number 
    
    """
    stop_words = stopwords.words('english')
    stemmer = PorterStemmer()
    regex = r"([a-zA-Z]+)"
    tokens = re.findall(regex, text.lower())
    
    numwords = 0
    words = []
    for t in tokens:
        if not t in stop_words:
            numwords += 1
            if (stem_words):
                words.append(stemmer.stem(t))
            else:
                words.append(t)
    return (words, numwords)

def make_countsdict(tokens):
    worddict = {}
    for word in tokens:
        if word in worddict:
            worddict[word] += 1
        else:
            worddict[word] = 1
    return worddict

def make_keywords(row, title_scale = 0.3):
    tokenized = tokenize(row["transcript"])
    words = tokenized[0]
    numwords = tokenized[1]
    worddict = make_countsdict(words)
    # divide by numwords
    counts = [(word,count) for word,count in worddict.items()]
    freq = [(word, count/numwords) for word, count in counts]

    # tokenize title
    tokenized_title = tokenize(row["title"])
    titledict = make_countsdict(tokenized_title[0])
    title_freq = [(word, count/tokenized_title[1]) for word, count in titledict.items()]

    # combine
    title_scaled = [(word, count*title_scale) for word, count in title_freq]

    # get top 20
    total = freq + title_scaled
    sortedtotal = sorted(total, key=lambda x: x[1], reverse=True) 
    top_20 = {}
    top = 0
    for word,freq in sortedtotal:
        if word not in top_20:
            top_20[word] = freq
            top += 1
            if top == 20: 
                break
    row["keywords"] = top_20

def create_inverted_index(input_data):
    """creates the inverted index
    
    Arguments
    =========
    input_data: dataframe with keywords column (dictionary word: frequency)
    
    Returns
    =======
    {String : list of tuples}
    
    """
    idx = {}
    doc_id = 0
    for index, row in input_data.iterrows():
        for word, freq in row["keywords"].items():
            if idx.get(word) is None:
                idx[word] = []
            idx.get(word).append((index,freq))
    return idx

def run(input_data):
    """
    Constructs data structures for search
    """
    inverted_index = create_inverted_index(input_data)
    save_json_file('inverted_index_keywords.json', inverted_index)

def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, data_file_name)
    df = pd.read_json (file_path, convert_dates=False)
    df["keywords"] = ""
    for index, row in df.iterrows():
        make_keywords(row)
    df.to_json('total_data_keywords.json', orient='records')
    with open('total_data_keywords.json', 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False, orient='records')
    print('Successfully Created and Saved Files')
    
    keywords = pd.read_json ('total_data_keywords.json', convert_dates=False)
    run(keywords)
    print("Successfully made inverted index")



if __name__ == "__main__":
    main()