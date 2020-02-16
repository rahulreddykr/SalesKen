import requests
from flask import jsonify

if __name__ == '__main__':
    url = "http://localhost:8005/group_similar_text"
    sent = []
    with open('list_of_sentences', 'r') as f:
        sent = f.readlines()
    print(sent)
    data = requests.post(url, json={"sentences" : sent})
    print(data, data.text)