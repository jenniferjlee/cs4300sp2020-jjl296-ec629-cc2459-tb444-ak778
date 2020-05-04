from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.data.processor import load_json_file
import os
from app.irsystem.data.processor import tokenize
from app.irsystem.models.search import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()

project_name = "CUSmiles"
net_id = "Jennifer Lee: jjl296, Camilo Cedeno-Tobon: cc2459, Tanmay Bansal: tb444, Alina Kim: ak778, Ein Chang: ec629"

documents = load_json_file('final_data5.json')
transcript_idf_values = load_json_file('transcript_idf_values.json')
transcript_inverted_index = load_json_file('transcript_inverted_index.json')
transcript_norms = load_json_file('transcript_norms.json')
title_idf_values = load_json_file('title_idf_values.json')
title_inverted_index = load_json_file('title_inverted_index.json')
title_norms = load_json_file('title_norms.json')

# Keyword Search
inverted_index_keyword = load_json_file('inverted_index_keywords.json')

classifiedDocs = load_json_file('final_data_classified.json')

# Popular Topics
topicDocs = load_json_file('topics.json')
similarDocs = load_json_file('similars_final.json')



@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    random = request.args.get('random')
    similar = request.args.get('similar')
    topic = request.args.get('topic')

    
    output_message = ''
    data = []
    topics = []
    stems = []
    stemming_words = []
    if (not query):
        output_message = "Let's C U Smile!"
        topic0 = []
        topic1 = []
        topic2 = []
        for doc in classifiedDocs:
            topic_num = doc.get('topic')
            if topic_num == 1:
                topic1.append((doc.get('topic_strength'), doc))
            elif topic_num == 0:
                topic0.append((doc.get('topic_strength'), doc))
            else:
                topic2.append((doc.get('topic_strength'), doc))
        topic0.sort(key=lambda x:x[0])
        topic0.reverse()
        topic1.sort(key=lambda x:x[0])
        topic1.reverse()
        topic2.sort(key=lambda x:x[0])
        topic2.reverse()
        topics = [[],[],[]]
        for i in range(10):
            topics[0].append(topic0[i][1])
            topics[1].append(topic1[i][1])
            topics[2].append(topic2[i][1])
                
    else:
        transcript_results = search_tfdf_method(query, transcript_inverted_index, transcript_norms, transcript_idf_values, tokenize)
        title_results = search_tfdf_method(query, title_inverted_index, title_norms, title_idf_values, tokenize)
        combined_results1 = get_combined_results(transcript_results, title_results, 0.4, 0.6)

        keyword_results = search_keyword_method(query, len(transcript_norms), inverted_index_keyword, tokenize)
        combined_results2 = get_combined_results(combined_results1, keyword_results, 10, 1.5)
        # top_results = get_top_k(keyword_results, 25, documents)

        top_results = get_top_k(combined_results2, 25, documents)
        output_message = "Results for " + query
        data = top_results


        isRecent = request.args.get('r_sort')
        isPopular = request.args.get('p_sort')


        if (isRecent=="new"):
            data = sort_by_recency(combined_results, 25, documents, True)

        if (isRecent=="old"):
            data = sort_by_recency(combined_results, 25, documents, False)


        if (len(data)==0):
            # change url to final link!
            data = [{'title':'No Results Found', 'url':'https://cusmiles-v2.herokuapp.com/'}]
        else:
            stems = ps.stem(query)
            for d in data:
                for word in d['title'].split():
                    if ps.stem(word) in stems and len(word) >1:
                        stemming_words.append(word)
                for word in d['summary'].split():
                    if ps.stem(word) in stems and len(word) >1:
                        stemming_words.append(word)

    if (random == "Give me Anything!"):
        output_message, data = random_helper()
    if topic is not None:
        output_message, data = topic_helper(topic)
    if similar is not None:
        output_message = similar
        data = similarDocs[similar]
    if query is None:
        query = ""
    
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, topics=topics, query=query, stemming_words=stemming_words)


def random_helper():
    output_message = "Let's C U Smile!"
    data = get_random(documents)
    return output_message, data

def topic_helper(topic):
    output_message = "Uplifting News on " + topic
    # if topic == "Money":
    #     greendocs = []
    #     for doc in classifiedDocs:
    #         topic_num = doc.get('topic')
    #         if topic_num == 0:
    #             greendocs.append((doc.get('topic_strength'), doc))
    #     greendocs.sort(key=lambda x:x[0])
    #     greendocs.reverse()
    # data = []
    # for i in range(10):
    #     data.append(greendocs[i][1])
    data = []
    for doc in topicDocs:
        category = doc.get('topic')
        if topic == category:
            data.append(doc)
    return output_message,data 

            
    
