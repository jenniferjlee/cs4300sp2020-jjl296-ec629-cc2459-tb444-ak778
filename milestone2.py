import json
import re
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

data = []
with open("data/total_data.json", "r") as read_file:
    data = json.load(read_file)

# data: list of objects with keys: 'source', 'title', 'url', 'date', 'transcript'

def tokenize(text):
    # Returns a list of lowercase words that make up the text
    return re.findall(r"[a-z]+", text.lower())

transcript_lengths = []
dates = []

def tokenize_transcript(tokenize,data):
    # Returns a list of words contained in an entire transcript.
    scripts = []
    for article in data:
      script = tokenize(article['transcript'])
      scripts.append(script)
      transcript_lengths.append(len(script))
      dates.append(article['date'])
    return scripts

tokenized_transcripts = tokenize_transcript(tokenize, data)
transcript_lengths.sort()
dates.sort()

# average # of words per article
# print(sum(transcript_lengths) / len(transcript_lengths))

# print(len(dates))
# print(dates)

# plt.hist(transcript_lengths, bins = 100)
# plt.title('Frequency of Article Lengths') 
# plt.xlabel('Number of Words in Article')
# plt.ylabel('Number of Articles')
# plt.show()

datesFreq = defaultdict(int)
def whichYear(data):
  # Returns a dict of date years and freq of all articles.
    yearAndFreq = defaultdict(int)
    for article in data:
      year = article['date'].split("-")[0]     
      yearAndFreq[int(year)] += 1
      datesFreq[article['date']] += 1

    return yearAndFreq

yearFreq = whichYear(data)
# print(datesFreq)
# {2020: 439, 2018: 249, 2019: 374}

# labels = '2018', '2019', '2020'
# sizes = [249, 374, 439]
# colors = ['yellowgreen', 'lightcoral', 'lightskyblue']
# # Plot
# plt.pie(sizes, labels=labels, colors=colors,
# autopct='%1.1f%%')
# plt.title('Frequency of Article Dates') 
# plt.axis('equal')
# plt.show()


# plt.title('Frequency of Article Dates') 
# plt.xlabel('Dates (2020 to 2018)')
# plt.ylabel('Frequency')
# x = datesFreq.keys()
# y = datesFreq.values()
# plt.scatter(x, y)
# plt.show()