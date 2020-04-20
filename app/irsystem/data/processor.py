import os
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
import re
import numpy as np
import math
import nltk

"""
This file processes and cleans the text inside the articles.
Additionally, all data structures (i.e. inverted index) useful for query search
are created here and saved as json files.


"""
data_file_name = "total_data_url.json"

def load_json_file(name):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, name)
    with open(file_path, encoding = 'utf-8') as json_file:
        data = json.load(json_file)
    return data

def save_json_file(name, input_data):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, name)
    with open(file_path, 'w') as f:
        f.write(json.dumps(input_data, ensure_ascii=False,indent=2))


def tokenize(text, stem_words = True):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Arguments
    =========
    text: String
    stem_words: boolean
    
    Returns
    =======
    List
    
    """
    stop_words = stopwords.words('english')
    stemmer = PorterStemmer()
    regex = r"([a-zA-Z]+)"
    tokens = re.findall(regex, text.lower())
    if (stem_words):
        return [stemmer.stem(t) for t in tokens if not t in stop_words]
    else:
        return [t for t in tokens if not t in stop_words]

def tokenize_articles(input_data, feature_name, tokenize_method):
    """ adds tokenized transcript (or title) as a feature of each document in dataset
    
    Arguments
    =========
    news_data: list of dictionaries
    
    feature_name: String
    
    tokenize_method: function
    
    Returns 
    =======
    data set with tokenized text for specified feature
    
    """
    for article in input_data:
        new_feature_name = feature_name + '_toks'
        article[new_feature_name] = tokenize_method(article[feature_name])
    return input_data

def create_doc_term_matrix(input_data, feature_name):
    """creates the doc_term matrix
    
    Arguments
    =========
    news_data: list of dictionaries
    
    feature_name: String
    
    Returns
    =======
    list of dictionaries where keys are the types in a document
    corresponding to the index of the list
    
    """
    matrix = []
    for article in input_data:
        tokens = article[feature_name]
        info = {}
        for t in set(tokens):
            info[t] = tokens.count(t)
        info = {k: v for k, v in sorted(info.items(), key=lambda item: item[1], reverse = True)}
        matrix.append(info)
    return matrix

def create_inverted_index(input_doc_term_matrix):
    """creates the inverted index
    
    Arguments
    =========
    input_doc_term_matrix: list of dictionaries
    
    Returns
    =======
    {String : list of tuples}
    
    """
    idx = {}
    doc_id = 0
    for doc in input_doc_term_matrix:
        for key, val in doc.items():
            if idx.get(key) is None:
                idx[key] = []
            idx.get(key).append((doc_id, val))
        doc_id+=1
    return idx

def create_idf(input_inverted_index):
    """computes the inverse document frequency of each type in dataset
    
    Arguments
    =========
    input_inverted_index: {String : list of tuples}
    
    Returns
    =======
    Dictionary {String : Float}
    
    """
    idf = {}
    for key,val in input_inverted_index.items():
        idf[key] = 1/math.log(1+len(val))
        #idf[key] = 1/(1+len(val))
    return idf

def create_tfidf_matrix(input_doc_term_matrix, input_idf):
    """creates tf-idf matrix
    
    Arguments
    =========
    input_doc_term_matrix: list of dictionaries
    
    input_idf: {String: Float}
    
    Returns
    =======
    list of dictionaries
    
    """
    matrix = []
    for doc in input_doc_term_matrix:
        info = {}
        for key,tf in doc.items():
            idf = 0
            if (input_idf.get(key) is not None):
                idf = input_idf.get(key)
            info[key] = tf*idf
        info = {k: v for k, v in sorted(info.items(), key=lambda item: item[1], reverse = True)}
        matrix.append(info)
    return matrix

def remove_non_frequent_types(input_inverted_index, min_df):
    """Removes terms from inverted index 
    that appear in less than min_df documents
    
    Arguments
    =========
    input_inverted_index: {String : list of tuples}
    
    min_df: Int
    
    Returns
    =======
    {String : List of Tuples}
    
    """
    total_types = len(input_inverted_index)
    idx_copy = input_inverted_index.copy()
    count = 0
    for key,val in idx_copy.items():
        if (len(val) < min_df):
            del input_inverted_index[key]
            count+=1
    print("Percent of Types Removed: ", count/(total_types*1.0))
    print("Number of Types Remaining: ", total_types - count)
    return input_inverted_index

def compute_doc_norms(input_tfidf_matrix):
    """ computes l2 norm of each document
    
    Arguments
    ========
    input_tfidf_matrix: List of Dictionaries
    
    Returns
    =======
    numpy.array
    
    """
    norms = []
    doc_id = 0
    for doc in input_tfidf_matrix:
        accum = 0
        for val in doc.values():
            accum += math.pow(val, 2)
        norms.append(math.sqrt(accum))
        doc_id += 1
    return norms


def run(feature, input_data):
    # Create doc term matrix
    doc_term_matrix = create_doc_term_matrix(input_data, feature + '_toks')
    # Create inverted index
    inverted_index = create_inverted_index(doc_term_matrix)
    inverted_index = remove_non_frequent_types(inverted_index, 2)
    # Compute idf values
    idf_values = create_idf(inverted_index)
    # Create tfidf matrix
    tfidf_matrix = create_tfidf_matrix(doc_term_matrix, idf_values)
    # Compute doc norms
    norms = compute_doc_norms(tfidf_matrix)
    # Save data structures
    save_json_file(feature + '_inverted_index.json', inverted_index)
    save_json_file(feature + '_tfidf_matrix.json', tfidf_matrix)
    save_json_file(feature + '_norms.json', norms)




def main():
    # Load in data
    data = load_json_file(data_file_name)
    # Quick description of dataset
    num_articles = len(data)
    print(str(num_articles) + ' articles loaded')
    print('Each article has the following features:')
    print(data[477].keys())
    # Tokenize transcripts and titles
    data = tokenize_articles(data, 'transcript', tokenize)
    data = tokenize_articles(data, 'title', tokenize)
    # Create and save relevant data structures
    run('transcript', data)
    print('Successfully Created and Saved Files')



    

if __name__ == "__main__":
    main()
