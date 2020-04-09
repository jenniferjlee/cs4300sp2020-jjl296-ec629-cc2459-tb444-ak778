import json
import re
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse

# data = []
# with open("data/newser.json", "r") as read_file:
#     data = json.load(read_file)

# for article in data:
#     old_date = article['date']
#     datetime_object = parse(old_date)
#     # datetime_object = datetime.strptime(old_date, '%b %d %Y %X %p %Z')
#     new_date = str(datetime_object.year) + "-" + str(datetime_object.month) + "-" + str(datetime_object.day)
#     article['date'] = new_date

# with open('newser_final.json', 'w') as json_file:
#     json.dump(data, json_file)

data = []
with open("data/thenewdaily.json", "r") as read_file:
    data = json.load(read_file)

for article in data:
    old_date = article['date']
    datetime_object = parse(old_date)
    new_date = str(datetime_object.year) + "-" + str(datetime_object.month) + "-" + str(datetime_object.day)
    print(new_date)
    article['date'] = new_date

with open('newdaily_final.json', 'w') as json_file:
    json.dump(data, json_file)