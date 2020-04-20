from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.data.processor import load_json_file
import os
from app.irsystem.data.processor import tokenize
from app.irsystem.models.search import *

project_name = "CUSmiles"
net_id = "Jennifer Lee: jjl296, Camilo Cedeno-Tobon: cc2459, Tanmay Bansal: tb444, Alina Kim: ak778, Ein Chang: ec629 "

documents = load_json_file('total_data.json')
inverted_index = load_json_file('transcript_inverted_index.json')
tfidf_matrix = load_json_file('transcript_tfidf_matrix.json')
norms = load_json_file('transcript_norms.json')



@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = 'No results'
    else:
        results = search_transcripts(query, tfidf_matrix, inverted_index, norms, tokenize)
        top_5 = get_top_k(results, 5, documents)
        output_message = "Your search: " + query
        data = top_5
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

