from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.data.processor import load_json_file
import os
from app.irsystem.data.processor import tokenize
from app.irsystem.models.search import *

project_name = "CUSmiles"
net_id = "Jennifer Lee: jjl296, Camilo Cedeno-Tobon: cc2459, Tanmay Bansal: tb444, Alina Kim: ak778, Ein Chang: ec629"

# Camilo's changes
documents = load_json_file('final_data4.json')
transcript_idf_values = load_json_file('transcript_idf_values.json')
transcript_inverted_index = load_json_file('transcript_inverted_index.json')
transcript_norms = load_json_file('transcript_norms.json')
title_idf_values = load_json_file('title_idf_values.json')
title_inverted_index = load_json_file('title_inverted_index.json')
title_norms = load_json_file('title_norms.json')

# Ein's changes
"""documents = load_json_file('final_data2.json')
inverted_index = load_json_file('transcript_inverted_index1.json')
tfidf_matrix = load_json_file('transcript_tfidf_matrix1.json')
norms = load_json_file('transcript_norms1.json')"""

classifiedDocs = load_json_file('final_data_classified.json')

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
        combined_results = get_combined_results(transcript_results, title_results, 0.4, 0.6)
        top_results = get_top_k(combined_results, 25, documents)
        output_message = "Your search: " + query
        data = top_results

        #update data to have similar {title, links}

        #Change to sort by: relevancy and popularity once this works

        # sorting top results
        # FUTURE TODO: use top results + most recent etc
        isRecent = request.args.get('r_sort')
        isPopular = request.args.get('p_sort')


        if (isRecent=="new"):
            data = sort_by_recency(transcript_results, 25, documents, True)

        if (isRecent=="old"):
            data = sort_by_recency(transcript_results, 25, documents, False)


        if (len(data)==0):
            # change url to final link!
            data = [{'title':'No Results Found', 'url':'https://cusmiles-v2.herokuapp.com/'}]

    if (random == "Give me Anything!"):
        output_message, data = random_helper()
    if topic is not None:
        output_message, data = topic_helper(topic)
    if similar is not None:
        output_message = "Articles similar to "
        data = similarDocs[similar]
    if query is None:
        query = ""
    
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, topics=topics, query=query)


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

            
    
