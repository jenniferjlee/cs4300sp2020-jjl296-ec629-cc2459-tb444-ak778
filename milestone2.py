import json
import re
import matplotlib.pyplot as plt

data = []
with open("data/total_data.json", "r") as read_file:
    data = json.load(read_file)

# data: list of objects with keys: 'source', 'title', 'url', 'date', 'transcript'

def tokenize(text):
    # Returns a list of lowercase words that make up the text
    return re.findall(r"[a-z]+", text.lower())

transcript_lengths = []

def tokenize_transcript(tokenize,data):
    # Returns a list of words contained in an entire transcript.
    script = []
    for article in data:
        script = tokenize(article['transcript'])
        transcript_lengths.append(len(script))
    return script

tokenized_transcripts = tokenize_transcript(tokenize, data)
transcript_lengths.sort()

plt.hist(transcript_lengths, bins = 100)
plt.title('Frequency of Article Lengths') 
plt.xlabel('Number of Words in Article')
plt.ylabel('Number of Articles')
plt.show()


