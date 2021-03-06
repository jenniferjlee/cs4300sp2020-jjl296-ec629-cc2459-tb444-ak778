import os
import json
from langdetect import detect
from langdetect import DetectorFactory
DetectorFactory.seed = 0
import numpy as np

def load_json_file(name):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, name)
    with open(file_path, encoding = 'utf-8') as json_file:
        data = json.load(json_file)
    return data

# remove non-english and unclassified transcripts
def diff_langs(data):
  
  # lang_counts = dict()
  # lang_counts['unclassified'] = 0

  articles1 = []
  articles2 = []

  split = True

  for post in data:
    transcript = post['transcript']
    try:
      lang = detect(transcript)
      if lang == 'en':
        if split:
          articles1.append(post)
          split = False
        else:
          articles2.append(post)
          split = True
      # if lang not in lang_counts:
      #   lang_counts[lang] = 1
      # else:
      #   lang_counts[lang] += 1
    except:
      continue
      # print(len(transcript))
      # lang_counts['unclassified'] += 1


  with open('HALF1.json', 'w') as json_file:
      json.dump(articles1, json_file)
  with open('HALF2.json', 'w') as json_file:
      json.dump(articles2, json_file)

def main():
  # Load in data
  data_file_name = "lang.json"
  data = load_json_file(data_file_name)
  lang_freq = diff_langs(data)

    # print(lang_freq)
    # print(len(lang_freq))
  # data_file_name = "f_data.json"
  # data = load_json_file(data_file_name)
  # print(len(data))

if __name__ == "__main__":
    main()