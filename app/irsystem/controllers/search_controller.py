from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.data.processor import load_json_file
import os
from app.irsystem.data.processor import tokenize
from app.irsystem.models.search import *

project_name = "CUSmiles"
net_id = "Jennifer Lee: jjl296, Camilo Cedeno-Tobon: cc2459, Tanmay Bansal: tb444, Alina Kim: ak778, Ein Chang: ec629 "

# Camilo's changes
documents = load_json_file('final_data2.json')
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



@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        src = []
        url = []
        output_message = 'No results'
        # idk why spaces don't work
        place_holder = "try_keywords_like_'dog'"

        # output_message = "Let's C U Smile!"
        # data = get_random(documents)
        # return render_template('search.html', name=project_name, netid=net_id, 
        # output_message=output_message, data=data)
    else:
        transcript_results = search_tfdf_method(query, transcript_inverted_index, transcript_norms, transcript_idf_values, tokenize)
        title_results = search_tfdf_method(query, title_inverted_index, title_norms, title_idf_values, tokenize)
        combined_results = get_combined_results(transcript_results, title_results, 0.4, 0.6)
        top_results = get_top_k(combined_results, 10, documents)
        output_message = "Your search: " + query
        place_holder = query
        data = top_results
        if (len(data)==0):
            data = [{'title':'No Results Found', 'url':''}]
    print(place_holder)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, placeholder=place_holder)

@irsystem.route('/random', methods=['GET'])
def random():
    output_message = "Let's C U Smile!"
    data = get_random(documents)
    return render_template('search.html', name=project_name, netid=net_id, 
    output_message=output_message, data=data)
